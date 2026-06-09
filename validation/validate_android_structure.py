#!/usr/bin/env python3
"""Validate Android source structure after repeated MVP extractions."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "android-mvp/app/src/main/java/cn/shike/app"


def read(relative: str) -> str:
    """Read a Kotlin source file.

    Args:
        relative: File path under the Android app package.

    Returns:
        File content.
    """

    return (SOURCE_ROOT / relative).read_text(encoding="utf-8")


def line_count(relative: str) -> int:
    """Count source lines in a Kotlin file.

    Args:
        relative: File path under the Android app package.

    Returns:
        Number of lines in the file.
    """

    return len(read(relative).splitlines())


def main() -> int:
    required_files = [
        "MainActivity.kt",
        "ShikeApp.kt",
        "CaptureLaunchers.kt",
        "CaptureResultActions.kt",
        "BackendAnalysisActions.kt",
        "BackendOutcomeActions.kt",
        "BackendEndpointActions.kt",
        "BackendTriggerActions.kt",
        "SampleActions.kt",
        "ReviewActions.kt",
        "data/InboxDatabase.kt",
        "data/InboxEntities.kt",
        "data/InboxSeedFactory.kt",
        "data/LegacyInboxSnapshot.kt",
        "ui/ActionPlannerExecutionControls.kt",
        "ui/AgendaCard.kt",
        "ui/AgendaCardFooter.kt",
        "ui/AgendaCardHeader.kt",
        "ui/BackendAnalysisControls.kt",
        "ui/BackendEndpointControls.kt",
        "ui/BottomNavItem.kt",
        "ui/CapturedImagePreview.kt",
        "ui/CaptureEntryPanel.kt",
        "ui/ConfirmBannerActions.kt",
        "ui/DashboardHeader.kt",
        "ui/DashboardNotificationBadge.kt",
        "ui/DateStrip.kt",
        "ui/DebugDemoScreen.kt",
        "ui/DemoRouteStep.kt",
        "ui/FrontendStateComponents.kt",
        "ui/ActionCardUiModel.kt",
        "ui/AnalyzeProgressPanel.kt",
        "ui/HomeActionScreen.kt",
        "ui/HomeAgendaList.kt",
        "ui/HomePendingReviewPanel.kt",
        "ui/ImportCaptureActions.kt",
        "ui/MainScreenRoutes.kt",
        "ui/OfflineSampleActions.kt",
        "ui/OcrDraftEditor.kt",
        "ui/MainFlowScreens.kt",
        "ui/ParseConfirmHeader.kt",
        "ui/ReviewDecisionActions.kt",
        "ui/ReviewRiskChecklist.kt",
        "ui/StructuredActionCard.kt",
        "ui/ShikeMainScreen.kt",
        "ui/ShikeDesignTokens.kt",
        "ui/SystemStatusRow.kt",
    ]
    kotlin_files = sorted(path for path in SOURCE_ROOT.rglob("*.kt") if path.is_file())
    app_source = "\n".join(path.read_text(encoding="utf-8") for path in kotlin_files)

    checks = [
        ("source_root_exists", SOURCE_ROOT.is_dir()),
        ("required_files_present", all((SOURCE_ROOT / path).is_file() for path in required_files)),
        ("main_activity_shell_under_150_lines", line_count("MainActivity.kt") <= 150),
        ("shike_app_coordinator_under_160_lines", line_count("ShikeApp.kt") <= 160),
        ("shike_main_screen_under_160_lines", line_count("ui/ShikeMainScreen.kt") <= 160),
        (
            "action_helpers_under_80_lines",
            all(line_count(path) <= 80 for path in required_files if path.endswith("Actions.kt")),
        ),
        (
            "core_callbacks_still_named",
            all(
                token in app_source
                for token in [
                    "updateReviewedItem",
                    "applyBackendOutcome",
                    "analyzeCourseWithBackend",
                    "analyzeEventWithBackend",
                    "saveBackendEndpoint",
                ]
            ),
        ),
        (
            "activity_result_boundary_extracted",
            "rememberCaptureLaunchers" in app_source
            and "ActivityResultContracts.TakePicturePreview" in app_source
            and ("ActivityResultContracts.GetContent" in app_source or "ActivityResultContracts.PickVisualMedia" in app_source),
        ),
        (
            "backend_action_boundaries_extracted",
            all(
                token in app_source
                for token in [
                    "runBackendAnalysisAction",
                    "applyBackendOutcomeSelection",
                    "saveBackendEndpointAction",
                    "analyzeCourseWithBackendAction",
                    "analyzeEventWithBackendAction",
                ]
            ),
        ),
        (
            "agenda_card_boundary_extracted",
            "fun AgendaCard" in read("ui/AgendaCard.kt") and "fun AgendaCard" not in read("ui/HomeOverview.kt"),
        ),
        (
            "agenda_card_footer_boundary_extracted",
            "fun AgendaCardFooter" in read("ui/AgendaCardFooter.kt")
            and "TextButton" in read("ui/AgendaCardFooter.kt")
            and "TextButton" not in read("ui/AgendaCard.kt"),
        ),
        (
            "agenda_card_header_boundary_extracted",
            "fun AgendaCardHeader" in read("ui/AgendaCardHeader.kt")
            and "detailLines.forEach" in read("ui/AgendaCardHeader.kt")
            and "detailLines.forEach" not in read("ui/AgendaCard.kt"),
        ),
        (
            "review_risk_checklist_boundary_extracted",
            "fun RiskChecklistPanel" in read("ui/ReviewRiskChecklist.kt")
            and "fun RiskChecklistPanel" not in read("ui/ParseConfirmPanel.kt"),
        ),
        (
            "review_decision_actions_boundary_extracted",
            "fun ReviewDecisionActions" in read("ui/ReviewDecisionActions.kt")
            and "fun ReviewDecisionActions" not in read("ui/ParseConfirmPanel.kt"),
        ),
        (
            "backend_analysis_controls_boundary_extracted",
            "fun BackendAnalysisControls" in read("ui/BackendAnalysisControls.kt")
            and "fun BackendAnalysisControls" not in read("ui/ImportPanel.kt"),
        ),
        (
            "backend_endpoint_controls_boundary_extracted",
            "fun BackendEndpointControls" in read("ui/BackendEndpointControls.kt")
            and "fun BackendEndpointControls" not in read("ui/ImportPanel.kt"),
        ),
        (
            "import_capture_actions_boundary_extracted",
            "fun ImportCaptureActions" in read("ui/ImportCaptureActions.kt")
            and "fun ImportCaptureActions" not in read("ui/ImportPanel.kt"),
        ),
        (
            "offline_sample_actions_boundary_extracted",
            "fun OfflineSampleActions" in read("ui/OfflineSampleActions.kt")
            and "fun OfflineSampleActions" not in read("ui/ImportPanel.kt"),
        ),
        (
            "ocr_draft_editor_boundary_extracted",
            "fun OcrDraftEditor" in read("ui/OcrDraftEditor.kt")
            and "fun OcrDraftEditor" not in read("ui/ImportPanel.kt"),
        ),
        (
            "captured_image_preview_boundary_extracted",
            "fun CapturedImagePreview" in read("ui/CapturedImagePreview.kt")
            and "contentDescription = \"拍照预览\"" in read("ui/CapturedImagePreview.kt")
            and "contentDescription = \"拍照预览\"" not in read("ui/ImportPanel.kt"),
        ),
        (
            "dashboard_header_boundary_extracted",
            "fun DashboardHeader" in read("ui/DashboardHeader.kt")
            and "fun DashboardHeader" not in read("ui/HomeOverview.kt"),
        ),
        (
            "dashboard_notification_badge_boundary_extracted",
            "fun DashboardNotificationBadge" in read("ui/DashboardNotificationBadge.kt")
            and "铃" in read("ui/DashboardNotificationBadge.kt")
            and "铃" not in read("ui/DashboardHeader.kt"),
        ),
        (
            "system_status_row_boundary_extracted",
            "fun SystemStatusRow" in read("ui/SystemStatusRow.kt")
            and "fun SystemStatusRow" not in read("ui/HomeOverview.kt"),
        ),
        (
            "date_strip_boundary_extracted",
            "fun DateStrip" in read("ui/DateStrip.kt")
            and "fun DateStrip" not in read("ui/HomeOverview.kt"),
        ),
        (
            "home_agenda_list_boundary_extracted",
            "fun HomeAgendaList" in read("ui/HomeAgendaList.kt")
            and "AgendaCard(" in read("ui/HomeAgendaList.kt")
            and "AgendaCard(" not in read("ui/ShikeMainScreen.kt"),
        ),
        (
            "demo_route_step_boundary_extracted",
            "fun DemoRouteStep" in read("ui/DemoRouteStep.kt")
            and "课程截图" not in read("ui/DemoRouteStep.kt")
            and "fun DemoRouteStep" not in read("ui/SummarySections.kt"),
        ),
        (
            "bottom_nav_item_boundary_extracted",
            "fun BottomNavItem" in read("ui/BottomNavItem.kt")
            and "首页" not in read("ui/BottomNavItem.kt")
            and "fun BottomNavItem" not in read("ui/BottomNavigation.kt"),
        ),
        (
            "confirm_banner_actions_boundary_extracted",
            "fun ConfirmBannerActions" in read("ui/ConfirmBannerActions.kt")
            and "executionActionButtonLabelsFor" in read("ui/ConfirmBannerActions.kt")
            and "打开日历" not in read("ui/ConfirmBanner.kt"),
        ),
        (
            "parse_confirm_header_boundary_extracted",
            "fun ParseConfirmHeader" in read("ui/ParseConfirmHeader.kt")
            and "可编辑" in read("ui/ParseConfirmHeader.kt")
            and "可编辑" not in read("ui/ParseConfirmPanel.kt"),
        ),
        (
            "action_planner_execution_controls_boundary_extracted",
            "fun ActionPlannerExecutionControls" in read("ui/ActionPlannerExecutionControls.kt")
            and "executionActionButtonLabelsFor" in read("ui/ActionPlannerExecutionControls.kt")
            and "打开日历" not in read("ui/ActionPlannerPanel.kt"),
        ),
        (
            "no_large_kotlin_file_over_220_lines",
            all(len(path.read_text(encoding="utf-8").splitlines()) <= 220 for path in kotlin_files),
        ),
    ]

    passed = sum(1 for _, ok in checks)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"ANDROID_STRUCTURE_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
