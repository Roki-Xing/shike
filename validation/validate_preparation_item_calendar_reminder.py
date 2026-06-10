#!/usr/bin/env python3
"""Validate preparation items flow into calendar and reminder drafts."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    """Read a UTF-8 project file.

    Args:
        relative: File path under the Shike root.

    Returns:
        File content.
    """

    return (ROOT / relative).read_text(encoding="utf-8")


def main() -> int:
    """Run calendar/reminder preparation propagation checks.

    Returns:
        Process exit code.
    """

    evidence = read("android-mvp/app/src/main/java/cn/shike/app/domain/ActionCardEvidence.kt")
    system_actions = read("android-mvp/app/src/main/java/cn/shike/app/system/SystemActions.kt")
    reminder_payload = read("android-mvp/app/src/main/java/cn/shike/app/system/ReminderPayload.kt")
    reminder_scheduler = read("android-mvp/app/src/main/java/cn/shike/app/system/ReminderScheduler.kt")
    test = read("android-mvp/app/src/test/java/cn/shike/app/PreparationCalendarReminderTest.kt")

    checks = [
        ("shared_reminder_detail_builder_present", "fun reminderDetailFor(item: ShikeItem): String" in evidence),
        ("calendar_description_contains_source_task_location_preparation", all(token in system_actions for token in ["来源：拾刻识别", "任务：$it", "地点：$it", "准备事项："])),
        ("calendar_copy_keeps_user_save_boundary", "打开系统日历新增页" in system_actions and "由用户在日历中保存" in system_actions and "确认后写入" not in system_actions),
        ("reminder_payload_uses_shared_detail", "import cn.shike.app.domain.reminderDetailFor" in reminder_payload and "detail = reminderDetailFor(item)" in reminder_payload),
        ("immediate_notification_uses_shared_detail", "detail = reminderDetailFor(item)" in system_actions),
        ("scheduled_reminder_still_uses_alarm_manager", "ScheduledReminder" in reminder_payload and "AlarmManager" in reminder_scheduler),
        ("unit_test_checks_calendar_preparation_copy", all(token in test for token in ["准备事项：带书", "任务：上英语口语，记得带书", "由用户在日历中保存"])),
        ("unit_test_checks_reminder_preparation_copy", "英语口语课 · E520 · 记得带书" in test),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"PREPARATION_ITEM_CALENDAR_REMINDER_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
