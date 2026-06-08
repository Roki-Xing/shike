#!/usr/bin/env python3
"""Validate Android-to-FastAPI model bridge readiness."""

from __future__ import annotations

import subprocess
from pathlib import Path

from source_tree import read_android_source

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    """Read a UTF-8 text file under `shike`.

    Args:
        relative: File path under `shike`.

    Returns:
        File content.
    """

    return (ROOT / relative).read_text(encoding="utf-8")


def command_passes(command: list[str]) -> bool:
    """Run a command from the workspace root and return its pass status.

    Args:
        command: Command and arguments.

    Returns:
        True when the command exits with status code 0.
    """

    result = subprocess.run(command, cwd=ROOT.parent, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return result.returncode == 0


def main() -> int:
    android_source = read_android_source(ROOT)
    manifest = read("android-mvp/app/src/main/AndroidManifest.xml")
    docs = "\n".join(
        read(path)
        for path in [
            "docs/android-mvp-implementation.md",
            "docs/device-runbook.md",
            "README.md",
        ]
    )

    checks = [
        ("persistence_checks_pass", command_passes(["python3", "shike/validation/validate_persistence.py"])),
        ("internet_permission_present", "android.permission.INTERNET" in manifest),
        ("backend_base_url_present", "BACKEND_BASE_URL" in android_source and "https://roky.chat" in android_source),
        ("http_client_present", "HttpURLConnection" in android_source and "requestMethod = \"POST\"" in android_source),
        ("analyze_endpoint_called", "/v1/analyze" in android_source),
        ("json_request_body_present", "JSONObject()" in android_source and "scene_hint" in android_source and "ocr_text" in android_source),
        ("response_json_mapping_present", "itemFromAnalyzeJson" in android_source and "suggested_actions" in android_source),
        ("actions_mapping_present", "actionsFromJson" in android_source and "optJSONArray" in android_source),
        ("backend_buttons_present", "解析当前草稿" in android_source and "活动样例解析" in android_source),
        ("model_status_visible", "modelStatus" in android_source and "模型状态" in android_source),
        (
            "fallback_to_local_confirmation_present",
            "backendFailureOutcome(" in android_source
            and "云侧解析失败，本地待确认" in android_source
            and "云侧暂不可用，已切换为本地确认" in android_source,
        ),
        ("network_timeout_present", "connectTimeout = 8000" in android_source and "readTimeout = 60000" in android_source),
        ("backend_smoke_still_passes", command_passes(["python3", "shike/backend/verify_backend.py"])),
        ("bridge_documented", "https://roky.chat" in docs and "10.0.2.2:8000" in docs and "/v1/analyze" in docs and "回退本地 MockModelAdapter" in docs),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"MODEL_BRIDGE_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
