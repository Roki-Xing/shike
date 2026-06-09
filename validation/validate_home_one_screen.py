#!/usr/bin/env python3
"""Validate the productized one-screen home and fixed bottom navigation."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI_ROOT = ROOT / "android-mvp/app/src/main/java/cn/shike/app/ui"


def read(relative: str) -> str:
    return (UI_ROOT / relative).read_text(encoding="utf-8")


def body_between(text: str, start: str, end: str) -> str:
    start_index = text.index(start)
    end_index = text.index(end, start_index)
    return text[start_index:end_index]


def main() -> int:
    main_screen = read("ShikeMainScreen.kt")
    main_flow = read("MainFlowScreens.kt")
    home_screen = read("HomeActionScreen.kt")
    progress_panel = read("AnalyzeProgressPanel.kt")
    bottom_nav = read("BottomNavigation.kt")
    home_agenda = read("HomeAgendaList.kt")
    home_body = body_between(home_screen, "fun HomeActionScreen", "private fun ScreenshotPromptEntry")
    settings_body = body_between(main_flow, "fun PrivacySettingsScreen", "private fun VersionUnlockRow")

    checks = [
        ("main_screen_uses_scaffold", "Scaffold(" in main_screen and "bottomBar =" in main_screen),
        ("bottom_nav_fixed_outside_scroll_column", main_screen.index("bottomBar =") < main_screen.index(".verticalScroll(")),
        ("bottom_nav_has_four_user_tabs", all(label in bottom_nav for label in ["首页", "导入", "收件箱", "设置"]) and "调试" not in bottom_nav),
        ("home_excludes_debug_screen", "DebugDemoScreen" not in home_body and "BackendEndpointControls" not in home_body),
        (
            "home_contains_primary_action_and_import",
            "HomeAgendaList(" in home_body
            and "AnalyzeProgressPanel(" in home_body
            and "HomePendingReviewPanel" in home_body,
        ),
        (
            "home_excludes_full_confirm_and_action_plan",
            "ParseConfirmPanel(" not in home_body
            and "ConfirmBanner(" not in home_body
            and "ActionPlannerPanel(" not in home_body,
        ),
        (
            "home_keeps_summary_compact",
            "TodaySummaryPanel" not in home_body and "DemoRoutePanel" not in home_body and "DeliveryReadinessPanel" not in home_body,
        ),
        (
            "home_agenda_has_quick_actions",
            all(token in home_agenda for token in ["onGallery", "onManualInput", "导入截图", "手动输入"])
            and "QuickImportPanel" not in main_flow,
        ),
        (
            "home_keeps_screenshot_flow_on_home",
            "mutableStateOf(ShikeMainSection.Home)" in main_screen
            and "selectedSection = ShikeMainSection.Import" not in main_screen
            and "ScreenshotDetectedSheet" in home_screen
            and "正在把截图变成行动卡" in progress_panel,
        ),
        ("settings_hides_backend_connection", "BackendEndpointControls" not in settings_body and "后端连接" not in settings_body),
        ("settings_has_about_and_developer_hint", "关于拾刻" in settings_body and "连续点击版本号 5 次" in settings_body),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"HOME_ONE_SCREEN_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
