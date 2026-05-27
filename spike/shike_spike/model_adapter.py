"""Mock model adapter for the Shike technical spike."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ModelInput:
    """Input for local model analysis.

    Args:
        input_id: Stable sample identifier.
        source_type: Source such as screenshot or camera.
        ocr_text: OCR text extracted from the image.
        scene_hint: Optional expected scene.

    Returns:
        The dataclass represents normalized input for adapters.
    """

    input_id: str
    source_type: str
    ocr_text: str
    scene_hint: str | None = None


class MockModelAdapter:
    """Rule-backed adapter that simulates model output for the MVP scenes."""

    def analyze(self, model_input: ModelInput) -> dict[str, Any]:
        """Analyze one OCR text sample.

        Args:
            model_input: Input sample with OCR text and optional hint.

        Returns:
            A dict shaped like `ShikeModelOutput`.
        """

        text = model_input.ocr_text
        if self._is_course(text, model_input.scene_hint):
            return self._course_output(text)
        if self._is_event(text, model_input.scene_hint):
            return self._event_output(text)
        return {
            "scene_type": "unknown",
            "confidence": 0.41,
            "title": "未确认碎片",
            "time": None,
            "location": None,
            "task": {"summary": "需要人工确认", "priority": "low", "topic": "unknown"},
            "suggested_actions": [{"type": "reminder", "label": "稍后确认", "requires_permission": True}],
            "missing_fields": ["scene_type", "time", "location"],
            "explanation": "当前内容缺少稳定时间地点任务结构，先进入待确认。"
        }

    @staticmethod
    def _is_course(text: str, hint: str | None) -> bool:
        return hint == "course_notice" or "课" in text or "作业" in text or "教室" in text

    @staticmethod
    def _is_event(text: str, hint: str | None) -> bool:
        return hint == "event_poster" or "活动" in text or "分享会" in text or "主办" in text

    @staticmethod
    def _course_output(text: str) -> dict[str, Any]:
        deadline = "今晚22:00" if "22:00" in text else None
        return {
            "scene_type": "course_notice",
            "confidence": 0.94,
            "title": "高数A班教室变更",
            "time": {
                "start_text": "今晚18:30",
                "deadline_text": deadline,
                "normalized_start": "2026-04-24T18:30:00+08:00",
                "normalized_deadline": "2026-04-24T22:00:00+08:00" if deadline else None,
            },
            "location": {"raw": "B203", "map_query": "B203", "confidence": 0.82},
            "task": {
                "summary": "查看新教室路线并提交第5章作业",
                "priority": "high",
                "topic": "course",
            },
            "suggested_actions": [
                {"type": "calendar", "label": "加入日历", "requires_permission": True},
                {"type": "reminder", "label": "课前30分钟提醒", "requires_permission": True},
                {"type": "map", "label": "打开教室路线", "requires_permission": False},
            ],
            "missing_fields": [],
            "explanation": "文本包含课程、时间、地点和截止事项，适合转成行动卡。",
        }

    @staticmethod
    def _event_output(text: str) -> dict[str, Any]:
        has_registration = any(token in text for token in ["http://", "https://", "报名链接", "二维码"])
        return {
            "scene_type": "event_poster",
            "confidence": 0.91,
            "title": "AI应用分享会",
            "time": {
                "start_text": "4月24日19:30",
                "deadline_text": "今晚22:00" if "22:00" in text else None,
                "normalized_start": "2026-04-24T19:30:00+08:00",
                "normalized_deadline": "2026-04-24T22:00:00+08:00" if "22:00" in text else None,
            },
            "location": {"raw": "图书馆报告厅", "map_query": "图书馆报告厅", "confidence": 0.88},
            "task": {"summary": "报名并前往AI应用分享会", "priority": "high", "topic": "event"},
            "suggested_actions": [
                {"type": "calendar", "label": "加入活动日历", "requires_permission": True},
                {"type": "reminder", "label": "报名截止前提醒", "requires_permission": True},
                {"type": "map", "label": "打开活动地点", "requires_permission": False},
            ],
            "missing_fields": [] if has_registration else ["registration_url"],
            "explanation": "海报包含活动主题、时间、地点和报名截止，适合生成活动行动卡。",
        }
