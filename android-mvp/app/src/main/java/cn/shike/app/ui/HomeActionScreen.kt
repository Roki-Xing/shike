package cn.shike.app.ui

import androidx.compose.runtime.Composable
import cn.shike.app.data.ScreenshotCandidate
import cn.shike.app.domain.ShikeItem
import cn.shike.app.system.VisibleScreenCapturePrompt

@Composable
fun HomeActionScreen(
    selected: ShikeItem,
    todayAgendaState: TodayAgendaState,
    executionResults: List<ExecutionResult>,
    isConfirmed: Boolean,
    onGallery: () -> Unit,
    onManualInput: () -> Unit,
    onAddCalendar: (ShikeItem) -> Unit,
    onReminder: (ShikeItem) -> Unit,
    onOpenMap: (ShikeItem) -> Unit,
    onboardingDismissed: Boolean,
    onDismissOnboarding: () -> Unit,
    onEnableScreenshotAssistFromOnboarding: () -> Unit,
    modelStatus: String,
    pendingScreenshotCandidate: ScreenshotCandidate?,
    onImportScreenshotCandidate: (ScreenshotCandidate) -> Unit,
    onIgnoreScreenshotCandidate: () -> Unit,
    visibleScreenCapturePrompt: VisibleScreenCapturePrompt?,
    onImportVisibleScreenCapture: () -> Unit,
    onDismissVisibleScreenCapture: () -> Unit,
    onReviewed: (ShikeItem) -> Unit,
) {
    DashboardHeader()
    DateStrip()
    if (!onboardingDismissed) {
        PermissionOnboarding(
            onEnableScreenshotAssist = onEnableScreenshotAssistFromOnboarding,
            onDismiss = onDismissOnboarding,
        )
    }
    ScreenshotPromptEntry(
        pendingScreenshotCandidate = pendingScreenshotCandidate,
        onImportScreenshotCandidate = onImportScreenshotCandidate,
        onIgnoreScreenshotCandidate = onIgnoreScreenshotCandidate,
        visibleScreenCapturePrompt = visibleScreenCapturePrompt,
        onImportVisibleScreenCapture = onImportVisibleScreenCapture,
        onDismissVisibleScreenCapture = onDismissVisibleScreenCapture,
    )
    HomeAgendaList(
        item = selected,
        state = todayAgendaState,
        onGallery = onGallery,
        onManualInput = onManualInput,
    )
    AnalyzeProgressPanel(
        analyzeProgressStateFor(
            modelStatus = modelStatus,
            hasPendingImage = pendingScreenshotCandidate != null || visibleScreenCapturePrompt != null,
            selectedStatus = selected.status,
        ),
    )
    HomePendingReviewPanel(selected)
    ParseConfirmPanel(selected, onReviewed = onReviewed)
    ConfirmBanner(
        selected = selected,
        isConfirmed = isConfirmed,
        executionResults = executionResults,
        onAddCalendar = onAddCalendar,
        onReminder = onReminder,
        onOpenMap = onOpenMap,
    )
}

@Composable
private fun ScreenshotPromptEntry(
    pendingScreenshotCandidate: ScreenshotCandidate?,
    onImportScreenshotCandidate: (ScreenshotCandidate) -> Unit,
    onIgnoreScreenshotCandidate: () -> Unit,
    visibleScreenCapturePrompt: VisibleScreenCapturePrompt?,
    onImportVisibleScreenCapture: () -> Unit,
    onDismissVisibleScreenCapture: () -> Unit,
) {
    visibleScreenCapturePrompt?.let { prompt ->
        VisibleScreenCapturePromptCard(
            prompt = prompt,
            onImport = onImportVisibleScreenCapture,
            onDismiss = onDismissVisibleScreenCapture,
        )
    }
    pendingScreenshotCandidate?.let { candidate ->
        ScreenshotDetectedSheet(
            candidate = candidate,
            onImport = onImportScreenshotCandidate,
            onIgnore = onIgnoreScreenshotCandidate,
        )
    }
}
