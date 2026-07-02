"""Tests for vivo OCR adapter text/audit separation."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from shike_backend.adapters.vivo_ocr_adapter import VivoOcrAdapter
from shike_backend.schemas import OcrRequest


class FakeVivoOcrResponse:
    """Small fake response compatible with `requests.post` usage."""

    status_code = 200

    def json(self) -> dict[str, object]:
        """Return a vivo-like OCR payload with multiline text."""

        long_line = "记得带书" + "很重要" * 120
        return {
            "error_code": 0,
            "result": {
                "OCR": [
                    {
                        "words": "明天晚上七点半上英语课",
                        "x": 10,
                        "y": 110,
                        "width": 500,
                        "height": 40,
                        "confidence": 0.93,
                    },
                    {
                        "words": "地点是E306",
                        "x": 10,
                        "y": 170,
                        "width": 260,
                        "height": 40,
                        "confidence": 0.91,
                    },
                    {
                        "words": long_line,
                        "x": 10,
                        "y": 230,
                        "width": 900,
                        "height": 40,
                        "confidence": 0.89,
                    },
                ]
            },
        }


class VivoOcrAdapterTest(unittest.TestCase):
    """The model path must receive raw OCR, while logs use summaries."""

    def test_recognize_detail_keeps_full_multiline_text_for_model_input(self) -> None:
        adapter = VivoOcrAdapter(
            app_id="app-id",
            app_key="app-key",
            base_url="https://example.test",
            uri="/ocr/general_recognition",
            timeout_seconds=3,
            max_retries=0,
        )
        request = OcrRequest(
            input_id="ocr-raw-text-001",
            source_type="screenshot",
            image_base64="aW1hZ2UtYmFzZTY0LXBheWxvYWQ=",
            pos=2,
        )

        with patch("shike_backend.adapters.vivo_ocr_adapter.requests.post", return_value=FakeVivoOcrResponse()):
            detail = adapter.recognize_detail(request)

        self.assertIn("\n地点是E306\n", detail.response.text)
        self.assertIn("很重要" * 40, detail.response.text)
        self.assertGreater(len(detail.response.text), 300)
        self.assertFalse(detail.response.text.endswith("..."))
        self.assertAlmostEqual(0.91, detail.response.confidence, places=2)
        self.assertEqual("明天晚上七点半上英语课", detail.blocks[0].text)
        self.assertIn("很重要" * 40, detail.blocks[2].text)


if __name__ == "__main__":
    unittest.main()
