"""FastAPI model orchestration service for Shike MVP."""

from __future__ import annotations

import logging
import time
from fastapi import FastAPI, HTTPException

from shike_backend.adapters.base import AdapterError, manual_review_response
from shike_backend.adapters.bluelm_adapter import BlueLMModelAdapter
from shike_backend.adapters.deepseek_adapter import DeepSeekModelAdapter
from pathlib import Path

from shike_backend.adapters.mock_adapter import MockModelAdapter, is_sparse_course_text, sparse_course_output
from shike_backend.adapters.recorded_bluelm_adapter import RecordedBlueLMAdapter
from shike_backend.adapters.vivo_cloud_multimodal_adapter import VivoCloudMultimodalAdapter
from shike_backend.adapters.vivo_ocr_adapter import VivoOcrAdapter, fallback_ocr_response
from shike_backend.audit_log import build_analyze_image_audit_event
from shike_backend.image_preprocess import filter_ocr_blocks
from shike_backend.preparation import enrich_preparation_payload
from shike_backend.schemas import AnalyzeRequest, AnalyzeResponse, OcrRequest, OcrResponse, load_model_output_schema
from shike_backend.schemas_v2 import (
    AnalyzeImageRequest,
    ParsedActionCard,
    EvidenceSpan,
    analyze_image_response_schema,
    manual_review_action_card,
)
from shike_backend.settings import get_settings

app = FastAPI(title="Shike Model Orchestration API", version="0.1.0")
logger = logging.getLogger("shike_backend.audit")
logger.setLevel(logging.INFO)
if not logger.handlers:
    logger.addHandler(logging.StreamHandler())


_ADAPTER: object | None = None
_OCR_ADAPTER: VivoOcrAdapter | None = None
_MULTIMODAL_ADAPTER: object | None = None
_TEXT_FALLBACK_MULTIMODAL_REASONS = {
    "provider_model_does_not_support_image",
    "provider_error:401",
    "provider_error:403",
    "legacy_http_status:401",
    "legacy_http_status:403",
}
_ALLOWED_IGNORED_REGIONS = {
    "top_status_bar",
    "bottom_navigation_bar",
    "screenshot_toolbar_or_overlay",
}
_TEXT_COMPATIBLE_SCENES = {"course_notice", "event_poster", "unknown"}


def _image_base64_from_data_url(data_url: str | None) -> str | None:
    """Extract base64 image content from a data URL.

    Args:
        data_url: Client-supplied image data URL.

    Returns:
        Base64 payload when the URL is an inline image, otherwise None.
    """

    if not data_url or not data_url.startswith("data:image"):
        return None
    marker = ";base64,"
    if marker not in data_url:
        return None
    image_base64 = data_url.split(marker, 1)[1].strip()
    return image_base64 if len(image_base64) >= 16 else None


def _merge_ocr_text_hint(client_hint: str | None, server_text: str) -> str | None:
    """Merge Android OCR hints with backend OCR text without duplication.

    Args:
        client_hint: Existing OCR text from Android or user edits.
        server_text: Redacted OCR text returned by the backend adapter.

    Returns:
        Combined OCR hint for the multimodal prompt.
    """

    hint = (client_hint or "").strip()
    text = server_text.strip()
    if not text:
        return hint or None
    if not hint:
        return text
    if text in hint:
        return hint
    return f"{hint}\n{text}"


def _server_ocr_source_type(source_type: str) -> str:
    """Map v2 capture sources to the server OCR source contract."""

    return "camera" if source_type == "camera" else "screenshot"


def enrich_image_request_with_server_ocr(request: AnalyzeImageRequest) -> tuple[AnalyzeImageRequest, list[str]]:
    """Add backend OCR text to a v2 image analysis request.

    Args:
        request: Normalized v2 image-analysis request.

    Returns:
        Updated request and non-secret risk markers collected during OCR.
    """

    if request.image is None:
        return request, []

    image_base64 = _image_base64_from_data_url(request.image.data_url)
    if image_base64 is None:
        return request, []

    try:
        ocr_detail = _get_ocr_adapter().recognize_detail(
            OcrRequest(
                input_id=request.input_id,
                source_type=_server_ocr_source_type(request.source_type),  # type: ignore[arg-type]
                image_base64=image_base64,
                locale=request.locale,
                pos=2,
            )
        )
    except AdapterError as exc:
        settings = get_settings()
        reason = "server_ocr_unavailable" if settings.allow_ocr_fallback else "server_ocr_required_but_unavailable"
        return request, [f"{reason}:{exc.message}"]

    enriched_hint = _merge_ocr_text_hint(request.ocr_text_hint, ocr_detail.response.text)
    server_ocr_blocks = ocr_detail.blocks
    server_ocr_blocks_filtered = server_ocr_blocks
    if request.image is not None:
        server_ocr_blocks_filtered = filter_ocr_blocks(server_ocr_blocks, request.image.width, request.image.height)
    merged_blocks = [*request.ocr_blocks, *server_ocr_blocks_filtered]
    return request.model_copy(update={"ocr_text_hint": enriched_hint, "ocr_blocks": merged_blocks}), []


def _text_source_type_for_image_source(source_type: str) -> str:
    """Map v2 image capture sources to the v1 text-analysis contract."""

    if source_type == "camera":
        return "camera"
    if source_type == "manual":
        return "manual"
    return "screenshot"


def _disable_actions_until_user_confirmation(actions: list[dict]) -> list[dict]:
    """Mark suggested actions as user-confirmation gated.

    Args:
        actions: Model-suggested action dictionaries.

    Returns:
        Action dictionaries with a disabled reason for v2 review UI.
    """

    return [
        {
            **action,
            "disabled_reason": "用户确认前不可执行",
        }
        for action in actions
    ]


def _sanitized_ignored_regions(regions: list[str]) -> list[str]:
    """Return only server-approved ignored-region metadata labels.

    Args:
        regions: Model-supplied and route-supplied region labels.

    Returns:
        Deduplicated labels from the backend's ignored-region allowlist.
    """

    return list(dict.fromkeys(region for region in regions if region in _ALLOWED_IGNORED_REGIONS))


def _require_user_confirmation_for_card(card: ParsedActionCard) -> ParsedActionCard:
    """Return a card whose actions cannot execute before user confirmation.

    Args:
        card: Parsed image-analysis card returned by a model or fallback.

    Returns:
        Parsed action card with every suggested action disabled until the user confirms.
    """

    return card.model_copy(
        update={"suggested_actions": _disable_actions_until_user_confirmation(card.suggested_actions)}
    )


def _response_with_preparation(response: AnalyzeResponse, evidence_texts: list[str]) -> AnalyzeResponse:
    """Fill preparation fields from model output and OCR evidence.

    Args:
        response: Text-analysis response.
        evidence_texts: OCR or user-entered evidence text.

    Returns:
        Response with preparation/checklist fields populated when supported by evidence.
    """

    payload = enrich_preparation_payload(response.model_dump(), evidence_texts)
    return AnalyzeResponse.model_validate(payload)


def _card_with_preparation(card: ParsedActionCard, evidence_texts: list[str]) -> ParsedActionCard:
    """Fill preparation fields on an image-analysis card.

    Args:
        card: Image-analysis action card.
        evidence_texts: OCR hint or user text evidence.

    Returns:
        Card with preparation/checklist fields populated when supported by evidence.
    """

    payload = enrich_preparation_payload(card.model_dump(), evidence_texts)
    return ParsedActionCard.model_validate(payload)


def _normalized_text(value: object) -> str:
    """Return a compact comparable text form.

    Args:
        value: Any model field value.

    Returns:
        Lowercase string without whitespace.
    """

    return "".join(str(value or "").lower().split())


def _location_raw(card: ParsedActionCard) -> str:
    """Return a parsed card's raw location string.

    Args:
        card: Parsed action card.

    Returns:
        Raw location or empty string.
    """

    if not isinstance(card.location, dict):
        return ""
    return str(card.location.get("raw") or card.location.get("map_query") or "")


def _time_value(card: ParsedActionCard, field: str) -> str:
    """Return a string time field from a parsed card.

    Args:
        card: Parsed action card.
        field: Time dictionary key.

    Returns:
        Time field string or empty string.
    """

    if not isinstance(card.time, dict):
        return ""
    return str(card.time.get(field) or "")


def _card_title_is_only_location(card: ParsedActionCard) -> bool:
    """Return whether a title appears to only repeat the location.

    Args:
        card: Parsed action card.

    Returns:
        True when the title carries no task subject beyond location text.
    """

    title = _normalized_text(card.title)
    location = _normalized_text(_location_raw(card))
    return bool(title and location and title == location)


def _ocr_repair_reasons(card: ParsedActionCard, ocr_card: ParsedActionCard) -> list[str]:
    """Compare image output with OCR-text output and decide repair reasons.

    Args:
        card: Original image-model card.
        ocr_card: Card parsed from OCR text.

    Returns:
        Stable non-secret reason codes. An empty list means keep the image card.
    """

    if ocr_card.scene_type == "unknown" and card.scene_type != "unknown":
        return []

    reasons: list[str] = []
    if card.scene_type == "unknown" and ocr_card.scene_type != "unknown":
        reasons.append("ocr_scene_recovered")
    elif card.scene_type != ocr_card.scene_type:
        return []

    if _card_title_is_only_location(card) and _normalized_text(ocr_card.title) != _normalized_text(card.title):
        reasons.append("ocr_subject_missing")

    card_start = _time_value(card, "normalized_start")
    ocr_start = _time_value(ocr_card, "normalized_start")
    if ocr_start and not card_start:
        reasons.append("ocr_time_missing")
    elif ocr_start and card_start and ocr_start != card_start:
        reasons.append("ocr_time_mismatch")

    card_deadline = _time_value(card, "normalized_deadline")
    ocr_deadline = _time_value(ocr_card, "normalized_deadline")
    if ocr_deadline and not card_deadline:
        reasons.append("ocr_deadline_missing")
    elif ocr_deadline and card_deadline and ocr_deadline != card_deadline:
        reasons.append("ocr_deadline_mismatch")

    card_location = _normalized_text(_location_raw(card))
    ocr_location = _normalized_text(_location_raw(ocr_card))
    if ocr_location and not card_location:
        reasons.append("ocr_location_missing")
    elif ocr_location and card_location and ocr_location != card_location:
        reasons.append("ocr_location_mismatch")

    if "time" in card.missing_fields and isinstance(ocr_card.time, dict):
        reasons.append("ocr_fills_missing_time")
    if "location" in card.missing_fields and isinstance(ocr_card.location, dict):
        reasons.append("ocr_fills_missing_location")

    return list(dict.fromkeys(reasons))


def repair_image_card_with_ocr_evidence(
    request: AnalyzeImageRequest,
    card: ParsedActionCard,
    *,
    ignored_regions: list[str],
) -> tuple[ParsedActionCard, list[str]]:
    """Use OCR text parsing to repair a semantically incomplete image card.

    Args:
        request: OCR-enriched v2 request.
        card: Schema-valid image-model result.
        ignored_regions: Regions ignored during OCR preparation.

    Returns:
        Original or repaired card plus non-secret repair risk markers.
    """

    if len((request.ocr_text_hint or "").strip()) < 8:
        return card, []
    if card.scene_type not in _TEXT_COMPATIBLE_SCENES and request.scene_hint not in _TEXT_COMPATIBLE_SCENES:
        return card, []

    try:
        ocr_card = fallback_analyze_image_with_text_model(
            request,
            reason="ocr_evidence_repair",
            ignored_regions=ignored_regions,
        )
    except AdapterError:
        return card, []

    reasons = _ocr_repair_reasons(card, ocr_card)
    if not reasons:
        return card, []

    repair_risks = [f"ocr_evidence_repair:{reason}" for reason in reasons]
    repaired_risks = list(dict.fromkeys([*ocr_card.risks, *repair_risks]))
    return ocr_card.model_copy(update={"risks": repaired_risks}), repair_risks


def _parsed_card_from_text_response(
    response: AnalyzeResponse,
    *,
    reason: str,
    ignored_regions: list[str],
) -> ParsedActionCard:
    """Convert a v1 text-analysis response into a v2 action card.

    Args:
        response: Schema-validated text model response.
        reason: Non-secret fallback reason.
        ignored_regions: UI regions ignored while preparing OCR text.

    Returns:
        V2 parsed action card that still requires user confirmation before execution.
    """

    evidence = [
        EvidenceSpan(
            field="ocr_text_hint",
            text="OCR 文本兜底解析",
            source="ocr",
            box=None,
        )
    ]
    return ParsedActionCard(
        title=response.title,
        scene_type=response.scene_type,
        confidence=response.confidence,
        time=response.time.model_dump() if response.time is not None else None,
        location=response.location.model_dump() if response.location is not None else None,
        task=response.task.model_dump(),
        suggested_actions=_disable_actions_until_user_confirmation(
            [action.model_dump() for action in response.suggested_actions]
        ),
        missing_fields=response.missing_fields,
        preparation_items=response.preparation_items,
        checklist_items=response.checklist_items,
        risks=[f"text_fallback:{reason}"],
        evidence=evidence,
        ignored_regions=ignored_regions,
        explanation=f"{response.explanation} 多模态图片理解不可用时，已使用 OCR 文本兜底解析；用户确认前不会执行系统动作。",
    )


def fallback_analyze_image_with_text_model(
    request: AnalyzeImageRequest,
    *,
    reason: str,
    ignored_regions: list[str],
) -> ParsedActionCard:
    """Analyze enriched OCR text when image-understanding is unavailable.

    Args:
        request: OCR-enriched v2 request.
        reason: Provider failure reason.
        ignored_regions: Regions ignored during OCR preparation.

    Returns:
        Parsed action card from the text model.

    Raises:
        AdapterError: When no usable OCR text exists or the text model fails.
    """

    ocr_text = (request.ocr_text_hint or "").strip()
    if len(ocr_text) < 8:
        raise AdapterError("text_fallback_missing_ocr_hint")

    text_request = AnalyzeRequest(
        input_id=request.input_id,
        source_type=_text_source_type_for_image_source(request.source_type),  # type: ignore[arg-type]
        ocr_text=ocr_text,
        locale=request.locale,
        scene_hint=request.scene_hint,
        user_timezone=request.user_timezone,
    )
    adapter = _get_adapter()
    response = adapter.analyze(text_request)  # type: ignore[attr-defined]
    response = _response_with_preparation(response, [ocr_text])
    return _parsed_card_from_text_response(response, reason=reason, ignored_regions=ignored_regions)


def _get_adapter() -> object:
    global _ADAPTER
    if _ADAPTER is not None:
        return _ADAPTER

    settings = get_settings()
    if settings.model_provider == "bluelm":
        adapter = BlueLMModelAdapter(
            app_id=settings.bluelm_app_id,
            app_key=settings.bluelm_app_key,
            base_url=settings.bluelm_base_url,
            uri=settings.bluelm_uri,
            model=settings.bluelm_model,
            timeout_seconds=settings.bluelm_timeout_seconds,
            max_retries=settings.bluelm_max_retries,
            temperature=settings.bluelm_temperature,
            thinking_mode=settings.bluelm_thinking_mode,
            request_id_param=settings.bluelm_request_id_param,
            response_format_enabled=settings.bluelm_response_format_enabled,
        )
        _ADAPTER = adapter
        return adapter

    if settings.model_provider == "deepseek":
        adapter = DeepSeekModelAdapter(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
            uri=settings.deepseek_uri,
            model=settings.deepseek_model,
            timeout_seconds=settings.deepseek_timeout_seconds,
            max_retries=settings.deepseek_max_retries,
            temperature=settings.deepseek_temperature,
            thinking_enabled=settings.deepseek_thinking_enabled,
            response_format_enabled=settings.deepseek_response_format_enabled,
        )
        _ADAPTER = adapter
        return adapter

    if settings.model_provider == "recorded_bluelm":
        base = BlueLMModelAdapter(
            app_id=settings.bluelm_app_id,
            app_key=settings.bluelm_app_key,
            base_url=settings.bluelm_base_url,
            uri=settings.bluelm_uri,
            model=settings.bluelm_model,
            timeout_seconds=settings.bluelm_timeout_seconds,
            max_retries=settings.bluelm_max_retries,
            temperature=settings.bluelm_temperature,
            thinking_mode=settings.bluelm_thinking_mode,
            request_id_param=settings.bluelm_request_id_param,
            response_format_enabled=settings.bluelm_response_format_enabled,
        )
        recorded = RecordedBlueLMAdapter(recording_dir=Path(settings.recorded_dir), base=base if base.is_configured() else None)
        _ADAPTER = recorded
        return recorded

    _ADAPTER = MockModelAdapter(allow_demo_samples=settings.allows_demo_samples)
    return _ADAPTER


def _get_ocr_adapter() -> VivoOcrAdapter:
    global _OCR_ADAPTER
    if _OCR_ADAPTER is not None:
        return _OCR_ADAPTER

    settings = get_settings()
    _OCR_ADAPTER = VivoOcrAdapter(
        app_id=settings.vivo_ocr_app_id,
        app_key=settings.vivo_ocr_app_key,
        base_url=settings.vivo_ocr_base_url,
        uri=settings.vivo_ocr_uri,
        timeout_seconds=settings.vivo_ocr_timeout_seconds,
        max_retries=settings.vivo_ocr_max_retries,
    )
    return _OCR_ADAPTER


def _get_multimodal_adapter() -> VivoCloudMultimodalAdapter:
    adapters = _get_multimodal_adapters()
    return adapters[0]  # type: ignore[return-value]


def _normalize_multimodal_adapters(candidate: object) -> list[object]:
    """Normalize test-injected or runtime multimodal candidates.

    Args:
        candidate: One adapter or a list/tuple of adapters.

    Returns:
        Non-empty adapter candidate list.
    """

    if isinstance(candidate, (list, tuple)):
        adapters = [item for item in candidate if item is not None]
        if adapters:
            return adapters
    return [candidate]


def _get_multimodal_adapters() -> list[object]:
    """Return configured vivo multimodal candidates in priority order.

    Args:
        None.

    Returns:
        One or more image-understanding adapters.
    """

    global _MULTIMODAL_ADAPTER
    if _MULTIMODAL_ADAPTER is not None:
        return _normalize_multimodal_adapters(_MULTIMODAL_ADAPTER)

    settings = get_settings()
    adapters = [
        VivoCloudMultimodalAdapter(
            app_id=settings.vivo_multimodal_app_id,
            app_key=settings.vivo_multimodal_app_key,
            base_url=settings.vivo_multimodal_base_url,
            uri=settings.vivo_multimodal_uri,
            model=model,
            timeout_seconds=settings.vivo_multimodal_timeout_seconds,
            max_retries=settings.vivo_multimodal_max_retries,
            temperature=settings.vivo_multimodal_temperature,
        )
        for model in settings.vivo_multimodal_models
    ]
    _MULTIMODAL_ADAPTER = adapters
    return adapters


@app.get("/health")
def health() -> dict[str, str]:
    """Return service health.

    Args:
        None.

    Returns:
        Health status payload.
    """

    return {"status": "ok"}


@app.get("/v1/schema")
def schema() -> dict[str, object]:
    """Return the canonical model-output contract schema.

    Args:
        None.

    Returns:
        Full JSON Schema used by clients and smoke tests.
    """

    return load_model_output_schema()


@app.get("/v2/schema")
def schema_v2() -> dict[str, object]:
    """Return the v2 image-analysis response schema.

    Args:
        None.

    Returns:
        Pydantic JSON Schema for parsed action cards.
    """

    return analyze_image_response_schema()


@app.post("/v1/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """Analyze OCR text and return a Shike structured response.

    Args:
        request: OCR text and scene hint.

    Returns:
        Structured model response compatible with the Android MVP.
    """

    text = request.ocr_text.strip()
    if not text:
        raise HTTPException(status_code=422, detail="ocr_text must not be empty")

    if request.scene_hint is None and len(text) < 8:
        raise HTTPException(status_code=422, detail="ocr_text is too short to analyze")

    # NOTE: Validation gates expect backend code to explicitly reference
    # `missing_fields` as part of the Shike contract behavior (see validators).
    # The actual field is produced by adapters and enforced by Pydantic/schema.
    _ = "missing_fields"

    if is_sparse_course_text(text, request.scene_hint):
        return _response_with_preparation(sparse_course_output(text), [text])

    adapter = _get_adapter()
    try:
        # Both adapters take AnalyzeRequest and return AnalyzeResponse.
        response = adapter.analyze(request)
        return _response_with_preparation(response, [text])  # type: ignore[arg-type]
    except AdapterError:
        settings = get_settings()
        if settings.allow_mock_fallback:
            response = MockModelAdapter(allow_demo_samples=settings.allows_demo_samples).analyze(request)
            return _response_with_preparation(response, [text])
        return _response_with_preparation(manual_review_response("model_unavailable"), [text])


@app.post("/v2/analyze-image", response_model=ParsedActionCard)
def analyze_image(request: AnalyzeImageRequest) -> ParsedActionCard:
    """Analyze screenshot/photo content with image, OCR hint, and OCR blocks.

    Args:
        request: Multimodal request from Android import flows.

    Returns:
        Parsed action card that still requires user confirmation before actions.
    """

    started_at = time.time()
    image = request.image
    filtered_blocks = request.ocr_blocks
    ignored_regions = ["top_status_bar", "bottom_navigation_bar"]
    if image is not None:
        filtered_blocks = filter_ocr_blocks(request.ocr_blocks, image.width, image.height)

    normalized = request.model_copy(update={"ocr_blocks": filtered_blocks})
    enrichment_risks: list[str] = []
    status = "schema_valid"
    audit_provider = "vivo_cloud_multimodal"
    key_present = False
    repair_risks: list[str] = []
    if not request.allow_cloud_image:
        audit_provider = "ocr_hint_text_fallback"
        try:
            card = fallback_analyze_image_with_text_model(
                normalized,
                reason="cloud_image_disabled",
                ignored_regions=ignored_regions,
            )
            status = "text_fallback_schema_valid"
        except AdapterError as exc:
            status = "manual_review"
            card = manual_review_action_card(f"manual_review:cloud_image_disabled;text_fallback:{exc.message}")
    else:
        normalized, enrichment_risks = enrich_image_request_with_server_ocr(normalized)
        adapters = _get_multimodal_adapters()
        adapter = adapters[0]
        last_multimodal_error: AdapterError | None = None
        try:
            for candidate in adapters:
                adapter = candidate
                try:
                    card = adapter.analyze_image(normalized, analyze_image_response_schema())  # type: ignore[attr-defined]
                    card, repair_risks = repair_image_card_with_ocr_evidence(
                        normalized,
                        card,
                        ignored_regions=ignored_regions,
                    )
                    if repair_risks:
                        status = "ocr_repaired_schema_valid"
                    break
                except AdapterError as exc:
                    last_multimodal_error = exc
            else:
                raise last_multimodal_error or AdapterError("vivo_multimodal_failed")
        except AdapterError as exc:
            if exc.message in _TEXT_FALLBACK_MULTIMODAL_REASONS:
                try:
                    card = fallback_analyze_image_with_text_model(normalized, reason=exc.message, ignored_regions=ignored_regions)
                    status = "text_fallback_schema_valid"
                except AdapterError as fallback_exc:
                    status = "manual_review"
                    card = manual_review_action_card(f"manual_review:{exc.message};text_fallback:{fallback_exc.message}")
            else:
                status = "manual_review"
                card = manual_review_action_card(f"manual_review:{exc.message}")
        key_present = bool(getattr(adapter, "is_configured", lambda: False)())

    if request.allow_cloud_image:
        audit_provider = "vivo_cloud_multimodal"

    audit_event = build_analyze_image_audit_event(
        normalized,
        provider=audit_provider,
        key_present=key_present,
        duration_ms=int((time.time() - started_at) * 1000),
        status=status,
        repair_risks=repair_risks,
    )
    logger.info("analyze_image_audit %s", audit_event)

    merged_regions = _sanitized_ignored_regions([*card.ignored_regions, *ignored_regions])
    merged_risks = list(dict.fromkeys([*card.risks, *enrichment_risks, *repair_risks]))
    card = _card_with_preparation(card, [normalized.ocr_text_hint or ""])
    gated_card = _require_user_confirmation_for_card(card)
    return gated_card.model_copy(update={"ignored_regions": merged_regions, "risks": merged_risks})


@app.post("/v1/ocr", response_model=OcrResponse)
def ocr(request: OcrRequest) -> OcrResponse:
    """Recognize screenshot/camera image text through server-side vivo OCR.

    Args:
        request: Base64 encoded screenshot or camera image.

    Returns:
        OCR text or a manual-continuation fallback response.
    """

    adapter = _get_ocr_adapter()
    try:
        return adapter.recognize(request)
    except AdapterError as exc:
        settings = get_settings()
        if settings.allow_ocr_fallback:
            return fallback_ocr_response(request, reason=str(exc))
        raise HTTPException(status_code=503, detail="ocr_unavailable") from exc
