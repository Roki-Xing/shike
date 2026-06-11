"""Tests for backend preparation-item enrichment."""

from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

import shike_backend.main as main_module
import shike_backend.settings as settings_module
from shike_backend.adapters.base import AdapterError
from shike_backend.main import app
from shike_backend.preparation import preparation_items_from_text


def reset_backend_singletons() -> None:
    """Clear cached backend settings and adapters."""

    settings_module._CACHED = None  # type: ignore[attr-defined]
    main_module._ADAPTER = None
    main_module._OCR_ADAPTER = None
    main_module._MULTIMODAL_ADAPTER = None


class FailingImageAdapter:
    """Force `/v2/analyze-image` into OCR text fallback."""

    def is_configured(self) -> bool:
        """Return configured state for audit metadata."""

        return True

    def analyze_image(self, request: object, schema_json: dict[str, object]) -> object:
        """Raise a fallback-compatible image adapter error."""

        raise AdapterError("provider_model_does_not_support_image")


class PreparationItemsTest(unittest.TestCase):
    """Preparation fields must survive backend model and fallback paths."""

    def tearDown(self) -> None:
        reset_backend_singletons()

    def test_preparation_parser_extracts_exam_admission_ticket(self) -> None:
        text = "今天晚上七点需要上高数A 教室是B336 要考试记得带准考证"

        self.assertEqual(["带准考证"], preparation_items_from_text(text))

    def test_v1_analyze_returns_preparation_items_for_exam_text(self) -> None:
        env = {
            "SHIKE_BACKEND_ENV_FILE": "/dev/null",
            "SHIKE_RUNTIME_MODE": "release_user",
            "SHIKE_MODEL_PROVIDER": "mock",
            "SHIKE_ALLOW_MOCK_FALLBACK": "true",
        }
        with patch.dict(os.environ, env, clear=True):
            reset_backend_singletons()
            response = TestClient(app).post(
                "/v1/analyze",
                json={
                    "input_id": "prep-exam-ticket-v1",
                    "source_type": "manual",
                    "ocr_text": "今天晚上七点需要上高数A 教室是B336 要考试记得带准考证",
                    "scene_hint": "course_notice",
                    "user_timezone": "Asia/Shanghai",
                },
            )

        self.assertEqual(200, response.status_code)
        payload = response.json()
        self.assertEqual(["带准考证"], payload["preparation_items"])
        self.assertEqual("带准考证", payload["checklist_items"][0]["text"])
        self.assertIn("高数", payload["title"])
        self.assertEqual("B336", payload["location"]["raw"])

    def test_v2_text_fallback_returns_preparation_items_for_exam_text(self) -> None:
        env = {
            "SHIKE_BACKEND_ENV_FILE": "/dev/null",
            "SHIKE_RUNTIME_MODE": "release_user",
            "SHIKE_MODEL_PROVIDER": "mock",
            "SHIKE_ALLOW_MOCK_FALLBACK": "true",
        }
        with patch.dict(os.environ, env, clear=True):
            reset_backend_singletons()
            main_module._MULTIMODAL_ADAPTER = FailingImageAdapter()
            response = TestClient(app).post(
                "/v2/analyze-image",
                json={
                    "input_id": "prep-exam-ticket-v2",
                    "source_type": "recent_screenshot_assist",
                    "image": None,
                    "ocr_text_hint": "今天晚上七点需要上高数A 教室是B336 要考试记得带准考证",
                    "ocr_blocks": [],
                    "current_date": "2026-06-11",
                    "user_timezone": "Asia/Shanghai",
                    "locale": "zh-CN",
                    "scene_hint": "course_notice",
                    "allow_cloud_image": True,
                },
            )

        self.assertEqual(200, response.status_code)
        payload = response.json()
        self.assertEqual(["带准考证"], payload["preparation_items"])
        self.assertEqual("带准考证", payload["checklist_items"][0]["text"])
        self.assertTrue(all(action["disabled_reason"] == "用户确认前不可执行" for action in payload["suggested_actions"]))


if __name__ == "__main__":
    unittest.main()
