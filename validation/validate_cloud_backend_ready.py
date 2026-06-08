#!/usr/bin/env python3
"""Validate backend deployment readiness for cloud device testing.

This is not a live server verifier. It checks that the backend code and docs
support a secret-safe HTTPS deployment shape before operators collect cloud
device evidence.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "shike"


def command_passes(command: list[str]) -> bool:
    result = subprocess.run(command, cwd=WORKSPACE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return result.returncode == 0


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def main() -> int:
    settings_py = read("backend/shike_backend/settings.py")
    http_server_smoke = read("backend/shike_backend/eval/http_server_smoke.py")
    guide = read("docs/SHIKE_LANDING_APP_OPTIMIZATION_GUIDE.md")
    runbook = read("docs/server-deployment-runbook.md")

    checks = [
        ("secret_hygiene_passes", command_passes(["python3", "shike/validation/validate_secret_hygiene.py"])),
        ("backend_smoke_passes", command_passes(["python3", "shike/backend/verify_backend.py"])),
        ("settings_support_base_url_and_uri", "BLUELM_BASE_URL" in settings_py and "BLUELM_URI" in settings_py),
        ("provider_switch_supported", "SHIKE_MODEL_PROVIDER" in settings_py and "bluelm" in settings_py),
        ("guide_has_https_endpoints_requirements", "https://your-domain.example.com/health" in guide and "/v1/analyze" in guide),
        (
            "server_runbook_exists",
            all(
                token in runbook
                for token in [
                    "Shike Server Deployment Runbook",
                    "https://roky.chat",
                    "https://api.roky.chat",
                    "/etc/shike/shike-backend.env",
                    "/opt/shike/backend",
                    "systemd",
                    "Nginx HTTPS Proxy",
                    "certbot",
                ]
            ),
        ),
        (
            "server_runbook_has_public_smoke",
            all(
                token in runbook
                for token in [
                    "curl -fsS https://roky.chat/health",
                    "curl -fsS https://roky.chat/v1/schema",
                    "curl -fsS https://roky.chat/v1/analyze",
                    "cloud-smoke-001",
                    "shike_backend.eval.http_server_smoke",
                ]
            ),
        ),
        (
            "server_runbook_and_audit_logs_secret_safe",
            all(
                token in runbook
                for token in [
                    "Forbidden locations",
                    "BLUELM_APP_KEY=***",
                    "VIVO_AIGC_APP_KEY=***",
                    "VIVO_OCR_APP_KEY=***",
                    "VIVO_MULTIMODAL_APP_KEY=***",
                    "VIVO_MULTIMODAL_MODELS",
                    "Never log",
                    "Authorization",
                    "full OCR text",
                    "base64 image payload",
                ]
            )
            and re.search(r"sk-[A-Za-z0-9_=+-]{16,}", runbook) is None
            and command_passes(["python3", "shike/validation/validate_backend_audit_log.py"]),
        ),
        (
            "http_server_smoke_script_secret_safe",
            all(
                token in http_server_smoke
                for token in [
                    "uvicorn",
                    "/v2/analyze-image",
                    "http_smoke_actions_disabled",
                    "http_smoke_ignored_regions_allowed",
                    "http_smoke_log_secret_scan",
                    "http_server_smoke_metric",
                ]
            )
            and "AppKEY" in http_server_smoke
            and "Authorization" in http_server_smoke
            and re.search(r"sk-[A-Za-z0-9_=+-]{16,}", http_server_smoke) is None,
        ),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"CLOUD_BACKEND_READY_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
