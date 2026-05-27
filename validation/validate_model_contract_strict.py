#!/usr/bin/env python3
"""Strictly validate model output samples and backend responses against JSON Schema."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import jsonschema


WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "shike"


def read_json(relative: str) -> object:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def command_passes(command: list[str]) -> bool:
    result = subprocess.run(command, cwd=WORKSPACE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return result.returncode == 0


def validate(schema: dict, payload: object) -> bool:
    try:
        jsonschema.validate(instance=payload, schema=schema)
        return True
    except jsonschema.ValidationError:
        return False


def main() -> int:
    schema = read_json("contracts/model-output.schema.json")
    course_sample = read_json("contracts/sample-course-response.json")
    event_sample = read_json("contracts/sample-event-response.json")

    checks = [
        ("course_sample_schema_valid", validate(schema, course_sample)),
        ("event_sample_schema_valid", validate(schema, event_sample)),
        ("backend_smoke_passes", command_passes(["python3", "shike/backend/verify_backend.py"])),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"MODEL_CONTRACT_STRICT_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())

