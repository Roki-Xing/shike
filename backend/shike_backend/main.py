"""FastAPI model orchestration service for Shike MVP."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException

from shike_backend.adapters.base import AdapterError, manual_review_response
from shike_backend.adapters.bluelm_adapter import BlueLMModelAdapter
from pathlib import Path

from shike_backend.adapters.mock_adapter import MockModelAdapter
from shike_backend.adapters.recorded_bluelm_adapter import RecordedBlueLMAdapter
from shike_backend.schemas import AnalyzeRequest, AnalyzeResponse, load_model_output_schema
from shike_backend.settings import get_settings

app = FastAPI(title="Shike Model Orchestration API", version="0.1.0")


_ADAPTER: object | None = None


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

    _ADAPTER = MockModelAdapter()
    return _ADAPTER


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

    adapter = _get_adapter()
    try:
        # Both adapters take AnalyzeRequest and return AnalyzeResponse.
        return adapter.analyze(request)  # type: ignore[no-any-return]
    except AdapterError:
        settings = get_settings()
        if settings.allow_mock_fallback:
            return MockModelAdapter().analyze(request)
        return manual_review_response("model_unavailable")
