package cn.shike.app.ui

import android.graphics.Bitmap
import androidx.compose.foundation.clickable
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import cn.shike.app.data.ImageCleanupStatus
import cn.shike.app.data.InboxItemEntity
import cn.shike.app.data.ScreenshotCandidate
import cn.shike.app.domain.ShikeItem
import cn.shike.app.system.ScreenshotAssistDiagnostics
import cn.shike.app.system.VisibleScreenCapturePrompt

@Composable
fun CaptureHubScreen(
    captureSource: String,
    capturedBitmap: Bitmap?,
    ocrDraft: String,
    onOcrDraftChange: (String) -> Unit,
    analysisUiState: AnalysisUiState,
    onGallery: () -> Unit,
    onCamera: () -> Unit,
    onManualInput: () -> Unit,
    pendingScreenshotCandidate: ScreenshotCandidate?,
    onImportScreenshotCandidate: (ScreenshotCandidate) -> Unit,
    onIgnoreScreenshotCandidate: () -> Unit,
    visibleScreenCapturePrompt: VisibleScreenCapturePrompt?,
    onImportVisibleScreenCapture: () -> Unit,
    onDismissVisibleScreenCapture: () -> Unit,
    onSavePendingReview: () -> Unit,
    onRetryAnalyze: () -> Unit,
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
    CaptureEntryPanel(
        captureSource = captureSource,
        capturedBitmap = capturedBitmap,
        ocrDraft = ocrDraft,
        onOcrDraftChange = onOcrDraftChange,
        onGallery = onGallery,
        onCamera = onCamera,
        onManualInput = onManualInput,
    )
    if (analysisUiState is AnalysisUiState.Analyzing) {
        ShikeLoadingSkeleton("解析中", "正在解析 OCR 文本")
    }
    if (analysisUiState is AnalysisUiState.Failed) {
        RecoverableErrorState(
            title = "AI 解析暂不可用",
            detail = "截图已保留为待确认，你可以换图、手动输入或稍后重新解析。",
            repairActions = listOf(
                RecoverableRepairAction("重新选择截图", onGallery),
                RecoverableRepairAction("手动输入", onManualInput),
                RecoverableRepairAction("先存入待确认", onSavePendingReview),
                RecoverableRepairAction("重新解析", onRetryAnalyze),
            ),
        )
    }
}

@Composable
fun ParseConfirmScreen(
    selected: ShikeItem,
    onReviewed: (ShikeItem) -> Unit,
) {
    ParseConfirmPanel(selected, onReviewed = onReviewed)
}

@Composable
fun ActionPlanScreen(
    selected: ShikeItem,
    isConfirmed: Boolean,
    executionResults: List<ExecutionResult>,
    sourceImageCleanupStatus: ImageCleanupStatus,
    selectedSourceMediaStoreUri: String?,
    onDeleteSourceImage: () -> Unit,
    onKeepSourceImage: () -> Unit,
    onAddCalendar: (ShikeItem) -> Unit,
    onReminder: (ShikeItem) -> Unit,
    onOpenMap: (ShikeItem) -> Unit,
    onCompleteArrangement: () -> Unit,
) {
    ActionPlannerPanel(
        item = selected,
        isConfirmed = isConfirmed,
        executionResults = executionResults,
        sourceImageCleanupStatus = sourceImageCleanupStatus,
        selectedSourceMediaStoreUri = selectedSourceMediaStoreUri,
        onDeleteSourceImage = onDeleteSourceImage,
        onKeepSourceImage = onKeepSourceImage,
        onAddCalendar = onAddCalendar,
        onReminder = onReminder,
        onOpenMap = onOpenMap,
        onCompleteArrangement = onCompleteArrangement,
    )
}

@Composable
fun InboxScreen(
    selected: ShikeItem,
    captureSource: String,
    executionResults: List<ExecutionResult>,
    inboxHistory: List<InboxItemEntity>,
) {
    InboxPanel(
        item = selected,
        captureSource = captureSource,
        executionResults = executionResults,
        historyEntries = inboxHistory.map(::inboxWorkbenchEntryFromEntity),
    )
}

@Composable
fun PrivacySettingsScreen(
    cloudEnhancedEnabled: Boolean,
    onCloudEnhancedChange: (Boolean) -> Unit,
    localMultimodalStatus: LocalMultimodalStatus,
    onLocalMultimodalPreferenceChange: (LocalMultimodalPreference) -> Unit,
    screenshotAssistDiagnostics: ScreenshotAssistDiagnostics?,
    screenshotAssistEnabled: Boolean,
    onScreenshotAssistChange: (Boolean) -> Unit,
    onClearLocalData: () -> Unit,
    developerModeState: DeveloperModeState,
    onVersionTap: () -> Unit,
) {
    PrivacyPanel(
        cloudEnhancedEnabled = cloudEnhancedEnabled,
        onCloudEnhancedChange = onCloudEnhancedChange,
        localMultimodalStatus = localMultimodalStatus,
        onLocalMultimodalPreferenceChange = onLocalMultimodalPreferenceChange,
        screenshotAssistDiagnostics = screenshotAssistDiagnostics,
        screenshotAssistEnabled = screenshotAssistEnabled,
        onScreenshotAssistChange = onScreenshotAssistChange,
        onClearLocalData = onClearLocalData,
    )
    SectionCard("关于拾刻") {
        VersionUnlockRow(
            version = "0.1.0",
            developerModeState = developerModeState,
            onVersionTap = onVersionTap,
        )
        val remainingTaps = (DEVELOPER_MODE_UNLOCK_TAPS - developerModeState.tapCount).coerceAtLeast(0)
        KeyValue("高级设置", if (developerModeState.enabled) "已开启" else "连续点击版本号 5 次后显示")
        ShikeStatusPill(
            if (developerModeState.enabled) "高级设置已开启" else "普通模式已隐藏高级配置",
            ShikeColors.BrandSoft,
            ShikeColors.Brand,
        )
        if (!developerModeState.enabled && developerModeState.tapCount > 0) {
            KeyValue("剩余点击", "${remainingTaps} 次")
        }
    }
}

@Composable
private fun VersionUnlockRow(
    version: String,
    developerModeState: DeveloperModeState,
    onVersionTap: () -> Unit,
) {
    KeyValue(
        label = "版本",
        value = version,
        modifier = Modifier.clickable(onClick = onVersionTap),
    )
    if (developerModeState.enabled) {
        ShikeStatusPill("已进入高级设置页", ShikeColors.BrandSoft, ShikeColors.Brand)
    }
}
