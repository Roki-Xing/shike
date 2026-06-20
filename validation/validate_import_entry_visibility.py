#!/usr/bin/env python3
"""Validate that import is a first-class entry point in the Shike Android UI."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI_ROOT = ROOT / "android-mvp/app/src/main/java/cn/shike/app/ui"
APP_ROOT = ROOT / "android-mvp/app/src/main/java/cn/shike/app"


def read_ui(relative: str) -> str:
    """Read a UTF-8 UI source file.

    Args:
        relative: File path under the Android UI source root.

    Returns:
        File content.
    """

    return (UI_ROOT / relative).read_text(encoding="utf-8")


def read_app(relative: str) -> str:
    """Read a UTF-8 app source file.

    Args:
        relative: File path under the Android app source root.

    Returns:
        File content.
    """

    return (APP_ROOT / relative).read_text(encoding="utf-8")


def body_between(text: str, start: str, end: str) -> str:
    start_index = text.index(start)
    end_index = text.index(end, start_index)
    return text[start_index:end_index]


def main() -> int:
    """Run import-entry visibility checks.

    Returns:
        Process exit code.
    """

    home_screen = read_ui("HomeActionScreen.kt")
    focused_card = read_ui("FocusedHomeCard.kt")
    main_routes = read_ui("MainScreenRoutes.kt")
    main_screen = read_ui("ShikeMainScreen.kt")
    bottom_navigation = read_ui("BottomNavigation.kt")
    screen_host = read_app("ShikeScreenHost.kt")

    home_signature = body_between(home_screen, "fun HomeActionScreen", ") {")
    home_body = body_between(home_screen, "fun HomeActionScreen", "private fun ScreenshotPromptEntry")
    home_route_signature = body_between(main_routes, "fun HomeRouteContent", ") {")
    home_route_body = body_between(main_routes, "fun HomeRouteContent", "@Composable\nfun ImportRouteContent")

    checks = [
        (
            "quick_import_bar_component_exists",
            "fun QuickImportBar(" in focused_card
            and all(token in focused_card for token in ["导入截图", "拍照识别", "手动输入"]),
        ),
        (
            "home_accepts_three_import_actions",
            "onGallery: () -> Unit" in home_signature
            and "onCamera: () -> Unit" in home_signature
            and "onManualInput: () -> Unit" in home_signature,
        ),
        (
            "home_route_passes_camera_action",
            "onCamera: () -> Unit" in home_route_signature
            and "HomeActionScreen(" in home_route_body
            and "onGallery = onGallery" in home_route_body
            and "onCamera = onCamera" in home_route_body
            and "onManualInput = onManualInput" in home_route_body,
        ),
        (
            "quick_import_bar_is_always_visible_on_home",
            "QuickImportBar(" in home_body
            and home_body.index("QuickImportBar(") < home_body.index("when (flowState)")
            and "when (flowState) {\n        ImportFlowState.Idle -> QuickImportBar" not in home_body,
        ),
        (
            "ready_state_keeps_import_available",
            "ImportFlowState.Reviewing, ImportFlowState.Planning ->" in home_body
            and "FocusedActionReviewCard(" in home_body
            and home_body.count("QuickImportBar(") == 1,
        ),
        (
            "bottom_nav_has_center_import_action",
            "onImportClick: () -> Unit" in bottom_navigation
            and "CenterImportButton(" in bottom_navigation
            and all(token in bottom_navigation for token in ["+ 导入", "新建行动卡", "从截图导入", "拍照识别", "手动输入"])
            and 'BottomNavItem("导入"' not in bottom_navigation,
        ),
        (
            "main_screen_owns_import_sheet_state",
            "showImportSheet" in main_screen
            and "ImportActionSheet(" in main_screen
            and "openImportEntry" in main_screen,
        ),
        (
            "home_import_routes_to_import_flow",
            "openImportEntry(onGallery)" in main_screen
            and "openImportEntry(onCamera)" in main_screen
            and "openImportEntry(onManualInput)" in main_screen
            and "selectedSection = ShikeMainSection.Import" in main_screen,
        ),
        (
            "screen_host_keeps_real_capture_callbacks",
            "onGallery = captureLaunchers.launchGallery" in screen_host
            and "onCamera = captureLaunchers.launchCamera" in screen_host
            and "onManualInput = { state.enterManualInput() }" in screen_host,
        ),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"IMPORT_ENTRY_VISIBILITY_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
