#!/usr/bin/env python3
"""Validate configurable backend URL readiness for emulator and real devices."""

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
    docs = "\n".join(
        read(path)
        for path in [
            "docs/android-mvp-implementation.md",
            "docs/device-runbook.md",
            "README.md",
        ]
    )

    checks = [
        ("manual_review_checks_pass", command_passes(["python3", "shike/validation/validate_manual_review.py"])),
        ("default_backend_url_present", "DEFAULT_BACKEND_BASE_URL = \"http://10.0.2.2:8000\"" in android_source),
        ("backend_url_state_present", "var backendUrl by remember" in android_source),
        ("backend_url_field_visible", "label = { Text(\"后端地址\") }" in android_source),
        ("save_backend_button_present", "保存后端地址" in android_source),
        ("backend_url_preference_key_present", "KEY_BACKEND_BASE_URL" in android_source and "backend_base_url" in android_source),
        ("backend_url_saved_to_preferences", "saveBackendBaseUrl" in android_source and ".putString(KEY_BACKEND_BASE_URL" in android_source),
        ("backend_url_loaded_from_preferences", "loadBackendBaseUrl" in android_source and "initialBackendUrl" in android_source),
        ("backend_url_normalized", "normalizeBackendUrl" in android_source and "trimEnd('/')" in android_source),
        ("call_analyze_uses_configured_url", "callAnalyzeApi(endpoint" in android_source and "normalizeBackendUrl(backendBaseUrl)" in android_source),
        ("real_device_lan_documented", "192.168.1.10:8000" in docs and "后端地址" in docs),
        ("config_documented", "保存后端地址" in docs and "真机" in docs),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"BACKEND_CONFIG_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
