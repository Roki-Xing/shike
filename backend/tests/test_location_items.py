"""Tests for backend location enrichment."""

from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

import shike_backend.main as main_module
import shike_backend.settings as settings_module
from shike_backend.adapters.base import AdapterError
from shike_backend.location import enrich_location_payload, extract_location_from_text
from shike_backend.main import app
from shike_backend.schemas_v2 import AnalyzeImageRequest, ParsedActionCard


def reset_backend_singletons() -> None:
    """Clear cached backend settings and adapters."""

    settings_module._CACHED = None  # type: ignore[attr-defined]
    main_module._ADAPTER = None
    main_module._OCR_ADAPTER = None
    main_module._MULTIMODAL_ADAPTER = None


class LocationBlindImageAdapter:
    """Return a schema-valid image card that misses OCR location evidence."""

    def is_configured(self) -> bool:
        """Return configured state for audit metadata."""

        return True

    def analyze_image(self, request: AnalyzeImageRequest, schema_json: dict[str, object]) -> ParsedActionCard:
        """Return a card without location although OCR hint contains it."""

        return ParsedActionCard(
            title="高数A考试",
            scene_type="course_notice",
            confidence=0.86,
            time={
                "start_text": "今天晚上七点",
                "deadline_text": None,
                "normalized_start": "2026-06-11T19:00:00+08:00",
                "normalized_deadline": None,
            },
            location=None,
            task={"summary": "参加高数A考试，记得带准考证", "priority": "high", "topic": "course"},
            suggested_actions=[
                {"type": "calendar", "label": "添加到日历", "requires_permission": True},
                {"type": "reminder", "label": "设置提醒", "requires_permission": True},
            ],
            missing_fields=["location"],
            preparation_items=[],
            checklist_items=[],
            risks=[],
            evidence=[],
            ignored_regions=[],
            explanation="图片模型漏掉了地点字段。",
        )


class LocationItemsTest(unittest.TestCase):
    """Location evidence must survive backend image and text paths."""

    def tearDown(self) -> None:
        reset_backend_singletons()

    def test_location_parser_extracts_plain_room_number(self) -> None:
        self.assertEqual("303", extract_location_from_text("今天晚上七点上高数A 地点303"))
        self.assertEqual("303", extract_location_from_text("今天晚上七点上高数A 地点是303"))
        self.assertEqual("303", extract_location_from_text("今天晚上七点上高数A 教室是303"))
        self.assertEqual("B地点303", extract_location_from_text("晚上九点上 高数 B地点在303"))

    def test_location_enrichment_prefers_more_specific_ocr_evidence(self) -> None:
        payload = {
            "title": "高数B",
            "scene_type": "course_notice",
            "location": {"raw": "303", "map_query": "303", "confidence": 0.76},
            "task": {"summary": "晚上九点上高数，地点303", "priority": "medium", "topic": "course"},
            "suggested_actions": [
                {"type": "map", "label": "查看地图", "requires_permission": True},
            ],
            "missing_fields": ["deadline_text", "normalized_deadline"],
            "explanation": "模型只返回了普通房间号。",
        }

        enriched = enrich_location_payload(payload, ["晚上九点上 高数 B地点在303"])

        self.assertEqual("B地点303", enriched["location"]["raw"])
        self.assertEqual("B地点303", enriched["location"]["map_query"])
        self.assertNotIn("location", enriched["missing_fields"])

    def test_v1_analyze_keeps_plain_room_number_location(self) -> None:
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
                    "input_id": "location-303-v1",
                    "source_type": "manual",
                    "ocr_text": "今天晚上七点需要上高数A 地点303 要考试记得带准考证",
                    "scene_hint": "course_notice",
                    "user_timezone": "Asia/Shanghai",
                },
            )

        self.assertEqual(200, response.status_code)
        payload = response.json()
        self.assertEqual("303", payload["location"]["raw"])
        self.assertEqual("303", payload["location"]["map_query"])
        self.assertTrue(any(action["type"] == "map" for action in payload["suggested_actions"]))
        self.assertNotIn("location", payload["missing_fields"])

    def test_v2_image_result_repairs_location_from_ocr_hint(self) -> None:
        env = {
            "SHIKE_BACKEND_ENV_FILE": "/dev/null",
            "SHIKE_RUNTIME_MODE": "release_user",
            "SHIKE_MODEL_PROVIDER": "mock",
            "SHIKE_ALLOW_MOCK_FALLBACK": "true",
        }
        with patch.dict(os.environ, env, clear=True):
            reset_backend_singletons()
            main_module._MULTIMODAL_ADAPTER = LocationBlindImageAdapter()
            response = TestClient(app).post(
                "/v2/analyze-image",
                json={
                    "input_id": "location-303-v2",
                    "source_type": "recent_screenshot_assist",
                    "image": None,
                    "ocr_text_hint": "今天晚上七点需要上高数A 地点303 要考试记得带准考证",
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
        self.assertEqual("303", payload["location"]["raw"])
        self.assertEqual("303", payload["location"]["map_query"])
        self.assertTrue(any(action["type"] == "map" for action in payload["suggested_actions"]))
        self.assertNotIn("location", payload["missing_fields"])
        self.assertTrue(all(action["disabled_reason"] == "用户确认前不可执行" for action in payload["suggested_actions"]))


if __name__ == "__main__":
    unittest.main()
