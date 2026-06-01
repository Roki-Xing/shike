package cn.shike.app

import android.graphics.Bitmap
import android.os.Handler
import android.os.Looper
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import cn.shike.app.data.BackendAnalysisInput
import cn.shike.app.data.BackendAnalysisOutcome
import cn.shike.app.data.InboxItemEntity
import cn.shike.app.data.InitialTodayState
import cn.shike.app.data.backendAnalysisInputForCurrentDraft
import cn.shike.app.data.inboxItemEntityFrom
import cn.shike.app.domain.ShikeItem
import cn.shike.app.ui.ShikeMainScreen
import cn.shike.app.ui.TodayAgendaState
import cn.shike.app.ui.pendingExecutionResults

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
) {
    var selected by remember { mutableStateOf(initialItem) }
    var isConfirmed by remember { mutableStateOf(initialItem.status == "已安排") }
    var captureSource by remember { mutableStateOf(initialCaptureSource) }
    var capturedBitmap by remember { mutableStateOf<Bitmap?>(null) }
    var modelStatus by remember { mutableStateOf("模型编排：本地 mock 待命") }
    var ocrDraft by remember { mutableStateOf(initialItem.rawText) }
    var backendUrl by remember { mutableStateOf(initialBackendUrl) }
    var executionResults by remember { mutableStateOf(pendingExecutionResults()) }
    var todayAgendaState by remember { mutableStateOf(initialTodayState.toTodayAgendaState()) }
    var cloudEnhancedEnabled by remember { mutableStateOf(true) }
    var inboxHistory by remember { mutableStateOf(initialInboxHistory) }
    val mainHandler = remember { Handler(Looper.getMainLooper()) }

    fun persistSelection(item: ShikeItem, source: String) {
        selected = item
        isConfirmed = item.status == "已安排"
        captureSource = source
        ocrDraft = item.rawText
        todayAgendaState = TodayAgendaState.Ready
        executionResults = pendingExecutionResults()
        onPersist(item, source)
        inboxHistory = listOf(inboxItemEntityFrom(item, source, System.currentTimeMillis())) + inboxHistory
    }
    fun updateReviewedItem(item: ShikeItem) { modelStatus = applyReviewedItemSelection(item, ::persistSelection) }
    fun applyBackendOutcome(outcome: BackendAnalysisOutcome) { capturedBitmap = null; modelStatus = applyBackendOutcomeSelection(outcome, ::persistSelection) }
    fun applyCourseSample() { capturedBitmap = null; applyCourseSampleSelection(::persistSelection) }
    fun applyEventSample() { capturedBitmap = null; applyEventSampleSelection(::persistSelection) }
    fun applyCameraPreview(bitmap: Bitmap) { capturedBitmap = bitmap; applyCameraPreviewSelection(bitmap, ::persistSelection) }
    fun applyGalleryImage(label: String) { capturedBitmap = null; applyGalleryImageSelection(label, ::persistSelection) }
    fun analyzeWithBackend(input: BackendAnalysisInput) {
        if (!cloudEnhancedEnabled) {
            val fallback = cloudEnhancementDisabledFallback()
            modelStatus = fallback.modelStatus
            captureSource = fallback.captureSource
            todayAgendaState = fallback.todayAgendaState
            return
        }
        val result = runBackendAnalysisAction(
            backendUrl = backendUrl,
            input = input,
            ocrDraft = ocrDraft,
            mainHandler = mainHandler,
            onOutcome = ::applyBackendOutcome,
        )
        backendUrl = result.endpoint
        modelStatus = result.statusMessage
        todayAgendaState = TodayAgendaState.Error
        onSaveBackendUrl(result.endpoint)
    }
    fun analyzeCourseWithBackend() = analyzeCourseWithBackendAction(::analyzeWithBackend)
    fun analyzeEventWithBackend() = analyzeEventWithBackendAction(::analyzeWithBackend)
    fun analyzeCurrentDraftWithBackend() = analyzeWithBackend(backendAnalysisInputForCurrentDraft(captureSource, selected))
    fun saveBackendEndpoint() {
        val result = saveBackendEndpointAction(backendUrl, onSaveBackendUrl)
        backendUrl = result.endpoint
        modelStatus = result.statusMessage
    }
    fun clearLocalDataSelection() {
        onClearLocalData()
        val cleared = clearedLocalDataState()
        selected = cleared.item
        isConfirmed = false
        captureSource = cleared.captureSource
        capturedBitmap = null
        modelStatus = cleared.modelStatus
        ocrDraft = cleared.item.rawText
        backendUrl = cleared.backendUrl
        cloudEnhancedEnabled = cleared.cloudEnhancedEnabled
        executionResults = pendingExecutionResults()
        todayAgendaState = cleared.todayAgendaState
    }

    val captureLaunchers = rememberCaptureLaunchers(
        onCameraPreview = ::applyCameraPreview,
        onCameraUnavailable = {
            captureSource = "错误状态：相机未返回图片，保留当前行动卡。"
            todayAgendaState = TodayAgendaState.Error
        },
        onCameraPermissionDenied = {
            captureSource = "错误状态：相机权限被拒绝，可改用相册或文本分享入口。"
            todayAgendaState = TodayAgendaState.Error
        },
        onGalleryImage = ::applyGalleryImage,
        onGalleryUnavailable = {
            captureSource = "错误状态：未选择图片，保留当前行动卡。"
            todayAgendaState = TodayAgendaState.Error
        },
    )

    ShikeMainScreen(
        selected = selected,
        todayAgendaState = todayAgendaState,
        executionResults = executionResults,
        isConfirmed = isConfirmed,
        captureSource = captureSource,
        capturedBitmap = capturedBitmap,
        modelStatus = modelStatus,
        ocrDraft = ocrDraft,
        onOcrDraftChange = { ocrDraft = it },
        backendUrl = backendUrl,
        inboxHistory = inboxHistory,
        onBackendUrlChange = { backendUrl = it },
        onSaveBackendUrl = ::saveBackendEndpoint,
        onGallery = captureLaunchers.launchGallery,
        onCamera = captureLaunchers.launchCamera,
        onManualInput = {
            todayAgendaState = TodayAgendaState.Ready
            captureSource = "手动输入入口：请编辑 OCR 文本草稿后选择后端解析或离线样例。"
        },
        onBackendCourse = ::analyzeCurrentDraftWithBackend,
        onBackendEvent = ::analyzeEventWithBackend,
        onCourse = ::applyCourseSample,
        onEvent = ::applyEventSample,
        cloudEnhancedEnabled = cloudEnhancedEnabled,
        onCloudEnhancedChange = { cloudEnhancedEnabled = it },
        onClearLocalData = ::clearLocalDataSelection,
        onReviewed = ::updateReviewedItem,
        onAddCalendar = { runCalendarExecution(it, executionResults, { next -> executionResults = next }, onAddCalendar) },
        onReminder = { runReminderExecution(it, executionResults, { next -> executionResults = next }, onReminder) },
        onOpenMap = { runMapExecution(it, executionResults, { next -> executionResults = next }, onOpenMap) },
    )
}

private fun InitialTodayState.toTodayAgendaState(): TodayAgendaState =
    if (this == InitialTodayState.Empty) TodayAgendaState.Empty else TodayAgendaState.Ready
