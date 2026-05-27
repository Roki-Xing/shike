"""Rule-backed mock adapter used for offline demo and fallback."""

from __future__ import annotations

from shike_backend.schemas import AnalyzeRequest, AnalyzeResponse


class MockModelAdapter:
    """A deterministic adapter that simulates model output for MVP scenes."""

    def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        text = request.ocr_text
        if self._is_course(text, request.scene_hint):
            return self._course_output(text)
        if self._is_event(text, request.scene_hint):
            return self._event_output(text)
        return AnalyzeResponse(
            scene_type="unknown",
            confidence=0.41,
            title="未确认碎片",
            time=None,
            location=None,
            task={"summary": "需要人工确认", "priority": "low", "topic": "unknown"},
            suggested_actions=[{"type": "reminder", "label": "稍后确认", "requires_permission": True}],
            missing_fields=["scene_type", "time", "location"],
            explanation="当前内容缺少稳定时间地点任务结构，先进入待确认。",
        )

    @staticmethod
    def _is_course(text: str, hint: str | None) -> bool:
        return hint == "course_notice" or any(token in text for token in ["课", "作业", "教室"])

    @staticmethod
    def _is_event(text: str, hint: str | None) -> bool:
        return hint == "event_poster" or any(token in text for token in ["活动", "分享会", "主办"])

    @staticmethod
    def _course_output(text: str) -> AnalyzeResponse:
        deadline = "今晚22:00" if "22:00" in text else "今晚22:00"
        return AnalyzeResponse(
            scene_type="course_notice",
            confidence=0.94,
            title="高数A班教室变更",
            time={
                "start_text": "今晚18:30",
                "deadline_text": deadline,
                "normalized_start": "2026-04-24T18:30:00+08:00",
                "normalized_deadline": "2026-04-24T22:00:00+08:00",
            },
            location={"raw": "B203", "map_query": "B203", "confidence": 0.82},
            task={"summary": "查看新教室路线并提交第5章作业", "priority": "high", "topic": "course"},
            suggested_actions=[
                {"type": "calendar", "label": "加入日历", "requires_permission": True},
                {"type": "reminder", "label": "课前30分钟提醒", "requires_permission": True},
                {"type": "map", "label": "打开教室路线", "requires_permission": False},
            ],
            missing_fields=[],
            explanation="文本包含课程、时间、地点和截止事项，适合转成行动卡。",
        )

    @staticmethod
    def _event_output(text: str) -> AnalyzeResponse:
        return AnalyzeResponse(
            scene_type="event_poster",
            confidence=0.91,
            title="AI应用分享会",
            time={
                "start_text": "4月24日19:30",
                "deadline_text": "今晚22:00",
                "normalized_start": "2026-04-24T19:30:00+08:00",
                "normalized_deadline": "2026-04-24T22:00:00+08:00",
            },
            location={"raw": "图书馆报告厅", "map_query": "图书馆报告厅", "confidence": 0.88},
            task={"summary": "报名并前往AI应用分享会", "priority": "high", "topic": "event"},
            suggested_actions=[
                {"type": "calendar", "label": "加入活动日历", "requires_permission": True},
                {"type": "reminder", "label": "报名截止前提醒", "requires_permission": True},
                {"type": "map", "label": "打开活动地点", "requires_permission": False},
            ],
            missing_fields=["registration_url"],
            explanation="海报包含活动主题、时间、地点和报名截止，适合生成活动行动卡。",
        )

