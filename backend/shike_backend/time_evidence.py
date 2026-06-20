"""Evidence-backed time enrichment for Shike action cards."""

from __future__ import annotations

from datetime import date, datetime, timedelta
import re
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


_CLOCK_RE = r"(?:[0-2]?\d[:：][0-5]\d|[一二三四五六七八九十两0-9]{1,3}点(?:半|[0-9]{1,2}分)?)"
_TIME_RE = re.compile(
    rf"(?P<prefix>今天晚上|今天早上|今天上午|今天下午|今晚|明天早上|明天上午|明天下午|明天晚上|明晚|明天|本周[一二三四五六日天]|这周[一二三四五六日天]|下周[一二三四五六日天]|周[一二三四五六日天]|晚上|早上|上午|下午|中午)?\s*(?P<clock>{_CLOCK_RE})"
)
_TASK_CONTEXT_RE = re.compile(r"(上课|上|考试|高数|英语口语|教室|会议|组会|活动|集合|签到|面试|笔试)")
_TIME_MISSING_FIELDS = {"time", "start_time", "exact_start_time", "normalized_start"}
_ACTIONABLE_SCENES = {
    "course_notice",
    "event_poster",
    "meeting_notice",
    "interview_notice",
    "exam_notice",
    "travel_ticket",
}
_CN_DIGITS = {
    "零": 0,
    "〇": 0,
    "一": 1,
    "二": 2,
    "两": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
}


def enrich_time_payload(
    payload: dict[str, Any],
    evidence_texts: list[str],
    *,
    current_date: str,
    user_timezone: str,
) -> tuple[dict[str, Any], list[str]]:
    """Return a payload with OCR-backed start time filled when safer.

    Args:
        payload: Schema-compatible action-card payload.
        evidence_texts: OCR or user-provided evidence text.
        current_date: Client-local reference date in ISO format.
        user_timezone: Client IANA timezone.

    Returns:
        Updated payload and non-secret repair reason codes.
    """

    evidence = extract_time_from_text("\n".join(evidence_texts), current_date=current_date, user_timezone=user_timezone)
    if evidence is None:
        return payload, []

    existing = _time_payload(payload.get("time"))
    evidence_start = str(evidence.get("normalized_start") or "")
    existing_start = str(existing.get("normalized_start") or "") if existing else ""
    existing_start_text = str(existing.get("start_text") or "") if existing else ""

    reasons: list[str] = []
    if not existing:
        reasons.append("ocr_time_missing")
    elif evidence_start and not existing_start:
        reasons.append("ocr_normalized_time_missing")
    elif evidence_start and existing_start and evidence_start != existing_start:
        reasons.append("ocr_time_mismatch")
    elif evidence.get("start_text") and not existing_start_text:
        reasons.append("ocr_start_text_missing")

    if not reasons:
        return payload, []

    enriched = dict(payload)
    merged_time = dict(existing or {})
    for key, value in evidence.items():
        if value is None:
            continue
        if key == "start_text" and merged_time.get("start_text"):
            continue
        merged_time[key] = value
    merged_time.setdefault("deadline_text", None)
    merged_time.setdefault("normalized_deadline", None)
    enriched["time"] = merged_time
    enriched["missing_fields"] = _clean_time_missing_fields(enriched.get("missing_fields"))
    enriched["suggested_actions"] = _ensure_time_actions(enriched)
    return enriched, reasons


def extract_time_from_text(text: str, *, current_date: str, user_timezone: str) -> dict[str, str | None] | None:
    """Extract a concrete start time from OCR evidence.

    Args:
        text: OCR or user-provided text.
        current_date: Client-local reference date in ISO format.
        user_timezone: Client IANA timezone.

    Returns:
        Time payload containing `start_text` and `normalized_start`, if found.
    """

    normalized = " ".join(text.replace("：", ":").split())
    if not normalized:
        return None

    candidates: list[dict[str, str | None]] = []
    for match in _TIME_RE.finditer(normalized):
        start_text = re.sub(r"\s+", "", match.group(0)).strip()
        prefix = (match.group("prefix") or "").strip()
        if _looks_like_noise_time(normalized, match.start(), match.end(), start_text):
            continue
        if not prefix and not _has_task_context(normalized, match.start(), match.end()):
            continue
        hour_minute = _parse_clock(match.group("clock"), prefix=prefix)
        if hour_minute is None:
            continue
        day = _resolve_day(prefix, current_date)
        if day is None:
            continue
        zone = _zone_for(user_timezone)
        hour, minute = hour_minute
        normalized_start = datetime(day.year, day.month, day.day, hour, minute, tzinfo=zone).isoformat()
        candidates.append({
            "start_text": start_text,
            "deadline_text": None,
            "normalized_start": normalized_start,
            "normalized_deadline": None,
        })
    return _best_time_candidate(candidates)


def _time_payload(value: object) -> dict[str, Any] | None:
    return dict(value) if isinstance(value, dict) else None


def _has_task_context(text: str, start: int, end: int) -> bool:
    window = text[max(0, start - 12) : min(len(text), end + 18)]
    return _TASK_CONTEXT_RE.search(window) is not None


def _looks_like_noise_time(text: str, start: int, end: int, value: str) -> bool:
    """Return whether a matched time is likely screenshot chrome."""

    if any(token in value for token in ("今天", "今晚", "明天", "周", "晚上", "下午", "上午", "早上")):
        return False
    before = text[max(0, start - 8) : start]
    after = text[end : min(len(text), end + 18)]
    return bool(re.search(r"^\s*$", before) and re.search(r"\d+(?:\.\d+)?KB/s|标题|未分类", after))


def _best_time_candidate(candidates: list[dict[str, str | None]]) -> dict[str, str | None] | None:
    """Prefer the most contextual time candidate."""

    if not candidates:
        return None
    return max(candidates, key=lambda item: _time_candidate_score(str(item.get("start_text") or "")))


def _time_candidate_score(value: str) -> int:
    score = 0
    if any(token in value for token in ("今天", "今晚", "明天", "周", "本周", "这周", "下周")):
        score += 4
    if any(token in value for token in ("晚上", "早上", "上午", "下午", "中午")):
        score += 2
    if re.search(r"[一二三四五六七八九十两]点", value):
        score += 1
    return score


def _parse_clock(value: str, *, prefix: str) -> tuple[int, int] | None:
    text = value.strip().replace("：", ":")
    if ":" in text:
        raw_hour, raw_minute = text.split(":", 1)
        try:
            hour = int(raw_hour)
            minute = int(raw_minute)
        except ValueError:
            return None
    else:
        match = re.match(r"([一二三四五六七八九十两0-9]{1,3})点(?:(半)|([0-9]{1,2})分)?", text)
        if not match:
            return None
        hour = _parse_chinese_number(match.group(1))
        minute = 30 if match.group(2) else int(match.group(3) or 0)
    if hour is None or not (0 <= hour <= 23 and 0 <= minute <= 59):
        return None
    if any(token in prefix for token in ("晚上", "今晚", "明晚", "下午")) and 1 <= hour <= 11:
        hour += 12
    return hour, minute


def _parse_chinese_number(value: str) -> int | None:
    if value.isdigit():
        return int(value)
    if value == "十":
        return 10
    if "十" in value:
        left, _, right = value.partition("十")
        tens = _CN_DIGITS.get(left, 1 if left == "" else None)
        ones = _CN_DIGITS.get(right, 0 if right == "" else None)
        if tens is None or ones is None:
            return None
        return tens * 10 + ones
    if len(value) == 1:
        return _CN_DIGITS.get(value)
    return None


def _resolve_day(prefix: str, current_date: str) -> date | None:
    try:
        base = date.fromisoformat(current_date)
    except ValueError:
        return None
    if "明天" in prefix or prefix in {"明晚"}:
        return base + timedelta(days=1)
    if match := re.search(r"(?:本周|这周|周)([一二三四五六日天])", prefix):
        return _resolve_weekday(base, match.group(1), next_week=False)
    if match := re.search(r"下周([一二三四五六日天])", prefix):
        return _resolve_weekday(base, match.group(1), next_week=True)
    return base


def _resolve_weekday(base: date, weekday_text: str, *, next_week: bool) -> date:
    weekdays = {"一": 0, "二": 1, "三": 2, "四": 3, "五": 4, "六": 5, "日": 6, "天": 6}
    target = weekdays[weekday_text]
    delta = target - base.weekday()
    if next_week:
        delta += 7
    elif delta < 0:
        delta += 7
    return base + timedelta(days=delta)


def _zone_for(user_timezone: str) -> ZoneInfo:
    try:
        return ZoneInfo(user_timezone)
    except ZoneInfoNotFoundError:
        return ZoneInfo("Asia/Shanghai")


def _clean_time_missing_fields(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item) not in _TIME_MISSING_FIELDS]


def _ensure_time_actions(payload: dict[str, Any]) -> list[dict[str, Any]]:
    actions = [dict(item) for item in payload.get("suggested_actions", []) if isinstance(item, dict)]
    scene = str(payload.get("scene_type") or "")
    if scene in _ACTIONABLE_SCENES and not any(action.get("type") == "calendar" for action in actions):
        actions.insert(0, {"type": "calendar", "label": "加入日历", "requires_permission": True})
    if not any(action.get("type") == "reminder" for action in actions):
        actions.append({"type": "reminder", "label": "设置提醒", "requires_permission": True})
    return actions
