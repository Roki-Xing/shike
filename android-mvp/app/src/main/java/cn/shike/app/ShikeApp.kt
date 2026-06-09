package cn.shike.app

import android.graphics.Bitmap
import android.os.Handler
import android.os.Looper
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import cn.shike.app.data.BackendImagePayload
import cn.shike.app.data.ImageCleanupStatus
import cn.shike.app.data.InboxItemEntity
import cn.shike.app.data.InitialTodayState
import cn.shike.app.data.ScreenshotCandidate
import cn.shike.app.domain.ShikeItem
import cn.shike.app.system.VisibleScreenCapturePrompt
import cn.shike.app.ui.LocalMultimodalInstallState
import cn.shike.app.ui.LocalMultimodalStatus

@Composable
fun ShikeApp(
    initialItem: ShikeItem,
    initialCaptureSource: String,
    initialTodayState: InitialTodayState,
    initialBackendUrl: String,
    initialInboxHistory: List<InboxItemEntity>,
    onPersist: (ShikeItem, String) -> Unit,
    onSaveBackendUrl: (String) -> Unit,
    onClearLocalData: () -> Unit,
    onAddCalendar: (ShikeItem) -> Unit,
    onReminder: (ShikeItem) -> Unit,
    onOpenMap: (ShikeItem) -> Unit,
    pendingScreenshotCandidate: ScreenshotCandidate? = null,
    onImportScreenshotCandidate: () -> Unit = {},
    screenshotAssistEnabled: Boolean = false,
    onScreenshotAssistEnabledChange: (Boolean) -> Unit = {},
    onboardingDismissed: Boolean = true,
    onDismissOnboarding: () -> Unit = {},
    onEnableScreenshotAssistFromOnboarding: () -> Unit = {},
    onDeleteSourceImage: (String?) -> Unit = {},
    onBuildImagePayload: (String, String) -> BackendImagePayload? = { _, _ -> null },
    onBuildBitmapPayload: (Bitmap) -> BackendImagePayload? = { null },
    visibleScreenCapturePrompt: VisibleScreenCapturePrompt? = null,
    onVisibleScreenCapturePromptConsumed: () -> Unit = {},
    pendingSharedText: String? = null,
    onPendingSharedTextConsumed: () -> Unit = {},
    onImageCleanupStatusChange: (ImageCleanupStatus) -> Unit = {},
    imageCleanupStatusFromSystem: ImageCleanupStatus? = null,
    onImageCleanupStatusConsumed: () -> Unit = {},
) {
    val state = rememberShikeAppState(
        initialItem,
        initialCaptureSource,
        initialTodayState,
        initialBackendUrl,
        initialInboxHistory,
    )
    var screenshotAssistSwitchEnabled by remember(screenshotAssistEnabled) { mutableStateOf(screenshotAssistEnabled) }
    val mainHandler = remember { Handler(Looper.getMainLooper()) }
    val actions = remember(state, mainHandler) {
        ShikeAppActions(
            state = state,
            mainHandler = mainHandler,
            onPersist = onPersist,
            onSaveBackendUrl = onSaveBackendUrl,
            onClearLocalData = onClearLocalData,
            onDeleteSourceImage = onDeleteSourceImage,
            onImageCleanupStatusChange = onImageCleanupStatusChange,
            onImportScreenshotCandidate = onImportScreenshotCandidate,
            onBuildImagePayload = onBuildImagePayload,
            onBuildBitmapPayload = onBuildBitmapPayload,
        )
    }

    LaunchedEffect(imageCleanupStatusFromSystem) {
        val status = imageCleanupStatusFromSystem ?: return@LaunchedEffect
        actions.consumeImageCleanupStatus(status)
        onImageCleanupStatusConsumed()
    }

    LaunchedEffect(pendingSharedText) {
        actions.consumeSharedText(pendingSharedText, onPendingSharedTextConsumed)
    }

    val localMultimodalStatus = LocalMultimodalStatus(
        installState = LocalMultimodalInstallState.NotInstalled,
        preference = state.localMultimodalPreference,
        cloudEnhancedEnabled = state.cloudEnhancedEnabled,
    )

    val captureLaunchers = rememberCaptureLaunchers(
        onCameraPreview = actions::applyCameraPreview,
        onCameraUnavailable = actions::onCameraUnavailable,
        onCameraPermissionDenied = actions::onCameraPermissionDenied,
        onGalleryImage = actions::applyGalleryImage,
        onGalleryUnavailable = actions::onGalleryUnavailable,
    )
    ShikeScreenHost(
        state = state,
        captureLaunchers = captureLaunchers,
        localMultimodalStatus = localMultimodalStatus,
        screenshotAssistSwitchEnabled = screenshotAssistSwitchEnabled,
        onboardingDismissed = onboardingDismissed,
        pendingScreenshotCandidate = pendingScreenshotCandidate,
        visibleScreenCapturePrompt = visibleScreenCapturePrompt,
        onSaveBackendEndpoint = actions::saveBackendEndpoint,
        onAnalyzeCurrentDraft = actions::analyzeCurrentDraftWithBackend,
        onAnalyzeEvent = actions::analyzeEventWithBackend,
        onCourseSample = actions::applyCourseSample,
        onEventSample = actions::applyEventSample,
        onScreenshotAssistChange = {
            screenshotAssistSwitchEnabled = it
            onScreenshotAssistEnabledChange(it)
        },
        onDismissOnboarding = onDismissOnboarding,
        onEnableScreenshotAssistFromOnboarding = {
            screenshotAssistSwitchEnabled = true
            onEnableScreenshotAssistFromOnboarding()
        },
        onImportScreenshotCandidate = actions::applyScreenshotCandidate,
        onIgnoreScreenshotCandidate = onImportScreenshotCandidate,
        onVisibleScreenCapturePromptConsumed = onVisibleScreenCapturePromptConsumed,
        onClearLocalData = actions::clearLocalDataSelection,
        onReviewed = actions::updateReviewedItem,
        onDeleteSourceImage = actions::requestDeleteSourceImage,
        onKeepSourceImage = actions::keepSourceImage,
        onAddCalendar = { runCalendarExecution(it, state.executionResults, { next -> state.executionResults = next }, onAddCalendar) },
        onReminder = { runReminderExecution(it, state.executionResults, { next -> state.executionResults = next }, onReminder) },
        onOpenMap = { runMapExecution(it, state.executionResults, { next -> state.executionResults = next }, onOpenMap) },
    )
}
