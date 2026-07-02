#!/usr/bin/env python3
"""Validate the Shike Product Feel Sprint polish layer."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UI_ROOT = ROOT / "android-mvp/app/src/main/java/cn/shike/app/ui"
TEST_ROOT = ROOT / "android-mvp/app/src/test/java/cn/shike/app"

ORDINARY_UI_FILES = [
    "ShikeMainScreen.kt",
    "HomeActionScreen.kt",
    "ProductHomeHero.kt",
    "ProductHomeState.kt",
    "SmartActionCard.kt",
    "SmartActionCardUiModel.kt",
    "ActionPlannerPanel.kt",
    "ActionPlannerExecutionControls.kt",
    "InboxPanel.kt",
    "BottomNavigation.kt",
]
FORBIDDEN = ["Mock", "schema", "provider", "后端", "validation", "AppKEY", "token"]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def function_body(text: str, start: str, end: str) -> str:
    start_index = text.index(start)
    end_index = text.index(end, start_index)
    return text[start_index:end_index]


def main() -> int:
    ordinary_ui = "\n".join(read(UI_ROOT / name) for name in ORDINARY_UI_FILES if (UI_ROOT / name).is_file())
    home = read(UI_ROOT / "HomeActionScreen.kt") + read(UI_ROOT / "ProductHomeHero.kt")
    smart_model = read(UI_ROOT / "SmartActionCardUiModel.kt")
    smart_card = read(UI_ROOT / "SmartActionCard.kt")
    sanitizer = read(UI_ROOT / "UserFacingCopySanitizer.kt")
    planner = read(UI_ROOT / "ActionPlannerPanel.kt") + read(UI_ROOT / "ActionPlannerExecutionControls.kt")
    main_screen = read(UI_ROOT / "ShikeMainScreen.kt")
    settings_source = read(UI_ROOT / "ReadinessSections.kt")
    settings_body = function_body(settings_source, "fun PrivacyPanel", "@Composable\nprivate fun SettingPlainRow")
    smart_test = read(TEST_ROOT / "SmartActionCardUiModelTest.kt")
    prep_mapper = read(UI_ROOT / "PreparationSuggestionMapper.kt") if (UI_ROOT / "PreparationSuggestionMapper.kt").is_file() else ""

    checks = [
        ("ordinary_ui_hides_forbidden_engineering_words", all(word not in ordinary_ui for word in FORBIDDEN)),
        ("ordinary_ui_hides_deadline_word", "deadline" not in ordinary_ui.lower()),
        ("home_keeps_core_positioning", "把截图变成今天能做的事" in home or "截图变行动卡" in home),
        ("pending_card_does_not_force_full_hero", "ProductHomeState.Empty" in home and "ProductHomeMiniHeader" in home and "ProductHomeHero(" in home),
        ("approximate_time_not_marked_concrete", "大概" in smart_model and "SmartFieldState.NeedsReview" in smart_model and "已识别到具体时间" not in smart_model + smart_card),
        ("preparation_item_quotes_are_cleaned", "cleanPreparationItem" in sanitizer and "带红领巾'" in smart_test and "带红领巾" in smart_test),
        ("scene_preparation_mapper_exists", "班会" in prep_mapper and "准备发言" in prep_mapper and "带课本" in prep_mapper),
        ("bottom_nav_overlap_guard_exists", "bottomBarHeightWithSafeSpace = 148.dp" in main_screen and ".statusBarsPadding()" in main_screen and ".navigationBarsPadding()" in main_screen),
        ("settings_has_collapsed_advanced_diagnostics", "高级诊断" in settings_body and "diagnosticsExpanded" in settings_body and "ScreenshotAssistDiagnosticsPanel" in settings_body),
        ("planner_removes_gray_receipt_button", "执行上方动作后查看回执" not in planner and "日历草稿已打开" in planner and "我已保存" in planner and "还没保存" in planner),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"PRODUCT_FEEL_SPRINT_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
