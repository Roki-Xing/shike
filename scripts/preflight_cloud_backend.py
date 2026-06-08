#!/usr/bin/env python3
"""Secret-safe public backend preflight before cloud-device recording."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


DEFAULT_BASE_URL = "https://roky.chat"
DEFAULT_IMAGE_DATA_URL = (
    "data:image/png;base64,"
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)
ALLOWED_IGNORED_REGIONS = {
    "top_status_bar",
    "bottom_navigation_bar",
    "screenshot_toolbar_or_overlay",
}
CONFIRMATION_DISABLED_REASON = "用户确认前不可执行"
SECRET_MARKERS = ("sk-", "Authorization", "AppKEY", "BLUELM_APP_KEY", "VIVO_OCR_APP_KEY")


def normalize_base_url(base_url: str, *, allow_http: bool = False) -> str:
    """Normalize and validate a public backend base URL.

    Args:
        base_url: Backend origin URL.
        allow_http: Whether plain HTTP is allowed for local debugging.

    Returns:
        Normalized URL without trailing slash.

    Raises:
        ValueError: If the URL is unsafe for cloud-device preflight.
    """

    parsed = urllib.parse.urlsplit(base_url.strip())
    if parsed.scheme not in {"https", "http"} or not parsed.netloc:
        raise ValueError("base_url must include http(s) scheme and host")
    if parsed.username or parsed.password:
        raise ValueError("base_url must not embed credentials")
    if parsed.scheme == "http" and not allow_http:
        raise ValueError("cloud backend preflight requires https unless --allow-http is set")
    path = parsed.path.rstrip("/")
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, path, "", ""))


def redact_base_url(base_url: str) -> str:
    """Return a host-redacted URL for evidence output."""

    parsed = urllib.parse.urlsplit(base_url)
    return urllib.parse.urlunsplit((parsed.scheme, "HOST_REDACTED", parsed.path.rstrip("/"), "", ""))


def build_payload(*, allow_cloud_image: bool) -> dict[str, Any]:
    """Build a synthetic image-analysis request body.

    Args:
        allow_cloud_image: Whether the remote backend may call image models.

    Returns:
        A deterministic non-sensitive `/v2/analyze-image` request.
    """

    return {
        "input_id": "cloud-backend-preflight-001",
        "source_type": "screenshot_share",
        "image": {
            "data_url": DEFAULT_IMAGE_DATA_URL,
            "mime": "image/png",
            "width": 1,
            "height": 1,
            "sha256": "cloud-backend-preflight-synthetic-image",
        },
        "ocr_text_hint": "今晚18:30 项目讨论 B203",
        "ocr_blocks": [],
        "current_date": "2026-06-08",
        "user_timezone": "Asia/Shanghai",
        "allow_cloud_image": allow_cloud_image,
    }


def fetch_json(base_url: str, path: str, *, timeout_seconds: int) -> dict[str, Any]:
    """Fetch JSON from a backend route."""

    with urllib.request.urlopen(base_url + path, timeout=timeout_seconds) as response:
        return json.loads(response.read().decode("utf-8"))


def post_json(base_url: str, path: str, body: dict[str, Any], *, timeout_seconds: int) -> dict[str, Any]:
    """Post JSON to a backend route."""

    request = urllib.request.Request(
        base_url + path,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        return json.loads(response.read().decode("utf-8"))


def ignored_regions_allowed(regions: object) -> bool:
    """Return whether ignored-region metadata is from the backend allowlist."""

    return isinstance(regions, list) and all(
        isinstance(region, str) and region in ALLOWED_IGNORED_REGIONS for region in regions
    )


def actions_are_confirmation_gated(actions: object) -> bool:
    """Return whether every suggested action is disabled until user confirmation."""

    if not isinstance(actions, list) or not actions:
        return False
    return all(isinstance(action, dict) and action.get("disabled_reason") == CONFIRMATION_DISABLED_REASON for action in actions)


def safe_error_label(error: BaseException) -> str:
    """Return a compact non-secret error label."""

    if isinstance(error, urllib.error.HTTPError):
        return f"http_{error.code}"
    if isinstance(error, urllib.error.URLError):
        return "url_error"
    return error.__class__.__name__


def print_evidence(key: str, value: object) -> None:
    """Print one secret-safe evidence line."""

    text = f"{key}={value}"
    if any(marker.lower() in text.lower() for marker in SECRET_MARKERS):
        text = f"{key}=REDACTED"
    print(text)


def run_preflight(*, base_url: str, timeout_seconds: int, allow_cloud_image: bool) -> bool:
    """Run public backend preflight routes.

    Args:
        base_url: Normalized backend base URL.
        timeout_seconds: Per-request timeout.
        allow_cloud_image: Whether to allow image-model calls for this preflight.

    Returns:
        True when the backend passes all route and action-gate checks.
    """

    print_evidence("cloud_backend_preflight_base_url", redact_base_url(base_url))
    try:
        health = fetch_json(base_url, "/health", timeout_seconds=timeout_seconds)
        schema = fetch_json(base_url, "/v2/schema", timeout_seconds=timeout_seconds)
        result = post_json(
            base_url,
            "/v2/analyze-image",
            build_payload(allow_cloud_image=allow_cloud_image),
            timeout_seconds=max(timeout_seconds, 35),
        )
    except Exception as error:
        print_evidence("cloud_backend_preflight_status", "fail")
        print_evidence("cloud_backend_preflight_error", safe_error_label(error))
        print_evidence("CLOUD_BACKEND_PREFLIGHT_METRIC", "0/1")
        return False

    actions = result.get("suggested_actions")
    regions = result.get("ignored_regions", [])
    route_ok = (
        health.get("status") == "ok"
        and "title" in schema
        and bool(result.get("title"))
        and actions_are_confirmation_gated(actions)
        and ignored_regions_allowed(regions)
    )
    print_evidence("cloud_backend_preflight_health_status", health.get("status"))
    print_evidence("cloud_backend_preflight_schema_has_title", "title" in schema)
    print_evidence("cloud_backend_preflight_route_status", "pass" if route_ok else "fail")
    print_evidence("cloud_backend_preflight_actions_disabled", actions_are_confirmation_gated(actions))
    print_evidence("cloud_backend_preflight_ignored_regions_allowed", ignored_regions_allowed(regions))
    print_evidence("cloud_backend_preflight_cloud_image_allowed", allow_cloud_image)
    print_evidence("CLOUD_BACKEND_PREFLIGHT_METRIC", "1/1" if route_ok else "0/1")
    return route_ok


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description="Run secret-safe preflight against the public Shike backend.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Public backend base URL. Defaults to https://roky.chat")
    parser.add_argument("--timeout-seconds", type=int, default=20, help="Per-request timeout.")
    parser.add_argument("--allow-http", action="store_true", help="Allow http:// base URLs for local debugging only.")
    parser.add_argument(
        "--allow-cloud-image",
        action="store_true",
        help="Allow cloud image-model calls. Default stays false for deterministic pre-recording checks.",
    )
    return parser.parse_args()


def main() -> int:
    """Run CLI entrypoint."""

    args = parse_args()
    try:
        base_url = normalize_base_url(args.base_url, allow_http=args.allow_http)
    except ValueError as error:
        print_evidence("cloud_backend_preflight_status", "fail")
        print_evidence("cloud_backend_preflight_error", error)
        print_evidence("CLOUD_BACKEND_PREFLIGHT_METRIC", "0/1")
        return 2

    ok = run_preflight(
        base_url=base_url,
        timeout_seconds=args.timeout_seconds,
        allow_cloud_image=args.allow_cloud_image,
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
