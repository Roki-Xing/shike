package cn.shike.app.ui

import android.graphics.Bitmap
import androidx.compose.runtime.Composable
import cn.shike.app.data.InboxItemEntity
import cn.shike.app.domain.ShikeItem

@Composable
fun HomeActionScreen(
    selected: ShikeItem,
    todayAgendaState: TodayAgendaState,
    isConfirmed: Boolean,
    onGallery: () -> Unit,
    onCamera: () -> Unit,
    onManualInput: () -> Unit,
    onAddCalendar: (ShikeItem) -> Unit,
    onReminder: (ShikeItem) -> Unit,
    onOpenMap: (ShikeItem) -> Unit,
) {
    SystemStatusRow()
    DashboardHeader()
    DateStrip()
    HomeAgendaList(
        item = selected,
        state = todayAgendaState,
        onGallery = onGallery,
        onCamera = onCamera,
        onManualInput = onManualInput,
    )
    QuickImportPanel(
        onGallery = onGallery,
        onCamera = onCamera,
        onManualInput = onManualInput,
    )
    TodaySummaryPanel()
    HomePendingReviewPanel(selected)
    ConfirmBanner(
        selected = selected,
        isConfirmed = isConfirmed,
        onAddCalendar = onAddCalendar,
        onReminder = onReminder,
        onOpenMap = onOpenMap,
    )
}

@Composable
fun CaptureHubScreen(
    captureSource: String,
    capturedBitmap: Bitmap?,
    modelStatus: String,
    ocrDraft: String,
    onOcrDraftChange: (String) -> Unit,
    cloudEnhancedEnabled: Boolean,
    onGallery: () -> Unit,
    onCamera: () -> Unit,
    onManualInput: () -> Unit,
    onBackendCourse: () -> Unit,
    onBackendEvent: () -> Unit,
) {
    CaptureEntryPanel(
        captureSource = captureSource,
        capturedBitmap = capturedBitmap,
        modelStatus = modelStatus,
        ocrDraft = ocrDraft,
        onOcrDraftChange = onOcrDraftChange,
        cloudEnhancedEnabled = cloudEnhancedEnabled,
        onGallery = onGallery,
        onCamera = onCamera,
        onManualInput = onManualInput,
        onBackendCourse = onBackendCourse,
        onBackendEvent = onBackendEvent,
    )
    if ("请求后端" in modelStatus) {
        ShikeLoadingSkeleton("解析中", "正在解析 OCR 文本")
    }
    if ("失败" in modelStatus) {
        ShikeErrorState("云侧增强暂不可用", "可继续手动确认，或切到调试页检查后端地址。")
    }
}

@Composable
private fun QuickImportPanel(
    onGallery: () -> Unit,
    onCamera: () -> Unit,
    onManualInput: () -> Unit,
) {
    SectionCard("快捷导入") {
        ImportCaptureActions(
            onGallery = onGallery,
            onCamera = onCamera,
            onManualInput = onManualInput,
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
    onAddCalendar: (ShikeItem) -> Unit,
    onReminder: (ShikeItem) -> Unit,
    onOpenMap: (ShikeItem) -> Unit,
) {
    ActionPlannerPanel(selected, isConfirmed, executionResults, onAddCalendar, onReminder, onOpenMap)
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
    onClearLocalData: () -> Unit,
    backendUrl: String,
    onBackendUrlChange: (String) -> Unit,
    onSaveBackendUrl: () -> Unit,
) {
    PrivacyPanel(
        cloudEnhancedEnabled = cloudEnhancedEnabled,
        onCloudEnhancedChange = onCloudEnhancedChange,
        onClearLocalData = onClearLocalData,
    )
    SectionCard("后端连接") {
        BackendEndpointControls(
            backendUrl = backendUrl,
            onBackendUrlChange = onBackendUrlChange,
            onSaveBackendUrl = onSaveBackendUrl,
        )
    }
}

@Composable
private fun HomePendingReviewPanel(selected: ShikeItem) {
    val hasMissingField = selected.time == "待确认" || selected.location == "待确认" || selected.status == "待确认"
    SectionCard("待确认") {
        if (hasMissingField) {
            KeyValue("当前卡片", selected.title)
            KeyValue("需要确认", listOf(selected.time, selected.location, selected.status).filter { it == "待确认" }.size.toString())
            ShikeStatusPill("进入解析确认页补齐字段", ShikeColors.WarningSoft, ShikeColors.Warning)
        } else {
            KeyValue("当前状态", "暂无待确认")
            KeyValue("下一步", "可在行动编排页继续处理")
        }
    }
}
