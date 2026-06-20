"""Regression tests for OCR-to-action-card training cases."""

from __future__ import annotations

import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

import shike_backend.main as main_module
import shike_backend.settings as settings_module
from shike_backend.main import app


ROOT = Path(__file__).resolve().parents[2]
CASES_PATH = ROOT / "validation/fixtures/shike_action_card_training_cases_v1.jsonl"


def reset_backend_singletons() -> None:
    """Clear cached backend settings and adapters."""

    settings_module._CACHED = None  # type: ignore[attr-defined]
    main_module._ADAPTER = None
    main_module._OCR_ADAPTER = None
    main_module._MULTIMODAL_ADAPTER = None


def training_case(case_id: str) -> dict[str, object]:
    """Return one JSONL training case by id.

    Args:
        case_id: Case identifier from the training set.

    Returns:
        Case dictionary.
    """

    for line in CASES_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        if record["case_id"] == case_id:
            return record
    raise AssertionError(f"missing training case: {case_id}")


def expected_first_card(case: dict[str, object]) -> dict[str, object]:
    """Return the first expected action card from a training case."""

    cards = case["expected_cards"]
    assert isinstance(cards, list) and cards
    card = cards[0]
    assert isinstance(card, dict)
    return card


class ActionCardTrainingSetTest(unittest.TestCase):
    """The v2 OCR fallback must preserve user-visible action-card fields."""

    def tearDown(self) -> None:
        reset_backend_singletons()

    def analyze_case(self, case_id: str) -> dict[str, object]:
        """Run one training case through `/v2/analyze-image` text fallback."""

        case = training_case(case_id)
        expected = expected_first_card(case)
        env = {
            "SHIKE_BACKEND_ENV_FILE": "/dev/null",
            "SHIKE_RUNTIME_MODE": "release_user",
            "SHIKE_MODEL_PROVIDER": "mock",
            "SHIKE_ALLOW_MOCK_FALLBACK": "true",
        }
        with patch.dict(os.environ, env, clear=True):
            reset_backend_singletons()
            response = TestClient(app).post(
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

        self.assertEqual(200, response.status_code)
        payload = response.json()
        self.assertTrue(all(action["disabled_reason"] == "用户确认前不可执行" for action in payload["suggested_actions"]))
        self.assertTrue(all(token not in json.dumps(payload, ensure_ascii=False) for token in case.get("do_not_output", [])))
        return payload

    def test_course_plain_303_location_survives_action_card(self) -> None:
        payload = self.analyze_case("course_002")

        self.assertEqual("course_notice", payload["scene_type"])
        self.assertIn("高数", payload["title"])
        self.assertEqual("B地点303", payload["location"]["raw"])
        self.assertIn("晚上九点", json.dumps(payload["time"], ensure_ascii=False))

    def test_exam_ticket_and_classroom_survive_action_card(self) -> None:
        payload = self.analyze_case("exam_001")

        self.assertEqual("exam_notice", payload["scene_type"])
        self.assertEqual("教3-205", payload["location"]["raw"])
        self.assertIn("带学生证", payload["preparation_items"])
        self.assertIn("带2B铅笔", payload["preparation_items"])

    def test_noise_case_ignores_metadata_and_keeps_location(self) -> None:
        payload = self.analyze_case("ocr_noise_004")

        serialized = json.dumps(payload, ensure_ascii=False)
        self.assertEqual("course_notice", payload["scene_type"])
        self.assertEqual("B地点303", payload["location"]["raw"])
        self.assertNotIn("14字", serialized)
        self.assertNotIn("未分类", serialized)

    def test_cancelled_course_becomes_assignment_without_map(self) -> None:
        payload = self.analyze_case("course_008")

        actions = {action["type"] for action in payload["suggested_actions"]}
        self.assertEqual("assignment_deadline", payload["scene_type"])
        self.assertIsNone(payload["location"])
        self.assertNotIn("map", actions)
        self.assertNotIn("calendar", actions)

    def test_preparation_items_are_structured_not_title_noise(self) -> None:
        payload = self.analyze_case("course_006")

        self.assertEqual("实验楼A407", payload["location"]["raw"])
        self.assertIn("提前把代码跑通", payload["preparation_items"])
        self.assertNotIn("提前把代码跑通", payload["title"])

    def test_rescheduled_meeting_uses_new_time_not_cancelled_time(self) -> None:
        payload = self.analyze_case("meeting_004")

        self.assertEqual("meeting_notice", payload["scene_type"])
        self.assertEqual("周五14:00", payload["time"]["start_text"])
        self.assertIn("准备风险清单", payload["preparation_items"])

    def test_leisure_fragment_keeps_evidence_but_marks_task_missing(self) -> None:
        payload = self.analyze_case("negative_004")

        self.assertEqual("unknown", payload["scene_type"])
        self.assertEqual("今天下午", payload["time"]["start_text"])
        self.assertEqual("操场", payload["location"]["raw"])
        self.assertIn("task", payload["missing_fields"])


if __name__ == "__main__":
    unittest.main()
