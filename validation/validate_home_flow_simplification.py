#!/usr/bin/env python3
"""Validate that the ordinary home route stays compact and action-focused."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI_ROOT = ROOT / "android-mvp/app/src/main/java/cn/shike/app/ui"


def read(relative: str) -> str:
    """Read a UTF-8 UI source file.

    Args:
        relative: File path under the Android UI source root.

    Returns:
        File content.
    """

    return (UI_ROOT / relative).read_text(encoding="utf-8")


def body_between(text: str, start: str, end: str) -> str:
    start_index = text.index(start)
    end_index = text.index(end, start_index)
    return text[start_index:end_index]


def main() -> int:
    """Run home flow simplification checks.

    Returns:
        Process exit code.
    """

    home_screen = read("HomeActionScreen.kt")
    main_routes = read("MainScreenRoutes.kt")
    main_screen = read("ShikeMainScreen.kt")
    main_flow = read("MainFlowScreens.kt")
    progress_panel = read("AnalyzeProgressPanel.kt")
    action_planner = read("ActionPlannerPanel.kt")

    home_body = body_between(home_screen, "fun HomeActionScreen", "private fun ScreenshotPromptEntry")
    home_route_body = body_between(main_routes, "fun HomeRouteContent", "@Composable\nfun ImportRouteContent")
    import_route_body = body_between(main_routes, "fun ImportRouteContent", "{\n    CaptureHubScreen")
    import_full_body = body_between(main_routes, "fun ImportRouteContent", "}\n")

    checks = [
        (
            "home_keeps_only_summary_import_and_progress",
            "DashboardHeader()" in home_body
            and "DateStrip()" in home_body
            and "HomeAgendaList(" in home_body
            and "AnalyzeProgressPanel(" in home_body
            and "HomePendingReviewPanel(" in home_body,
        ),
        (
            "home_does_not_mount_confirm_or_action_plan",
            "ParseConfirmPanel(" not in home_body
            and "ConfirmBanner(" not in home_body
            and "ActionPlannerPanel(" not in home_body
            and "onAddCalendar" not in home_route_body
            and "onReminder" not in home_route_body
            and "onOpenMap" not in home_route_body,
        ),
        (
            "import_flow_owns_confirm_and_action_plan",
            "CaptureHubScreen(" in import_full_body
            and "ParseConfirmScreen(" in import_full_body
            and "ActionPlanScreen(" in import_full_body,
        ),
        (
            "analyze_progress_has_four_user_steps",
            all(token in progress_panel for token in ["读取图片", "OCR识别", "结构化解析", "生成行动卡"]),
        ),
        (
            "action_plan_keeps_cleanup_after_confirmation",
            "ScreenshotCleanupPrompt(" in action_planner
            and "isConfirmed && selectedSourceMediaStoreUri != null" in action_planner,
        ),
        (
            "bottom_padding_protects_nav_overlap",
            "Spacer(Modifier.height(112.dp))" in main_screen
            and ".navigationBarsPadding()" in main_screen,
        ),
        (
            "ordinary_user_tabs_stay_simple",
            all(token in main_screen for token in ["ShikeMainSection.Home", "ShikeMainSection.Import", "ShikeMainSection.Inbox", "ShikeMainSection.Settings"])
            and "DebugDemoScreen(" in main_screen,
        ),
        (
            "debug_tools_are_not_in_home_route",
            "DebugDemoScreen" not in home_route_body
            and "BackendEndpointControls" not in home_route_body
            and "OfflineSampleActions" not in home_route_body,
        ),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"HOME_FLOW_SIMPLIFICATION_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
