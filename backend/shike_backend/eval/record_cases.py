#!/usr/bin/env python3
"""Record provider responses for a subset of regression cases.

This is a practical demo tool:
- Runs with `SHIKE_MODEL_PROVIDER=recorded_bluelm`
- If BlueLM credentials are configured, it will call the online provider and
  write recordings under `shike/backend/shike_backend/eval/recordings/`.
- If not configured, it will fail fast (so you don't think you recorded).

Safety:
- Only run this on synthetic cases under `shike/validation/regression-cases.json`.
- Do not feed real screenshots/OCR containing PII.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Ensure imports work when running directly.
_BACKEND_ROOT = Path(__file__).resolve().parents[2]
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from shike_backend.adapters.bluelm_adapter import BlueLMModelAdapter
from shike_backend.adapters.recorded_bluelm_adapter import RecordedBlueLMAdapter
from shike_backend.schemas import AnalyzeRequest
from shike_backend.settings import Settings


WORKSPACE = Path(__file__).resolve().parents[4]
SHIKE_ROOT = WORKSPACE / "shike"
CASES_PATH = SHIKE_ROOT / "validation/regression-cases.json"


def main() -> int:
    limit = int(os.getenv("SHIKE_RECORD_LIMIT", "10"))
    settings = Settings.from_env()

    base = BlueLMModelAdapter(
        app_id=settings.bluelm_app_id,
        app_key=settings.bluelm_app_key,
        base_url=settings.bluelm_base_url,
        uri=settings.bluelm_uri,
        model=settings.bluelm_model,
        timeout_seconds=settings.bluelm_timeout_seconds,
        max_retries=settings.bluelm_max_retries,
        temperature=settings.bluelm_temperature,
    )
    if not base.is_configured():
        print("ERR\tbluelm_not_configured")
        return 2

    recorder = RecordedBlueLMAdapter(recording_dir=Path(settings.recorded_dir), base=base)
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    if not isinstance(cases, list):
        print("ERR\tinvalid_cases")
        return 2

    recorded = 0
    for case in cases:
        if not isinstance(case, dict) or "id" not in case or "input" not in case:
            continue
        if recorded >= limit:
            break
        req = AnalyzeRequest(
            input_id=case["id"],
            source_type="screenshot",
            ocr_text=case["input"],
            scene_hint=case.get("scene"),
            locale="zh-CN",
            user_timezone="Asia/Shanghai",
        )
        recorder.analyze(req)
        recorded += 1
        print(f"RECORDED\t{case['id']}")

    print(f"RECORDED_COUNT\t{recorded}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

