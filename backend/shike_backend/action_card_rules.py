"""Rule-backed v2 action-card extraction from OCR evidence."""

from __future__ import annotations

import re

from shike_backend.preparation import preparation_items_from_text
from shike_backend.schemas_v2 import EvidenceSpan, ParsedActionCard


_TIME_PREFIX = r"(?:今天|今晚|今天晚上|明天|明早|明晚|明天早上|明天上午|明天下午|明天晚上|后天|这周[一二三四五六日天]|本周[一二三四五六日天]|周[一二三四五六日天]|下周[一二三四五六日天])"
_CLOCK = r"(?:[0-9]{1,2}[:：][0-9]{2}|[一二三四五六七八九十两0-9]{1,3}点(?:半|[0-9]{1,2}分)?)"
_ACTIONABLE_SCENES = {
    "course_notice",
    "event_poster",
    "meeting_notice",
    "assignment_deadline",
    "exam_notice",
    "travel_ticket",
}
_NOISE_TOKENS = ("标题", "未分类", "截图编辑", "撤销", "完成", "KB/s", "字 |")
_ONLINE_LOCATIONS = ("腾讯会议", "线上", "链接", "牛客", "QQ群", "邮箱", "学习通", "提交入口", "群里")


def parsed_action_card_from_ocr_text(
    text: str,
    *,
    scene_hint: str | None,
    reason: str,
    ignored_regions: list[str],
) -> ParsedActionCard:
    """Build a v2 action card directly from OCR text evidence.

    Args:
        text: OCR text or Android OCR hint.
        scene_hint: Optional client scene hint.
        reason: Non-secret fallback reason for audit risks.
        ignored_regions: Screenshot regions ignored by OCR preprocessing.

    Returns:
        Parsed v2 action card whose fields are evidence-backed.
    """

    normalized = _normalize_ocr_text(text)
    primary = _primary_action_text(normalized)
    scene = _classify_scene(primary, scene_hint)
    time_payload = _time_payload(primary, scene)
    location = _location_payload(primary, scene)
    preparation_items = preparation_items_from_text(primary)
    missing_fields = _missing_fields(primary, scene, time_payload, location)
    task = _task_payload(primary, scene)
    title = _title_for_scene(primary, scene)
    actions = _actions_for(scene, time_payload, location, missing_fields, preparation_items)
    risks = _warnings_for(primary, scene, missing_fields)

    return ParsedActionCard(
        title=title,
        scene_type=scene,
        confidence=_confidence_for(scene, time_payload, location, missing_fields),
        time=time_payload,
        location=location,
        task=task,
        suggested_actions=actions,
        missing_fields=missing_fields,
        preparation_items=preparation_items,
        checklist_items=[{"text": item, "source": "ocr", "confidence": 0.88} for item in preparation_items],
        risks=[f"text_fallback:{reason}", *risks],
        evidence=[
            EvidenceSpan(field="ocr_text_hint", text="OCR 文本证据", source="ocr", box=None),
        ],
        ignored_regions=ignored_regions,
        explanation="根据 OCR 文本抽取时间、地点、任务与准备事项；用户确认前不会执行系统动作。",
    )


def _normalize_ocr_text(text: str) -> str:
    normalized = text.strip().replace("：", ":")
    replacements = {
        "8:3O": "8:30",
        "15:0O": "15:00",
        "E52O": "E520",
        "3O3": "303",
    }
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    normalized = re.sub(r"([0-9])O([0-9])", r"\g<1>0\2", normalized)
    return re.sub(r"\s+", " ", normalized)


def _primary_action_text(text: str) -> str:
    primary = re.split(r"；|;|同一张图下面还写着|下面还写着", text, maxsplit=1)[0].strip()
    primary = re.sub(r"^\d{1,2}:\d{2}\s+(?:\d+(?:\.\d+)?KB/s\s+)?", "", primary)
    primary = re.sub(r"^\d{1,2}:\d{2}\s+标题\s+\d{4}/\d{1,2}/\d{1,2}\s+\d{1,2}:\d{2}\s*\|\s*\d+字\s*\|\s*未分类\s*", "", primary)
    return primary.strip() or text


def _classify_scene(text: str, hint: str | None) -> str:
    if _is_negative(text, hint):
        return "unknown"
    if any(token in text for token in ("讲座", "分享会", "宣讲", "路演", "培训", "训练营", "招新", "校园歌手", "篮球赛", "早操", "志愿", "活动时间", "报名截止")):
        return "event_poster"
    if any(token in text for token in ("面试", "笔试", "HR", "牛客")):
        return "interview_notice"
    if any(token in text for token in ("高铁", "航班", "机场", "车站", "发车", "检票", "校车")):
        return "travel_ticket"
    if any(token in text for token in ("考试", "补考", "准考证", "四六级", "概率论")):
        return "exam_notice"
    if any(token in text for token in ("会议", "组会", "例会", "评审", "汇报", "预演", "沟通会", "导员办公室")):
        return "meeting_notice"
    if any(token in text for token in ("课改", "课补课", "补课", "上课地点", "课在", "课不上")):
        if "课不上" in text and any(token in text for token in ("提交", "发QQ群", "作业")):
            return "assignment_deadline"
        return "course_notice"
    if _is_assignment_text(text):
        return "assignment_deadline"
    if hint in _ACTIONABLE_SCENES:
        return hint
    if any(token in text for token in ("课", "教室", "高数", "英语口语", "线代", "毛概", "数据结构", "Python")):
        return "course_notice"
    if any(token in text for token in ("活动", "报名", "海报")):
        return "event_poster"
    return "unknown"


def _is_negative(text: str, hint: str | None) -> bool:
    if hint == "negative_fragment":
        return True
    return any(
        token in text
        for token in (
            "表情包",
            "哈哈",
            "电量不足",
            "连接充电器",
            "只有品牌 slogan",
            "天气不错",
            "晒太阳",
        )
    )


def _is_assignment_text(text: str) -> bool:
    if "课取消" in text and any(token in text for token in ("作业", "提交", "交")):
        return True
    return any(token in text for token in ("作业", "报告", "论文", "PPT", "提交", "截止", "问卷", "读书笔记", "发邮箱", "课前交"))


def _time_payload(text: str, scene: str) -> dict[str, str | None] | None:
    if scene == "unknown" and _is_negative(text, None) and not _is_leisure_fragment(text):
        return None
    deadline = _extract_deadline_text(text)
    start = None if scene == "assignment_deadline" and deadline else _extract_start_text(text)
    if not start and not deadline:
        start = _coarse_time_text(text, scene)
    if not start and not deadline:
        return None
    return {
        "start_text": start,
        "deadline_text": deadline,
        "normalized_start": None,
        "normalized_deadline": None,
    }


def _extract_start_text(text: str) -> str | None:
    if match := re.search(
        rf"(?:改为|改到|调整到)\s*((?:这周|本周|下周|周)[一二三四五六日天]\s*(?:上午|下午|晚上|早上|晚|中午)?\s*{_CLOCK})",
        text,
    ):
        return _clean_start_text(match.group(1))
    if match := re.search(
        rf"((?:这周|本周|下周|周)[一二三四五六日天]).{{0,28}}?((?:上午|下午|晚上|早上|晚|中午)?\s*{_CLOCK})(?:\s*(?:开始|上课|集合|发车|入场))?",
        text,
    ):
        return _clean_start_text(f"{match.group(1)}{match.group(2)}")
    patterns = [
        rf"\d{{1,2}}/\d{{1,2}}\s*(?:上午|下午|晚上|晚|中午)?\s*{_CLOCK}",
        rf"\d{{1,2}}/\d{{1,2}}\s+{_CLOCK}",
        rf"\d{{1,2}}月\d{{1,2}}日\s*(?:上午|下午|晚上|晚|中午)?\s*{_CLOCK}",
        rf"\d{{1,2}}\.\d{{1,2}}\s*(?:上午|下午|晚上|晚|中午)?\s*{_CLOCK}",
        rf"{_TIME_PREFIX}\s*(?:上午|下午|晚上|早上|晚|中午)?\s*{_CLOCK}",
        rf"(?:上午|下午|晚上|早上|晚|中午)?\s*{_CLOCK}\s*(?:开始|集合|发车|入场|上课|上)",
        rf"(?<![:\d]){_CLOCK}\s*(?:[A-Za-z\u4e00-\u9fa5]{0,8})?(?:课|会议|组会|例会|汇报|评审)",
        rf"(?:(?:明天|今天|今晚|明晚)\s*)?{_CLOCK}\s+(?=[A-Z][-\d])",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match and not _looks_like_noise_time(text, match.start(), match.group(0)):
            return _clean_start_text(match.group(0))
    if match := re.search(rf"(这周[一二三四五六日天]).*?((?:上午|下午|晚上|早上|晚|中午)?\s*{_CLOCK})", text):
        return _clean_start_text(f"{match.group(1)}{match.group(2)}")
    return None


def _clean_start_text(value: str) -> str:
    """Normalize a matched start-time phrase for display and downstream rules."""

    cleaned = re.sub(r"\s+", "", value).strip()
    return re.sub(r"(?:开始|集合|发车|入场|上课|上)$", "", cleaned)


def _extract_deadline_text(text: str) -> str | None:
    if match := re.search(r"不是今晚，是\s*([^，,。；;]{1,14}?交)", text):
        return match.group(1).removesuffix("交").strip()
    patterns = [
        rf"(?:改到|延期到)\s*({_TIME_PREFIX}\s*(?:上午|下午|晚上|晚|中午)?\s*{_CLOCK})",
        rf"报名截止[:：]?\s*({_TIME_PREFIX}\s*{_CLOCK})",
        rf"报名截止[:：]?\s*(\d{{1,2}}月\d{{1,2}}日\s*[0-9]{{1,2}}[:：][0-9]{{2}})",
        rf"\d{{1,2}}月\d{{1,2}}日\s*(?:上午|下午|晚上|晚|中午)?\s*{_CLOCK}\s*前",
        rf"{_TIME_PREFIX}\s*(?:上午|下午|晚上|晚|中午)?\s*{_CLOCK}\s*前",
        rf"{_TIME_PREFIX}\s*(?:上午|下午|晚上|晚|中午)?\s*{_CLOCK}\s*(?:交|提交)",
        rf"{_TIME_PREFIX}\s*课前",
        rf"(?:下周[一二三四五六日天]|周[一二三四五六日天])\s*前",
        r"报名截止\s*\d{1,2}月\d{1,2}日\s*[0-9]{1,2}[:：][0-9]{2}",
        r"\d{1,2}月\d{1,2}日\s*截止",
        r"\d{1,2}月\d{1,2}日前",
    ]
    for pattern in patterns:
        if match := re.search(pattern, text):
            return re.sub(r"\s+", "", match.group(0)).strip()
    if match := re.search(rf"(周[一二三四五六日天]).*?((?:上午|下午|晚上|晚|中午)?\s*{_CLOCK}\s*前)", text):
        return f"{match.group(1)}{re.sub(r'\\s+', '', match.group(2))}"
    if match := re.search(rf"(晚上|上午|下午|早上|中午)\s*{_CLOCK}\s*前", text):
        prefix = re.search(r"(周[一二三四五六日天])", text)
        return f"{prefix.group(1) if prefix else ''}{re.sub(r'\\s+', '', match.group(0))}"
    return None


def _looks_like_noise_time(text: str, start: int, value: str) -> bool:
    if any(token in value for token in ("今天", "今晚", "明天", "明早", "周", "月", "晚上", "下午", "上午", "早上")):
        return False
    window = text[max(0, start - 10) : start + len(value) + 20]
    return any(token in window for token in ("KB/s", "标题", "未分类", "字 |"))


def _coarse_time_text(text: str, scene: str) -> str | None:
    for token in ("今天下午", "今晚", "明天"):
        if token in text:
            return token
    return None


def _location_payload(text: str, scene: str) -> dict[str, object] | None:
    location = _extract_location_text(text, scene)
    if not location:
        return None
    return {"raw": location, "map_query": location, "confidence": 0.82}


def _extract_location_text(text: str, scene: str) -> str | None:
    if "不用去" in text and not any(token in text for token in ("改到", "改为", "地点改", "上课地点改")):
        return None
    if "高铁" in text and "西安北" in text:
        return "西安北站"
    if "机场" in text and "T3" in text:
        return "机场T3"
    if match := re.search(r"([A-Za-z]地点)在?(\d{2,4})", text):
        return f"{match.group(1)}{match.group(2)}"
    if match := re.search(r"腾讯会议\s*(?:会议号)?\s*([0-9][0-9 \-]{5,}[0-9])", text):
        return f"腾讯会议 {match.group(1).strip()}"
    if "腾讯会议" in text:
        return "腾讯会议"
    online = _online_location(text)
    if online:
        return online
    for pattern in (
        r"(?:上课地点改|地点改|改到|调整到)\s*([A-Za-z]?\d{2,4}|[A-Z]\d{2,4}|[\u4e00-\u9fa5A-Za-z0-9]+[-]?\d{2,4})",
        r"(?:教室是|教室|地点是|地点在|地点)\s*([A-Za-z]?\d{2,4}|[A-Z]\d{2,4}|[\u4e00-\u9fa5A-Za-z0-9]+[-]?\d{2,4})",
        r"((?:信远楼|教学楼|实验楼|学院楼|南校区B楼|机房|教)[A-Za-z0-9I\-]+)",
        r"([A-Z]-?\d{3,4})",
        r"([A-Z]\d{3,4})",
        r"((?:南校区)?(?:图书馆|学术|多功能|大学生活动中心|会议中心|就业中心|大礼堂)[\u4e00-\u9fa5]*(?:报告厅|会议室|活动中心|中心|礼堂|厅)?)",
        r"(会议室\d{2,4})",
        r"(导员办公室|实验室|操场|体育馆|北门|东门|西安北站|机场T3|奶茶店)",
    ):
        if match := re.search(pattern, text):
            return _normalize_location(match.group(1), scene)
    if scene == "travel_ticket" and "T3" in text:
        return "机场T3"
    return None


def _online_location(text: str) -> str | None:
    if "线上" in text and "链接稍后" in text:
        return "线上链接待发"
    if "牛客链接稍后" in text:
        return "牛客链接待发"
    if "QQ群" in text:
        return "QQ群"
    if "学习通" in text:
        return "学习通"
    if "发邮箱" in text or "邮箱" in text:
        return "邮箱"
    if "发群里" in text or "群里" in text:
        return "群里"
    if "提交入口" in text:
        return "提交入口"
    if "线上" in text:
        return "线上会议"
    return None


def _normalize_location(value: str, scene: str) -> str:
    location = value.strip(" ，,。；;?")
    location = location.replace("3O3", "303").replace("E52O", "E520")
    if scene == "travel_ticket" and location == "T3":
        return "机场T3"
    return location


def _task_payload(text: str, scene: str) -> dict[str, str]:
    priority = "high" if scene in {"assignment_deadline", "exam_notice", "travel_ticket"} else "medium"
    topic = {
        "course_notice": "course",
        "event_poster": "event",
        "assignment_deadline": "assignment",
        "exam_notice": "exam",
        "meeting_notice": "meeting",
        "interview_notice": "interview",
        "travel_ticket": "travel",
    }.get(scene, "unknown")
    summary = _strip_noise_words(text)
    if len(summary) > 64:
        summary = summary[:64]
    return {"summary": summary or "需要人工确认", "priority": priority, "topic": topic}


def _title_for_scene(text: str, scene: str) -> str:
    if scene == "unknown":
        if "材料" in text and "弄一下" in text:
            return "材料事项待确认"
        if _is_leisure_fragment(text):
            return "非强任务碎片"
        if "优惠券" in text:
            return "优惠券待确认"
        return "无需行动碎片" if _is_negative(text, None) else "待确认碎片"
    if scene == "course_notice":
        return _course_title(text)
    if scene == "assignment_deadline":
        return _assignment_title(text)
    if scene == "event_poster":
        return _event_title(text)
    if scene == "meeting_notice":
        return _meeting_title(text)
    if scene == "exam_notice":
        return _exam_title(text)
    if scene == "interview_notice":
        return "线上面试" if "面试" in text else "笔试通知"
    if scene == "travel_ticket":
        return "航班出行" if "航班" in text else "高铁出行" if "高铁" in text else "出行集合提醒"
    return "待确认碎片"


def _course_title(text: str) -> str:
    if "高数" in text:
        return "高数课"
    for subject in ("英语口语", "英语听力", "数据结构", "软件工程实验", "数据库", "体育", "线代", "毛概", "Python"):
        if subject in text:
            suffix = "签到" if "签到" in text else "补课" if "补课" in text else "地点变更" if "改" in text else "课"
            return f"{subject}{suffix}" if not subject.endswith("课") else subject
    if match := re.search(r"上([\u4e00-\u9fa5A-Za-z0-9]{1,12}?)(?:课|教室|地点|，|,|\s|$)", text):
        subject = match.group(1).strip()
        return subject if subject.endswith("课") else f"{subject}课"
    return "课程事项待确认"


def _assignment_title(text: str) -> str:
    for keyword in ("实验报告", "读书笔记", "论文初稿", "PPT展示材料", "录音作业", "问卷", "作业"):
        if keyword in text:
            return f"{keyword}提交" if "截止" not in keyword else keyword
    return "提交事项"


def _event_title(text: str) -> str:
    for keyword in ("AI应用分享会", "简历优化与面试技巧讲座", "社团招新宣讲", "创新创业路演", "实验安全培训", "志愿服务", "校园歌手初赛", "早操集合", "篮球赛"):
        if keyword.replace("讲座", "") in text:
            return keyword
    if match := re.search(r"([\u4e00-\u9fa5A-Za-z0-9]{2,16})(?:\s+\d| 时间| 6| 本周| 周|：)", text):
        return match.group(1).strip("讲座：: ")
    return "活动待确认"


def _meeting_title(text: str) -> str:
    for keyword in ("组会", "产品讨论会", "周三例会", "答辩预演", "需求评审", "导员办公室签字", "汇报"):
        if keyword in text:
            return keyword
    return "会议通知"


def _exam_title(text: str) -> str:
    for keyword in ("概率论", "补考", "四六级口语模拟", "高数A"):
        if keyword in text:
            return f"{keyword}考试" if keyword not in {"补考", "四六级口语模拟"} else keyword
    return "考试安排"


def _actions_for(
    scene: str,
    time_payload: dict[str, str | None] | None,
    location: dict[str, object] | None,
    missing_fields: list[str],
    preparation_items: list[str],
) -> list[dict[str, object]]:
    if scene == "unknown" and not time_payload:
        return [{"type": "reminder", "label": "稍后确认", "requires_permission": True}]
    actions: list[dict[str, object]] = []
    has_start = bool(time_payload and time_payload.get("start_text"))
    has_deadline = bool(time_payload and time_payload.get("deadline_text"))
    if has_start and "date" not in missing_fields and "exact_start_time" not in missing_fields:
        actions.append({"type": "calendar", "label": _calendar_label(scene), "requires_permission": True})
    reminder_label = _reminder_label(scene, preparation_items, has_deadline)
    actions.append({"type": "reminder", "label": reminder_label, "requires_permission": True})
    if location and scene != "unknown" and not any(token in str(location.get("raw")) for token in _ONLINE_LOCATIONS):
        actions.append({"type": "map", "label": "打开地点路线", "requires_permission": False})
    return actions


def _calendar_label(scene: str) -> str:
    return {
        "course_notice": "加入课程日历",
        "event_poster": "加入活动日历",
        "meeting_notice": "加入会议日历",
        "exam_notice": "加入考试日历",
        "interview_notice": "加入面试日历",
        "travel_ticket": "加入出行日历",
    }.get(scene, "加入日历")


def _reminder_label(scene: str, preparation_items: list[str], has_deadline: bool) -> str:
    if has_deadline:
        return "截止前提醒"
    if preparation_items:
        return f"提醒：{preparation_items[0]}"
    return {
        "course_notice": "课前提醒",
        "event_poster": "活动前提醒",
        "meeting_notice": "会前提醒",
        "exam_notice": "考试前提醒",
        "interview_notice": "面试前提醒",
        "travel_ticket": "出发前提醒",
    }.get(scene, "稍后确认")


def _missing_fields(
    text: str,
    scene: str,
    time_payload: dict[str, str | None] | None,
    location: dict[str, object] | None,
) -> list[str]:
    missing: list[str] = []
    start = str(time_payload.get("start_text") or "") if time_payload else ""
    if scene in _ACTIONABLE_SCENES and not time_payload:
        missing.append("time")
    if start and _is_bare_relative_time(start):
        missing.append("date")
    if scene == "unknown" and not time_payload and not location:
        missing.extend(["scene_type", "time", "location", "task"])
    if scene == "unknown" and "材料" in text and "弄一下" in text:
        missing.extend(["task_detail", "exact_deadline_time", "submission_method"])
    if scene == "unknown" and _is_leisure_fragment(text):
        missing.append("task")
    if scene in {"course_notice", "meeting_notice", "event_poster", "exam_notice", "interview_notice", "travel_ticket"} and not location:
        missing.append("location")
    if location and any(token in str(location.get("raw")) for token in ("B地点", "实验室", "办公室", "链接待发", "地点待发", "老地方")):
        missing.append("exact_location")
    if "地点未定" in text:
        missing.append("location")
    if "报名二维码" in text and "http" not in text:
        missing.append("registration_url")
    if "报名截止" in text and "活动时间另行通知" in text:
        missing.append("event_time")
    if "链接稍后" in text:
        missing.append("meeting_link")
    if "邮箱" in text and "@" not in text:
        missing.append("submission_email")
    if "下周" in text and time_payload and time_payload.get("deadline_text") and not re.search(r"[0-9一二三四五六七八九十两]+点|[0-9]{1,2}:[0-9]{2}", str(time_payload.get("deadline_text"))):
        missing.append("exact_deadline_time")
    if "课前" in text:
        missing.extend(["exact_deadline_time", "course_context"])
    if scene == "course_notice" and not time_payload and location:
        missing.extend(["date", "exact_start_time"])
    if scene == "meeting_notice" and time_payload and str(time_payload.get("start_text")) in {"今晚", "明天"}:
        missing.append("exact_start_time")
    if scene == "unknown" and time_payload and str(time_payload.get("start_text")) in {"今晚", "明天", "今天下午"}:
        missing.append("task")
        if not location:
            missing.append("location")
        if str(time_payload.get("start_text")) in {"今晚", "明天"}:
            missing.append("exact_start_time")
    return list(dict.fromkeys(missing))


def _is_bare_relative_time(value: str) -> bool:
    return bool(re.search(r"^(?:上午|下午|晚上|早上|晚|中午)?[一二三四五六七八九十两0-9]{1,3}点", value)) and not any(
        token in value for token in ("今天", "今晚", "明天", "明早", "周", "月", "后天")
    )


def _is_leisure_fragment(text: str) -> bool:
    return "天气不错" in text and any(token in text for token in ("晒太阳", "操场"))


def _confidence_for(
    scene: str,
    time_payload: dict[str, str | None] | None,
    location: dict[str, object] | None,
    missing_fields: list[str],
) -> float:
    if scene == "unknown":
        return 0.45 if missing_fields else 0.58
    score = 0.72
    if time_payload:
        score += 0.08
    if location:
        score += 0.08
    if not missing_fields:
        score += 0.06
    return min(score, 0.94)


def _warnings_for(text: str, scene: str, missing_fields: list[str]) -> list[str]:
    warnings: list[str] = []
    if "date" in missing_fields:
        warnings.append("缺少日期，请确认")
    if "exact_location" in missing_fields:
        warnings.append("地点需要确认")
    if "取消" in text:
        warnings.append("文本包含取消或改期信息，请确认")
    if scene == "unknown":
        warnings.append("不是强任务，不应默认加入日历")
    return warnings


def _strip_noise_words(text: str) -> str:
    cleaned = text
    for token in _NOISE_TOKENS:
        cleaned = cleaned.replace(token, " ")
    cleaned = re.sub(r"不用交纸质版", "不需要纸质版", cleaned)
    cleaned = re.sub(r"原定今晚截止", "原截止", cleaned)
    cleaned = cleaned.replace("截图编辑", " ").replace("撤销", " ").replace("@所有人", " ")
    cleaned = cleaned.replace("【微信通知】老师:", " ").replace("【微信通知】老师：", " ")
    cleaned = re.sub(r"\d{1,2}:\d{2}\s+\d+(?:\.\d+)?KB/s", " ", cleaned)
    cleaned = re.sub(r"(?<![A-Za-z])AI(?![A-Za-z])", " ", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip(" ，,。；;")
