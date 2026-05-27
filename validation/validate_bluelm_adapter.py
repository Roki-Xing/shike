#!/usr/bin/env python3
"""Validate BlueLM adapter plumbing without requiring real credentials.

This is a structural/contract gate:
- Ensures adapter modules and prompt files exist.
- Ensures `/health`, `/v1/schema`, `/v1/analyze` still work via local smoke.
- Ensures `SHIKE_MODEL_PROVIDER=bluelm` with missing credentials degrades safely.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "shike"


def command_passes(command: list[str], env: dict[str, str] | None = None) -> bool:
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
    required_files = [
        ROOT / "backend/shike_backend/schemas.py",
        ROOT / "backend/shike_backend/settings.py",
        ROOT / "backend/shike_backend/privacy.py",
        ROOT / "backend/shike_backend/adapters/base.py",
        ROOT / "backend/shike_backend/adapters/mock_adapter.py",
        ROOT / "backend/shike_backend/adapters/bluelm_adapter.py",
        ROOT / "backend/shike_backend/adapters/vivo_auth.py",
        ROOT / "backend/shike_backend/prompts/analyze_system_prompt.txt",
        ROOT / "backend/shike_backend/prompts/analyze_user_template.txt",
    ]

    checks: list[tuple[str, bool]] = []
    checks.append(("secret_hygiene_passes", command_passes(["python3", "shike/validation/validate_secret_hygiene.py"])))
    checks.append(("backend_smoke_passes", command_passes(["python3", "shike/backend/verify_backend.py"])))
    checks.append(("required_files_exist", all(p.is_file() for p in required_files)))

    # Provider switch: ensure bluelm mode does not break when credentials are missing.
    checks.append(
        (
            "bluelm_mode_degrades_without_credentials",
            command_passes(
                ["python3", "shike/backend/verify_backend.py"],
                env={
                    "SHIKE_MODEL_PROVIDER": "bluelm",
                    "BLUELM_APP_ID": "",
                    "BLUELM_APP_KEY": "",
                    "SHIKE_ALLOW_MOCK_FALLBACK": "true",
                },
            ),
        )
    )

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"BLUELM_ADAPTER_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())

