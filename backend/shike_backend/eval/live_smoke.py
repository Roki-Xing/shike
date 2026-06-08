#!/usr/bin/env python3
"""Run secret-safe live smoke checks for vivo LLM, OCR, and v2 route flows.

This script reads credentials only from environment variables and prints a
redacted, line-oriented evidence log. It never prints auth headers, AppKEY
values, full OCR text, or base64 image payloads.
"""

from __future__ import annotations

import argparse
import base64
import mimetypes
import time
from pathlib import Path

from fastapi.testclient import TestClient

from shike_backend.adapters.base import AdapterError
from shike_backend.adapters.bluelm_adapter import BlueLMModelAdapter
from shike_backend.adapters.vivo_cloud_multimodal_adapter import VivoCloudMultimodalAdapter
from shike_backend.adapters.vivo_ocr_adapter import VivoOcrAdapter
from shike_backend.schemas import AnalyzeRequest, OcrRequest
from shike_backend.schemas_v2 import AnalyzeImageRequest, analyze_image_response_schema
from shike_backend.settings import Settings


DEFAULT_TEXT = "高数A班今晚18:30改到B203，作业第5章今晚22:00前提交。"
DEFAULT_IMAGE_DATA_URL = (
    "data:image/png;base64,"
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)
ALLOWED_IGNORED_REGIONS = {
    "top_status_bar",
    "bottom_navigation_bar",
    "screenshot_toolbar_or_overlay",
}


def _print_evidence(key: str, value: object) -> None:
    """Print one redacted evidence line."""

    print(f"{key}={value}")


def _ignored_regions_allowed(regions: object) -> bool:
    """Return whether route metadata contains only safe ignored-region labels.

    Args:
        regions: JSON value from the route response.

    Returns:
        True when every region is a backend-approved metadata label.
    """

    return isinstance(regions, list) and all(
        isinstance(region, str) and region in ALLOWED_IGNORED_REGIONS for region in regions
    )


def run_bluelm(settings: Settings, *, timeout_seconds: int, text: str) -> bool:
    """Run one BlueLM structured extraction smoke check."""

    adapter = BlueLMModelAdapter(
        app_id=settings.bluelm_app_id,
        app_key=settings.bluelm_app_key,
        base_url=settings.bluelm_base_url,
        uri=settings.bluelm_uri,
        model=settings.bluelm_model,
        timeout_seconds=timeout_seconds,
        max_retries=0,
        temperature=settings.bluelm_temperature,
        thinking_mode=settings.bluelm_thinking_mode,
        request_id_param=settings.bluelm_request_id_param,
        response_format_enabled=settings.bluelm_response_format_enabled,
    )

    start = time.time()
    _print_evidence("provider", "bluelm")
    _print_evidence("model", settings.bluelm_model)
    _print_evidence("key_present", adapter.is_configured())
    _print_evidence("ocr_length", len(text))

    try:
        response = adapter.analyze(
            AnalyzeRequest(
                input_id="live-blue-001",
                source_type="screenshot",
                ocr_text=text,
                scene_hint="course_notice",
            )
        )
    except AdapterError as exc:
        _print_evidence("bluelm_status", "fail")
        _print_evidence("bluelm_error", str(exc))
        _print_evidence("bluelm_latency_ms", int((time.time() - start) * 1000))
        return False

    _print_evidence("bluelm_status", "pass")
    _print_evidence("result_schema_valid", "true")
    _print_evidence("scene_type", response.scene_type)
    _print_evidence("suggested_actions", ",".join(action.type for action in response.suggested_actions))
    _print_evidence("bluelm_latency_ms", int((time.time() - start) * 1000))
    return True


def run_ocr(settings: Settings, *, timeout_seconds: int, image_path: Path | None) -> bool:
    """Run one vivo OCR smoke check when an image is available."""

    if image_path is None:
        _print_evidence("ocr_status", "skip")
        _print_evidence("ocr_reason", "missing_ocr_image")
        return False
    if not image_path.is_file():
        _print_evidence("ocr_status", "skip")
        _print_evidence("ocr_reason", "ocr_image_not_found")
        return False

    adapter = VivoOcrAdapter(
        app_id=settings.vivo_ocr_app_id,
        app_key=settings.vivo_ocr_app_key,
        base_url=settings.vivo_ocr_base_url,
        uri=settings.vivo_ocr_uri,
        timeout_seconds=timeout_seconds,
        max_retries=0,
    )

    image_base64 = base64.b64encode(image_path.read_bytes()).decode("ascii")
    start = time.time()
    _print_evidence("ocr_provider", "vivo_general_ocr")
    _print_evidence("ocr_key_present", adapter.is_configured())
    _print_evidence("image_base64_present", "true")
    _print_evidence("image_persisted", "false")

    try:
        result = adapter.recognize(
            OcrRequest(
                input_id="live-ocr-001",
                source_type="screenshot",
                image_base64=image_base64,
                pos=2,
            )
        )
    except AdapterError as exc:
        _print_evidence("ocr_status", "fail")
        _print_evidence("ocr_error", str(exc))
        _print_evidence("ocr_latency_ms", int((time.time() - start) * 1000))
        return False

    _print_evidence("ocr_status", "pass")
    _print_evidence("ocr_engine", result.engine)
    _print_evidence("ocr_text_length", len(result.text))
    _print_evidence("ocr_image_cleared", str(result.image_cleared).lower())
    _print_evidence("ocr_latency_ms", int((time.time() - start) * 1000))
    return True


def _image_url_from_file(image_path: Path) -> str:
    """Build a provider-safe data URL from a local synthetic image file."""

    mime = mimetypes.guess_type(str(image_path))[0] or "image/png"
    if mime not in {"image/jpeg", "image/png", "image/webp"}:
        mime = "image/png"
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def run_multimodal(
    settings: Settings,
    *,
    timeout_seconds: int,
    image_path: Path | None,
    image_url: str | None,
    models: list[str],
) -> bool:
    """Run one or more secret-safe vivo multimodal smoke checks."""

    source_url = image_url or DEFAULT_IMAGE_DATA_URL
    if image_path is not None:
        if not image_path.is_file():
            _print_evidence("multimodal_status", "fail")
            _print_evidence("multimodal_error", "image_file_not_found")
            return False
        source_url = _image_url_from_file(image_path)

    candidate_models = models or list(settings.vivo_multimodal_models)
    any_passed = False
    _print_evidence("multimodal_provider", "vivo_cloud_multimodal")
    _print_evidence("multimodal_key_present", bool(settings.vivo_multimodal_app_key))
    _print_evidence("multimodal_image_url_kind", "public_url" if source_url.startswith("http") else "data_url")

    for model in candidate_models:
        adapter = VivoCloudMultimodalAdapter(
            app_id=settings.vivo_multimodal_app_id,
            app_key=settings.vivo_multimodal_app_key,
            base_url=settings.vivo_multimodal_base_url,
            uri=settings.vivo_multimodal_uri,
            model=model,
            timeout_seconds=timeout_seconds,
            max_retries=0,
            temperature=settings.vivo_multimodal_temperature,
        )
        start = time.time()
        _print_evidence("multimodal_model", model)
        _print_evidence("multimodal_configured", adapter.is_configured())

        try:
            card = adapter.analyze_image(
                AnalyzeImageRequest(
                    input_id="live-v2-image-001",
                    source_type="screenshot_share",
                    image={
                        "data_url": source_url,
                        "mime": "image/png",
                        "width": 1,
                        "height": 1,
                        "sha256": "live-smoke-synthetic-image",
                    },
                    ocr_text_hint="今晚18:30 项目讨论 B203",
                    ocr_blocks=[],
                    current_date="2026-06-06",
                    user_timezone="Asia/Shanghai",
                    allow_cloud_image=True,
                ),
                analyze_image_response_schema(),
            )
        except AdapterError as exc:
            _print_evidence("multimodal_status", "fail")
            _print_evidence("multimodal_error", exc.message)
            _print_evidence("multimodal_latency_ms", int((time.time() - start) * 1000))
            continue

        _print_evidence("multimodal_status", "pass")
        _print_evidence("multimodal_scene_type", card.scene_type)
        _print_evidence("multimodal_schema_valid", bool(card.title and card.suggested_actions))
        _print_evidence("multimodal_latency_ms", int((time.time() - start) * 1000))
        any_passed = True
        break

    return any_passed


def run_route_v2(*, image_path: Path | None, image_url: str | None) -> bool:
    """Run the FastAPI `/v2/analyze-image` route with live backend credentials.

    Args:
        image_path: Optional synthetic local image for the route request.
        image_url: Optional public or data image URL.

    Returns:
        True when the route returns a schema-valid, confirmation-gated card.
    """

    from shike_backend.main import app

    source_url = image_url or DEFAULT_IMAGE_DATA_URL
    width = 1
    height = 1
    if image_path is not None:
        if not image_path.is_file():
            _print_evidence("route_v2_status", "fail")
            _print_evidence("route_v2_error", "image_file_not_found")
            return False
        source_url = _image_url_from_file(image_path)
        width = 960
        height = 540

    start = time.time()
    payload = {
        "input_id": "live-route-v2-001",
        "source_type": "screenshot_share",
        "image": {
            "data_url": source_url,
            "mime": "image/png",
            "width": width,
            "height": height,
            "sha256": "live-smoke-synthetic-image",
        },
        "ocr_text_hint": "今晚18:30 项目讨论 B203",
        "ocr_blocks": [],
        "current_date": "2026-06-06",
        "user_timezone": "Asia/Shanghai",
        "allow_cloud_image": True,
    }

    response = TestClient(app).post("/v2/analyze-image", json=payload)
    _print_evidence("route_v2_http_status", response.status_code)
    if response.status_code != 200:
        _print_evidence("route_v2_status", "fail")
        _print_evidence("route_v2_latency_ms", int((time.time() - start) * 1000))
        return False

    body = response.json()
    suggested_actions = body.get("suggested_actions", [])
    actions_disabled = bool(suggested_actions) and all(
        action.get("disabled_reason") == "用户确认前不可执行" for action in suggested_actions
    )
    schema_valid = bool(body.get("title")) and bool(suggested_actions)
    raw_ignored_regions = body.get("ignored_regions", [])
    ignored_regions_allowed = _ignored_regions_allowed(raw_ignored_regions)
    ignored_regions = ",".join(raw_ignored_regions if isinstance(raw_ignored_regions, list) else [])
    risk_kinds = ",".join(str(item).split(":", 1)[0] for item in body.get("risks", []))

    route_ok = schema_valid and actions_disabled and ignored_regions_allowed
    _print_evidence("route_v2_status", "pass" if route_ok else "fail")
    _print_evidence("route_v2_schema_valid", str(schema_valid).lower())
    _print_evidence("route_v2_actions_disabled", str(actions_disabled).lower())
    _print_evidence("route_v2_ignored_regions_allowed", str(ignored_regions_allowed).lower())
    _print_evidence("route_v2_scene_type", body.get("scene_type", "unknown"))
    _print_evidence("route_v2_ignored_regions", ignored_regions)
    _print_evidence("route_v2_risk_kinds", risk_kinds)
    _print_evidence("route_v2_latency_ms", int((time.time() - start) * 1000))
    return route_ok


def main() -> int:
    """Run selected live smoke checks."""

    parser = argparse.ArgumentParser(description="Run redacted vivo AIGC live smoke checks.")
    parser.add_argument("--ocr-image", type=Path, help="Synthetic jpg/png/bmp image for OCR smoke.")
    parser.add_argument("--multimodal", action="store_true", help="Run vivo image-understanding smoke.")
    parser.add_argument("--multimodal-image", type=Path, help="Synthetic image for multimodal smoke.")
    parser.add_argument("--multimodal-image-url", help="Public non-private image URL for multimodal smoke.")
    parser.add_argument("--route-v2", action="store_true", help="Run the FastAPI /v2/analyze-image route smoke.")
    parser.add_argument("--route-v2-image", type=Path, help="Synthetic image for route-level v2 smoke.")
    parser.add_argument("--route-v2-image-url", help="Public or data image URL for route-level v2 smoke.")
    parser.add_argument(
        "--multimodal-models",
        default="",
        help="Comma-separated candidate models. Defaults to VIVO_MULTIMODAL_MODELS or VIVO_MULTIMODAL_MODEL.",
    )
    parser.add_argument("--skip-bluelm", action="store_true", help="Skip BlueLM smoke.")
    parser.add_argument("--skip-ocr", action="store_true", help="Skip OCR smoke.")
    parser.add_argument("--timeout-seconds", type=int, default=20, help="Per-request timeout.")
    parser.add_argument("--text", default=DEFAULT_TEXT, help="Synthetic text for BlueLM smoke.")
    args = parser.parse_args()

    settings = Settings.from_env()
    successes = 0
    expected = 0

    if not args.skip_bluelm:
        expected += 1
        successes += int(run_bluelm(settings, timeout_seconds=args.timeout_seconds, text=args.text))
    if not args.skip_ocr:
        expected += 1
        successes += int(run_ocr(settings, timeout_seconds=args.timeout_seconds, image_path=args.ocr_image))
    if args.multimodal:
        expected += 1
        models = [item.strip() for item in args.multimodal_models.split(",") if item.strip()]
        successes += int(
            run_multimodal(
                settings,
                timeout_seconds=args.timeout_seconds,
                image_path=args.multimodal_image,
                image_url=args.multimodal_image_url,
                models=models,
            )
        )
    if args.route_v2:
        expected += 1
        route_image = args.route_v2_image or args.ocr_image
        successes += int(run_route_v2(image_path=route_image, image_url=args.route_v2_image_url))

    _print_evidence("live_smoke_metric", f"{successes}/{expected}")
    return 0 if successes == expected else 1


if __name__ == "__main__":
    raise SystemExit(main())
