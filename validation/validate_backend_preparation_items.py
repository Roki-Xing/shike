#!/usr/bin/env python3
"""Validate backend preparation-item extraction for real screenshot text."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def run_unit_test() -> bool:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "backend")
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "backend.tests.test_preparation_items"],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        print(result.stdout)
    return result.returncode == 0


def main() -> int:
    schemas = read("backend/shike_backend/schemas.py")
    schemas_v2 = read("backend/shike_backend/schemas_v2.py")
    preparation = read("backend/shike_backend/preparation.py")
    main_py = read("backend/shike_backend/main.py")
    prompt = read("backend/shike_backend/prompts/analyze_system_prompt.txt")
    image_prompt = read("backend/shike_backend/prompts/analyze_image_system_prompt.txt")
    contract = json.loads(read("contracts/model-output.schema.json"))
    tests = read("backend/tests/test_preparation_items.py")

    checks = [
        ("v1_schema_has_preparation_fields", "preparation_items" in schemas and "checklist_items" in schemas),
        ("v2_schema_has_preparation_fields", "preparation_items" in schemas_v2 and "checklist_items" in schemas_v2),
        (
            "contract_allows_preparation_fields",
            "preparation_items" in contract["properties"] and "checklist_items" in contract["properties"],
        ),
        (
            "parser_extracts_exam_ticket",
            all(token in preparation for token in ["记得带", "带准考证", "preparation_items_from_text"]),
        ),
        (
            "main_enriches_v1_and_v2",
            all(token in main_py for token in ["_response_with_preparation", "_card_with_preparation", "enrich_preparation_payload"]),
        ),
        (
            "prompts_request_preparation_fields",
            all(token in prompt + image_prompt for token in ["带准考证", "preparation_items", "checklist_items"]),
        ),
        (
            "tests_cover_user_sentence",
            "今天晚上七点需要上高数A 教室是B336 要考试记得带准考证" in tests and "带准考证" in tests,
        ),
        ("unit_test_passes", run_unit_test()),
    ]

    passed = 0
    for name, ok in checks:
        if ok:
            passed += 1
            print(f"PASS\t{name}")
        else:
            print(f"FAIL\t{name}")

    print(f"BACKEND_PREPARATION_ITEMS_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
