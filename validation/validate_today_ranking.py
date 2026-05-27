#!/usr/bin/env python3
"""Validate TodayActionItem ranking rules with synthetic S2 samples."""

from __future__ import annotations

from dataclasses import dataclass


NOW_MINUTE = 12 * 60


@dataclass(frozen=True)
class TodayActionItem:
    """One synthetic today-action candidate.

    Args:
        item_id: Stable sample identifier.
        title: User-facing title.
        status: Inbox-like status.
        start_minute: Minutes from midnight when the event starts.
        deadline_minute: Minutes from midnight when the item is due.
        needs_confirmation: Whether the item still needs user review.
        needs_location: Whether the next action needs a location.
        has_location: Whether the item has usable location text.
        confidence: Synthetic parse confidence.

    Returns:
        Immutable sample item used by the ranking verifier.
    """

    item_id: str
    title: str
    status: str
    start_minute: int | None
    deadline_minute: int | None
    needs_confirmation: bool
    needs_location: bool
    has_location: bool
    confidence: float


def minutes_until(value: int | None) -> int | None:
    """Compute minutes from the fixed baseline to a same-day minute.

    Args:
        value: Minute from midnight, or None.

    Returns:
        Non-negative minutes until the value, or None.
    """

    if value is None:
        return None
    return max(value - NOW_MINUTE, 0)


def urgency_score(minutes: int | None, near_weight: int, same_day_weight: int) -> int:
    """Score near same-day times.

    Args:
        minutes: Minutes until the event/deadline.
        near_weight: Score when the time is very close.
        same_day_weight: Score when the time is still today.

    Returns:
        Integer urgency score.
    """

    if minutes is None:
        return 0
    if minutes <= 120:
        return near_weight
    if minutes <= 24 * 60:
        return same_day_weight
    return 0


def ranking_score(item: TodayActionItem) -> int:
    """Compute the deterministic Today Action ranking score.

    Args:
        item: Synthetic action item.

    Returns:
        Higher score means the item should appear earlier.
    """

    if item.status in {"已忽略", "已完成"}:
        return -1000

    score = 0
    score += urgency_score(minutes_until(item.deadline_minute), 70, 45)
    score += urgency_score(minutes_until(item.start_minute), 40, 20)

    if item.needs_confirmation:
        score += 30
    if item.confidence < 0.65:
        score += 25
    if item.needs_location and not item.has_location:
        score += 20
    if item.status == "即将截止":
        score += 15
    if item.status == "待确认":
        score += 10
    if item.status == "已安排":
        score -= 8

    return score


def sort_items(items: list[TodayActionItem]) -> list[TodayActionItem]:
    """Sort today-action items by score and stable tie-breakers.

    Args:
        items: Synthetic action items.

    Returns:
        Items sorted for display.
    """

    return sorted(
        items,
        key=lambda item: (
            -ranking_score(item),
            minutes_until(item.deadline_minute) if item.deadline_minute is not None else 10_000,
            minutes_until(item.start_minute) if item.start_minute is not None else 10_000,
            item.item_id,
        ),
    )


def sample_items() -> list[TodayActionItem]:
    """Build the required 10 synthetic S2 ranking samples.

    Args:
        None.

    Returns:
        Ten representative today-action samples.
    """

    return [
        TodayActionItem("activity-deadline-low-confidence", "活动报名截止需确认", "即将截止", 19 * 60, 13 * 60, True, False, True, 0.58),
        TodayActionItem("assignment-deadline", "高数作业今晚提交", "即将截止", None, 22 * 60, False, False, True, 0.92),
        TodayActionItem("meeting-soon", "项目会议马上开始", "已安排", 13 * 60 + 30, None, False, True, True, 0.9),
        TodayActionItem("missing-location-map", "面试地点待补全", "待确认", 18 * 60, None, True, True, False, 0.8),
        TodayActionItem("low-confidence-fragment", "低置信度截图碎片", "待确认", None, None, True, False, True, 0.42),
        TodayActionItem("course-scheduled", "高数A班教室变更", "已安排", 18 * 60 + 30, None, False, True, True, 0.95),
        TodayActionItem("travel-ticket", "周末车票提醒", "已安排", 3 * 24 * 60, None, False, True, True, 0.91),
        TodayActionItem("backend-fallback", "云侧解析失败待复核", "待确认", None, None, True, False, True, 0.6),
        TodayActionItem("completed-task", "已完成报名", "已完成", None, 14 * 60, False, False, True, 0.98),
        TodayActionItem("ignored-ad", "已忽略广告截图", "已忽略", None, 13 * 60, False, False, True, 0.7),
    ]


def run_checks() -> list[tuple[str, bool, str]]:
    """Run Today Action ranking assertions.

    Args:
        None.

    Returns:
        List of named check results.
    """

    items = sample_items()
    ordered = sort_items(items)
    ids = [item.item_id for item in ordered]
    scores = [ranking_score(item) for item in ordered]

    return [
        ("ten_synthetic_samples", len(items) == 10, str(len(items))),
        ("sorted_scores_descending", scores == sorted(scores, reverse=True), ",".join(map(str, scores))),
        ("low_confidence_deadline_first", ids[0] == "activity-deadline-low-confidence", ids[0]),
        ("deadline_before_start_only", ids.index("assignment-deadline") < ids.index("meeting-soon"), ",".join(ids[:4])),
        ("missing_location_stays_pending", ids.index("missing-location-map") < ids.index("course-scheduled"), ",".join(ids[:6])),
        ("completed_and_ignored_bottom", set(ids[-2:]) == {"completed-task", "ignored-ad"}, ",".join(ids[-2:])),
        ("deterministic_order", ids == [item.item_id for item in sort_items(list(reversed(items)))], ",".join(ids)),
    ]


def main() -> int:
    """Run the Today Action ranking verifier.

    Args:
        None.

    Returns:
        Process status code.
    """

    checks = run_checks()
    passed = sum(1 for _, ok, _ in checks if ok)
    for name, ok, evidence in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}\t{evidence}")
    print(f"TODAY_RANKING_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
