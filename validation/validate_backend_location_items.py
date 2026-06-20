#!/usr/bin/env python3
"""Validate backend location extraction for plain room numbers."""

from __future__ import annotations

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
        [sys.executable, "-m", "unittest", "backend.tests.test_location_items"],
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
    location = read("backend/shike_backend/location.py")
    main_py = read("backend/shike_backend/main.py")
    tests = read("backend/tests/test_location_items.py")

    checks = [
        ("location_module_present", "extract_location_from_text" in location and "enrich_location_payload" in location),
        ("plain_room_number_patterns_present", all(token in location for token in ["地点是", "教室是", "\\d{2,4}"])),
        ("main_enriches_location_before_preparation", "enrich_location_payload" in main_py and "_card_with_preparation" in main_py),
        (
            "tests_cover_location_303",
            "今天晚上七点需要上高数A 地点303 要考试记得带准考证" in tests and "LocationBlindImageAdapter" in tests,
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
    print(f"BACKEND_LOCATION_ITEMS_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
