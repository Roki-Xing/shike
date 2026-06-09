#!/usr/bin/env python3
"""Validate calendar prefill accuracy and missing-time guards."""

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
    """Run calendar prefill source and regression checks.

    Returns:
        Process exit code.
    """

    model_client = read("android-mvp/app/src/main/java/cn/shike/app/data/ModelApiClient.kt")
    model_time_parser = read("android-mvp/app/src/main/java/cn/shike/app/data/ModelTimeParser.kt")
    system_actions = read("android-mvp/app/src/main/java/cn/shike/app/system/SystemActions.kt")
    action_gate = read("android-mvp/app/src/main/java/cn/shike/app/ui/ExecutionActionGate.kt")
    model_test = read("android-mvp/app/src/test/java/cn/shike/app/ModelApiClientTest.kt")
    system_test = read("android-mvp/app/src/test/java/cn/shike/app/SystemActionsTest.kt")
    action_gate_test = read("android-mvp/app/src/test/java/cn/shike/app/ExecutionActionGateTest.kt")
    execution_result = read("android-mvp/app/src/main/java/cn/shike/app/ui/ExecutionResult.kt")

    checks = [
        (
            "model_mapping_reads_normalized_start",
            "normalized_start" in model_time_parser
            and "startEpochMillisFromTime" in model_client
            and "sampleCourse().startEpochMillis" not in model_client
            and "sampleEvent().startEpochMillis" not in model_client,
        ),
        (
            "model_mapping_parses_chinese_relative_time",
            "parseRelativeChineseTime" in model_time_parser
            and "明天" in model_time_parser
            and "晚上" in model_time_parser
            and "chineseNumberToInt" in model_time_parser,
        ),
        (
            "calendar_uses_calendar_draft",
            "data class CalendarDraft" in system_actions
            and "fun calendarDraftFrom" in system_actions
            and "CalendarContract.EXTRA_EVENT_BEGIN_TIME, startMillis" in system_actions
            and "requireNotNull(draft.startAtMillis)" in system_actions,
        ),
        (
            "calendar_copy_does_not_claim_saved",
            "打开系统日历新增页" in system_actions
            and "由用户在日历中保存" in system_actions
            and "已写入" not in system_actions
            and "已同步" not in system_actions
            and "已打开系统日历新增页，请在日历中保存" in execution_result,
        ),
        (
            "missing_epoch_blocks_calendar_and_reminder",
            "item.startEpochMillis <= 0L" in action_gate
            and "canUseCalendar = isConfirmed && !missingTime" in action_gate
            and "canUseReminder = isConfirmed && !missingTime" in action_gate,
        ),
        (
            "unit_tests_cover_normalized_start",
            "itemFromAnalyzeJson_usesNormalizedStartInsteadOfSampleEpoch" in model_test
            and "2026-06-10T09:00:00+08:00" in model_test
            and "assertNotEquals(sampleCourse().startEpochMillis" in model_test,
        ),
        (
            "unit_tests_cover_relative_chinese_time",
            "itemFromAnalyzeImageJson_normalizesChineseRelativeStartTextWhenNormalizedStartMissing" in model_test
            and "明天早上九点" in model_test
            and "Asia/Shanghai" in model_test,
        ),
        (
            "unit_tests_cover_calendar_draft_and_missing_time",
            "calendarDraftFrom_usesParsedEpochAndDisablesWhenTimeIsMissing" in system_test
            and "补充具体时间后可加入日历" in system_test
            and "executionActionGateFor_timeTextWithoutEpochBlocksCalendarAndReminder" in action_gate_test,
        ),
        (
            "null_deadline_is_filtered",
            "deadline_text" in model_client
            and "takeUnless { it.equals(\"null\", ignoreCase = true) }" in model_client
            and "assertFalseContainsNull" in model_test,
        ),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"CALENDAR_PREFILL_ACCURACY_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
