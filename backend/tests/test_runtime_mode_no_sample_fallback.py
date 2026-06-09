"""Tests for runtime-mode gating of mock sample fallback."""

from __future__ import annotations

import json
import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

import shike_backend.main as main_module
import shike_backend.settings as settings_module
from shike_backend.main import app


FORBIDDEN_SAMPLE_TOKENS = ("18:30", "22:00", "第5章", "教室变更")


def reset_backend_singletons() -> None:
    """Clear cached settings and route adapters between env-driven tests."""

    settings_module._CACHED = None  # type: ignore[attr-defined]
    main_module._ADAPTER = None
    main_module._OCR_ADAPTER = None
    main_module._MULTIMODAL_ADAPTER = None


class RuntimeModeNoSampleFallbackTest(unittest.TestCase):
    """Cloud-device and release modes must not inject fixed demo course fields."""

    def tearDown(self) -> None:
        reset_backend_singletons()

    def test_deepseek_failure_in_cloud_mode_uses_evidence_only_fallback(self) -> None:
        env = {
            "SHIKE_BACKEND_ENV_FILE": "/dev/null",
            "SHIKE_RUNTIME_MODE": "cloud_device_test",
            "SHIKE_MODEL_PROVIDER": "deepseek",
            "SHIKE_ALLOW_MOCK_FALLBACK": "true",
        }
        with patch.dict(os.environ, env, clear=True):
            reset_backend_singletons()
            response = TestClient(app).post(
                "/v1/analyze",
                json={
                    "input_id": "cloud-fallback-course-nine-001",
                    "source_type": "screenshot",
                    "ocr_text": "今晚九点上高数，教室是B203",
                    "scene_hint": "course_notice",
                    "user_timezone": "Asia/Shanghai",
                },
            )

        self.assertEqual(200, response.status_code)
        payload = response.json()
        serialized = json.dumps(payload, ensure_ascii=False)
        self.assertIn("高数", payload["title"])
        self.assertIn("今晚九点", payload["time"]["start_text"])
        self.assertEqual("B203", payload["location"]["raw"])
        for token in FORBIDDEN_SAMPLE_TOKENS:
            self.assertNotIn(token, serialized)

    def test_mock_provider_in_release_mode_is_evidence_only(self) -> None:
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
                    "input_id": "release-mock-course-nine-001",
                    "source_type": "manual",
                    "ocr_text": "今晚九点上高数，教室是B203",
                    "scene_hint": "course_notice",
                    "user_timezone": "Asia/Shanghai",
                },
            )

        self.assertEqual(200, response.status_code)
        payload = response.json()
        serialized = json.dumps(payload, ensure_ascii=False)
        self.assertIn("高数", payload["title"])
        self.assertIn("今晚九点", payload["time"]["start_text"])
        self.assertEqual("B203", payload["location"]["raw"])
        for token in FORBIDDEN_SAMPLE_TOKENS:
            self.assertNotIn(token, serialized)


if __name__ == "__main__":
    unittest.main()
