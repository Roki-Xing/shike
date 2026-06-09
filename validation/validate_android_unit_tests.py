#!/usr/bin/env python3
"""Validate the Android local unit-test baseline."""

from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    """Read a UTF-8 project file.

    Args:
        relative: File path under the Shike root.

    Returns:
        File content.
    """

    return (ROOT / relative).read_text(encoding="utf-8")


def test_result_passed(relative: str, suite_name: str, expected_tests: int) -> bool:
    """Check the Gradle JUnit XML result from the latest local unit-test run.

    Args:
        relative: Test result XML path under the Shike root.
        suite_name: Expected JUnit test-suite name.
        expected_tests: Number of test cases expected in the suite.

    Returns:
        True when the test suite exists and reports no failures or errors.
    """

    result_path = ROOT / relative
    if not result_path.is_file():
        return False
    suite = ElementTree.parse(result_path).getroot()
    return (
        int(suite.attrib.get("tests", "-1")) == expected_tests
        and int(suite.attrib.get("failures", "-1")) == 0
        and int(suite.attrib.get("errors", "-1")) == 0
        and suite.attrib.get("name") == suite_name
    )


def main() -> int:
    """Run Android unit-test baseline checks.

    Returns:
        Process exit code.
    """

    build_gradle = read("android-mvp/app/build.gradle.kts")
    privacy_source = read("android-mvp/app/src/main/java/cn/shike/app/data/PrivacyRedaction.kt")
    privacy_test = read("android-mvp/app/src/test/java/cn/shike/app/data/PrivacyRedactionTest.kt")
    capture_test = read("android-mvp/app/src/test/java/cn/shike/app/data/CaptureImportMapperTest.kt")
    share_test = read("android-mvp/app/src/test/java/cn/shike/app/data/ShareImportMapperTest.kt")
    ocr_engine_source = read("android-mvp/app/src/main/java/cn/shike/app/data/OcrEngine.kt")
    ocr_engine_test = read("android-mvp/app/src/test/java/cn/shike/app/data/OcrEngineTest.kt")
    initial_selection_source = read("android-mvp/app/src/main/java/cn/shike/app/data/InitialSelectionMapper.kt")
    initial_selection_test = read("android-mvp/app/src/test/java/cn/shike/app/data/InitialSelectionMapperTest.kt")
    review_status_test = read("android-mvp/app/src/test/java/cn/shike/app/data/ReviewStatusMapperTest.kt")
    review_actions_test = read("android-mvp/app/src/test/java/cn/shike/app/ReviewActionsTest.kt")
    capture_result_test = read("android-mvp/app/src/test/java/cn/shike/app/CaptureResultActionsTest.kt")
    model_explanation_test = read("android-mvp/app/src/test/java/cn/shike/app/ModelExplanationTest.kt")
    model_api_client_source = read("android-mvp/app/src/main/java/cn/shike/app/data/ModelApiClient.kt")
    analyze_image_api_client_source = read("android-mvp/app/src/main/java/cn/shike/app/data/BackendImageApiClient.kt")
    model_api_client_test = read("android-mvp/app/src/test/java/cn/shike/app/ModelApiClientTest.kt")
    analyze_image_api_client_test = read("android-mvp/app/src/test/java/cn/shike/app/data/AnalyzeImageApiClientTest.kt")
    today_action_item_test = read("android-mvp/app/src/test/java/cn/shike/app/TodayActionItemMapperTest.kt")
    execution_action_gate_source = read("android-mvp/app/src/main/java/cn/shike/app/ui/ExecutionActionGate.kt")
    execution_action_gate_test = read("android-mvp/app/src/test/java/cn/shike/app/ExecutionActionGateTest.kt")
    inbox_workbench_source = read("android-mvp/app/src/main/java/cn/shike/app/ui/InboxWorkbench.kt")
    inbox_workbench_test = read("android-mvp/app/src/test/java/cn/shike/app/InboxWorkbenchTest.kt")
    reminder_payload_source = read("android-mvp/app/src/main/java/cn/shike/app/system/ReminderPayload.kt")
    reminder_payload_test = read("android-mvp/app/src/test/java/cn/shike/app/ReminderPayloadTest.kt")
    execution_test = read("android-mvp/app/src/test/java/cn/shike/app/ExecutionResultActionsTest.kt")
    execution_state_test = read("android-mvp/app/src/test/java/cn/shike/app/ExecutionResultStateTest.kt")
    date_strip_source = read("android-mvp/app/src/main/java/cn/shike/app/ui/DateStrip.kt")
    date_strip_test = read("android-mvp/app/src/test/java/cn/shike/app/DateStripTest.kt")
    system_actions_source = read("android-mvp/app/src/main/java/cn/shike/app/system/SystemActions.kt")
    system_actions_test = read("android-mvp/app/src/test/java/cn/shike/app/SystemActionsTest.kt")
    screen_capture_prompt_source = read("android-mvp/app/src/main/java/cn/shike/app/system/VisibleScreenCapturePrompt.kt")
    screen_capture_prompt_test = read("android-mvp/app/src/test/java/cn/shike/app/ScreenCapturePromptTest.kt")
    screenshot_cleanup_prompt_source = read("android-mvp/app/src/main/java/cn/shike/app/ui/ScreenshotCleanupPrompt.kt")
    screenshot_cleanup_prompt_test = read("android-mvp/app/src/test/java/cn/shike/app/ScreenshotCleanupPromptTest.kt")
    reminder_permission_fallback_source = read("android-mvp/app/src/main/java/cn/shike/app/ReminderPermissionFallback.kt")
    reminder_permission_fallback_test = read("android-mvp/app/src/test/java/cn/shike/app/ReminderPermissionFallbackTest.kt")
    backend_analysis_runner_source = read("android-mvp/app/src/main/java/cn/shike/app/data/BackendAnalysisRunner.kt")
    backend_analysis_outcome_source = read("android-mvp/app/src/main/java/cn/shike/app/data/BackendAnalysisOutcomes.kt")
    backend_analysis_runner_test = read("android-mvp/app/src/test/java/cn/shike/app/BackendAnalysisRunnerTest.kt")
    backend_endpoint_test = read("android-mvp/app/src/test/java/cn/shike/app/BackendEndpointActionsTest.kt")
    backend_trigger_test = read("android-mvp/app/src/test/java/cn/shike/app/BackendTriggerActionsTest.kt")
    backend_outcome_source = read("android-mvp/app/src/main/java/cn/shike/app/BackendOutcomeActions.kt")
    backend_outcome_test = read("android-mvp/app/src/test/java/cn/shike/app/BackendOutcomeActionsTest.kt")
    sample_actions_test = read("android-mvp/app/src/test/java/cn/shike/app/SampleActionsTest.kt")
    inbox_entities_source = read("android-mvp/app/src/main/java/cn/shike/app/data/InboxEntities.kt")
    inbox_entities_test = read("android-mvp/app/src/test/java/cn/shike/app/data/InboxEntitiesTest.kt")
    local_inbox_store_source = read("android-mvp/app/src/main/java/cn/shike/app/data/LocalInboxStore.kt")
    legacy_inbox_snapshot_source = read("android-mvp/app/src/main/java/cn/shike/app/data/LegacyInboxSnapshot.kt")
    local_inbox_store_test = read("android-mvp/app/src/test/java/cn/shike/app/data/LocalInboxStoreTest.kt")
    readiness_sections = read("android-mvp/app/src/main/java/cn/shike/app/ui/ReadinessSections.kt")
    local_data_clear_source = read("android-mvp/app/src/main/java/cn/shike/app/LocalDataClearActions.kt")
    local_data_clear_test = read("android-mvp/app/src/test/java/cn/shike/app/LocalDataClearActionsTest.kt")
    cloud_enhancement_test = read("android-mvp/app/src/test/java/cn/shike/app/CloudEnhancementActionsTest.kt")
    developer_mode_source = read("android-mvp/app/src/main/java/cn/shike/app/ui/DeveloperModeUnlock.kt")
    developer_mode_test = read("android-mvp/app/src/test/java/cn/shike/app/DeveloperModeUnlockTest.kt")
    local_multimodal_source = read("android-mvp/app/src/main/java/cn/shike/app/ui/LocalMultimodalStatus.kt")
    local_multimodal_test = read("android-mvp/app/src/test/java/cn/shike/app/LocalMultimodalStatusTest.kt")
    local_multimodal_runtime_source = read("android-mvp/app/src/main/java/cn/shike/app/data/LocalMultimodalRuntime.kt")
    local_multimodal_runtime_test = read("android-mvp/app/src/test/java/cn/shike/app/data/LocalMultimodalRuntimeTest.kt")
    image_preprocess_policy_source = read("android-mvp/app/src/main/java/cn/shike/app/data/ImagePreprocessPolicy.kt")
    image_preprocess_policy_test = read("android-mvp/app/src/test/java/cn/shike/app/data/ImagePreprocessPolicyTest.kt")
    image_thumbnail_cache_source = read("android-mvp/app/src/main/java/cn/shike/app/data/ImageThumbnailCache.kt")
    image_thumbnail_cache_test = read("android-mvp/app/src/test/java/cn/shike/app/data/ImageThumbnailCacheTest.kt")
    screenshot_candidate_store_source = read("android-mvp/app/src/main/java/cn/shike/app/data/ScreenshotCandidateStore.kt")
    screenshot_candidate_store_test = read("android-mvp/app/src/test/java/cn/shike/app/data/ScreenshotCandidateStoreTest.kt")
    docs = "\n".join(
        read(path)
        for path in [
            "README.md",
            "materials/device-demo-checklist.md",
            "docs/device-runbook.md",
            "docs/current-validation-status.md",
            "prototype/demo.html",
        ]
    )

    checks = [
        ("junit_dependency_configured", 'testImplementation("junit:junit:4.13.2")' in build_gradle),
        (
            "privacy_redaction_source_is_pure_logic",
            "fun redactSensitiveLogText(text: String): String" in privacy_source
            and "Context" not in privacy_source
            and "android." not in privacy_source,
        ),
        (
            "privacy_redaction_unit_test_exists",
            "class PrivacyRedactionTest" in privacy_test
            and privacy_test.count("@Test") == 2
            and "redactSensitiveLogText_removesPersonalAndLocalNetworkData" in privacy_test
            and "redactSensitiveLogText_keepsNonSensitiveActionTextReadable" in privacy_test,
        ),
        (
            "privacy_redaction_test_asserts_sensitive_tokens",
            all(
                token in privacy_test
                for token in [
                    "[手机号已脱敏]",
                    "[邮箱已脱敏]",
                    "[学号已脱敏]",
                    "[局域网地址已脱敏]",
                    "课程提醒",
                ]
            ),
        ),
        (
            "gradle_unit_test_result_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.data.PrivacyRedactionTest.xml",
                "cn.shike.app.data.PrivacyRedactionTest",
                2,
            ),
        ),
        (
            "capture_import_unit_test_exists",
            "class CaptureImportMapperTest" in capture_test
            and capture_test.count("@Test") == 8
            and "cameraSelectionFromPreview_startsPendingImageDraftWithoutEventSample" in capture_test
            and "gallerySelectionFromImage_startsPendingImageDraftWithoutCourseSample" in capture_test
            and "screenshotSelectionFromCandidate_keepsAssistantDraftPendingAndSampleFree" in capture_test
            and "selectionFromCaptureDraft_routesOnlyImageDraftsToPendingImageCards" in capture_test
            and "captureDraftFromInput_preservesOriginalAndThumbnailUrisSeparately" in capture_test
            and "captureDraftFromInput_keepsCameraThumbnailOutOfOriginalMediaUri" in capture_test
            and "captureDraftDeleteState_tracksSystemConfirmationStates" in capture_test
            and "backendSourceTypeFromCaptureSource_mapsAllProductEntrypoints" in capture_test,
        ),
        (
            "capture_draft_thumbnail_contract_unit_tested",
            "val thumbnailUri: String? = null" in ocr_engine_source
            and "val thumbnailUri: String? = null" in read("android-mvp/app/src/main/java/cn/shike/app/data/CaptureImportMapper.kt")
            and "thumbnailUri = input.thumbnailUri" in read("android-mvp/app/src/main/java/cn/shike/app/data/CaptureImportMapper.kt")
            and "file:/private-cache/shike-image-thumbnails/thumb-42.jpg" in capture_test
            and "assertEquals(\"content://media/external/images/media/42\", draft.sourceMediaStoreUri)" in capture_test
            and "assertEquals(null, draft.sourceMediaStoreUri)" in capture_test,
        ),
        (
            "capture_draft_delete_state_contract_unit_tested",
            "enum class ScreenshotDeleteState" in read("android-mvp/app/src/main/java/cn/shike/app/data/CaptureImportMapper.kt")
            and "val canDeleteOriginal: Boolean" in read("android-mvp/app/src/main/java/cn/shike/app/data/CaptureImportMapper.kt")
            and "val deleteState: ScreenshotDeleteState" in read("android-mvp/app/src/main/java/cn/shike/app/data/CaptureImportMapper.kt")
            and "ScreenshotDeleteState.NotAvailable" in read("android-mvp/app/src/main/java/cn/shike/app/data/CaptureImportMapper.kt")
            and "ScreenshotDeleteState.RequestingSystemConfirmation" in read("android-mvp/app/src/main/java/cn/shike/app/data/CaptureImportMapper.kt")
            and "ScreenshotDeleteState.Deleted" in read("android-mvp/app/src/main/java/cn/shike/app/data/CaptureImportMapper.kt")
            and "captureDraftDeleteState_tracksSystemConfirmationStates" in capture_test
            and "assertEquals(true, draft.canDeleteOriginal)" in capture_test
            and "assertEquals(false, draft.canDeleteOriginal)" in capture_test
            and "ImageCleanupStatus.DELETE_REQUESTED" in capture_test
            and "ImageCleanupStatus.DELETED" in capture_test
            and "ImageCleanupStatus.FAILED" in capture_test,
        ),
        (
            "share_import_unit_test_exists",
            "class ShareImportMapperTest" in share_test
            and share_test.count("@Test") == 4
            and "sharedTextCaptureDraft_keepsShareChannelAndRawText" in share_test
            and "itemFromSharedText_activityTextMapsToEventReviewCard" in share_test
            and "itemFromSharedText_courseTextMapsToCourseReviewCard" in share_test,
        ),
        (
            "import_mapping_test_asserts_core_channels",
            all(
                token in capture_test + share_test
                for token in [
                    "相机拍照预览",
                    "相册图片",
                    "截图助手导入",
                    "系统分享文本",
                    "分享导入的活动",
                    "分享导入的课程通知",
                ]
            ),
        ),
        (
            "gradle_import_test_results_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.data.CaptureImportMapperTest.xml",
                "cn.shike.app.data.CaptureImportMapperTest",
                8,
            )
            and test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.data.ShareImportMapperTest.xml",
                "cn.shike.app.data.ShareImportMapperTest",
                4,
            ),
        ),
        (
            "ocr_engine_unit_test_exists",
            "interface OcrEngine" in ocr_engine_source
            and "class ManualOcrEngine" in ocr_engine_source
            and "class MockOcrEngine" in ocr_engine_source
            and "data class OcrResult" in ocr_engine_source
            and "class OcrEngineTest" in ocr_engine_test
            and ocr_engine_test.count("@Test") == 3
            and "manualOcrEngine_keepsUserTextAndReportsBlankFailure" in ocr_engine_test
            and "mockOcrEngine_keepsImageImportsNeutralUntilBackendAnalysis" in ocr_engine_test
            and "captureDraftFromInput_recordsOcrMetadataAndPrivacyChoice" in ocr_engine_test
            and "未识别到稳定文字" in ocr_engine_source,
        ),
        (
            "gradle_ocr_engine_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.data.OcrEngineTest.xml",
                "cn.shike.app.data.OcrEngineTest",
                3,
            ),
        ),
        (
            "initial_selection_unit_test_exists",
            "fun buildInitialSelection(" in initial_selection_source
            and "fun buildRuntimeSharedTextSelection(" in initial_selection_source
            and "class InitialSelectionMapperTest" in initial_selection_test
            and initial_selection_test.count("@Test") == 5
            and "buildInitialSelection_sharedTextWinsOverSavedSnapshot" in initial_selection_test
            and "buildRuntimeSharedTextSelection_mapsNewIntentTextToReadyDraft" in initial_selection_test
            and "buildRuntimeSharedTextSelection_ignoresBlankText" in initial_selection_test
            and "buildInitialSelection_savedSnapshotRestoresReadyState" in initial_selection_test
            and "buildInitialSelection_noShareNoSavedShowsEmptyState" in initial_selection_test
            and "文本分享入口（待确认，未落盘）" in initial_selection_test
            and "今日行动台空状态" in initial_selection_test,
        ),
        (
            "gradle_initial_selection_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.data.InitialSelectionMapperTest.xml",
                "cn.shike.app.data.InitialSelectionMapperTest",
                5,
            ),
        ),
        (
            "execution_result_unit_test_exists",
            "class ExecutionResultActionsTest" in execution_test
            and execution_test.count("@Test") == 3
            and "runCalendarExecution_recordsResultBeforeSystemAction" in execution_test
            and "runReminderExecution_recordsPermissionAwareReminderResult" in execution_test
            and "runMapExecution_preservesExistingCalendarResult" in execution_test
            and "permission_blocked" in execution_test,
        ),
        (
            "gradle_execution_result_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.ExecutionResultActionsTest.xml",
                "cn.shike.app.ExecutionResultActionsTest",
                3,
            ),
        ),
        (
            "execution_result_state_unit_test_exists",
            "class ExecutionResultStateTest" in execution_state_test
            and execution_state_test.count("@Test") == 4
            and "pendingExecutionResults_startsAllActionsInConfirmationState" in execution_state_test
            and "recordExecutionResult_replacesOnlyMatchingActionAndAppendsLatestResult" in execution_state_test
            and "executionResultFactories_keepPermissionAndFallbackWording" in execution_state_test
            and "imageCleanupResults_distinguishSystemConfirmationStates" in execution_state_test
            and "permission_blocked" in execution_state_test
            and "地图不可用" in execution_state_test,
        ),
        (
            "gradle_execution_result_state_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.ExecutionResultStateTest.xml",
                "cn.shike.app.ExecutionResultStateTest",
                4,
            ),
        ),
        (
            "date_strip_date_boundary_unit_tested",
            "fun formatTodayForHome(date: LocalDate): String" in date_strip_source
            and "fun dateStripSubtitle(): String" in date_strip_source
            and "系统日期仅用于排序提示，不作为任务时间" in date_strip_source
            and "农历" not in date_strip_source
            and "5月24日" not in date_strip_source
            and "class DateStripTest" in date_strip_test
            and date_strip_test.count("@Test") == 2
            and "formatTodayForHome_usesInjectedSystemDateWithoutLunarOrFixedDemoDate" in date_strip_test
            and "dateStripSubtitle_statesDateIsSortingHintNotTaskTime" in date_strip_test
            and test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.DateStripTest.xml",
                "cn.shike.app.DateStripTest",
                2,
            ),
        ),
        (
            "calendar_system_action_copy_unit_tested",
            "fun calendarInsertDescriptionFor(item: ShikeItem): String" in system_actions_source
            and "calendarInsertDescriptionFor(item)" in system_actions_source
            and "确认后写入" not in system_actions_source
            and "打开系统日历新增页" in system_actions_source
            and "由用户在日历中保存" in system_actions_source
            and "class SystemActionsTest" in system_actions_test
            and system_actions_test.count("@Test") == 1
            and "calendarInsertDescriptionFor_onlyDescribesSystemInsertPage" in system_actions_test
            and 'assertFalse(description.contains("确认后写入"))' in system_actions_test
            and test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.SystemActionsTest.xml",
                "cn.shike.app.SystemActionsTest",
                1,
            ),
        ),
        (
            "visible_screen_capture_prompt_copy_unit_tested",
            "data class VisibleScreenCapturePrompt" in screen_capture_prompt_source
            and "fun visibleScreenCapturePrompt(): VisibleScreenCapturePrompt" in screen_capture_prompt_source
            and "不会直接获得图片" in screen_capture_prompt_source
            and "导入页选择这张截图" in screen_capture_prompt_source
            and "移入回收站" in screen_capture_prompt_source
            and "后台监听" not in screen_capture_prompt_source
            and "全局监听" not in screen_capture_prompt_source
            and "自动读取" not in screen_capture_prompt_source
            and "class ScreenCapturePromptTest" in screen_capture_prompt_test
            and screen_capture_prompt_test.count("@Test") == 1
            and "visibleScreenCapturePrompt_keepsAndroidCallbackBoundaryHonest" in screen_capture_prompt_test
            and test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.ScreenCapturePromptTest.xml",
                "cn.shike.app.ScreenCapturePromptTest",
                1,
            ),
        ),
        (
            "screenshot_cleanup_prompt_copy_unit_tested",
            "fun cleanupStatusLabel(status: ImageCleanupStatus): String" in screenshot_cleanup_prompt_source
            and "status.name" not in screenshot_cleanup_prompt_source
            and all(
                token in screenshot_cleanup_prompt_source
                for token in [
                    "当前来源不支持直接移入回收站",
                    "等待你的选择",
                    "已选择保留原图",
                    "正在等待系统确认",
                    "已移入系统回收站",
                    "系统确认未完成",
                ]
            )
            and "class ScreenshotCleanupPromptTest" in screenshot_cleanup_prompt_test
            and screenshot_cleanup_prompt_test.count("@Test") == 1
            and "cleanupStatusLabel_usesUserFacingChineseCopy" in screenshot_cleanup_prompt_test
            and 'assertFalse(labels.any { it.contains("_") })' in screenshot_cleanup_prompt_test
            and test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.ScreenshotCleanupPromptTest.xml",
                "cn.shike.app.ScreenshotCleanupPromptTest",
                1,
            ),
        ),
        (
            "reminder_permission_fallback_unit_test_exists",
            "fun reminderPermissionFallbackCopyFor(" in reminder_permission_fallback_source
            and "data class ReminderPermissionFallbackCopy" in reminder_permission_fallback_source
            and "REMINDER_PERMISSION_BLOCKED_STATUS" in reminder_permission_fallback_source
            and "class ReminderPermissionFallbackTest" in reminder_permission_fallback_test
            and reminder_permission_fallback_test.count("@Test") == 2
            and "reminderPermissionFallbackCopyFor_namesPermissionBlockedAndKeepsCard" in reminder_permission_fallback_test
            and "reminderExecutionResult_usesSharedPermissionFallbackCopy" in reminder_permission_fallback_test
            and "已保留「AI应用分享会」行动卡" in reminder_permission_fallback_test,
        ),
        (
            "gradle_reminder_permission_fallback_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.ReminderPermissionFallbackTest.xml",
                "cn.shike.app.ReminderPermissionFallbackTest",
                2,
            ),
        ),
        (
            "review_status_unit_test_exists",
            "class ReviewStatusMapperTest" in review_status_test
            and review_status_test.count("@Test") == 3
            and "mapReviewedItemState_confirmedItemBecomesScheduled" in review_status_test
            and "mapReviewedItemState_ignoredItemStaysIgnored" in review_status_test
            and "mapReviewedItemState_preservesReviewedFields" in review_status_test
            and "模型编排：用户已确认" in review_status_test
            and "模型编排：用户已忽略" in review_status_test,
        ),
        (
            "gradle_review_status_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.data.ReviewStatusMapperTest.xml",
                "cn.shike.app.data.ReviewStatusMapperTest",
                3,
            ),
        ),
        (
            "review_actions_unit_test_exists",
            "class ReviewActionsTest" in review_actions_test
            and review_actions_test.count("@Test") == 2
            and "applyReviewedItemSelection_persistsConfirmedItemAndSource" in review_actions_test
            and "applyReviewedItemSelection_persistsIgnoredItemAndSource" in review_actions_test
            and "用户确认修正：活动海报" in review_actions_test
            and "用户确认修正：课程通知" in review_actions_test,
        ),
        (
            "gradle_review_actions_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.ReviewActionsTest.xml",
                "cn.shike.app.ReviewActionsTest",
                2,
            ),
        ),
        (
            "capture_result_actions_unit_test_exists",
            "class CaptureResultActionsTest" in capture_result_test
            and capture_result_test.count("@Test") == 3
            and "applyCameraPreviewSizeSelection_persistsCameraDraftAndSource" in capture_result_test
            and "applyGalleryImageSelection_persistsPendingImageDraftWithoutSampleFields" in capture_result_test
            and "applyScreenshotCandidateSelection_persistsPendingDraftWithoutSampleFields" in capture_result_test
            and "相机拍照预览 1080x1440" in capture_result_test
            and "相册图片 course-screenshot.png" in capture_result_test,
        ),
        (
            "gradle_capture_result_actions_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.CaptureResultActionsTest.xml",
                "cn.shike.app.CaptureResultActionsTest",
                3,
            ),
        ),
        (
            "model_explanation_unit_test_exists",
            "class ModelExplanationTest" in model_explanation_test
            and model_explanation_test.count("@Test") == 3
            and "modelExplanation_usesBackendExplanationWhenPresent" in model_explanation_test
            and "modelExplanation_explainsBackendFallbackBeforeLocalConfirmation" in model_explanation_test
            and "modelExplanation_marksConfirmedCourseFieldsAsTrusted" in model_explanation_test
            and "本地规则保留行动卡" in model_explanation_test
            and "关键字段已确认" in model_explanation_test,
        ),
        (
            "gradle_model_explanation_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.ModelExplanationTest.xml",
                "cn.shike.app.ModelExplanationTest",
                3,
            ),
        ),
        (
            "model_api_client_unit_test_exists",
            'testImplementation("org.json:json:20240303")' in build_gradle
            and "fun buildAnalyzeRequestPayload(" in model_api_client_source
            and 'put("source_type", sourceType)' in model_api_client_source
            and 'put("ocr_text", ocrText)' in model_api_client_source
            and 'put("scene_hint", sceneHint(scene))' in model_api_client_source
            and "assignment_deadline" in model_api_client_source
            and "meeting_notice" in model_api_client_source
            and "interview_notice" in model_api_client_source
            and "travel_ticket" in model_api_client_source
            and "class ModelApiClientTest" in model_api_client_test
            and model_api_client_test.count("@Test") == 8
            and "buildAnalyzeRequestPayload_keepsBackendContractFields" in model_api_client_test
            and "buildAnalyzeRequestPayload_acceptsShareTextAndManualSourceTypes" in model_api_client_test
            and "buildAnalyzeRequestPayload_mapsExtendedSceneHints" in model_api_client_test
            and "itemFromAnalyzeJson_courseNoticeCombinesTimeLocationAndActions" in model_api_client_test
            and "itemFromAnalyzeJson_eventPosterUsesFallbacksForBlankFields" in model_api_client_test
            and "itemFromAnalyzeJson_unknownSceneFallsBackToPendingLabel" in model_api_client_test
            and "actionsFromJson_ignoresBlankAndMalformedActions" in model_api_client_test
            and "normalizeBackendUrl_stripsPathQueryAndFragment" in model_api_client_test
            and "android-demo-test" in model_api_client_test
            and "Asia/Shanghai" in model_api_client_test
            and "云端 AI 解析：OCR 原文兜底" in model_api_client_test
            and "稍后确认" in model_api_client_test,
        ),
        (
            "backend_url_normalization_strips_path_query_fragment",
            "fun normalizeBackendUrl(url: String): String" in model_api_client_source
            and "URI(" in model_api_client_source
            and "uri?.host" in model_api_client_source
            and "normalizeBackendUrl_stripsPathQueryAndFragment" in model_api_client_test
            and "192.168.1.10:8000/v1/analyze" in model_api_client_test
            and "http://192.168.1.10:8000/v1/analyze?x=1#frag" in model_api_client_test
            and "https://example.test:8443/api/v1/analyze/" in model_api_client_test,
        ),
        (
            "model_api_request_payload_contract_tested",
            "buildAnalyzeRequestPayload_keepsBackendContractFields" in model_api_client_test
            and all(
                token in model_api_client_test
                for token in [
                    'getString("input_id")',
                    'getString("source_type")',
                    'getString("ocr_text")',
                    'getString("scene_hint")',
                    'getString("locale")',
                    'getString("user_timezone")',
                    "course_notice",
                    "event_poster",
                    "assignment_deadline",
                    "meeting_notice",
                    "interview_notice",
                    "travel_ticket",
                    "share_text",
                    "manual",
                    "zh-CN",
                    "Asia/Shanghai",
                ]
            ),
        ),
        (
            "source_type_contract_covers_share_text_and_manual",
            "fun backendSourceTypeFromCaptureSource" in read("android-mvp/app/src/main/java/cn/shike/app/data/CaptureImportMapper.kt")
            and "backendSourceTypeFromCaptureSource_mapsAllProductEntrypoints" in capture_test
            and "backendAnalysisInputForCurrentDraft_usesCaptureSourceSpecificBackendType" in backend_analysis_runner_test
            and "buildAnalyzeRequestPayload_acceptsShareTextAndManualSourceTypes" in model_api_client_test
            and "share_text" in model_api_client_test
            and "manual" in model_api_client_test,
        ),
        (
            "gradle_model_api_client_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.ModelApiClientTest.xml",
                "cn.shike.app.ModelApiClientTest",
                8,
            ),
        ),
        (
            "analyze_image_api_client_unit_test_exists",
            "fun buildAnalyzeImageRequestPayload(" in analyze_image_api_client_source
            and "allowCloudImage: Boolean = true" in analyze_image_api_client_source
            and ".put(\"allow_cloud_image\", allowCloudImage)" in analyze_image_api_client_source
            and "class AnalyzeImageApiClientTest" in analyze_image_api_client_test
            and analyze_image_api_client_test.count("@Test") == 5
            and "buildAnalyzeImageRequestPayload_includesImageOcrHintAndUserContext" in analyze_image_api_client_test
            and "buildAnalyzeImageRequestPayload_canDisableCloudImageUpload" in analyze_image_api_client_test
            and "backendAnalysisInputForCurrentDraft_keepsImageUriForV2Route" in analyze_image_api_client_test
            and "backendAnalysisPathFor_textOnlyDraftStaysOnV1" in analyze_image_api_client_test
            and "itemFromAnalyzeImageJson_omitsJsonNullDeadlineAndKeepsStructuredFields" in analyze_image_api_client_test
            and "assertFalse(item.time.contains(\"null\"))" in analyze_image_api_client_test
            and "任务：上英语口语" in analyze_image_api_client_test
            and "allowCloudImage = false" in analyze_image_api_client_test
            and "assertFalse(payload.getBoolean(\"allow_cloud_image\"))" in analyze_image_api_client_test
            and test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.data.AnalyzeImageApiClientTest.xml",
                "cn.shike.app.data.AnalyzeImageApiClientTest",
                5,
            ),
        ),
        (
            "today_action_item_mapper_unit_test_exists",
            "class TodayActionItemMapperTest" in today_action_item_test
            and today_action_item_test.count("@Test") == 3
            and "todayActionItemFrom_scheduledItemUsesRouteActionAndConfirmedFooter" in today_action_item_test
            and "todayActionItemFrom_dueSoonItemKeepsDeadlineActionAndReviewFooter" in today_action_item_test
            and "todayActionItemFrom_pendingItemFallsBackToPrimaryActionOrDetail" in today_action_item_test
            and "查看路线" in today_action_item_test
            and "查看详情" in today_action_item_test,
        ),
        (
            "gradle_today_action_item_mapper_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.TodayActionItemMapperTest.xml",
                "cn.shike.app.TodayActionItemMapperTest",
                3,
            ),
        ),
        (
            "execution_action_gate_unit_test_exists",
            "fun executionActionGateFor(" in execution_action_gate_source
            and "canUseCalendar = isConfirmed && !missingTime" in execution_action_gate_source
            and "canUseReminder = isConfirmed && !missingTime" in execution_action_gate_source
            and "canUseMap = isConfirmed && !missingLocation" in execution_action_gate_source
            and "class ExecutionActionGateTest" in execution_action_gate_test
            and execution_action_gate_test.count("@Test") == 7
            and "executionActionGateFor_unconfirmedItemBlocksAllSensitiveActions" in execution_action_gate_test
            and "executionActionGateFor_confirmedItemAllowsCompleteFields" in execution_action_gate_test
            and "executionActionGateFor_missingFieldsBlockCalendarReminderAndMap" in execution_action_gate_test
            and "assertFalse(gate.canUseCalendar)" in execution_action_gate_test,
        ),
        (
            "execution_action_button_label_unit_test_exists",
            "data class ExecutionActionButtonLabels" in execution_action_gate_source
            and "fun executionActionButtonLabelsFor(" in execution_action_gate_source
            and "打开日历" in execution_action_gate_source
            and "设置提醒" in execution_action_gate_source
            and "查看路线" in execution_action_gate_source
            and "补充时间后可用" in execution_action_gate_source
            and "补充地点后可用" in execution_action_gate_source
            and "去开启通知" in execution_action_gate_source
            and "executionResults.hasReminderPermissionBlocked()" in execution_action_gate_source
            and "executionActionButtonLabelsFor_usesGuideActionCopyAfterConfirmation" in execution_action_gate_test
            and "executionActionButtonLabelsFor_namesMissingFieldRecovery" in execution_action_gate_test
            and "executionActionButtonLabelsFor_blocksUnconfirmedActionsWithReviewCopy" in execution_action_gate_test,
        ),
        (
            "execution_action_notification_recovery_label_unit_tested",
            "REMINDER_PERMISSION_BLOCKED_STATUS" in execution_action_gate_source
            and "hasReminderPermissionBlocked" in execution_action_gate_source
            and "executionActionButtonLabelsFor_namesNotificationRecoveryAfterPermissionBlocked" in execution_action_gate_test
            and "assertEquals(\"去开启通知\", labels.reminder)" in execution_action_gate_test
            and "permission_blocked" in execution_action_gate_test,
        ),
        (
            "gradle_execution_action_gate_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.ExecutionActionGateTest.xml",
                "cn.shike.app.ExecutionActionGateTest",
                7,
            ),
        ),
        (
            "inbox_workbench_unit_test_exists",
            "fun selectedInboxStatusFor(" in inbox_workbench_source
            and "fun visibleInboxEntries(" in inbox_workbench_source
            and "fun inboxWorkbenchEntryFrom(" in inbox_workbench_source
            and "fun inboxStatusPriority(" in inbox_workbench_source
            and "const val inboxAllStatusFilter = \"全部\"" in inbox_workbench_source
            and "fun inboxArchiveActionStateFor(" in inbox_workbench_source
            and "data class InboxArchiveActionState" in inbox_workbench_source
            and "class InboxWorkbenchTest" in inbox_workbench_test
            and inbox_workbench_test.count("@Test") == 5
            and "selectedInboxStatusFor_unsupportedStatusFallsBackToPendingReview" in inbox_workbench_test
            and "inboxWorkbenchEntryFrom_searchesRawTextExplanationAndExecutionSummary" in inbox_workbench_test
            and "visibleInboxEntries_respectsArchiveStatusAndSearchQuery" in inbox_workbench_test
            and "visibleInboxEntries_allStatusPrioritizesUrgentReviewAndScheduleOrder" in inbox_workbench_test
            and "inboxArchiveActionStateFor_separatesArchiveAndRestoreDecisions" in inbox_workbench_test
            and "archivedKeys = setOf(current.archiveKey)" in inbox_workbench_test,
        ),
        (
            "inbox_all_status_sorting_unit_tested",
            "selectedStatus == inboxAllStatusFilter || entry.status == selectedStatus" in inbox_workbench_source
            and "compareBy<InboxWorkbenchEntry> { inboxStatusPriority(it.status) }" in inbox_workbench_source
            and "\"即将截止\" -> 0" in inbox_workbench_source
            and "\"待确认\" -> 1" in inbox_workbench_source
            and "\"已安排\" -> 2" in inbox_workbench_source
            and "thenBy { it.startEpochMillis }" in inbox_workbench_source
            and "assertEquals(listOf(due, pending, scheduledEarly, scheduledLate), visible)" in inbox_workbench_test
            and "selectedStatus = inboxAllStatusFilter" in inbox_workbench_test,
        ),
        (
            "inbox_archive_action_state_unit_tested",
            "InboxArchiveActionState" in inbox_workbench_source
            and "archiveEnabled = false" in inbox_workbench_source
            and "restoreEnabled = true" in inbox_workbench_source
            and "已归档但未删除，恢复后回到状态筛选结果。" in inbox_workbench_source
            and "不会删除原始信息" in inbox_workbench_test
            and "assertFalse(archived.archiveEnabled)" in inbox_workbench_test
            and "assertTrue(archived.restoreEnabled)" in inbox_workbench_test,
        ),
        (
            "gradle_inbox_workbench_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.InboxWorkbenchTest.xml",
                "cn.shike.app.InboxWorkbenchTest",
                5,
            ),
        ),
        (
            "reminder_payload_unit_test_exists",
            "fun scheduledReminderFrom(" in reminder_payload_source
            and "fun reminderScheduleResultDetail(" in reminder_payload_source
            and "fun shouldRestoreScheduledReminder(" in reminder_payload_source
            and "fun reminderDeliveryPayloadFrom(" in reminder_payload_source
            and "data class ReminderDeliveryPayload" in reminder_payload_source
            and "class ReminderPayloadTest" in reminder_payload_test
            and reminder_payload_test.count("@Test") == 6
            and "scheduledReminderFrom_keepsStablePayloadFields" in reminder_payload_test
            and "scheduledReminderFrom_nearStartUsesOneMinuteFallbackAndResultMode" in reminder_payload_test
            and "shouldRestoreScheduledReminder_rejectsExpiredPayload" in reminder_payload_test
            and "reminderDeliveryPayloadFrom_keepsIntentPayloadFields" in reminder_payload_test
            and "reminderDeliveryPayloadFrom_defaultsMissingDetailAndId" in reminder_payload_test
            and "reminderDeliveryPayloadFrom_rejectsMissingOrBlankTitle" in reminder_payload_test
            and "调度模式：系统普通定时" in reminder_payload_test,
        ),
        (
            "reminder_delivery_payload_contract_tested",
            "REMINDER_FALLBACK_DETAIL" in reminder_payload_test
            and "assertNull(reminderDeliveryPayloadFrom(title = null" in reminder_payload_test
            and "assertNull(reminderDeliveryPayloadFrom(title = \"\"" in reminder_payload_test
            and "\"课程提醒\".hashCode()" in reminder_payload_test
            and "notificationId = null" in reminder_payload_test
            and "明天 09:00 · 腾讯会议" in reminder_payload_test,
        ),
        (
            "gradle_reminder_payload_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.ReminderPayloadTest.xml",
                "cn.shike.app.ReminderPayloadTest",
                6,
            ),
        ),
        (
            "backend_analysis_runner_unit_test_exists",
            "fun backendAnalyzeText(" in backend_analysis_runner_source
            and "fun backendSuccessOutcome(" in backend_analysis_outcome_source
            and "fun backendFailureOutcome(" in backend_analysis_outcome_source
            and "fun backendFailureFallbackCopyFor(" in backend_analysis_outcome_source
            and "fun backendAnalysisInputForCurrentDraft(" in backend_analysis_runner_source
            and "data class BackendFailureFallbackCopy" in backend_analysis_outcome_source
            and "class BackendAnalysisRunnerTest" in backend_analysis_runner_test
            and backend_analysis_runner_test.count("@Test") == 6
            and "backendAnalysisInputForCurrentDraft_usesCaptureSourceSpecificBackendType" in backend_analysis_runner_test
            and "backendAnalyzeText_prefersEditedOcrDraftAndDoesNotFallbackToImageSampleRawText" in backend_analysis_runner_test
            and "backendFailureOutcome_redactsSensitiveTextAndKeepsFallbackReviewState" in backend_analysis_runner_test
            and "backendFailureOutcomeForRealMathDraft_doesNotInjectCourseSampleFields" in backend_analysis_runner_test
            and "backendFailureFallbackCopyFor_redactsEvidenceBeforeUiPersistence" in backend_analysis_runner_test
            and "backendSuccessOutcome_preservesReturnedItemAndBackendSource" in backend_analysis_runner_test
            and "云侧暂不可用，已切换为本地确认" in backend_analysis_runner_test
            and "[手机号已脱敏]" in backend_analysis_runner_test,
        ),
        (
            "backend_failure_fallback_copy_unit_tested",
            "BackendFailureFallbackCopy" in backend_analysis_outcome_source
            and "redactSensitiveLogText(textForAnalyze)" in backend_analysis_outcome_source
            and "日志已脱敏" in backend_analysis_outcome_source
            and "demo@example.com" in backend_analysis_runner_test
            and "assertFalse(copy.rawText.contains(\"demo@example.com\"))" in backend_analysis_runner_test
            and "assertFalse(copy.rawText.contains(\"192.168.0.2\"))" in backend_analysis_runner_test,
        ),
        (
            "gradle_backend_analysis_runner_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.BackendAnalysisRunnerTest.xml",
                "cn.shike.app.BackendAnalysisRunnerTest",
                6,
            ),
        ),
        (
            "backend_endpoint_unit_test_exists",
            "class BackendEndpointActionsTest" in backend_endpoint_test
            and backend_endpoint_test.count("@Test") == 4
            and "saveBackendEndpointAction_addsHttpSchemeAndTrimsSlash" in backend_endpoint_test
            and "saveBackendEndpointAction_keepsHttpsEndpoint" in backend_endpoint_test
            and "saveBackendEndpointAction_blankInputFallsBackToDefault" in backend_endpoint_test
            and "migrateLegacyBackendBaseUrl_replacesOldEmulatorDefaultOnly" in backend_endpoint_test
            and "migrateLegacyBackendBaseUrl" in backend_endpoint_test
            and "http://10.0.2.2:8000" in backend_endpoint_test
            and "DEFAULT_BACKEND_BASE_URL" in backend_endpoint_test
            and "云侧连接已保存" in backend_endpoint_test,
        ),
        (
            "gradle_backend_endpoint_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.BackendEndpointActionsTest.xml",
                "cn.shike.app.BackendEndpointActionsTest",
                4,
            ),
        ),
        (
            "backend_trigger_unit_test_exists",
            "class BackendTriggerActionsTest" in backend_trigger_test
            and backend_trigger_test.count("@Test") == 2
            and "analyzeCourseWithBackendAction_dispatchesCourseScreenshotInput" in backend_trigger_test
            and "analyzeEventWithBackendAction_dispatchesEventCameraInput" in backend_trigger_test
            and "screenshot" in backend_trigger_test
            and "camera" in backend_trigger_test
            and "课程通知" in backend_trigger_test
            and "活动海报" in backend_trigger_test,
        ),
        (
            "gradle_backend_trigger_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.BackendTriggerActionsTest.xml",
                "cn.shike.app.BackendTriggerActionsTest",
                2,
            ),
        ),
        (
            "backend_outcome_unit_test_exists",
            "class BackendOutcomeActionsTest" in backend_outcome_test
            and backend_outcome_test.count("@Test") == 3
            and "applyBackendOutcomeSelection_persistsBackendItemAndSource" in backend_outcome_test
            and "applyBackendOutcomeSelection_preservesFallbackStatusMessage" in backend_outcome_test
            and "sanitizeBackendOutcomeCopy_redactsSensitiveTokensAndFallsBackToDefaults" in backend_outcome_test
            and "云端 AI 解析：活动海报" in backend_outcome_test
            and "云侧解析失败，本地待确认" in backend_outcome_test
            and "云侧解析结果待确认" in backend_outcome_test,
        ),
        (
            "backend_outcome_copy_sanitization_unit_tested",
            "fun sanitizeBackendOutcomeSource(" in backend_outcome_source
            and "fun sanitizeBackendOutcomeStatus(" in backend_outcome_source
            and "redactSensitiveLogText(source.orEmpty().trim())" in backend_outcome_source
            and "redactSensitiveLogText(statusMessage.orEmpty().trim())" in backend_outcome_source
            and "persistSelection(outcome.item, sanitizeBackendOutcomeSource(outcome.source))" in backend_outcome_source
            and "return sanitizeBackendOutcomeStatus(outcome.statusMessage)" in backend_outcome_source
            and "sanitizeBackendOutcomeCopy_redactsSensitiveTokensAndFallsBackToDefaults" in backend_outcome_test
            and "sanitizeBackendOutcomeSource" in backend_outcome_test
            and "sanitizeBackendOutcomeStatus" in backend_outcome_test
            and "13812345678" in backend_outcome_test
            and "demo@example.com" in backend_outcome_test
            and "学号：2026123456" in backend_outcome_test
            and "10.0.2.2:8000" in backend_outcome_test
            and "assertFalse(status.contains(\"2026123456\"))" in backend_outcome_test
            and "云侧解析结果待确认" in backend_outcome_test,
        ),
        (
            "gradle_backend_outcome_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.BackendOutcomeActionsTest.xml",
                "cn.shike.app.BackendOutcomeActionsTest",
                3,
            ),
        ),
        (
            "sample_actions_unit_test_exists",
            "class SampleActionsTest" in sample_actions_test
            and sample_actions_test.count("@Test") == 2
            and "applyCourseSampleSelection_persistsCourseSampleWithSource" in sample_actions_test
            and "applyEventSampleSelection_persistsEventSampleWithSource" in sample_actions_test
            and "离线样例：课程通知截图" in sample_actions_test
            and "离线样例：活动海报拍照" in sample_actions_test,
        ),
        (
            "gradle_sample_actions_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.SampleActionsTest.xml",
                "cn.shike.app.SampleActionsTest",
                2,
            ),
        ),
        (
            "inbox_entities_thumbnail_uri_contract_unit_tested",
            "data class CaptureDraftEntity" in inbox_entities_source
            and "val localImageUri: String?" in inbox_entities_source
            and "val thumbnailUri: String?" in inbox_entities_source
            and "class InboxEntitiesTest" in inbox_entities_test
            and inbox_entities_test.count("@Test") == 4
            and "captureDraftEntity_keepsOriginalAndThumbnailUrisSeparate" in inbox_entities_test
            and "content://media/external/images/media/42" in inbox_entities_test
            and "file:/private-cache/shike-image-thumbnails/thumb-42.jpg" in inbox_entities_test
            and test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.data.InboxEntitiesTest.xml",
                "cn.shike.app.data.InboxEntitiesTest",
                4,
            ),
        ),
        (
            "local_inbox_action_codec_unit_test_exists",
            "fun encodeInboxActions(" in local_inbox_store_source
            and "fun decodeInboxActions(" in local_inbox_store_source
            and ".putString(KEY_ACTIONS, encodeInboxActions(item.actions))" in local_inbox_store_source
            and "val actions = decodeInboxActions(preferences.getString(KEY_ACTIONS, null))" in legacy_inbox_snapshot_source
            and "class LocalInboxStoreTest" in local_inbox_store_test
            and local_inbox_store_test.count("@Test") == 4
            and "encodeInboxActions_filtersBlankLabelsAndEscapesSeparators" in local_inbox_store_test
            and "decodeInboxActions_trimsLabelsAndFallsBackToCourseActions" in local_inbox_store_test
            and "提醒|地图" in local_inbox_store_test
            and "assertEquals(listOf(\"加入日历\", \"课前提醒\", \"打开地图\"), decodeInboxActions(null))" in local_inbox_store_test,
        ),
        (
            "local_inbox_capture_source_sanitization_unit_tested",
            "fun sanitizeInboxCaptureSource(" in local_inbox_store_source
            and ".putString(KEY_CAPTURE_SOURCE, sanitizeInboxCaptureSource(captureSource))" in local_inbox_store_source
            and "legacyInboxCaptureSourceFromPreferences(preferences(context))" in local_inbox_store_source
            and "redactSensitiveLogText(captureSource.orEmpty().trim())" in local_inbox_store_source
            and "sanitizeInboxCaptureSource_redactsSensitiveSourceAndFallsBackToDefault" in local_inbox_store_test
            and "13812345678" in local_inbox_store_test
            and "demo@example.com" in local_inbox_store_test
            and "192.168.0.2:8000" in local_inbox_store_test
            and "assertFalse(sanitized.contains(\"demo@example.com\"))" in local_inbox_store_test,
        ),
        (
            "local_inbox_raw_text_sanitization_unit_tested",
            "fun sanitizeInboxRawText(" in local_inbox_store_source
            and ".putString(KEY_RAW_TEXT, sanitizeInboxRawText(item.rawText))" in local_inbox_store_source
            and "rawText = sanitizeInboxRawText(preferences.getString(KEY_RAW_TEXT, null))" in legacy_inbox_snapshot_source
            and "DEFAULT_RAW_TEXT" in local_inbox_store_source
            and "sanitizeInboxRawText_redactsSensitiveRawTextAndFallsBackToDefault" in local_inbox_store_test
            and "学号：2026123456" in local_inbox_store_test
            and "10.0.2.2:8000" in local_inbox_store_test
            and "assertFalse(sanitized.contains(\"2026123456\"))" in local_inbox_store_test
            and "assertFalse(sanitized.contains(\"10.0.2.2\"))" in local_inbox_store_test,
        ),
        (
            "gradle_local_inbox_store_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.data.LocalInboxStoreTest.xml",
                "cn.shike.app.data.LocalInboxStoreTest",
                4,
            ),
        ),
        (
            "local_data_clear_unit_test_exists",
            "class LocalDataClearActionsTest" in local_data_clear_test
            and local_data_clear_test.count("@Test") == 7
            and "clearedLocalDataState_resetsToCourseSampleAndEmptyTodayState" in local_data_clear_test
            and "clearedLocalDataState_resetsBackendUrlToDefault" in local_data_clear_test
            and "clearedLocalDataState_explainsSafeRestartPath" in local_data_clear_test
            and "requestLocalDataClearConfirmation_requiresSecondAppConfirmation" in local_data_clear_test
            and "cancelLocalDataClearConfirmation_keepsCacheAndDismissesPrompt" in local_data_clear_test
            and "confirmLocalDataClearConfirmation_onlyClearsAfterPromptIsVisible" in local_data_clear_test
            and "TodayAgendaState.Empty" in local_data_clear_test,
        ),
        (
            "gradle_local_data_clear_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.LocalDataClearActionsTest.xml",
                "cn.shike.app.LocalDataClearActionsTest",
                7,
            ),
        ),
        (
            "local_data_clear_requires_app_internal_confirmation",
            "data class LocalDataClearConfirmationState" in local_data_clear_source
            and "shouldClearLocalData = state.isAwaitingConfirmation" in local_data_clear_source
            and "清除拾刻缓存" in readiness_sections
            and "确认清除" in readiness_sections
            and "不会删除系统相册原截图" in readiness_sections
            and "requestLocalDataClearConfirmation(clearConfirmationState)" in readiness_sections
            and "confirmLocalDataClearConfirmation(clearConfirmationState)" in readiness_sections
            and "onClearLocalData()" in readiness_sections,
        ),
        (
            "cloud_enhancement_unit_test_exists",
            "class CloudEnhancementActionsTest" in cloud_enhancement_test
            and cloud_enhancement_test.count("@Test") == 3
            and "cloudEnhancementDisabledFallback_keepsTodayActionReady" in cloud_enhancement_test
            and "cloudEnhancementDisabledFallback_statesBackendIsNotCalled" in cloud_enhancement_test
            and "cloudEnhancementDisabledFallback_keepsLocalDraftAndOfflineEntry" in cloud_enhancement_test
            and "未调用云端 AI" in cloud_enhancement_test,
        ),
        (
            "gradle_cloud_enhancement_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.CloudEnhancementActionsTest.xml",
                "cn.shike.app.CloudEnhancementActionsTest",
                3,
            ),
        ),
        (
            "developer_mode_unlock_unit_test_exists",
            "const val DEVELOPER_MODE_UNLOCK_TAPS = 5" in developer_mode_source
            and "data class DeveloperModeState" in developer_mode_source
            and "fun developerModeStateAfterVersionTap(" in developer_mode_source
            and "fun visibleSectionsForDeveloperMode(" in developer_mode_source
            and "class DeveloperModeUnlockTest" in developer_mode_test
            and developer_mode_test.count("@Test") == 3
            and "developerModeStateAfterVersionTap_keepsDebugHiddenBeforeFifthTap" in developer_mode_test
            and "developerModeStateAfterVersionTap_unlocksDebugOnFifthTapAndTargetsDebug" in developer_mode_test
            and "developerModeStateAfterVersionTap_keepsUnlockedStateStableAfterExtraTaps" in developer_mode_test
            and "ShikeMainSection.Debug" in developer_mode_test,
        ),
        (
            "gradle_developer_mode_unlock_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.DeveloperModeUnlockTest.xml",
                "cn.shike.app.DeveloperModeUnlockTest",
                3,
            ),
        ),
        (
            "local_multimodal_status_unit_test_exists",
            "enum class LocalMultimodalInstallState" in local_multimodal_source
            and "NotInstalled" in local_multimodal_source
            and "Available" in local_multimodal_source
            and "InitFailed" in local_multimodal_source
            and "enum class LocalMultimodalPreference" in local_multimodal_source
            and "fun allowCloudImageForPreference" in local_multimodal_source
            and "fun localMultimodalUiState(" in local_multimodal_source
            and "不打包模型" in local_multimodal_source
            and "不会假装可用" in local_multimodal_source
            and "同一 JSON Schema" in local_multimodal_source
            and "class LocalMultimodalStatusTest" in local_multimodal_test
            and local_multimodal_test.count("@Test") == 4
            and "localMultimodalUiState_reportsNotInstalledWithoutClaimingAvailability" in local_multimodal_test
            and "localMultimodalUiState_usesAvailableLocalOnlyWhenRequestedOrCloudDisabled" in local_multimodal_test
            and "localMultimodalUiState_reportsInitializationFailureAsManualReviewBoundary" in local_multimodal_test
            and "allowCloudImageForPreference_disablesImageUploadWhenLocalPreferred" in local_multimodal_test,
        ),
        (
            "gradle_local_multimodal_status_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.LocalMultimodalStatusTest.xml",
                "cn.shike.app.LocalMultimodalStatusTest",
                4,
            ),
        ),
        (
            "local_multimodal_runtime_contract_unit_test_exists",
            "data class LocalMultimodalConfig" in local_multimodal_runtime_source
            and "val multimodal: Boolean = true" in local_multimodal_runtime_source
            and "interface LocalMultimodalEngine" in local_multimodal_runtime_source
            and "fun init(config: LocalMultimodalConfig): Int" in local_multimodal_runtime_source
            and "fun callVit(rgbBytes: ByteArray, width: Int, height: Int): Int" in local_multimodal_runtime_source
            and "fun generate(prompt: String): String" in local_multimodal_runtime_source
            and "class LocalMultimodalRuntime" in local_multimodal_runtime_source
            and "local_multimodal_sdk_missing" in local_multimodal_runtime_source
            and "schema_valid" in local_multimodal_runtime_source
            and "用户确认前不可执行" in local_multimodal_runtime_source
            and "class LocalMultimodalRuntimeTest" in local_multimodal_runtime_test
            and local_multimodal_runtime_test.count("@Test") == 3
            and "analyze_runsInitVitGenerateThenSchemaGateBeforeManualReviewCard" in local_multimodal_runtime_test
            and "analyze_returnsUnavailableWithoutCallingSdkWhenEngineMissing" in local_multimodal_runtime_test
            and "analyze_rejectsJsonMissingRequiredFieldsAndDoesNotInjectSample" in local_multimodal_runtime_test,
        ),
        (
            "gradle_local_multimodal_runtime_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.data.LocalMultimodalRuntimeTest.xml",
                "cn.shike.app.data.LocalMultimodalRuntimeTest",
                3,
            ),
        ),
        (
            "image_preprocess_policy_unit_test_exists",
            "object ImagePreprocessPolicy" in image_preprocess_policy_source
            and "const val MAX_EDGE = 1600" in image_preprocess_policy_source
            and "const val JPEG_QUALITY = 82" in image_preprocess_policy_source
            and 'const val OUTPUT_MIME = "image/jpeg"' in image_preprocess_policy_source
            and "fun sampleSizeFor(" in image_preprocess_policy_source
            and "fun outputDimensionsFor(" in image_preprocess_policy_source
            and "fun mimeForBytes(bytes: ByteArray): String?" in image_preprocess_policy_source
            and "fun thumbnailDimensionsFor(" in image_preprocess_policy_source
            and "fun thumbnailFileNameFor(sha256: String): String" in image_preprocess_policy_source
            and "fun chromeCropFor(" in image_preprocess_policy_source
            and "enum class ImagePreprocessSource" in image_preprocess_policy_source
            and "fun sha256Hex(bytes: ByteArray): String" in image_preprocess_policy_source
            and "class ImagePreprocessPolicyTest" in image_preprocess_policy_test
            and image_preprocess_policy_test.count("@Test") == 9
            and "sampleSizeFor_limitsLongEdgeToConfiguredMaximum" in image_preprocess_policy_test
            and "outputDimensionsFor_swapsWidthAndHeightForRotatedExifOrientations" in image_preprocess_policy_test
            and "outputMimeAndDigest_matchBackendImageContract" in image_preprocess_policy_test
            and "thumbnailDimensionsFor_limitsLongEdgeWithoutUpscalingSmallImages" in image_preprocess_policy_test
            and "mimeForBytes_detectsSupportedImageFormatsByMagicBytes" in image_preprocess_policy_test
            and "mimeForBytes_rejectsNonImageBytes" in image_preprocess_policy_test
            and "chromeCropFor_cropsTallScreenshotChromeWithoutChangingWidth" in image_preprocess_policy_test
            and "chromeCropFor_doesNotCropCameraImages" in image_preprocess_policy_test
            and "chromeCropFor_keepsSmallScreenshotsUsable" in image_preprocess_policy_test,
        ),
        (
            "gradle_image_preprocess_policy_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.data.ImagePreprocessPolicyTest.xml",
                "cn.shike.app.data.ImagePreprocessPolicyTest",
                9,
            ),
        ),
        (
            "image_thumbnail_cache_unit_test_exists",
            "object ImageThumbnailCache" in image_thumbnail_cache_source
            and "fun cacheThumbnailBytes(" in image_thumbnail_cache_source
            and "ImagePreprocessPolicy.THUMBNAIL_CACHE_DIR" in image_thumbnail_cache_source
            and "class ImageThumbnailCacheTest" in image_thumbnail_cache_test
            and image_thumbnail_cache_test.count("@Test") == 2
            and "cacheThumbnailBytes_persistsPrivateDigestNamedJpeg" in image_thumbnail_cache_test
            and "cacheThumbnailBytes_reusesExistingFileForSameDigest" in image_thumbnail_cache_test,
        ),
        (
            "gradle_image_thumbnail_cache_test_passed",
            test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.data.ImageThumbnailCacheTest.xml",
                "cn.shike.app.data.ImageThumbnailCacheTest",
                2,
            ),
        ),
        (
            "screenshot_candidate_store_unit_test_exists",
            "fun isLikelyScreenshot(" in screenshot_candidate_store_source
            and "screenWidth" not in screenshot_candidate_store_source
            and "screenHeight" not in screenshot_candidate_store_source
            and "setOf(width, height)" not in screenshot_candidate_store_source
            and "fun loadScreenshotAssistEnabled(" in screenshot_candidate_store_source
            and "fun saveScreenshotAssistEnabled(" in screenshot_candidate_store_source
            and "fun clearScreenshotAssistPreference(" in screenshot_candidate_store_source
            and "class ScreenshotCandidateStoreTest" in screenshot_candidate_store_test
            and screenshot_candidate_store_test.count("@Test") == 7
            and "isLikelyScreenshot_acceptsScreenshotNameOrPathSignals" in screenshot_candidate_store_test
            and "isLikelyScreenshot_rejectsScreenSizedImagesWithoutScreenshotSignals" in screenshot_candidate_store_test
            and "screenshotDisplayNameDigest_isStableAndDoesNotExposeTheName" in screenshot_candidate_store_test
            and "shouldNotifyScreenshotCandidate_rejectsDuplicateContentUri" in screenshot_candidate_store_test
            and "screenshotAssistLookbackWindow_matchesAndroid16Guide" in screenshot_candidate_store_test
            and "screenshotCandidateFromNotificationImport_preservesCandidateMetadata" in screenshot_candidate_store_test
            and "screenshotAssistPreference_persistsAcrossRestartAndCanBeCleared" in screenshot_candidate_store_test
            and "KEY_SCREENSHOT_ASSIST_ENABLED" in screenshot_candidate_store_test
            and test_result_passed(
                "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.data.ScreenshotCandidateStoreTest.xml",
                "cn.shike.app.data.ScreenshotCandidateStoreTest",
                7,
            ),
        ),
        (
            "android_unit_test_guard_documented",
            "validate_android_unit_tests.py" in docs
            and "ANDROID_UNIT_TEST_METRIC 86/86" in docs
            and "testDebugUnitTest" in docs,
        ),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"ANDROID_UNIT_TEST_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
