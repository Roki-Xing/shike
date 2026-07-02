#!/usr/bin/env python3
"""Prevent the ordinary demo flow from regressing into an engineering console."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UI_ROOT = ROOT / "android-mvp/app/src/main/java/cn/shike/app/ui"
SYSTEM_ROOT = ROOT / "android-mvp/app/src/main/java/cn/shike/app/system"

USER_FILES = [
    "HomeActionScreen.kt",
    "ProductHomeHero.kt",
    "ProductHomeState.kt",
    "SmartActionCard.kt",
    "SmartActionCardUiModel.kt",
    "ActionPlannerPanel.kt",
    "ActionPlannerExecutionControls.kt",
    "InboxPanel.kt",
    "AnalyzeProgressPanel.kt",
    "BottomNavigation.kt",
]

FORBIDDEN = ["Mock", "schema", "provider", "后端", "validation", "AppKEY", "token", "云端 AI 解析", "OCR文本包含"]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    user_ui = "\n".join(read(UI_ROOT / name) for name in USER_FILES if (UI_ROOT / name).is_file())
    home_screen = read(UI_ROOT / "HomeActionScreen.kt")
    home = read(UI_ROOT / "ProductHomeHero.kt")
    smart_model = read(UI_ROOT / "SmartActionCardUiModel.kt")
    smart_card = read(UI_ROOT / "SmartActionCard.kt")
    planner = read(UI_ROOT / "ActionPlannerPanel.kt") + read(UI_ROOT / "ActionPlannerExecutionControls.kt")
    inbox = read(UI_ROOT / "InboxPanel.kt")
    progress = read(UI_ROOT / "AnalyzeProgressPanel.kt")
    system_actions = read(SYSTEM_ROOT / "SystemActions.kt")

    checks = [
        ("ordinary_ui_hides_engineering_words", all(word not in user_ui for word in FORBIDDEN)),
        ("home_has_screenshot_to_action_positioning", "把截图变成今天能做的事" in home and "课程变更、活动海报、群通知" in home and "导入截图" in home),
        ("pending_card_compresses_full_hero", "ProductHomeState.Empty" in home_screen and "ProductHomeMiniHeader" in home_screen and "FocusedActionReviewCard" in home_screen),
        ("coarse_morning_time_needs_review", "今天上午" in smart_model and "SmartFieldState.NeedsReview" in smart_model and "确认具体开始时间" in smart_model),
        ("campus_room_does_not_promise_public_navigation", "isCampusRoomCode" in smart_model and "复制地点" in planner and "CopyOnly" in system_actions),
        ("planner_has_next_two_things_not_completion_illusion", "下一步，先完成这 2 件" in planner and "保存日历草稿" in planner and "执行上方动作后查看回执" not in planner),
        ("inbox_is_workbench_not_debug_table", "行动台" in inbox and "搜课程、地点、活动" in inbox and "查看识别依据" in inbox),
        ("parse_progress_has_delight_steps", "读截图" in progress and "找时间地点" in progress and "生成行动卡" in progress and "等你确认" in progress),
        ("action_card_has_scene_preparation_pack", "课前包" in smart_card and "PreparationSuggestionMapper" not in smart_card and "preparationItemsForUi" in smart_model + read(UI_ROOT / "PreparationSuggestionMapper.kt")),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"DEMO_VIDEO_PAINPOINTS_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
