"""Tests for DeepSeek OCR-text structuring adapter."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from shike_backend.adapters.deepseek_adapter import DeepSeekModelAdapter, build_deepseek_payload
from shike_backend.schemas import AnalyzeRequest


class FakeDeepSeekResponse:
    """Small fake response compatible with `requests.post` usage."""

    status_code = 200

    def json(self) -> dict[str, object]:
        """Return a DeepSeek chat-completions response shape."""

        return {
            "choices": [
                {
                    "message": {
                        "content": (
                            '{"scene_type":"course_notice","confidence":0.9,"title":"高数课",'
                            '"time":{"start_text":"今晚九点","deadline_text":null,'
                            '"normalized_start":"2026-06-08T21:00:00+08:00",'
                            '"normalized_deadline":null},'
                            '"location":{"raw":"B203","map_query":"B203","confidence":0.9},'
                            '"task":{"summary":"今晚九点上高数课，教室是B203",'
                            '"priority":"medium","topic":"course"},'
                            '"suggested_actions":['
                            '{"type":"calendar","label":"加入日历","requires_permission":true},'
                            '{"type":"reminder","label":"设置提醒","requires_permission":true},'
                            '{"type":"map","label":"查看地点","requires_permission":false}],'
                            '"missing_fields":[],"explanation":"OCR文本已包含课程、时间和地点。"}'
                        )
                    }
                }
            ]
        }


class DeepSeekAdapterTest(unittest.TestCase):
    """Verify DeepSeek request and response handling."""

    def test_build_deepseek_payload_uses_json_output_and_text_messages(self) -> None:
        payload = build_deepseek_payload(
            model="deepseek-v4-flash",
            system_prompt="system",
            user_prompt="user",
            temperature=0.1,
            thinking_enabled=False,
            response_format_enabled=True,
        )

        self.assertEqual("deepseek-v4-flash", payload["model"])
        self.assertEqual({"type": "json_object"}, payload["response_format"])
        self.assertEqual({"type": "disabled"}, payload["thinking"])
        self.assertEqual("system", payload["messages"][0]["content"])
        self.assertEqual("user", payload["messages"][1]["content"])

    def test_analyze_maps_ocr_text_to_shike_schema(self) -> None:
        adapter = DeepSeekModelAdapter(
            api_key="test-api-key",
            base_url="https://api.deepseek.com",
            uri="/chat/completions",
            model="deepseek-v4-flash",
            timeout_seconds=20,
            max_retries=0,
            temperature=0.1,
            thinking_enabled=False,
            response_format_enabled=True,
        )

        with patch("shike_backend.adapters.deepseek_adapter.requests.post", return_value=FakeDeepSeekResponse()) as post:
            response = adapter.analyze(
                AnalyzeRequest(
                    input_id="deepseek-course-001",
                    source_type="manual",
                    ocr_text="今晚九点上高数，教室是B203",
                    locale="zh-CN",
                    scene_hint="course_notice",
                    user_timezone="Asia/Shanghai",
                )
            )

        self.assertEqual("高数课", response.title)
        self.assertEqual("course_notice", response.scene_type)
        self.assertEqual("2026-06-08T21:00:00+08:00", response.time.normalized_start)
        self.assertEqual("B203", response.location.raw)
        request_payload = post.call_args.kwargs["json"]
        self.assertIn("今晚九点上高数，教室是B203", request_payload["messages"][1]["content"])
        self.assertNotIn("image_url", str(request_payload))


if __name__ == "__main__":
    unittest.main()
