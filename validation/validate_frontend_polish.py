#!/usr/bin/env python3
"""Validate Android frontend productization boundaries."""

from __future__ import annotations

import re
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
    required_files = [
        "AppSections.kt",
        "BottomNavigation.kt",
        "CaptureEntryPanel.kt",
        "DebugDemoScreen.kt",
        "FrontendStateComponents.kt",
        "MainFlowScreens.kt",
        "ShikeDesignTokens.kt",
        "ShikeMainScreen.kt",
    ]
    main_flow = read("MainFlowScreens.kt")
    main_screen = read("ShikeMainScreen.kt")
    debug_screen = read("DebugDemoScreen.kt")
    capture_entry = read("CaptureEntryPanel.kt")
    tokens = read("ShikeDesignTokens.kt")
    state_components = read("FrontendStateComponents.kt")
    bottom_nav = read("BottomNavigation.kt")

    home_body = body_between(main_flow, "fun HomeActionScreen", "fun CaptureHubScreen")
    capture_body = body_between(capture_entry, "fun CaptureEntryPanel", "}")

    screen_names = [
        "HomeActionScreen",
        "CaptureHubScreen",
        "ParseConfirmScreen",
        "ActionPlanScreen",
        "InboxScreen",
        "PrivacySettingsScreen",
        "DebugDemoScreen",
    ]
    state_names = ["ShikeEmptyState", "ShikeErrorState", "ShikeLoadingSkeleton"]
    token_names = ["ShikeColors", "ShikeTypography", "ShikeSpacing"]
    debug_only_tokens = ["BackendEndpointControls", "OfflineSampleActions", "DeliveryReadinessPanel", "DemoRoutePanel"]
    home_forbidden_text = ["validate_", "交付物自检", "3分钟演示路线", "后端地址", "课程样例", "活动样例"]

    checks = [
        ("required_frontend_files_present", all((UI_ROOT / path).is_file() for path in required_files), ",".join(required_files)),
        ("screen_shells_present", all(f"fun {name}" in (debug_screen if name == "DebugDemoScreen" else main_flow) for name in screen_names), ",".join(screen_names)),
        ("design_tokens_present", all(f"object {name}" in tokens for name in token_names), ",".join(token_names)),
        ("state_components_present", all(f"fun {name}" in state_components for name in state_names), ",".join(state_names)),
        ("root_uses_section_state", "var selectedSection" in main_screen and "when (selectedSection)" in main_screen, "selectedSection"),
        (
            "default_home_excludes_debug_content",
            all(token not in home_body for token in debug_only_tokens + home_forbidden_text),
            "home body",
        ),
        (
            "debug_screen_owns_demo_and_samples",
            all(token in debug_screen for token in debug_only_tokens),
            "debug screen",
        ),
        (
            "backend_endpoint_not_in_home_or_import",
            "BackendEndpointControls" not in home_body and "BackendEndpointControls" not in capture_body,
            "home/import",
        ),
        (
            "settings_hides_backend_endpoint",
            "fun PrivacySettingsScreen" in main_flow
            and "BackendEndpointControls" not in body_between(main_flow, "fun PrivacySettingsScreen", "private fun HomePendingReviewPanel"),
            "settings",
        ),
        (
            "loading_empty_error_reachable",
            "ShikeLoadingSkeleton" in main_flow and "ShikeErrorState" in main_flow and "TodayAgendaState.Empty" in read("HomeAgendaList.kt"),
            "state usage",
        ),
        (
            "bottom_nav_routes_real_sections",
            all(name in bottom_nav for name in ["ShikeMainSection.Home", "ShikeMainSection.Import", "ShikeMainSection.Inbox", "ShikeMainSection.Settings"])
            and "ShikeMainSection.Debug" not in bottom_nav,
            "bottom nav",
        ),
        (
            "home_has_quick_import",
            "QuickImportPanel" not in home_body
            and "HomeAgendaList(" in home_body
            and "导入截图" in read("HomeAgendaList.kt")
            and "ImportCaptureActions" in capture_entry,
            "home import cta",
        ),
    ]

    passed = sum(1 for _, ok, _ in checks if ok)
    for name, ok, evidence in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}\t{evidence}")
    print(f"FRONTEND_POLISH_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
