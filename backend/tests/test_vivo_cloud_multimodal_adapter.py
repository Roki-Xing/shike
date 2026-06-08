import json
import unittest
from unittest.mock import ANY, patch

from shike_backend.adapters.vivo_cloud_multimodal_adapter import VivoCloudMultimodalAdapter
from shike_backend.schemas_v2 import AnalyzeImageRequest, analyze_image_response_schema


class _FakeResponse:
    def __init__(self, status_code: int, body: dict[str, object]) -> None:
        self.status_code = status_code
        self._body = body

    def json(self) -> dict[str, object]:
        return self._body


class VivoCloudMultimodalAdapterTest(unittest.TestCase):
    def test_analyze_image_falls_back_from_openai_provider_401_to_signed_vivogpt_vision_chat(self) -> None:
        card = {
            "title": "项目讨论",
            "scene_type": "meeting_notice",
            "confidence": 0.81,
            "time": {"text": "今晚18:30"},
            "location": {"text": "B203"},
            "task": {"summary": "参加项目讨论", "priority": "medium", "topic": "项目"},
            "suggested_actions": [
                {
                    "type": "calendar",
                    "label": "加入日历",
                    "requires_permission": False,
                    "disabled_reason": "用户确认前不可执行",
                }
            ],
            "missing_fields": [],
            "risks": [],
            "evidence": [
                {"field": "title", "text": "项目讨论", "source": "vision", "box": None}
            ],
            "ignored_regions": ["top_status_bar"],
            "explanation": "图片和 OCR hint 指向一个会议通知。",
        }
        calls: list[dict[str, object]] = []

        def fake_post(url: str, **kwargs: object) -> _FakeResponse:
            calls.append({"url": url, **kwargs})
            if len(calls) == 1:
                return _FakeResponse(
                    200,
                    {
                        "error": {
                            "code": "401",
                            "message": "The current OpenAI-compatible model route is unauthorized.",
                        }
                    },
                )
            return _FakeResponse(200, {"code": 0, "data": {"content": json.dumps(card, ensure_ascii=False)}})

        adapter = VivoCloudMultimodalAdapter(
            app_id="test-app-id",
            app_key="test-app-key",
            base_url="https://api-ai.vivo.com.cn",
            uri="/v1/chat/completions",
            model="vivo-BlueLM-V-2.0",
            timeout_seconds=3,
            max_retries=0,
            temperature=0.1,
        )
        request = AnalyzeImageRequest(
            input_id="vision-fallback-001",
            source_type="screenshot_share",
            image={
                "data_url": "data:image/png;base64,AA==",
                "mime": "image/png",
                "width": 1,
                "height": 1,
                "sha256": "fixture1",
            },
            ocr_text_hint="今晚18:30 项目讨论 B203",
            ocr_blocks=[],
            current_date="2026-06-08",
            user_timezone="Asia/Shanghai",
        )

        with patch("shike_backend.adapters.vivo_cloud_multimodal_adapter.requests.post", side_effect=fake_post):
            result = adapter.analyze_image(request, analyze_image_response_schema())

        self.assertEqual("项目讨论", result.title)
        self.assertEqual(2, len(calls))
        self.assertTrue(str(calls[1]["url"]).endswith("/vivogpt/completions"))
        self.assertEqual({"requestId": ANY}, calls[1]["params"])

        legacy_headers = calls[1]["headers"]
        self.assertIsInstance(legacy_headers, dict)
        self.assertNotIn("Authorization", legacy_headers)
        self.assertIn("X-AI-GATEWAY-SIGNATURE", legacy_headers)
        self.assertEqual("application/json", legacy_headers["Content-Type"])

        legacy_body = calls[1]["json"]
        self.assertIsInstance(legacy_body, dict)
        self.assertEqual("vivo-BlueLM-V-2.0", legacy_body["model"])
        self.assertEqual("vision-fallback-001", legacy_body["sessionId"])
        self.assertEqual("text", legacy_body["messages"][0]["contentType"])
        self.assertEqual("image", legacy_body["messages"][1]["contentType"])
        self.assertEqual("data:image/png;base64,AA==", legacy_body["messages"][1]["content"])


if __name__ == "__main__":
    unittest.main()
