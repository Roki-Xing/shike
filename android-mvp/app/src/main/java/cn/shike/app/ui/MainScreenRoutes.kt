package cn.shike.app.ui

import android.graphics.Bitmap
import androidx.compose.runtime.Composable
import cn.shike.app.data.ImageCleanupStatus
import cn.shike.app.data.ScreenshotCandidate
import cn.shike.app.domain.ShikeItem
import cn.shike.app.system.VisibleScreenCapturePrompt

enum class ImportRouteStage {
    Entry,
    Analyzing,
    Reviewing,
    Planning,
    Completed,
}

fun importFlowStageFor(modelStatus: String, selectedStatus: String, isConfirmed: Boolean): ImportRouteStage =
    when {
        "解析中" in modelStatus || "正在解析" in modelStatus -> ImportRouteStage.Analyzing
        isConfirmed || selectedStatus == "已安排" -> ImportRouteStage.Planning
        selectedStatus == "待确认" -> ImportRouteStage.Reviewing
        else -> ImportRouteStage.Entry
    }

@Composable
fun HomeRouteContent(
    selected: ShikeItem,
    todayAgendaState: TodayAgendaState,
    modelStatus: String,
    pendingScreenshotCandidate: ScreenshotCandidate?,
    visibleScreenCapturePrompt: VisibleScreenCapturePrompt?,
    onboardingDismissed: Boolean,
    onGallery: () -> Unit,
    onCamera: () -> Unit,
    onManualInput: () -> Unit,
    onOpenCurrentAction: () -> Unit,
    onDismissOnboarding: () -> Unit,
    onEnableScreenshotAssistFromOnboarding: () -> Unit,
    onImportScreenshotCandidate: (ScreenshotCandidate) -> Unit,
    onIgnoreScreenshotCandidate: () -> Unit,
    onImportVisibleScreenCapture: () -> Unit,
    onDismissVisibleScreenCapture: () -> Unit,
) {
    HomeActionScreen(
        selected = selected,
        todayAgendaState = todayAgendaState,
        onGallery = onGallery,
        onCamera = onCamera,
        onManualInput = onManualInput,
        onOpenCurrentAction = onOpenCurrentAction,
        onboardingDismissed = onboardingDismissed,
        onDismissOnboarding = onDismissOnboarding,
        onEnableScreenshotAssistFromOnboarding = onEnableScreenshotAssistFromOnboarding,
        modelStatus = modelStatus,
        pendingScreenshotCandidate = pendingScreenshotCandidate,
        onImportScreenshotCandidate = onImportScreenshotCandidate,
        onIgnoreScreenshotCandidate = onIgnoreScreenshotCandidate,
        visibleScreenCapturePrompt = visibleScreenCapturePrompt,
        onImportVisibleScreenCapture = onImportVisibleScreenCapture,
        onDismissVisibleScreenCapture = onDismissVisibleScreenCapture,
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
    pendingScreenshotCandidate: ScreenshotCandidate?,
    visibleScreenCapturePrompt: VisibleScreenCapturePrompt?,
    sourceImageCleanupStatus: ImageCleanupStatus,
    selectedSourceMediaStoreUri: String?,
    onOcrDraftChange: (String) -> Unit,
    onGallery: () -> Unit,
    onCamera: () -> Unit,
    onManualInput: () -> Unit,
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
    importFlowCompleted: Boolean,
    onCompleteArrangement: () -> Unit,
    onReturnHome: () -> Unit,
) {
    val importStage = if (importFlowCompleted) {
        ImportRouteStage.Completed
    } else {
        importFlowStageFor(modelStatus, selected.status, isConfirmed)
    }
    when (importStage) {
        ImportRouteStage.Entry -> CaptureHubScreen(
            captureSource, capturedBitmap, modelStatus, ocrDraft, onOcrDraftChange,
            onGallery, onCamera, onManualInput, pendingScreenshotCandidate, onImportScreenshotCandidate,
            onIgnoreScreenshotCandidate, visibleScreenCapturePrompt, onImportVisibleScreenCapture,
            onDismissVisibleScreenCapture,
        )
        ImportRouteStage.Analyzing -> AnalyzeProgressPanel(
            analyzeProgressStateFor(
                modelStatus = modelStatus,
                hasPendingImage = pendingScreenshotCandidate != null || visibleScreenCapturePrompt != null,
                selectedStatus = selected.status,
            ),
        )
        ImportRouteStage.Reviewing -> ParseConfirmScreen(selected, onReviewed = onReviewed)
        ImportRouteStage.Planning -> ActionPlanScreen(
            selected, isConfirmed, executionResults, sourceImageCleanupStatus,
            selectedSourceMediaStoreUri, onDeleteSourceImage, onKeepSourceImage,
            onAddCalendar, onReminder, onOpenMap, onCompleteArrangement,
        )
        ImportRouteStage.Completed -> CompletionSummaryScreen(
            results = executionResults,
            onReturnHome = onReturnHome,
        )
    }
}
