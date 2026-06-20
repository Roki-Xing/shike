#!/usr/bin/env python3
"""Validate the post-arrangement completion page closes the user flow."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    """Read a UTF-8 project file.

    Args:
        relative: Project-relative file path.

    Returns:
        File content, or an empty string when absent.
    """

    path = ROOT / relative
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def exists(relative: str) -> bool:
    """Return true when a project-relative file exists."""

    return (ROOT / relative).is_file()


def main() -> int:
    completion = read("android-mvp/app/src/main/java/cn/shike/app/ui/CompletionSummaryScreen.kt")
    planner = read("android-mvp/app/src/main/java/cn/shike/app/ui/ActionPlannerPanel.kt")
    routes = read("android-mvp/app/src/main/java/cn/shike/app/ui/MainScreenRoutes.kt")
    flow = read("android-mvp/app/src/main/java/cn/shike/app/ui/MainFlowScreens.kt")
    main_screen = read("android-mvp/app/src/main/java/cn/shike/app/ui/ShikeMainScreen.kt")
    execution = read("android-mvp/app/src/main/java/cn/shike/app/ui/ExecutionResult.kt")
    test = read("android-mvp/app/src/test/java/cn/shike/app/CompletionSummaryStateTest.kt")

    checks = [
        ("completion_screen_file_exists", exists("android-mvp/app/src/main/java/cn/shike/app/ui/CompletionSummaryScreen.kt")),
        (
            "completion_state_model_exists",
            "data class CompletionSummaryState" in completion
            and "completionSummaryState(" in completion
            and "calendarStatus" in completion
            and "reminderStatus" in completion
            and "mapStatus" in completion
            and "sourceImageStatus" in completion,
        ),
        (
            "completion_page_has_user_facing_results",
            "已安排" in completion
            and "日历：已打开系统新增页" in completion
            and "提醒：" in completion
            and "地图：" in completion
            and "原截图：" in completion
            and "回到今日行动台" in completion,
        ),
        (
            "completion_page_uses_execution_results",
            "ExecutionResult" in completion
            and "results.firstOrNull" in completion
            and "原截图" in completion
            and "已移入回收站" in completion
            and "已保留" in completion,
        ),
        (
            "planner_finish_button_has_callback",
            "onCompleteArrangement: () -> Unit" in planner
            and "onClick = onCompleteArrangement" in planner
            and "enabled = isConfirmed" in planner
            and "完成安排" in planner,
        ),
        (
            "import_route_completed_shows_completion_page",
            "ImportRouteStage.Completed -> CompletionSummaryScreen(" in routes
            and "onReturnHome" in routes
            and "ActionPlanScreen(" in routes,
        ),
        (
            "flow_passes_completion_callback",
            "onCompleteArrangement" in flow
            and "CompletionSummaryScreen(" in routes
            and "ActionPlannerPanel(" in flow,
        ),
        (
            "main_screen_tracks_completed_stage",
            "importFlowCompleted" in main_screen
            and "selectedSection = ShikeMainSection.Home" in main_screen
            and "onCompleteArrangement = { importFlowCompleted = true }" in main_screen
            and "onReturnHome = {" in main_screen
            and "importFlowCompleted = false" in main_screen,
        ),
        (
            "completion_copy_keeps_calendar_boundary",
            "已打开系统新增页" in completion + execution
            and "已写入日历" not in completion,
        ),
        (
            "completion_summary_unit_test_exists",
            "completionSummaryState_prefersRecordedExecutionResults" in test
            and "completionSummaryState_handlesKeptSourceImage" in test,
        ),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"COMPLETION_PAGE_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
