#!/usr/bin/env python3
"""Validate that ordinary user-facing screens do not expose engineering copy."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI_ROOT = ROOT / "android-mvp/app/src/main/java/cn/shike/app/ui"
APP_ROOT = ROOT / "android-mvp/app/src/main/java/cn/shike/app"

USER_SCREEN_FILES = [
    "ShikeMainScreen.kt",
    "MainFlowScreens.kt",
    "BottomNavigation.kt",
    "CaptureEntryPanel.kt",
    "HomeAgendaList.kt",
    "ParseConfirmPanel.kt",
    "ActionPlannerPanel.kt",
    "InboxPanel.kt",
]
FORBIDDEN_USER_COPY = ["MockModelAdapter", "/v1/analyze", "validate_", "后端地址", "交付物自检中心", "3分钟演示路线"]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    user_copy = "\n".join(read(UI_ROOT / path) for path in USER_SCREEN_FILES if (UI_ROOT / path).is_file())
    debug_copy = read(UI_ROOT / "DebugDemoScreen.kt")
    backend_runner = read(APP_ROOT / "data/BackendAnalysisRunner.kt")
    backend_actions = read(APP_ROOT / "BackendAnalysisActions.kt")
    endpoint_actions = read(APP_ROOT / "BackendEndpointActions.kt")
    bottom_nav = read(UI_ROOT / "BottomNavigation.kt")
    main_flow = read(UI_ROOT / "MainFlowScreens.kt")
    main_screen = read(UI_ROOT / "ShikeMainScreen.kt")
    readiness_sections = read(UI_ROOT / "ReadinessSections.kt")
    developer_mode = read(UI_ROOT / "DeveloperModeUnlock.kt")
    local_multimodal = read(UI_ROOT / "LocalMultimodalStatus.kt")

    checks = [
        ("ordinary_screens_hide_mock_copy", "MockModelAdapter" not in user_copy and "MockModelAdapter" not in backend_runner),
        ("ordinary_screens_hide_endpoint_path", "/v1/analyze" not in user_copy and "/v1/analyze" not in backend_actions),
        ("ordinary_screens_hide_validation_copy", "validate_" not in user_copy),
        ("ordinary_screens_hide_backend_address", "后端地址" not in user_copy),
        ("ordinary_screens_hide_delivery_self_check", "交付物自检中心" not in user_copy and "3分钟演示路线" not in user_copy),
        ("bottom_nav_hides_debug_tab", "BottomNavItem(\"调试\"" not in bottom_nav),
        (
            "product_copy_replaces_engineering_status",
            "云侧解析中" in backend_actions
            and "云侧连接已保存" in endpoint_actions
            and "云侧暂不可用，已切换为本地确认" in backend_runner,
        ),
        (
            "debug_screen_keeps_engineering_tools",
            "BackendEndpointControls" in debug_copy and "OfflineSampleActions" in debug_copy,
        ),
        (
            "settings_mentions_hidden_developer_mode",
            "高级设置" in main_flow and "普通模式已隐藏高级配置" in main_flow,
        ),
        (
            "settings_version_tap_unlocks_developer_mode",
            "VersionUnlockRow" in main_flow
            and "Modifier.clickable(onClick = onVersionTap)" in main_flow
            and "DEVELOPER_MODE_UNLOCK_TAPS = 5" in developer_mode
            and "developerModeStateAfterVersionTap" in main_screen,
        ),
        (
            "debug_entry_requires_unlock_state",
            "var developerModeState" in main_screen
            and "selectedSection = result.targetSection" in main_screen
            and "ShikeMainSection.Debug" not in bottom_nav,
        ),
        (
            "settings_names_local_multimodal_boundary",
            "解析方式" in readiness_sections
            and "本地优先处理" in readiness_sections
            and "端侧模型：未安装" in local_multimodal
            and "不会假装可用" in local_multimodal
            and "同一 JSON Schema" in local_multimodal,
        ),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"USER_FACING_COPY_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
