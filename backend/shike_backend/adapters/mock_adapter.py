"""Rule-backed mock adapter used for offline demo and fallback."""

from __future__ import annotations

from collections.abc import Iterable
import re

from shike_backend.schemas import AnalyzeRequest, AnalyzeResponse


COURSE_TOPIC_TOKENS = ("高数", "课程", "上课", "课")
SPECIFIC_TIME_TOKENS = ("18:30", "22:00", "10:00", "8:30", "12:30", "14:00", "16:30", "18:00")
LOCATION_TOKENS = ("B203", "教室", "报告厅", "会议室", "教学楼", "综合楼", "研讨室", "信远楼")
SPECIFIC_TIME_PATTERN = re.compile(
    r"(今天晚上|晚上|今晚|明天晚上|明晚|明早|明天|本周[一二三四五六日天]|周[一二三四五六日天])\s*"
    r"[一二三四五六七八九十0-9]{1,3}点(?:半|[0-9]{1,2}分)?"
)
LOCATION_EVIDENCE_PATTERN = re.compile(
    r"(?:教室是|教室|地点|改到|调整到|在)\s*[A-Za-z一-龥]*[A-Z]?\d{2,4}[A-Za-z一-龥]*|[A-Z]\d{2,4}"
)
DEMO_COURSE_TITLE = "高数A班教室变更"
DEMO_COURSE_TASK = "查看新教室路线并提交第5章作业"
DEMO_COURSE_LOCATION = "B203"
DEMO_COURSE_START = "今晚18:30"
DEMO_COURSE_DEADLINE = "今晚22:00"


def is_sparse_course_text(text: str, hint: str | None = None) -> bool:
    """Detect course text that lacks exact time and location.

    Args:
        text: OCR or manually entered text.
        hint: Optional scene hint from the client.

    Returns:
        True when the backend must keep the card in user-confirmation mode.
    """

    has_course_topic = hint == "course_notice" or any(token in text for token in COURSE_TOPIC_TOKENS)
    has_specific_time = any(token in text for token in SPECIFIC_TIME_TOKENS) or SPECIFIC_TIME_PATTERN.search(text) is not None
    has_location = any(token in text for token in LOCATION_TOKENS) or LOCATION_EVIDENCE_PATTERN.search(text) is not None
    return has_course_topic and not has_specific_time and not has_location


def sparse_course_output(text: str) -> AnalyzeResponse:
    """Build a safe confirmation-first course response for incomplete text."""

    title = "上高数 A" if "高数" in text else "课程事项待确认"
    start_text = "今天晚上" if "今天晚上" in text else None
    return AnalyzeResponse(
        scene_type="course_notice",
        confidence=0.72,
        title=title,
        time={
            "start_text": start_text,
            "deadline_text": None,
            "normalized_start": None,
            "normalized_deadline": None,
        },
        location=None,
        task={"summary": text, "priority": "medium", "topic": "course"},
        suggested_actions=[{"type": "reminder", "label": "先存入待确认", "requires_permission": True}],
        missing_fields=["exact_start_time", "location"],
        explanation="文本包含课程关键词和相对时间，但缺少具体上课时间和地点，因此需要用户确认后再安排。",
    )


class MockModelAdapter:
    """A deterministic adapter that simulates model output for MVP scenes."""

    def __init__(self, *, allow_demo_samples: bool = False) -> None:
        self.allow_demo_samples = allow_demo_samples

    def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        text = request.ocr_text
        if self._is_low_quality(text):
            return self._manual_review_output("低质量碎片", "OCR 内容疑似模糊或截断，先保留为待确认任务。")
        if self._is_negative(text, request.scene_hint):
            return self._negative_output()
        if self._is_assignment(text, request.scene_hint):
            return self._assignment_output(text)
        if self._is_interview(text, request.scene_hint):
            return self._interview_output(text)
        if self._is_travel(text, request.scene_hint):
            return self._travel_output(text)
        if self._is_meeting(text, request.scene_hint):
            return self._meeting_output(text)
        if self._is_course(text, request.scene_hint):
            return self._course_output(text)
        if self._is_event(text, request.scene_hint):
            return self._event_output(text)
        return self._manual_review_output("未确认碎片", "当前内容缺少稳定时间地点任务结构，先进入待确认。")

    @staticmethod
    def _contains_any(text: str, tokens: Iterable[str]) -> bool:
        return any(token in text for token in tokens)

    @classmethod
    def _is_low_quality(cls, text: str) -> bool:
        return cls._contains_any(text, ["图像模糊", "低质量", "模糊", "反光", "截断", "遮挡", "压缩"])

    @classmethod
    def _is_negative(cls, text: str, hint: str | None) -> bool:
        return hint == "negative_fragment" or cls._contains_any(
            text,
            ["无行动闲聊", "广告片段", "表情包文字", "无效截图", "纯说明文本", "营销海报角标", "非日程文本"],
        )

    @staticmethod
    def _is_course(text: str, hint: str | None) -> bool:
        return hint == "course_notice" or any(token in text for token in ["课", "教室", "调课", "签到"])

    @staticmethod
    def _is_sparse_course_text(text: str) -> bool:
        return is_sparse_course_text(text)

    @staticmethod
    def _is_event(text: str, hint: str | None) -> bool:
        return hint == "event_poster" or any(token in text for token in ["活动", "分享会", "主办"])

    @staticmethod
    def _is_assignment(text: str, hint: str | None) -> bool:
        if hint is not None:
            return hint == "assignment_deadline"
        return any(token in text for token in ["作业", "报告", "PPT", "论文", "提交", "截止", "逾期"])

    @staticmethod
    def _is_meeting(text: str, hint: str | None) -> bool:
        return hint == "meeting_notice" or any(
            token in text for token in ["会议", "周会", "例会", "组会", "沟通会", "答辩预演", "腾讯会议", "线上会议室"]
        )

    @staticmethod
    def _is_interview(text: str, hint: str | None) -> bool:
        return hint == "interview_notice" or any(token in text for token in ["面试", "笔试", "候选", "HR", "简历"])

    @staticmethod
    def _is_travel(text: str, hint: str | None) -> bool:
        return hint == "travel_ticket" or any(
            token in text for token in ["高铁", "车票", "航班", "机场", "车站", "校车", "地铁站", "报到", "检票", "集合", "证件"]
        )

    @classmethod
    def _missing_fields_for_text(cls, text: str) -> list[str]:
        if cls._is_low_quality(text) or "本周六" in text:
            return ["time", "location"]
        if "待确认" in text:
            return ["location"]
        if "报名截止" in text and not any(token in text for token in ["报名链接", "二维码", "http"]):
            return ["registration_url"]
        if "导师沟通会" in text or "实习通勤" in text:
            return ["time", "location"]
        return []

    @staticmethod
    def _time_for_text(text: str, *, default_start: str, default_deadline: str | None = None) -> dict[str, str | None]:
        if "本周六" in text or "低质量" in text or "图像模糊" in text:
            return {
                "start_text": None,
                "deadline_text": None,
                "normalized_start": None,
                "normalized_deadline": None,
            }
        start_text = default_start
        for token in ["今晚10:00", "今晚8:30", "今晚18:00", "明早12:30", "明早10:00", "明早8:30", "周三14:00", "周三12:30", "周三10:00", "周五16:30", "周五14:00", "周五12:30"]:
            if token in text:
                start_text = token
                break
        return {
            "start_text": start_text,
            "deadline_text": default_deadline,
            "normalized_start": "2026-04-24T18:30:00+08:00",
            "normalized_deadline": "2026-04-24T22:00:00+08:00" if default_deadline else None,
        }

    @classmethod
    def _location_for_text(cls, text: str, raw: str) -> dict[str, str | float | None] | None:
        if "待确认" in text or cls._is_low_quality(text) or "导师沟通会" in text or "实习通勤" in text:
            return None
        if "腾讯会议" in text:
            raw = "腾讯会议"
        elif "会议室301" in text:
            raw = "会议室301"
        elif "学院楼B402" in text:
            raw = "学院楼B402"
        elif "线上会议室" in text:
            raw = "线上会议室"
        elif "西安北站" in text:
            raw = "西安北站"
        elif "南校区东门" in text:
            raw = "南校区东门"
        elif "机场T3" in text:
            raw = "机场T3"
        elif "会议中心签到处" in text:
            raw = "会议中心签到处"
        return {"raw": raw, "map_query": raw, "confidence": 0.84}

    @staticmethod
    def _actions_for_missing(missing_fields: list[str], *, calendar: str, reminder: str, map_label: str) -> list[dict[str, object]]:
        if "time" in missing_fields:
            return [{"type": "reminder", "label": "稍后确认", "requires_permission": True}]
        actions: list[dict[str, object]] = [
            {"type": "calendar", "label": calendar, "requires_permission": True},
            {"type": "reminder", "label": reminder, "requires_permission": True},
        ]
        if "location" not in missing_fields:
            actions.append({"type": "map", "label": map_label, "requires_permission": False})
        return actions

    @staticmethod
    def _manual_review_output(title: str, explanation: str) -> AnalyzeResponse:
        return AnalyzeResponse(
            scene_type="unknown",
            confidence=0.41,
            title=title,
            time=None,
            location=None,
            task={"summary": "需要人工确认", "priority": "low", "topic": "unknown"},
            suggested_actions=[{"type": "reminder", "label": "稍后确认", "requires_permission": True}],
            missing_fields=["scene_type", "time", "location"],
            explanation=explanation,
        )

    @staticmethod
    def _negative_output() -> AnalyzeResponse:
        return AnalyzeResponse(
            scene_type="unknown",
            confidence=0.22,
            title="无需行动碎片",
            time=None,
            location=None,
            task={"summary": "无需生成行动", "priority": "low", "topic": "unknown"},
            suggested_actions=[{"type": "reminder", "label": "不生成行动，稍后确认", "requires_permission": True}],
            missing_fields=["scene_type", "time", "location", "task"],
            explanation="内容没有明确时间、地点或后续动作，避免误创建行动。",
        )

    def _course_output(self, text: str) -> AnalyzeResponse:
        if MockModelAdapter._is_sparse_course_text(text):
            return MockModelAdapter._sparse_course_output(text)

        if not self.allow_demo_samples:
            return MockModelAdapter._evidence_only_course_output(text)

        deadline = DEMO_COURSE_DEADLINE if "22:00" in text else DEMO_COURSE_DEADLINE
        missing_fields = MockModelAdapter._missing_fields_for_text(text)
        return AnalyzeResponse(
            scene_type="course_notice",
            confidence=0.72 if missing_fields else 0.94,
            title=DEMO_COURSE_TITLE,
            time=None if "time" in missing_fields else MockModelAdapter._time_for_text(
                text, default_start=DEMO_COURSE_START, default_deadline=deadline
            ),
            location=MockModelAdapter._location_for_text(text, DEMO_COURSE_LOCATION),
            task={"summary": DEMO_COURSE_TASK, "priority": "high", "topic": "course"},
            suggested_actions=MockModelAdapter._actions_for_missing(
                missing_fields,
                calendar="加入日历",
                reminder="课前30分钟提醒",
                map_label="打开教室路线",
            ),
            missing_fields=missing_fields,
            explanation="文本包含课程、时间、地点和截止事项，适合转成行动卡。",
        )

    @staticmethod
    def _evidence_only_course_output(text: str) -> AnalyzeResponse:
        """Build a course card only from fields present in evidence text.

        Args:
            text: OCR or manually entered course text.

        Returns:
            Schema-valid course card with missing fields marked instead of
            filling fixed demo sample values.
        """

        start_text = MockModelAdapter._extract_start_text(text)
        deadline_text = MockModelAdapter._extract_deadline_text(text)
        location_raw = MockModelAdapter._extract_location_text(text)
        base_missing = MockModelAdapter._missing_fields_for_text(text)
        if "time" in base_missing:
            start_text = None
            deadline_text = None
        if "location" in base_missing:
            location_raw = None
        missing_fields: list[str] = []
        if not start_text:
            missing_fields.append("time" if "time" in base_missing else "exact_start_time")
        if not location_raw:
            missing_fields.append("location")
        title = MockModelAdapter._course_title_from_text(text)
        location = (
            {"raw": location_raw, "map_query": location_raw, "confidence": 0.84}
            if location_raw
            else None
        )
        time = (
            {
                "start_text": start_text,
                "deadline_text": deadline_text,
                "normalized_start": None,
                "normalized_deadline": None,
            }
            if start_text or deadline_text
            else None
        )
        actions = MockModelAdapter._actions_for_missing(
            ["time" if not start_text else "", *missing_fields],
            calendar="加入日历",
            reminder="设置提醒",
            map_label="打开地点",
        )
        task_summary = MockModelAdapter._course_task_summary_from_text(text)
        return AnalyzeResponse(
            scene_type="course_notice",
            confidence=0.91 if not missing_fields else 0.72,
            title=title,
            time=time,
            location=location,
            task={"summary": task_summary, "priority": "medium", "topic": "course"},
            suggested_actions=actions,
            missing_fields=list(dict.fromkeys(missing_fields)),
            explanation="课程字段仅来自 OCR 或用户输入证据；缺失时间或地点时保持待确认，不使用固定演示样例。",
        )

    @staticmethod
    def _extract_start_text(text: str) -> str | None:
        for pattern in [
            r"(今天晚上|今晚|明天|明早|本周[一二三四五六日天]|周[一二三四五六日天])\s*[0-9]{1,2}[:：][0-9]{2}",
            r"(今天晚上|晚上|今晚|明天晚上|明晚|明早|明天|本周[一二三四五六日天]|周[一二三四五六日天])\s*[一二三四五六七八九十0-9]{1,3}点(?:半|[0-9]{1,2}分)?",
            r"[0-9]{1,2}[:：][0-9]{2}",
        ]:
            match = re.search(pattern, text)
            if match:
                return match.group(0).replace("：", ":")
        if "今天晚上" in text:
            return "今天晚上"
        if "今晚" in text:
            return "今晚"
        return None

    @staticmethod
    def _extract_deadline_text(text: str) -> str | None:
        match = re.search(r"(今晚|明天|明早|本周[一二三四五六日天]|周[一二三四五六日天])?\s*[0-9]{1,2}[:：][0-9]{2}\s*前", text)
        if match:
            return match.group(0).strip().replace("：", ":")
        match = re.search(r"(今晚|明天|明早|本周[一二三四五六日天]|周[一二三四五六日天])?\s*[一二三四五六七八九十0-9]{1,3}点(?:半|[0-9]{1,2}分)?\s*前", text)
        return match.group(0).strip() if match else None

    @staticmethod
    def _extract_location_text(text: str) -> str | None:
        for pattern in [
            r"([A-Za-z]地点在\d{2,4})",
            r"(?:教室是|教室|地点|改到|调整到|在)\s*([A-Za-z一-龥]*[A-Z]?\d{2,4}[A-Za-z一-龥]*)",
            r"(?:教室是|教室|地点|改到|调整到|在)\s*([A-Za-z一-龥]+(?:研讨室|报告厅|会议室)\d*)",
            r"([A-Z]\d{2,4})",
            r"([\u4e00-\u9fa5]{1,8}(?:教室|报告厅|会议室|教学楼)[A-Z]?\d{0,4})",
        ]:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip(" ，,。")
        return None

    @staticmethod
    def _course_title_from_text(text: str) -> str:
        if "高数" in text:
            suffix = " A" if "高数A" in text or "高数 A" in text else ""
            return f"上高数{suffix}".strip()
        match = re.search(r"(?<!早)(?<!晚)上([\u4e00-\u9fa5A-Za-z0-9]{1,16}?)(?:课|课程|教室|地点|在|，|,|\s|$)", text)
        if match:
            subject = match.group(1).strip()
            return subject if subject.endswith("课") else f"{subject}课"
        match = re.search(r"([\u4e00-\u9fa5A-Za-z0-9]{1,12})(?:课|课程|上课)", text)
        if match:
            return f"{match.group(1)}课"
        return "课程事项待确认"

    @staticmethod
    def _course_task_summary_from_text(text: str) -> str:
        summary = text.strip()
        if len(summary) > 48:
            summary = summary[:48]
        return summary or "课程事项待确认"

    @staticmethod
    def _sparse_course_output(text: str) -> AnalyzeResponse:
        return sparse_course_output(text)

    @staticmethod
    def _event_output(text: str) -> AnalyzeResponse:
        missing_fields = MockModelAdapter._missing_fields_for_text(text)
        return AnalyzeResponse(
            scene_type="event_poster",
            confidence=0.71 if {"time", "location"}.issubset(missing_fields) else 0.91,
            title="AI应用分享会",
            time=None if "time" in missing_fields else MockModelAdapter._time_for_text(
                text, default_start="4月24日19:30", default_deadline="今晚22:00"
            ),
            location=MockModelAdapter._location_for_text(text, "图书馆报告厅"),
            task={"summary": "报名并前往AI应用分享会", "priority": "high", "topic": "event"},
            suggested_actions=MockModelAdapter._actions_for_missing(
                missing_fields,
                calendar="加入活动日历",
                reminder="报名截止前提醒",
                map_label="打开活动地点",
            ),
            missing_fields=missing_fields,
            explanation="海报包含活动主题、时间、地点和报名截止，适合生成活动行动卡。",
        )

    @staticmethod
    def _assignment_output(text: str) -> AnalyzeResponse:
        missing_fields = MockModelAdapter._missing_fields_for_text(text)
        return AnalyzeResponse(
            scene_type="unknown",
            confidence=0.68 if missing_fields else 0.78,
            title="作业提交截止",
            time=None if "time" in missing_fields else {
                "start_text": None,
                "deadline_text": "今晚22:00",
                "normalized_start": None,
                "normalized_deadline": "2026-04-24T22:00:00+08:00",
            },
            location=MockModelAdapter._location_for_text(text, "教学平台"),
            task={"summary": "按要求提交作业材料", "priority": "high", "topic": "unknown"},
            suggested_actions=MockModelAdapter._actions_for_missing(
                missing_fields,
                calendar="加入截止日历",
                reminder="截止前提醒提交",
                map_label="打开提交入口",
            ),
            missing_fields=missing_fields,
            explanation="识别到作业/截止语义，但当前公开契约不扩展 scene_type，按 unknown 处理并给出可执行动作。",
        )

    @staticmethod
    def _meeting_output(text: str) -> AnalyzeResponse:
        missing_fields = MockModelAdapter._missing_fields_for_text(text)
        return AnalyzeResponse(
            scene_type="unknown",
            confidence=0.67 if missing_fields else 0.76,
            title="会议通知",
            time=None if "time" in missing_fields else MockModelAdapter._time_for_text(text, default_start="今晚10:00"),
            location=MockModelAdapter._location_for_text(text, "腾讯会议"),
            task={"summary": "准备会议进展和待协调事项", "priority": "medium", "topic": "unknown"},
            suggested_actions=MockModelAdapter._actions_for_missing(
                missing_fields,
                calendar="加入会议日历",
                reminder="会前提醒准备",
                map_label="打开会议地点",
            ),
            missing_fields=missing_fields,
            explanation="识别到会议语义，但当前公开契约不扩展 scene_type，按 unknown 处理并给出可执行动作。",
        )

    @staticmethod
    def _interview_output(text: str) -> AnalyzeResponse:
        missing_fields = MockModelAdapter._missing_fields_for_text(text)
        return AnalyzeResponse(
            scene_type="unknown",
            confidence=0.76 if missing_fields else 0.84,
            title="面试安排",
            time=None if "time" in missing_fields else MockModelAdapter._time_for_text(text, default_start="明天14:00"),
            location=MockModelAdapter._location_for_text(text, "线上会议室"),
            task={"summary": "准备面试材料并按时参加", "priority": "high", "topic": "unknown"},
            suggested_actions=MockModelAdapter._actions_for_missing(
                missing_fields,
                calendar="加入面试日历",
                reminder="面试前提醒",
                map_label="打开面试地点",
            ),
            missing_fields=missing_fields,
            explanation="识别到面试语义，但当前公开契约不扩展 scene_type，按 unknown 处理并给出可执行动作。",
        )

    @staticmethod
    def _travel_output(text: str) -> AnalyzeResponse:
        missing_fields = MockModelAdapter._missing_fields_for_text(text)
        return AnalyzeResponse(
            scene_type="unknown",
            confidence=0.67 if missing_fields else 0.8,
            title="出行集合提醒",
            time=None if "time" in missing_fields else MockModelAdapter._time_for_text(text, default_start="今晚10:00"),
            location=MockModelAdapter._location_for_text(text, "西安北站"),
            task={"summary": "按集合时间到达并检查证件", "priority": "high", "topic": "unknown"},
            suggested_actions=MockModelAdapter._actions_for_missing(
                missing_fields,
                calendar="加入出行日历",
                reminder="出发前提醒",
                map_label="打开集合地点",
            ),
            missing_fields=missing_fields,
            explanation="识别到出行语义，但当前公开契约不扩展 scene_type，按 unknown 处理并给出可执行动作。",
        )
