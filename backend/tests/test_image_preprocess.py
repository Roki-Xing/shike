"""Tests for backend OCR chrome filtering before multimodal prompting."""

from __future__ import annotations

import unittest

from shike_backend.image_preprocess import filter_ocr_blocks
from shike_backend.schemas_v2 import OcrBlock


class ImagePreprocessTest(unittest.TestCase):
    """Verify app/device chrome does not leak into semantic OCR hints."""

    def test_filter_ocr_blocks_removes_shike_ui_copy_anywhere_on_screen(self) -> None:
        blocks = [
            OcrBlock(text="快捷导入", x1=80, y1=420, x2=260, y2=470),
            OcrBlock(text="今日行动台空状态", x1=80, y1=520, x2=460, y2=570),
            OcrBlock(text="待确认", x1=80, y1=620, x2=220, y2=670),
            OcrBlock(text="收件箱状态", x1=80, y1=720, x2=300, y2=770),
            OcrBlock(text="今晚18:30 项目讨论 B203", x1=100, y1=900, x2=720, y2=960),
        ]

        filtered = filter_ocr_blocks(blocks, width=1080, height=2400)

        self.assertEqual(["今晚18:30 项目讨论 B203"], [block.text for block in filtered])


if __name__ == "__main__":
    unittest.main()
