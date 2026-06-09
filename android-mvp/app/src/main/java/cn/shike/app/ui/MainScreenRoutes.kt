package cn.shike.app.ui

import android.graphics.Bitmap
import androidx.compose.runtime.Composable
import cn.shike.app.data.ImageCleanupStatus
import cn.shike.app.data.ScreenshotCandidate
import cn.shike.app.domain.ShikeItem
import cn.shike.app.system.VisibleScreenCapturePrompt

@Composable
fun HomeRouteContent(
    selected: ShikeItem,
    todayAgendaState: TodayAgendaState,
    executionResults: List<ExecutionResult>,
    isConfirmed: Boolean,
    modelStatus: String,
    pendingScreenshotCandidate: ScreenshotCandidate?,
    visibleScreenCapturePrompt: VisibleScreenCapturePrompt?,
    onboardingDismissed: Boolean,
    onGallery: () -> Unit,
    onManualInput: () -> Unit,
    onAddCalendar: (ShikeItem) -> Unit,
    onReminder: (ShikeItem) -> Unit,
    onOpenMap: (ShikeItem) -> Unit,
    onDismissOnboarding: () -> Unit,
    onEnableScreenshotAssistFromOnboarding: () -> Unit,
    onImportScreenshotCandidate: (ScreenshotCandidate) -> Unit,
    onIgnoreScreenshotCandidate: () -> Unit,
    onImportVisibleScreenCapture: () -> Unit,
    onDismissVisibleScreenCapture: () -> Unit,
    onReviewed: (ShikeItem) -> Unit,
) {
    HomeActionScreen(
        selected, todayAgendaState, executionResults, isConfirmed,
        onGallery, onManualInput, onAddCalendar, onReminder, onOpenMap,
        onboardingDismissed, onDismissOnboarding, onEnableScreenshotAssistFromOnboarding,
        modelStatus, pendingScreenshotCandidate, onImportScreenshotCandidate,
        onIgnoreScreenshotCandidate, visibleScreenCapturePrompt, onImportVisibleScreenCapture,
        onDismissVisibleScreenCapture, onReviewed,
    )
}

@Composable
fun ImportRouteContent(
    selected: ShikeItem,
    executionResults: List<ExecutionResult>,
    isConfirmed: Boolean,
    captureSource: String,
    capturedBitmap: Bitmap?,
    modelStatus: String,
    ocrDraft: String,
    cloudEnhancedEnabled: Boolean,
    pendingScreenshotCandidate: ScreenshotCandidate?,
    visibleScreenCapturePrompt: VisibleScreenCapturePrompt?,
    sourceImageCleanupStatus: ImageCleanupStatus,
    selectedSourceMediaStoreUri: String?,
    onOcrDraftChange: (String) -> Unit,
    onGallery: () -> Unit,
    onCamera: () -> Unit,
    onManualInput: () -> Unit,
    onBackendCourse: () -> Unit,
    onBackendEvent: () -> Unit,
    onImportScreenshotCandidate: (ScreenshotCandidate) -> Unit,
    onIgnoreScreenshotCandidate: () -> Unit,
    onImportVisibleScreenCapture: () -> Unit,
    onDismissVisibleScreenCapture: () -> Unit,
    onReviewed: (ShikeItem) -> Unit,
    onDeleteSourceImage: () -> Unit,
    onKeepSourceImage: () -> Unit,
    onAddCalendar: (ShikeItem) -> Unit,
    onReminder: (ShikeItem) -> Unit,
    onOpenMap: (ShikeItem) -> Unit,
) {
    CaptureHubScreen(
        captureSource, capturedBitmap, modelStatus, ocrDraft, onOcrDraftChange,
        cloudEnhancedEnabled, onGallery, onCamera, onManualInput, onBackendCourse,
        onBackendEvent, pendingScreenshotCandidate, onImportScreenshotCandidate,
        onIgnoreScreenshotCandidate, visibleScreenCapturePrompt, onImportVisibleScreenCapture,
        onDismissVisibleScreenCapture,
    )
    ParseConfirmScreen(selected, onReviewed = onReviewed)
    ActionPlanScreen(
        selected, isConfirmed, executionResults, sourceImageCleanupStatus,
        selectedSourceMediaStoreUri, onDeleteSourceImage, onKeepSourceImage,
        onAddCalendar, onReminder, onOpenMap,
    )
}
