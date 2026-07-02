#!/usr/bin/env python3
"""Validate the Product Delight Sprint polish without weakening safety gates."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UI_ROOT = ROOT / "android-mvp/app/src/main/java/cn/shike/app/ui"
SYSTEM_ROOT = ROOT / "android-mvp/app/src/main/java/cn/shike/app/system"
TEST_ROOT = ROOT / "android-mvp/app/src/test/java/cn/shike/app"

USER_UI_FILES = [
    "AnalyzeProgressPanel.kt",
    "ActionReadinessBar.kt",
    "ActionReadinessUiModel.kt",
    "ActionCardUiModel.kt",
    "SmartActionCard.kt",
    "SmartActionCardUiModel.kt",
    "PreparationSuggestionMapper.kt",
    "FocusedHomeCard.kt",
    "ParseConfirmPanel.kt",
    "ActionPlannerPanel.kt",
    "ActionPlannerExecutionControls.kt",
    "ScreenshotCleanupPrompt.kt",
    "ProductHomeHero.kt",
    "HomeActionScreen.kt",
]
FORBIDDEN_USER_WORDS = ["Service is running", "backend", "schema", "provider", "Mock", "validation", "AppKEY", "token"]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def main() -> int:
    user_ui = "\n".join(read(UI_ROOT / name) for name in USER_UI_FILES)
    progress = read(UI_ROOT / "AnalyzeProgressPanel.kt")
    readiness_model = read(UI_ROOT / "ActionReadinessUiModel.kt")
    readiness_bar = read(UI_ROOT / "ActionReadinessBar.kt")
    prep_mapper = read(UI_ROOT / "PreparationSuggestionMapper.kt")
    sanitizer = read(UI_ROOT / "UserFacingCopySanitizer.kt")
    smart_model = read(UI_ROOT / "SmartActionCardUiModel.kt")
    cleanup = read(UI_ROOT / "ScreenshotCleanupPrompt.kt")
    notification = read(SYSTEM_ROOT / "ScreenshotNotification.kt")
    service = read(SYSTEM_ROOT / "ScreenshotAssistService.kt")
    readiness_test = read(TEST_ROOT / "ActionReadinessUiModelTest.kt")
    prep_test = read(TEST_ROOT / "PreparationSuggestionMapperTest.kt")
    sanitizer_test = read(TEST_ROOT / "UserFacingCopySanitizerTest.kt")

    due_word = "dead" + "line"
    checks = [
        ("ordinary_ui_hides_service_running", "Service is running" not in user_ui + notification + service),
        ("ordinary_ui_hides_engineering_words", all(word not in user_ui for word in FORBIDDEN_USER_WORDS[1:])),
        ("progress_has_screenshot_to_action_title", "正在把截图变成行动卡" in progress and "拾刻正在找时间、地点和准备事项" in progress),
        ("progress_has_four_user_steps", all(word in progress for word in ["读截图", "找时间地点", "生成行动卡", "等你确认"])),
        ("action_readiness_model_and_bar_exist", "data class ActionReadinessUiModel" in readiness_model and "fun actionReadinessUiModelFrom" in readiness_model and "fun ActionReadinessBar" in readiness_bar),
        ("action_readiness_user_copy_present", "行动准备度" in readiness_model and "这张卡已经可以安排" in readiness_model and "时间是建议值" in readiness_model),
        ("meeting_defaults_avoid_course_items", "班会" in prep_mapper and "准备发言" in prep_mapper and "带课本" in prep_mapper and "meetingFallbackDoesNotShowCourseItems" in prep_test),
        ("preparation_sanitizer_covers_trailing_quote", "cleanPreparationItem" in sanitizer and "带红领巾'" in sanitizer_test and "带红领巾" in sanitizer_test),
        ("ambiguous_time_is_not_marked_confirmed", "大概" in smart_model and "今天上午" in smart_model and "SmartFieldState.NeedsReview" in smart_model and "已确认具体时间" not in smart_model + readiness_model),
        ("source_image_cleanup_is_collapsed_secondary", "原图处理" in cleanup and "rememberSaveable" in cleanup and "展开原图处理" in cleanup and "OutlinedButton" in cleanup and "Button(" not in cleanup.replace("OutlinedButton(", "")),
        ("notification_copy_is_productized", "发现新截图" in notification and "要生成一张行动卡吗？" in notification and "拾刻截图提醒运行中" in service and "只在本机检测新截图，不会自动上传图片" in service),
        ("unit_tests_cover_delight_models", "ActionReadinessUiModelTest" in readiness_test and "PreparationSuggestionMapperTest" in prep_test and "UserFacingCopySanitizerTest" in sanitizer_test),
        ("due_time_word_is_mapped", due_word not in user_ui.lower() and "可能有截止时间，请确认" in sanitizer + sanitizer_test),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"PRODUCT_DELIGHT_SPRINT_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
