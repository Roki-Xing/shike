#!/usr/bin/env python3
"""Run a lightweight adapter evaluation on regression cases.

This is designed for demo readiness:
- Uses the same AnalyzeRequest/AnalyzeResponse contract as Android.
- Validates each output against `contracts/model-output.schema.json`.
- Produces a markdown report under `shike/docs/model-eval-report.md`.
- Supports partial runs with batch offsets and observable progress output.

By default it evaluates the currently configured backend provider:
  SHIKE_MODEL_PROVIDER=mock | bluelm | recorded_bluelm
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
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
    source_index: int
    case_id: str
    scene_expected: str
    ok: bool
    reason: str


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _action_types(response: dict[str, Any]) -> set[str]:
    return {item.get("type", "") for item in response.get("suggested_actions", []) if isinstance(item, dict)}


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(SHIKE_ROOT))
    except ValueError:
        return str(path)


def _run_secret_hygiene() -> bool:
    result = subprocess.run(
        ["python3", "shike/validation/validate_secret_hygiene.py"],
        cwd=WORKSPACE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return result.returncode == 0


def _case_records(raw_cases: list[Any]) -> list[tuple[int, dict[str, Any]]]:
    records: list[tuple[int, dict[str, Any]]] = []
    for index, case in enumerate(raw_cases, start=1):
        if isinstance(case, dict) and "id" in case and "input" in case:
            records.append((index, case))
    return records


def evaluate_case(adapter: Any, schema: dict[str, Any], case: dict[str, Any], source_index: int) -> CaseResult:
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
        return CaseResult(
            source_index=source_index,
            case_id=case["id"],
            scene_expected=case.get("scene", ""),
            ok=False,
            reason=f"adapter_error:{exc.message}",
        )

    response = response_model.model_dump()

    try:
        jsonschema.validate(instance=response, schema=schema)
    except jsonschema.ValidationError:
        return CaseResult(
            source_index=source_index,
            case_id=case["id"],
            scene_expected=case.get("scene", ""),
            ok=False,
            reason="schema_invalid",
        )

    expected_scene = case.get("scene")
    allowed_scenes = set(schema.get("properties", {}).get("scene_type", {}).get("enum", []))
    # Some regression groups use extended labels (e.g. "meeting_notice") that are
    # not part of the current response contract. Only enforce scene match when
    # the expected value is in the contract enum.
    if expected_scene and expected_scene in allowed_scenes and response.get("scene_type") != expected_scene:
        return CaseResult(
            source_index=source_index,
            case_id=case["id"],
            scene_expected=expected_scene,
            ok=False,
            reason="scene_mismatch",
        )

    expected_actions = set(case.get("expected_actions", []))
    if expected_actions:
        got = _action_types(response)
        if not expected_actions.issubset(got):
            return CaseResult(
                source_index=source_index,
                case_id=case["id"],
                scene_expected=expected_scene or "",
                ok=False,
                reason="actions_missing",
            )

    expected_fields = set(case.get("expected_fields", []))
    if "time" in expected_fields and response.get("time") is None:
        return CaseResult(
            source_index=source_index,
            case_id=case["id"],
            scene_expected=expected_scene or "",
            ok=False,
            reason="time_missing",
        )
    if "location" in expected_fields and response.get("location") is None:
        return CaseResult(
            source_index=source_index,
            case_id=case["id"],
            scene_expected=expected_scene or "",
            ok=False,
            reason="location_missing",
        )

    expected_missing = set(case.get("expected_missing_fields", []))
    if expected_missing:
        missing_fields = set(response.get("missing_fields", []))
        if not expected_missing.issubset(missing_fields):
            return CaseResult(
                source_index=source_index,
                case_id=case["id"],
                scene_expected=expected_scene or "",
                ok=False,
                reason="missing_fields_not_marked",
            )

    return CaseResult(source_index=source_index, case_id=case["id"], scene_expected=expected_scene or "", ok=True, reason="ok")


def _build_report(
    provider: str,
    cases_path: Path,
    report_path: Path,
    total_available: int,
    offset: int,
    limit: int | None,
    results: list[CaseResult],
    elapsed_seconds: float,
) -> str:
    passed = sum(1 for result in results if result.ok)
    selected_total = len(results)
    limit_text = "all" if limit is None else str(limit)
    lines = [
        "# Model Eval Report",
        "",
        f"- provider: `{provider}`",
        f"- cases file: `{_display_path(cases_path)}`",
        f"- report file: `{_display_path(report_path)}`",
        f"- selection: `{selected_total}` of `{total_available}` valid cases",
        f"- slice: `offset={offset}` `limit={limit_text}`",
        f"- passed: `{passed}/{selected_total}`",
        f"- elapsed seconds: `{elapsed_seconds:.2f}`",
        "",
        "| source_index | id | expected_scene | result | reason |",
        "| --- | --- | --- | --- | --- |",
    ]
    for result in results:
        lines.append(
            f"| {result.source_index} | {result.case_id} | {result.scene_expected} | {'PASS' if result.ok else 'FAIL'} | {result.reason} |"
        )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Shike adapter regression evaluation.")
    parser.add_argument("--cases-path", type=Path, default=CASES_PATH, help="Path to regression-cases.json.")
    parser.add_argument("--report-path", type=Path, default=REPORT_PATH, help="Markdown report output path.")
    parser.add_argument("--offset", type=int, default=0, help="Skip this many valid cases before evaluating.")
    parser.add_argument("--limit", type=int, default=None, help="Evaluate at most this many valid cases after offset.")
    parser.add_argument(
        "--progress-every",
        type=int,
        default=10,
        help="Print progress every N evaluated cases; use 0 to disable periodic progress lines.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.offset < 0:
        print("invalid offset; must be >= 0")
        return 2
    if args.limit is not None and args.limit <= 0:
        print("invalid limit; must be > 0 when provided")
        return 2
    if args.progress_every < 0:
        print("invalid progress-every; must be >= 0")
        return 2

    if not args.cases_path.is_file():
        print(f"missing regression cases: {args.cases_path}")
        return 2

    if not _run_secret_hygiene():
        print("secret hygiene failed; abort eval")
        return 3

    schema = load_model_output_schema()
    cases = _read_json(args.cases_path)
    if not isinstance(cases, list):
        print("invalid regression cases format")
        return 2

    records = _case_records(cases)
    if not records:
        print("no valid regression cases found")
        return 2

    if args.offset >= len(records):
        print(f"offset {args.offset} exceeds available valid cases {len(records)}")
        return 2

    end_index = len(records) if args.limit is None else min(args.offset + args.limit, len(records))
    selected_records = records[args.offset:end_index]
    if not selected_records:
        print("no cases selected for evaluation")
        return 2

    provider = os.getenv("SHIKE_MODEL_PROVIDER", "mock")
    adapter = _get_adapter()
    print(
        "MODEL_EVAL_START\t"
        f"provider={provider}\t"
        f"selected={len(selected_records)}\t"
        f"total_valid={len(records)}\t"
        f"offset={args.offset}\t"
        f"limit={'all' if args.limit is None else args.limit}"
    )

    results: list[CaseResult] = []
    started = time.perf_counter()
    for selected_index, (source_index, case) in enumerate(selected_records, start=1):
        result = evaluate_case(adapter, schema, case, source_index)
        results.append(result)
        if args.progress_every and (
            selected_index == 1 or selected_index % args.progress_every == 0 or selected_index == len(selected_records)
        ):
            print(
                "MODEL_EVAL_PROGRESS\t"
                f"{selected_index}/{len(selected_records)}\t"
                f"source_index={source_index}\t"
                f"case_id={result.case_id}\t"
                f"result={'PASS' if result.ok else 'FAIL'}\t"
                f"reason={result.reason}"
            )

    elapsed_seconds = time.perf_counter() - started
    passed = sum(1 for r in results if r.ok)
    total = len(results)

    args.report_path.parent.mkdir(parents=True, exist_ok=True)
    args.report_path.write_text(
        _build_report(
            provider=provider,
            cases_path=args.cases_path,
            report_path=args.report_path,
            total_available=len(records),
            offset=args.offset,
            limit=args.limit,
            results=results,
            elapsed_seconds=elapsed_seconds,
        ),
        encoding="utf-8",
    )

    print(f"model_eval_report_written\t{_display_path(args.report_path)}")
    print(
        "MODEL_EVAL_METRIC\t"
        f"{passed}/{total}\t"
        f"selected={total}\t"
        f"total_valid={len(records)}\t"
        f"elapsed_seconds={elapsed_seconds:.2f}"
    )
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
