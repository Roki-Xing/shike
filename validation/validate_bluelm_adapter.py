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


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8", errors="replace")


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
    adapter_source = read("backend/shike_backend/adapters/bluelm_adapter.py")
    settings_source = read("backend/shike_backend/settings.py")
    runbook = read("docs/bluelm-integration-runbook.md")

    body_probe = """
from shike_backend.adapters.bluelm_adapter import build_bluelm_payload

def body(model, mode):
    return build_bluelm_payload(
        model=model,
        system_prompt="sys",
        user_prompt="user",
        session_id="sid",
        temperature=0.2,
        thinking_mode=mode,
        response_format_enabled=True,
    )

assert "thinking" not in body("Volc-DeepSeek-V3.2", "provider_default")
assert "enable_thinking" not in body("qwen3.5-plus", "provider_default")
assert body("qwen3.5-plus", "disabled")["enable_thinking"] is False
assert body("qwen3.5-plus", "enabled")["enable_thinking"] is True
assert body("Doubao-Seed-2.0-mini", "disabled")["thinking"]["type"] == "disabled"
assert body("Doubao-Seed-2.0-mini", "enabled")["thinking"]["type"] == "enabled"
assert body("Doubao-Seed-2.0-mini", "enable")["thinking"]["type"] == "enable"
assert body("Volc-DeepSeek-V3.2", "disabled")["thinking"]["type"] == "disabled"
"""

    checks: list[tuple[str, bool]] = []
    checks.append(("secret_hygiene_passes", command_passes(["python3", "shike/validation/validate_secret_hygiene.py"])))
    checks.append(("backend_smoke_passes", command_passes(["python3", "shike/backend/verify_backend.py"])))
    checks.append(("required_files_exist", all(p.is_file() for p in required_files)))
    checks.append(
        (
            "model_specific_body_builder_present",
            "def build_bluelm_payload" in adapter_source
            and "enable_thinking" in adapter_source
            and '"thinking"' in adapter_source
            and "BLUELM_THINKING_MODE" in settings_source,
        )
    )
    checks.append(
        (
            "model_specific_body_probe_passes",
            command_passes(
                ["python3", "-c", body_probe],
                env={"PYTHONPATH": str(ROOT / "backend")},
            ),
        )
    )
    checks.append(
        (
            "runbook_documents_body_variants",
            "BLUELM_THINKING_MODE" in runbook
            and "provider_default" in runbook
            and "enable_thinking" in runbook
            and "thinking.type" in runbook
            and "requestId" in runbook
            and "request_id" in runbook,
        )
    )

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
