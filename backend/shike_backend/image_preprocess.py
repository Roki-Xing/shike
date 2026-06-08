"""Image and OCR preprocessing for multimodal analysis."""

from __future__ import annotations

import re

from shike_backend.schemas_v2 import OcrBlock


def build_ignored_regions(width: int, height: int) -> dict[str, list[float]]:
    """Build regions that prompts and filters should ignore.

    Args:
        width: Image width.
        height: Image height.

    Returns:
        Region name to bounding box in image coordinates.
    """

    return {
        "top_status_bar": [0, 0, float(width), float(height) * 0.09],
        "bottom_navigation_bar": [0, float(height) * 0.91, float(width), float(height)],
    }


def looks_like_system_status_text(text: str) -> bool:
    """Return whether OCR text looks like phone status bar text.

    Args:
        text: OCR text block.

    Returns:
        True when the text should not become task time/location.
    """

    normalized = text.strip()
    return bool(re.fullmatch(r"\d{1,2}:\d{2}", normalized)) or normalized in {
        "100%",
        "4G",
        "5G",
        "WiFi",
        "WIFI",
        "1.20KB/s",
    }


def looks_like_navigation_text(text: str) -> bool:
    """Return whether OCR text is Shike/system navigation chrome."""

    return text.strip() in {"首页", "今日", "导入", "收件箱", "设置", "我的", "返回"}


def looks_like_shike_app_chrome_text(text: str) -> bool:
    """Return whether OCR text is Shike UI copy instead of user content.

    Args:
        text: OCR text block.

    Returns:
        True when the block is app chrome that should not guide model semantics.
    """

    normalized = text.strip()
    if not normalized:
        return False
    exact_matches = {
        "今日行动台空状态",
        "快捷导入",
        "待确认",
        "收件箱状态",
        "确认并安排",
        "修改字段",
        "删除原截图",
        "解析当前草稿",
        "填入课程样例",
        "模型编排",
    }
    phrase_matches = (
        "今日行动台空状态",
        "快捷导入",
        "待确认",
        "收件箱状态",
        "演示样例",
    )
    return normalized in exact_matches or any(phrase in normalized for phrase in phrase_matches)


def filter_ocr_blocks(blocks: list[OcrBlock], width: int, height: int) -> list[OcrBlock]:
    """Filter OCR blocks that are likely device/app chrome.

    Args:
        blocks: OCR blocks from vivo OCR or client-side OCR.
        width: Image width.
        height: Image height.

    Returns:
        Blocks safe to send as semantic hints.
    """

    filtered: list[OcrBlock] = []
    for block in blocks:
        center_y = (block.y1 + block.y2) / 2
        text = block.text.strip()
        if center_y < height * 0.09 and looks_like_system_status_text(text):
            continue
        if center_y > height * 0.91 and looks_like_navigation_text(text):
            continue
        if looks_like_shike_app_chrome_text(text):
            continue
        if text in {"09:49", "09:50", "09:51", "10:28", "100%", "1.20KB/s"}:
            continue
        filtered.append(block)
    return filtered
