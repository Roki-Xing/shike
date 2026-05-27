#!/usr/bin/env python3
"""Run a lightweight adapter evaluation on regression cases.

This is designed for demo readiness:
- Uses the same AnalyzeRequest/AnalyzeResponse contract as Android.
- Validates each output against `contracts/model-output.schema.json`.
- Produces a small markdown report under `shike/docs/model-eval-report.md`.

By default it evaluates the currently configured backend provider:
  SHIKE_MODEL_PROVIDER=mock | bluelm | recorded_bluelm
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import jsonschema

# Make `shike_backend` importable when running this file directly from workspace root.
_BACKEND_ROOT = Path(__file__).resolve().parents[2]
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from shike_backend.adapters.base import AdapterError
from shike_backend.main import _get_adapter  # intentionally reuse backend selection
from shike_backend.schemas import AnalyzeRequest, load_model_output_schema


WORKSPACE = Path(__file__).resolve().parents[4]
SHIKE_ROOT = WORKSPACE / "shike"
CASES_PATH = SHIKE_ROOT / "validation/regression-cases.json"
REPORT_PATH = SHIKE_ROOT / "docs/model-eval-report.md"


@dataclass(frozen=True)
class CaseResult:
    case_id: str
    scene_expected: str
    ok: bool
    reason: str


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _action_types(response: dict[str, Any]) -> set[str]:
    return {item.get("type", "") for item in response.get("suggested_actions", []) if isinstance(item, dict)}


def _run_secret_hygiene() -> bool:
    result = subprocess.run(
        ["python3", "shike/validation/validate_secret_hygiene.py"],
        cwd=WORKSPACE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return result.returncode == 0


def evaluate_case(schema: dict[str, Any], case: dict[str, Any]) -> CaseResult:
    adapter = _get_adapter()
    request = AnalyzeRequest(
        input_id=case["id"],
        source_type="screenshot",
        ocr_text=case["input"],
        scene_hint=case.get("scene"),
        locale="zh-CN",
        user_timezone="Asia/Shanghai",
    )

    try:
        response_model = adapter.analyze(request)  # type: ignore[attr-defined]
    except AdapterError as exc:
        return CaseResult(case_id=case["id"], scene_expected=case.get("scene", ""), ok=False, reason=f"adapter_error:{exc.message}")

    response = response_model.model_dump()

    try:
        jsonschema.validate(instance=response, schema=schema)
    except jsonschema.ValidationError:
        return CaseResult(case_id=case["id"], scene_expected=case.get("scene", ""), ok=False, reason="schema_invalid")

    expected_scene = case.get("scene")
    allowed_scenes = set(schema.get("properties", {}).get("scene_type", {}).get("enum", []))
    # Some regression groups use extended labels (e.g. "meeting_notice") that are
    # not part of the current response contract. Only enforce scene match when
    # the expected value is in the contract enum.
    if expected_scene and expected_scene in allowed_scenes and response.get("scene_type") != expected_scene:
        return CaseResult(case_id=case["id"], scene_expected=expected_scene, ok=False, reason="scene_mismatch")

    expected_actions = set(case.get("expected_actions", []))
    if expected_actions:
        got = _action_types(response)
        if not expected_actions.issubset(got):
            return CaseResult(case_id=case["id"], scene_expected=expected_scene or "", ok=False, reason="actions_missing")

    expected_fields = set(case.get("expected_fields", []))
    if "time" in expected_fields and response.get("time") is None:
        return CaseResult(case_id=case["id"], scene_expected=expected_scene or "", ok=False, reason="time_missing")
    if "location" in expected_fields and response.get("location") is None:
        return CaseResult(case_id=case["id"], scene_expected=expected_scene or "", ok=False, reason="location_missing")

    expected_missing = set(case.get("expected_missing_fields", []))
    if expected_missing:
        missing_fields = set(response.get("missing_fields", []))
        if not expected_missing.issubset(missing_fields):
            return CaseResult(case_id=case["id"], scene_expected=expected_scene or "", ok=False, reason="missing_fields_not_marked")

    return CaseResult(case_id=case["id"], scene_expected=expected_scene or "", ok=True, reason="ok")


def main() -> int:
    if not CASES_PATH.is_file():
        print(f"missing regression cases: {CASES_PATH}")
        return 2

    if not _run_secret_hygiene():
        print("secret hygiene failed; abort eval")
        return 3

    schema = load_model_output_schema()
    cases = _read_json(CASES_PATH)
    if not isinstance(cases, list):
        print("invalid regression cases format")
        return 2

    results: list[CaseResult] = []
    for case in cases:
        if not isinstance(case, dict) or "id" not in case or "input" not in case:
            continue
        results.append(evaluate_case(schema, case))

    passed = sum(1 for r in results if r.ok)
    total = len(results)

    lines = []
    lines.append("# Model Eval Report")
    lines.append("")
    lines.append(f"- cases: {passed}/{total} passed")
    lines.append("")
    lines.append("| id | expected_scene | result | reason |")
    lines.append("| --- | --- | --- | --- |")
    for r in results:
        lines.append(f"| {r.case_id} | {r.scene_expected} | {'PASS' if r.ok else 'FAIL'} | {r.reason} |")
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"model_eval_report_written\t{REPORT_PATH.relative_to(SHIKE_ROOT)}")
    print(f"MODEL_EVAL_METRIC\t{passed}/{total}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
