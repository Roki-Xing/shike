package cn.shike.app

import androidx.compose.runtime.Composable
import cn.shike.app.data.ImageCleanupStatus
import cn.shike.app.data.ScreenshotCandidate
import cn.shike.app.domain.ShikeItem
import cn.shike.app.system.VisibleScreenCapturePrompt
import cn.shike.app.ui.LocalMultimodalStatus
import cn.shike.app.ui.ShikeMainScreen
import cn.shike.app.ui.TodayAgendaState

@Composable
fun ShikeScreenHost(
    state: ShikeAppState,
    captureLaunchers: CaptureLaunchers,
    localMultimodalStatus: LocalMultimodalStatus,
    screenshotAssistSwitchEnabled: Boolean,
    onboardingDismissed: Boolean,
    pendingScreenshotCandidate: ScreenshotCandidate?,
    visibleScreenCapturePrompt: VisibleScreenCapturePrompt?,
    onSaveBackendEndpoint: () -> Unit,
    onAnalyzeCurrentDraft: () -> Unit,
    onAnalyzeEvent: () -> Unit,
    onCourseSample: () -> Unit,
    onEventSample: () -> Unit,
    onScreenshotAssistChange: (Boolean) -> Unit,
    onDismissOnboarding: () -> Unit,
    onEnableScreenshotAssistFromOnboarding: () -> Unit,
    onImportScreenshotCandidate: (ScreenshotCandidate) -> Unit,
    onIgnoreScreenshotCandidate: () -> Unit,
    onVisibleScreenCapturePromptConsumed: () -> Unit,
    onClearLocalData: () -> Unit,
    onReviewed: (ShikeItem) -> Unit,
    onDeleteSourceImage: () -> Unit,
    onKeepSourceImage: () -> Unit,
    onAddCalendar: (ShikeItem) -> Unit,
    onReminder: (ShikeItem) -> Unit,
    onOpenMap: (ShikeItem) -> Unit,
) {
    ShikeMainScreen(
        selected = state.selected,
        todayAgendaState = state.todayAgendaState,
        executionResults = state.executionResults,
        isConfirmed = state.isConfirmed,
        captureSource = state.captureSource,
        capturedBitmap = state.capturedBitmap,
        modelStatus = state.modelStatus,
        ocrDraft = state.ocrDraft,
        onOcrDraftChange = { state.ocrDraft = it },
        backendUrl = state.backendUrl,
        inboxHistory = state.inboxHistory,
        onBackendUrlChange = { state.backendUrl = it },
        onSaveBackendUrl = onSaveBackendEndpoint,
        onGallery = captureLaunchers.launchGallery,
        onCamera = captureLaunchers.launchCamera,
        onManualInput = { state.enterManualInput() },
        onBackendCourse = onAnalyzeCurrentDraft,
        onBackendEvent = onAnalyzeEvent,
        onCourse = onCourseSample,
        onEvent = onEventSample,
        cloudEnhancedEnabled = state.cloudEnhancedEnabled,
        onCloudEnhancedChange = { state.cloudEnhancedEnabled = it },
        localMultimodalStatus = localMultimodalStatus,
        onLocalMultimodalPreferenceChange = { state.localMultimodalPreference = it },
        screenshotAssistEnabled = screenshotAssistSwitchEnabled,
        onScreenshotAssistChange = onScreenshotAssistChange,
        onboardingDismissed = onboardingDismissed,
        onDismissOnboarding = onDismissOnboarding,
        onEnableScreenshotAssistFromOnboarding = onEnableScreenshotAssistFromOnboarding,
        pendingScreenshotCandidate = pendingScreenshotCandidate,
        onImportScreenshotCandidate = onImportScreenshotCandidate,
        onIgnoreScreenshotCandidate = onIgnoreScreenshotCandidate,
        visibleScreenCapturePrompt = visibleScreenCapturePrompt,
        onImportVisibleScreenCapture = {
            onVisibleScreenCapturePromptConsumed()
            captureLaunchers.launchGallery()
        },
        onDismissVisibleScreenCapture = onVisibleScreenCapturePromptConsumed,
        onClearLocalData = onClearLocalData,
        onReviewed = onReviewed,
        sourceImageCleanupStatus = state.sourceImageCleanupStatus,
        selectedSourceMediaStoreUri = state.selectedSourceMediaStoreUri,
        onDeleteSourceImage = onDeleteSourceImage,
        onKeepSourceImage = onKeepSourceImage,
        onAddCalendar = onAddCalendar,
        onReminder = onReminder,
        onOpenMap = onOpenMap,
    )
}

fun ShikeAppState.enterManualInput() {
    todayAgendaState = TodayAgendaState.Ready
    selectedSourceMediaStoreUri = null
    sourceImageCleanupStatus = ImageCleanupStatus.NOT_SUPPORTED
    capturedBitmap = null
    captureSource = "手动输入：可编辑识别文字后生成行动卡。"
}
