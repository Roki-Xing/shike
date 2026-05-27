#!/usr/bin/env python3
"""Validate minimal backend configuration readiness for cloud device testing.

This is not a deployment verifier. It checks that the backend code supports
runtime configuration needed for an HTTPS-deployed instance, and that core
routes remain stable.
"""

from __future__ import annotations

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
    guide = read("docs/SHIKE_LANDING_APP_OPTIMIZATION_GUIDE.md")

    checks = [
        ("secret_hygiene_passes", command_passes(["python3", "shike/validation/validate_secret_hygiene.py"])),
        ("backend_smoke_passes", command_passes(["python3", "shike/backend/verify_backend.py"])),
        ("settings_support_base_url_and_uri", "BLUELM_BASE_URL" in settings_py and "BLUELM_URI" in settings_py),
        ("provider_switch_supported", "SHIKE_MODEL_PROVIDER" in settings_py and "bluelm" in settings_py),
        ("guide_has_https_endpoints_requirements", "https://your-domain.example.com/health" in guide and "/v1/analyze" in guide),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"CLOUD_BACKEND_READY_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())

