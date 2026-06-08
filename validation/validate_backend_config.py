#!/usr/bin/env python3
"""Validate configurable backend URL readiness for emulator and real devices."""

from __future__ import annotations

import subprocess
import re
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
    settings_py = read("backend/shike_backend/settings.py")
    backend_smoke = read("backend/verify_backend.py")
    http_server_smoke = read("backend/shike_backend/eval/http_server_smoke.py")
    docs = "\n".join(
        read(path)
        for path in [
            "docs/android-mvp-implementation.md",
            "docs/device-runbook.md",
            "README.md",
            "docs/bluelm-integration-runbook.md",
            "docs/server-deployment-runbook.md",
        ]
    )

    checks = [
        ("manual_review_checks_pass", command_passes(["python3", "shike/validation/validate_manual_review.py"])),
        ("default_backend_url_present", "DEFAULT_BACKEND_BASE_URL = \"https://roky.chat\"" in android_source),
        ("backend_url_state_present", "var backendUrl by remember" in android_source),
        ("backend_url_field_visible", "label = { Text(\"后端地址\") }" in android_source),
        ("save_backend_button_present", "保存后端地址" in android_source),
        ("backend_url_preference_key_present", "KEY_BACKEND_BASE_URL" in android_source and "backend_base_url" in android_source),
        ("backend_url_saved_to_preferences", "saveBackendBaseUrl" in android_source and ".putString(KEY_BACKEND_BASE_URL" in android_source),
        ("backend_url_loaded_from_preferences", "loadBackendBaseUrl" in android_source and "initialBackendUrl" in android_source),
        ("backend_url_normalized", "normalizeBackendUrl" in android_source and "trimEnd('/')" in android_source),
        ("call_analyze_uses_configured_url", "callAnalyzeApi(endpoint" in android_source and "normalizeBackendUrl(backendBaseUrl)" in android_source),
        ("real_device_lan_documented", "https://roky.chat" in docs and "192.168.1.10:8000" in docs and "后端地址" in docs),
        ("config_documented", "保存后端地址" in docs and "真机" in docs),
        (
            "backend_private_env_file_supported",
            "SHIKE_BACKEND_ENV_FILE" in settings_py
            and "DEFAULT_BACKEND_ENV_FILE" in settings_py
            and ".config/shike/bluelm.env" in settings_py
            and "_private_env_file_values" in settings_py,
        ),
        (
            "android16_vivo_env_aliases_supported",
            "VIVO_APP_ID" in settings_py
            and "VIVO_APP_KEY" in settings_py
            and "VIVO_CHAT_BASE_URL" in settings_py
            and "VIVO_CHAT_MODEL" in settings_py
            and "_split_vivo_chat_base_url" in settings_py
            and "test_from_env_accepts_android16_guide_vivo_aliases" in read("backend/tests/test_settings_env_file.py"),
        ),
        (
            "backend_smoke_is_env_isolated",
            "SHIKE_BACKEND_ENV_FILE" in backend_smoke
            and "/dev/null" in backend_smoke
            and 'os.environ["SHIKE_MODEL_PROVIDER"] = "mock"' in backend_smoke,
        ),
        (
            "private_env_file_documented",
            "~/.config/shike/bluelm.env" in docs
            and "SHIKE_BACKEND_ENV_FILE" in docs
            and "进程环境变量优先" in docs
            and "Never commit real values" in docs,
        ),
        (
            "http_server_smoke_script_present",
            "uvicorn" in http_server_smoke
            and "BACKEND_ROOT = Path(__file__).resolve().parents[2]" in http_server_smoke
            and "http_server_smoke_metric" in http_server_smoke,
        ),
        (
            "http_server_smoke_exercises_v2_image_route",
            "/health" in http_server_smoke
            and "/v2/schema" in http_server_smoke
            and "/v2/analyze-image" in http_server_smoke
            and "http_smoke_actions_disabled" in http_server_smoke
            and "http_smoke_ignored_regions_allowed" in http_server_smoke
            and "http_smoke_log_secret_scan" in http_server_smoke,
        ),
        (
            "vivo_private_env_aliases_documented",
            all(
                token in docs
                for token in [
                    "VIVO_AIGC_APP_ID=***",
                    "VIVO_AIGC_APP_KEY=***",
                    "VIVO_APP_ID=***",
                    "VIVO_APP_KEY=***",
                    "VIVO_CHAT_BASE_URL=https://api-ai.vivo.com.cn/v1",
                    "VIVO_CHAT_MODEL=",
                    "VIVO_OCR_APP_ID=***",
                    "VIVO_OCR_APP_KEY=***",
                    "VIVO_MULTIMODAL_APP_ID=***",
                    "VIVO_MULTIMODAL_APP_KEY=***",
                    "VIVO_MULTIMODAL_MODELS",
                ]
            )
            and re.search(r"sk-[A-Za-z0-9_=+-]{16,}", docs) is None,
        ),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"BACKEND_CONFIG_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
