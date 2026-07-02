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
    focused_card = read("FocusedHomeCard.kt")
    screenshot_assist_guide = read("ScreenshotAssistGuideDialog.kt")
    main_routes = read("MainScreenRoutes.kt")
    main_screen = read("ShikeMainScreen.kt")
    main_flow = read("MainFlowScreens.kt")
    progress_panel = read("AnalyzeProgressPanel.kt")
    structured_card = read("StructuredActionCard.kt")
    action_planner = read("ActionPlannerPanel.kt")
    capture_entry = read("CaptureEntryPanel.kt")
    parse_confirm = read("ParseConfirmPanel.kt")
    execution_controls = read("ActionPlannerExecutionControls.kt")

    home_body = body_between(home_screen, "fun HomeActionScreen", "private fun ScreenshotPromptEntry")
    home_route_body = body_between(main_routes, "fun HomeRouteContent", "@Composable\nfun ImportRouteContent")
    import_full_body = main_routes[main_routes.index("fun ImportRouteContent"):]

    checks = [
        (
            "home_uses_explicit_import_flow_state",
            all(token in home_screen for token in [
                "enum class ImportFlowState",
                "Idle",
                "Detected",
                "Analyzing",
                "Reviewing",
                "Planning",
                "Completed",
                "importFlowStateFor(",
            ])
            and "sealed class AnalysisUiState" in read("AnalysisUiState.kt")
            and "analysisUiState: AnalysisUiState" in home_screen
            and "analysisUiStateFor(modelStatus)" in main_screen,
        ),
        (
            "home_renders_only_one_primary_state",
            "when (flowState)" in home_body
            and "DashboardHeader()" not in home_body
            and "DateStrip()" not in home_body
            and "HomePendingReviewPanel(" not in home_body
            and "PermissionOnboarding(" not in home_body
            and "AnalyzeProgressPanel(" not in home_body,
        ),
        (
            "home_states_match_user_journey_copy",
            all(token in home_screen + focused_card + screenshot_assist_guide for token in [
                "今天还没有待处理截图",
                "开启截图助手",
                "检测到新截图",
                "交给拾刻",
                "确认并安排",
            ]),
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
            "import_flow_renders_one_stage_at_a_time",
            "val importStage = if (importFlowCompleted)" in main_routes
            and "importFlowStageFor(analysisUiState, selected.status, isConfirmed)" in main_routes
            and "when (importStage)" in main_routes
            and "ImportRouteStage.Entry ->" in main_routes
            and "ImportRouteStage.Analyzing ->" in main_routes
            and "ImportRouteStage.Reviewing ->" in main_routes
            and "ImportRouteStage.Planning ->" in main_routes
            and "ImportRouteStage.Completed ->" in main_routes
        ),
        (
            "import_entry_is_lightweight_not_flow_panel",
            "识别原文默认折叠" in capture_entry
            and "KeyValue(\"解析状态\"" not in capture_entry
            and "BackendAnalysisControls(" not in capture_entry,
        ),
        (
            "analyze_progress_has_product_steps",
            all(word in progress_panel for word in ["读截图", "找时间地点", "生成行动卡", "等你确认"])
            and '"待确认" in selectedStatus' not in progress_panel
            and '"解析中" in modelStatus || "正在解析" in modelStatus' not in progress_panel
            and "analysisUiState is AnalysisUiState.Analyzing" in progress_panel
            and "ImportFlowState.Analyzing" in home_screen,
        ),
        (
            "structured_card_is_result_card_not_key_value_table",
            "ActionCardHero(" in structured_card
            and "PreparationSection(" in structured_card
            and "SuggestedPlanSection(" in structured_card
            and "ConfirmationSection(" in structured_card
            and "ConfirmActionSection(" in structured_card
            and "KeyValue(" not in structured_card,
        ),
        (
            "confirm_page_has_single_primary_action",
            "OutlinedTextField(" not in parse_confirm
            and "ReviewEditSheet(" in parse_confirm
            and "确认并安排" in structured_card
            and "修改" in structured_card,
        ),
        (
            "action_plan_keeps_cleanup_after_confirmation",
            "ScreenshotCleanupPrompt(" in action_planner
            and "isConfirmed && selectedSourceMediaStoreUri != null" in action_planner,
        ),
        (
            "action_plan_has_product_next_steps",
            "下一步，先完成这 2 件" in action_planner
            and "保存日历草稿" in action_planner
            and "先存入待确认" in action_planner
            and "执行上方动作后查看回执" not in action_planner
            and "ExecutionResultPanel" not in action_planner
            and "完成安排" not in execution_controls,
        ),
        (
            "bottom_padding_protects_nav_overlap",
            "bottomBarHeightWithSafeSpace = 148.dp" in main_screen
            and ".statusBarsPadding()" in main_screen
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
