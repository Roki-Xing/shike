#!/usr/bin/env python3
"""Validate system-action UX copy and execution gating."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def main() -> int:
    system_actions = read("android-mvp/app/src/main/java/cn/shike/app/system/SystemActions.kt")
    execution_result = read("android-mvp/app/src/main/java/cn/shike/app/ui/ExecutionResult.kt")
    action_gate = read("android-mvp/app/src/main/java/cn/shike/app/ui/ExecutionActionGate.kt")
    controls = read("android-mvp/app/src/main/java/cn/shike/app/ui/ActionPlannerExecutionControls.kt")
    main_activity = read("android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt")

    checks = [
        (
            "calendar_copy_opens_insert_page_only",
            "已打开系统日历新增页，请在日历中保存" in execution_result
            and "已写入日历" not in system_actions
            and "已写入日历" not in execution_result,
        ),
        (
            "missing_time_disables_calendar_and_reminder",
            "canUseCalendar = isConfirmed && !missingTime" in action_gate
            and "canUseReminder = isConfirmed && !missingTime" in action_gate,
        ),
        (
            "missing_location_disables_map",
            "canUseMap = isConfirmed && !missingLocation" in action_gate and "补充地点后可用" in action_gate,
        ),
        (
            "controls_require_confirmed_gate",
            "enabled = gate.canUseCalendar" in controls
            and "enabled = gate.canUseReminder" in controls
            and "enabled = gate.canUseMap" in controls,
        ),
        (
            "reminder_shows_exact_or_degraded_mode",
            "精确定时" in execution_result and "系统普通定时" in execution_result,
        ),
        (
            "map_failure_copies_location_and_keeps_card",
            "copyMapLocationFallback" in main_activity and "已保留地点" in main_activity,
        ),
        (
            "execution_results_are_user_visible",
            all(token in execution_result for token in ["日历", "提醒", "地图"]) and '${result.action}执行结果' in execution_result,
        ),
    ]
    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"CALENDAR_MAP_REMINDER_UX_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
