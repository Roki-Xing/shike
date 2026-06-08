#!/usr/bin/env python3
"""Run a secret-safe HTTP smoke against a temporary Shike backend server."""

from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
from typing import Any
from pathlib import Path


DEFAULT_IMAGE_DATA_URL = (
    "data:image/png;base64,"
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)
SECRET_MARKERS = ("sk-", "Authorization", "AppKEY", "api_key", "password", "credential")
BACKEND_ROOT = Path(__file__).resolve().parents[2]
ALLOWED_IGNORED_REGIONS = {
    "top_status_bar",
    "bottom_navigation_bar",
    "screenshot_toolbar_or_overlay",
}


def _free_port() -> int:
    """Return a currently free localhost TCP port."""

    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _get_json(base_url: str, path: str, *, timeout_seconds: int) -> dict[str, Any]:
    """Fetch JSON from the temporary server.

    Args:
        base_url: Temporary server base URL.
        path: HTTP path to request.
        timeout_seconds: Per-request timeout.

    Returns:
        Parsed JSON object.
    """

    with urllib.request.urlopen(base_url + path, timeout=timeout_seconds) as response:
        return json.loads(response.read().decode("utf-8"))


def _post_json(base_url: str, path: str, body: dict[str, Any], *, timeout_seconds: int) -> dict[str, Any]:
    """Post JSON to the temporary server.

    Args:
        base_url: Temporary server base URL.
        path: HTTP path to request.
        body: JSON request body.
        timeout_seconds: Per-request timeout.

    Returns:
        Parsed JSON response.
    """

    request = urllib.request.Request(
        base_url + path,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        return json.loads(response.read().decode("utf-8"))


def _payload(*, allow_cloud_image: bool) -> dict[str, Any]:
    """Build a synthetic v2 image-analysis payload."""

    return {
        "input_id": "http-smoke-v2-001",
        "source_type": "screenshot_share",
        "image": {
            "data_url": DEFAULT_IMAGE_DATA_URL,
            "mime": "image/png",
            "width": 1,
            "height": 1,
            "sha256": "http-smoke-synthetic-image",
        },
        "ocr_text_hint": "今晚18:30 项目讨论 B203",
        "ocr_blocks": [],
        "current_date": "2026-06-07",
        "user_timezone": "Asia/Shanghai",
        "allow_cloud_image": allow_cloud_image,
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


def run_http_smoke(*, timeout_seconds: int, allow_cloud_image: bool) -> bool:
    """Run a temporary uvicorn server and smoke-test real HTTP routes.

    Args:
        timeout_seconds: Per-request timeout.
        allow_cloud_image: Whether the request should allow backend image-model calls.

    Returns:
        True when all HTTP route checks pass and the server log is secret-safe.
    """

    port = _free_port()
    base_url = f"http://127.0.0.1:{port}"
    env = dict(os.environ)
    existing_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(BACKEND_ROOT) if not existing_pythonpath else f"{BACKEND_ROOT}{os.pathsep}{existing_pythonpath}"
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "shike_backend.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        cwd=str(BACKEND_ROOT),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    route_ok = False
    log_secret_safe = False
    try:
        for _ in range(max(1, timeout_seconds * 4)):
            try:
                health = _get_json(base_url, "/health", timeout_seconds=1)
                if health.get("status") == "ok":
                    break
            except Exception:
                time.sleep(0.25)
        else:
            _print_evidence("http_smoke_status", "fail")
            _print_evidence("http_smoke_error", "server_start_timeout")
            return False

        health = _get_json(base_url, "/health", timeout_seconds=timeout_seconds)
        schema = _get_json(base_url, "/v2/schema", timeout_seconds=timeout_seconds)
        result = _post_json(
            base_url,
            "/v2/analyze-image",
            _payload(allow_cloud_image=allow_cloud_image),
            timeout_seconds=max(timeout_seconds, 40),
        )
        actions = result.get("suggested_actions", [])
        actions_disabled = bool(actions) and all(
            action.get("disabled_reason") == "用户确认前不可执行" for action in actions
        )
        schema_valid = bool(result.get("title")) and bool(actions)
        raw_ignored_regions = result.get("ignored_regions", [])
        ignored_regions_allowed = _ignored_regions_allowed(raw_ignored_regions)
        ignored_regions = ",".join(raw_ignored_regions if isinstance(raw_ignored_regions, list) else [])
        route_ok = schema_valid and actions_disabled and ignored_regions_allowed
        _print_evidence("http_smoke_health_status", health.get("status"))
        _print_evidence("http_smoke_schema_has_title", "title" in schema)
        _print_evidence("http_smoke_route_status", "pass" if route_ok else "fail")
        _print_evidence("http_smoke_scene_type", result.get("scene_type", "unknown"))
        _print_evidence("http_smoke_actions_disabled", actions_disabled)
        _print_evidence("http_smoke_ignored_regions_allowed", ignored_regions_allowed)
        _print_evidence("http_smoke_ignored_regions", ignored_regions)
        _print_evidence("http_smoke_risk_kinds", ",".join(str(item).split(":", 1)[0] for item in result.get("risks", [])))
    finally:
        proc.terminate()
        try:
            log_text, _ = proc.communicate(timeout=8)
        except subprocess.TimeoutExpired:
            proc.kill()
            log_text, _ = proc.communicate(timeout=8)
        has_secret_marker = any(marker.lower() in log_text.lower() for marker in SECRET_MARKERS)
        log_secret_safe = not has_secret_marker
        _print_evidence("http_smoke_log_secret_scan", "fail" if has_secret_marker else "pass")
    return route_ok and log_secret_safe


def main() -> int:
    """Run CLI entrypoint."""

    parser = argparse.ArgumentParser(description="Run a redacted temporary HTTP server smoke.")
    parser.add_argument("--timeout-seconds", type=int, default=20, help="Per-request timeout.")
    parser.add_argument(
        "--disable-cloud-image",
        action="store_true",
        help="Pass allow_cloud_image=false to prove the no-cloud-image branch over HTTP.",
    )
    args = parser.parse_args()
    ok = run_http_smoke(
        timeout_seconds=args.timeout_seconds,
        allow_cloud_image=not args.disable_cloud_image,
    )
    _print_evidence("http_server_smoke_metric", "1/1" if ok else "0/1")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
