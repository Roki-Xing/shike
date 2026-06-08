#!/usr/bin/env python3
"""Validate server-side vivo OCR import API plumbing without real credentials."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "shike"


def read(relative: str) -> str:
    """Read a UTF-8 project file."""

    path = ROOT / relative
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def command_passes(command: list[str], env: dict[str, str] | None = None) -> bool:
    """Run a command from the workspace root."""

    result = subprocess.run(
        command,
        cwd=WORKSPACE,
        env=(os.environ | env) if env else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return result.returncode == 0


def main() -> int:
    adapter = read("backend/shike_backend/adapters/vivo_ocr_adapter.py")
    settings = read("backend/shike_backend/settings.py")
    schemas = read("backend/shike_backend/schemas.py")
    main_py = read("backend/shike_backend/main.py")
    live_smoke = read("backend/shike_backend/eval/live_smoke.py")
    runbook = read("docs/bluelm-integration-runbook.md")
    android_ocr = read("android-mvp/app/src/main/java/cn/shike/app/data/OcrEngine.kt")

    required_files = [
        "backend/shike_backend/adapters/vivo_ocr_adapter.py",
        "backend/shike_backend/settings.py",
        "backend/shike_backend/schemas.py",
        "backend/shike_backend/main.py",
        "backend/shike_backend/eval/live_smoke.py",
    ]

    checks = [
        ("secret_hygiene_passes", command_passes(["python3", "shike/validation/validate_secret_hygiene.py"])),
        ("backend_smoke_passes", command_passes(["python3", "shike/backend/verify_backend.py"])),
        ("required_files_exist", all((ROOT / path).is_file() for path in required_files)),
        (
            "ocr_schema_present",
            "class OcrRequest" in schemas
            and "class OcrResponse" in schemas
            and 'Literal["screenshot", "camera"]' in schemas
            and "image_base64" in schemas,
        ),
        (
            "vivo_ocr_body_matches_doc",
            all(
                token in adapter
                for token in [
                    "/ocr/general_recognition",
                    "application/x-www-form-urlencoded",
                    '"image"',
                    '"pos"',
                    '"businessid"',
                    'f"aigc{self._app_id}"',
                    '"requestId"',
                    '"Authorization"',
                    "Bearer",
                ]
            ),
        ),
        (
            "ocr_route_present",
            '@app.post("/v1/ocr"' in main_py
            and "VivoOcrAdapter" in main_py
            and "fallback_ocr_response" in main_py,
        ),
        (
            "ocr_env_config_present",
            all(
                token in settings
                for token in [
                    "VIVO_OCR_APP_ID",
                    "VIVO_OCR_APP_KEY",
                    "VIVO_AIGC_APP_ID",
                    "VIVO_AIGC_APP_KEY",
                    "VIVO_OCR_BASE_URL",
                    "VIVO_OCR_URI",
                    "SHIKE_ALLOW_OCR_FALLBACK",
                ]
            ),
        ),
        (
            "ocr_fallback_without_credentials",
            command_passes(
                ["python3", "shike/backend/verify_backend.py"],
                env={
                    "VIVO_OCR_APP_ID": "",
                    "VIVO_OCR_APP_KEY": "",
                    "SHIKE_ALLOW_OCR_FALLBACK": "true",
                },
            ),
        ),
        (
            "runbook_documents_vivo_ocr",
            all(
                token in runbook
                for token in [
                    "/v1/ocr",
                    "/ocr/general_recognition",
                    "businessid",
                    "aigc + AppID",
                    "VIVO_OCR_APP_ID",
                    "VIVO_OCR_APP_KEY",
                    "image_base64",
                    "Android 不得",
                ]
            ),
        ),
        (
            "android_still_has_no_vivo_secret_config",
            "VIVO_OCR_APP_KEY" not in android_ocr and "BLUELM_APP_KEY" not in android_ocr and "sk-" not in android_ocr,
        ),
        (
            "live_smoke_is_secret_safe",
            all(
                token in live_smoke
                for token in [
                    "Run secret-safe live smoke",
                    "--ocr-image",
                    "result_schema_valid",
                    "image_base64_present",
                    "image_persisted",
                    "missing_ocr_image",
                    "live_smoke_metric",
                ]
            )
            and "Authorization" not in live_smoke
            and "AppKEY" in live_smoke
            and "values" in live_smoke,
        ),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"VIVO_OCR_ADAPTER_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
