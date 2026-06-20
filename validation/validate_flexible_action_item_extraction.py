#!/usr/bin/env python3
"""Validate OCR text can become structured, flexible action cards."""

from __future__ import annotations

import json
import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = ROOT / "backend"
CASES_PATH = ROOT / "validation/fixtures/shike_action_card_training_cases_v1.jsonl"
REPORT_PATH = ROOT / "docs/flexible-action-card-eval-report.md"
MIN_MAIN_FIELD_PASS = 52

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

import shike_backend.main as main_module  # noqa: E402
import shike_backend.settings as settings_module  # noqa: E402
from shike_backend.main import app  # noqa: E402


@dataclass(frozen=True)
class CaseResult:
    """Evaluation result for one training-set case."""

    case_id: str
    split: str
    difficulty: str
    main_ok: bool
    forbidden_ok: bool
    scene_ok: bool
    time_ok: bool
    location_ok: bool
    preparation_ok: bool
    actions_ok: bool
    missing_ok: bool
    reasons: list[str]


def read(relative: str) -> str:
    """Read a UTF-8 project file.

    Args:
        relative: File path under the Shike root.

    Returns:
        File content.
    """

    return (ROOT / relative).read_text(encoding="utf-8")


def load_cases() -> list[dict[str, object]]:
    """Load the action-card JSONL training set.

    Returns:
        Case dictionaries in file order.
    """

    return [json.loads(line) for line in CASES_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]


def reset_backend_singletons() -> None:
    """Reset cached backend settings and adapter instances."""

    settings_module._CACHED = None  # type: ignore[attr-defined]
    main_module._ADAPTER = None
    main_module._OCR_ADAPTER = None
    main_module._MULTIMODAL_ADAPTER = None


def analyze_case(client: TestClient, case: dict[str, object], expected: dict[str, object]) -> dict[str, object]:
    """Run a case through `/v2/analyze-image` with OCR text fallback.

    Args:
        client: FastAPI test client.
        case: Training-set case.
        expected: First expected card for the case.

    Returns:
        Parsed response payload.
    """

    response = client.post(
        "/v2/analyze-image",
        json={
            "input_id": case["case_id"],
            "source_type": "screenshot_share",
            "image": None,
            "ocr_text_hint": case["ocr_text"],
            "ocr_blocks": [],
            "current_date": case["reference_date"],
            "user_timezone": case["user_timezone"],
            "locale": "zh-CN",
            "scene_hint": expected["scene_type"],
            "allow_cloud_image": False,
        },
    )
    if response.status_code != 200:
        return {"_http_error": response.status_code, "_body": response.text}
    return response.json()


def evaluate_case(case: dict[str, object], payload: dict[str, object]) -> CaseResult:
    """Evaluate one backend response against training-set expectations."""

    expected = first_expected_card(case)
    reasons: list[str] = []
    if "_http_error" in payload:
        return CaseResult(
            case_id=str(case["case_id"]),
            split=str(case["split"]),
            difficulty=str(case["difficulty"]),
            main_ok=False,
            forbidden_ok=False,
            scene_ok=False,
            time_ok=False,
            location_ok=False,
            preparation_ok=False,
            actions_ok=False,
            missing_ok=False,
            reasons=[f"http_error:{payload['_http_error']}"],
        )

    forbidden_ok = _forbidden_output_clean(payload, case.get("do_not_output", []))
    scene_ok = payload.get("scene_type") == expected.get("scene_type")
    time_ok = _time_matches(payload.get("time"), expected.get("time"))
    location_ok = _location_matches(payload.get("location"), expected.get("location"))
    preparation_ok = _expected_strings_present(
        expected.get("preparation_items"),
        payload.get("preparation_items"),
    )
    actions_ok = _actions_match(payload.get("suggested_actions"), expected.get("suggested_actions"))
    missing_ok = _expected_missing_covered(payload.get("missing_fields"), expected.get("missing_fields"))

    if not forbidden_ok:
        reasons.append("forbidden_output")
    if not scene_ok:
        reasons.append(f"scene:{payload.get('scene_type')}!={expected.get('scene_type')}")
    if not time_ok:
        reasons.append("time")
    if not location_ok:
        reasons.append("location")
    if not preparation_ok:
        reasons.append("preparation")
    if not actions_ok:
        reasons.append("actions")
    if not missing_ok:
        reasons.append("missing_fields")

    main_ok = scene_ok and time_ok and location_ok and preparation_ok and actions_ok and missing_ok
    return CaseResult(
        case_id=str(case["case_id"]),
        split=str(case["split"]),
        difficulty=str(case["difficulty"]),
        main_ok=main_ok,
        forbidden_ok=forbidden_ok,
        scene_ok=scene_ok,
        time_ok=time_ok,
        location_ok=location_ok,
        preparation_ok=preparation_ok,
        actions_ok=actions_ok,
        missing_ok=missing_ok,
        reasons=reasons,
    )


def first_expected_card(case: dict[str, object]) -> dict[str, object]:
    """Return the first expected card from a training-set case."""

    cards = case["expected_cards"]
    if not isinstance(cards, list) or not cards or not isinstance(cards[0], dict):
        raise ValueError(f"invalid expected_cards for {case.get('case_id')}")
    return cards[0]


def _time_matches(actual: object, expected: object) -> bool:
    if not isinstance(expected, dict):
        return actual is None
    expected_has_visible_time = any(expected.get(field) is not None for field in ("start_text", "deadline_text"))
    if not expected_has_visible_time:
        return actual is None or isinstance(actual, dict)
    if not isinstance(actual, dict):
        return False
    return all(
        _field_matches(actual.get(field), expected.get(field))
        for field in ("start_text", "deadline_text")
        if expected.get(field) is not None
    )


def _location_matches(actual: object, expected: object) -> bool:
    if expected is None:
        return actual is None
    if not isinstance(expected, dict) or not isinstance(actual, dict):
        return False
    expected_raw = str(expected.get("raw") or "")
    actual_text = json.dumps(actual, ensure_ascii=False)
    return _field_matches(actual.get("raw"), expected_raw) or expected_raw in actual_text


def _field_matches(actual: object, expected: object) -> bool:
    if expected is None:
        return actual is None
    expected_text = _compact(str(expected))
    actual_text = _compact(str(actual or ""))
    return bool(expected_text and (expected_text in actual_text or actual_text in expected_text))


def _expected_strings_present(expected: object, actual: object) -> bool:
    if not isinstance(expected, list) or not expected:
        return True
    if not isinstance(actual, list):
        return False
    actual_texts = [str(item) for item in actual if isinstance(item, str)]
    return all(any(_field_matches(got, item) for got in actual_texts) for item in expected if isinstance(item, str))


def _actions_match(actual: object, expected: object) -> bool:
    if not isinstance(expected, list) or not isinstance(actual, list):
        return True
    expected_types = {item.get("type") for item in expected if isinstance(item, dict)}
    actual_types = {item.get("type") for item in actual if isinstance(item, dict)}
    return expected_types.issubset(actual_types)


def _expected_missing_covered(actual: object, expected: object) -> bool:
    if not isinstance(expected, list) or not expected:
        return True
    if not isinstance(actual, list):
        return False
    actual_items = {str(item) for item in actual}
    return all(str(item) in actual_items for item in expected)


def _compact(value: str) -> str:
    return value.replace(" ", "").replace("-", "").replace("在", "").replace("是", "")


def _forbidden_output_clean(payload: dict[str, object], forbidden: object) -> bool:
    """Return whether forbidden strings are absent from user-visible fields."""

    if not isinstance(forbidden, list) or not forbidden:
        return True
    visible = _visible_payload_text(payload)
    serialized = json.dumps(payload, ensure_ascii=False)
    for token in forbidden:
        value = str(token)
        if value == "null":
            if "null" in visible.lower():
                return False
            continue
        if value in serialized:
            return False
    return True


def _visible_payload_text(value: object) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(_visible_payload_text(item) for item in value)
    if isinstance(value, dict):
        return "\n".join(_visible_payload_text(item) for item in value.values())
    return ""


def run_dataset_eval() -> list[CaseResult]:
    """Run all training-set cases through the backend."""

    env = {
        "SHIKE_BACKEND_ENV_FILE": "/dev/null",
        "SHIKE_RUNTIME_MODE": "release_user",
        "SHIKE_MODEL_PROVIDER": "mock",
        "SHIKE_ALLOW_MOCK_FALLBACK": "true",
    }
    logging.getLogger("shike_backend.audit").disabled = True
    with patch.dict(os.environ, env, clear=True):
        reset_backend_singletons()
        client = TestClient(app)
        return [
            evaluate_case(case, analyze_case(client, case, first_expected_card(case)))
            for case in load_cases()
        ]


def write_report(results: list[CaseResult]) -> None:
    """Write the markdown evaluation report."""

    total = len(results)
    main_passed = sum(result.main_ok for result in results)
    forbidden_passed = sum(result.forbidden_ok for result in results)
    lines = [
        "# Flexible Action Card Eval Report",
        "",
        f"- cases: `{total}`",
        f"- main field pass: `{main_passed}/{total}`",
        f"- forbidden output pass: `{forbidden_passed}/{total}`",
        f"- threshold: `main >= {MIN_MAIN_FIELD_PASS}/{total}` and `forbidden == {total}/{total}`",
        f"- cases file: `validation/fixtures/{CASES_PATH.name}`",
        "",
        "| case_id | split | difficulty | main | forbidden | failed fields |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for result in results:
        lines.append(
            "| {case_id} | {split} | {difficulty} | {main} | {forbidden} | {reasons} |".format(
                case_id=result.case_id,
                split=result.split,
                difficulty=result.difficulty,
                main="PASS" if result.main_ok else "FAIL",
                forbidden="PASS" if result.forbidden_ok else "FAIL",
                reasons=", ".join(result.reasons) if result.reasons else "ok",
            )
        )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """Run source checks plus dataset evaluation."""

    evidence = read("android-mvp/app/src/main/java/cn/shike/app/domain/ActionCardEvidence.kt")
    model = read("android-mvp/app/src/main/java/cn/shike/app/ui/ActionCardUiModel.kt")
    api = read("android-mvp/app/src/main/java/cn/shike/app/data/ModelApiClient.kt")
    rules = read("backend/shike_backend/action_card_rules.py")
    prompt = read("backend/shike_backend/prompts/analyze_system_prompt.txt")
    image_prompt = read("backend/shike_backend/prompts/analyze_image_system_prompt.txt")
    test = read("backend/tests/test_action_card_training_set.py")
    cases = load_cases()
    results = run_dataset_eval()
    write_report(results)

    main_passed = sum(result.main_ok for result in results)
    forbidden_passed = sum(result.forbidden_ok for result in results)
    total = len(results)
    checks = [
        ("training_cases_present", total == 60 and CASES_PATH.is_file()),
        ("training_guide_archived", (ROOT / "docs/SHIKE_ACTION_CARD_TRAINING_SET_GUIDE.md").is_file()),
        ("backend_rules_parser_present", "parsed_action_card_from_ocr_text" in rules and "B地点" in rules),
        ("backend_training_tests_present", all(token in test for token in ["course_002", "ocr_noise_004", "exam_001"])),
        ("dataset_main_fields_meet_threshold", main_passed >= MIN_MAIN_FIELD_PASS),
        ("dataset_forbidden_outputs_clean", forbidden_passed == total),
        ("dataset_report_written", REPORT_PATH.is_file() and "Flexible Action Card Eval Report" in REPORT_PATH.read_text(encoding="utf-8")),
        ("domain_preparation_parser_present", "fun preparationItemsFromText(text: String)" in evidence),
        ("action_card_has_preparation_items_field", "val preparationItems: List<String>" in model),
        ("api_accepts_future_preparation_fields", all(token in api for token in ["preparation_items", "checklist_items", "准备："])),
        ("prompts_preserve_extra_actions", all(token in prompt + image_prompt for token in ["记得带书", "提前准备周报", "不要塞进 title"])),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"FLEXIBLE_ACTION_DATASET_MAIN_FIELDS\t{main_passed}/{total}")
    print(f"FLEXIBLE_ACTION_DATASET_FORBIDDEN\t{forbidden_passed}/{total}")
    print(f"FLEXIBLE_ACTION_ITEM_EXTRACTION_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
