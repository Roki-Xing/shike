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
import cn.shike.app.data.BackendAnalysisInput
import cn.shike.app.data.BackendAnalysisOutcome
import cn.shike.app.data.BackendImagePayload
import cn.shike.app.data.ImageCleanupStatus
import cn.shike.app.data.InboxItemEntity
import cn.shike.app.data.InitialTodayState
import cn.shike.app.data.ScreenshotCandidate
import cn.shike.app.data.backendAnalysisInputForCurrentDraft
import cn.shike.app.data.buildRuntimeSharedTextSelection
import cn.shike.app.data.inboxItemEntityFrom
import cn.shike.app.domain.ShikeItem
import cn.shike.app.system.VisibleScreenCapturePrompt
import cn.shike.app.ui.LocalMultimodalInstallState
import cn.shike.app.ui.LocalMultimodalPreference
import cn.shike.app.ui.LocalMultimodalStatus
import cn.shike.app.ui.ShikeMainScreen
import cn.shike.app.ui.TodayAgendaState
import cn.shike.app.ui.allowCloudImageForPreference
import cn.shike.app.ui.imageCleanupFailedResult
import cn.shike.app.ui.imageCleanupKeptResult
import cn.shike.app.ui.imageCleanupRequestedResult
import cn.shike.app.ui.imageCleanupDeletedResult
import cn.shike.app.ui.pendingExecutionResults
import cn.shike.app.ui.recordExecutionResult
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
    var selected by remember { mutableStateOf(initialItem) }
    var isConfirmed by remember { mutableStateOf(initialItem.status == "已安排") }
    var captureSource by remember { mutableStateOf(initialCaptureSource) }
    var selectedSourceMediaStoreUri by remember { mutableStateOf<String?>(null) }
    var sourceImageCleanupStatus by remember { mutableStateOf(ImageCleanupStatus.NOT_SUPPORTED) }
    var capturedBitmap by remember { mutableStateOf<Bitmap?>(null) }
    var modelStatus by remember { mutableStateOf("模型状态：等待导入") }
    var ocrDraft by remember { mutableStateOf(initialItem.rawText) }
    var backendUrl by remember { mutableStateOf(initialBackendUrl) }
    var executionResults by remember { mutableStateOf(pendingExecutionResults()) }
    var todayAgendaState by remember { mutableStateOf(initialTodayState.toTodayAgendaState()) }
    var cloudEnhancedEnabled by remember { mutableStateOf(true) }
    var localMultimodalPreference by remember { mutableStateOf(LocalMultimodalPreference.CloudFirst) }
    var screenshotAssistSwitchEnabled by remember(screenshotAssistEnabled) { mutableStateOf(screenshotAssistEnabled) }
    var inboxHistory by remember { mutableStateOf(initialInboxHistory) }
    val mainHandler = remember { Handler(Looper.getMainLooper()) }

    LaunchedEffect(imageCleanupStatusFromSystem) {
        val status = imageCleanupStatusFromSystem ?: return@LaunchedEffect
        sourceImageCleanupStatus = status
        executionResults = when (status) {
            ImageCleanupStatus.DELETED -> executionResults.recordExecutionResult(imageCleanupDeletedResult())
            ImageCleanupStatus.FAILED -> executionResults.recordExecutionResult(imageCleanupFailedResult())
            else -> executionResults
        }
        onImageCleanupStatusConsumed()
    }

    fun persistSelection(
        item: ShikeItem,
        source: String,
        sourceMediaStoreUri: String? = null,
        imageCleanupStatus: ImageCleanupStatus =
            if (sourceMediaStoreUri == null) ImageCleanupStatus.NOT_SUPPORTED else ImageCleanupStatus.NOT_REQUESTED,
    ) {
        selected = item
        isConfirmed = item.status == "已安排"
        captureSource = source
        selectedSourceMediaStoreUri = sourceMediaStoreUri
        sourceImageCleanupStatus = imageCleanupStatus
        ocrDraft = item.rawText
        todayAgendaState = TodayAgendaState.Ready
        executionResults = pendingExecutionResults()
        onPersist(item, source)
        inboxHistory = listOf(inboxItemEntityFrom(item, source, System.currentTimeMillis())) + inboxHistory
    }
    LaunchedEffect(pendingSharedText) {
        val selection = buildRuntimeSharedTextSelection(pendingSharedText) ?: return@LaunchedEffect
        capturedBitmap = null
        persistSelection(
            item = selection.item,
            source = selection.captureSource,
            imageCleanupStatus = ImageCleanupStatus.NOT_SUPPORTED,
        )
        todayAgendaState = selection.todayState.toTodayAgendaState()
        onPendingSharedTextConsumed()
    }
    fun updateReviewedItem(item: ShikeItem) { modelStatus = applyReviewedItemSelection(item, ::persistSelection) }
    fun applyBackendOutcome(outcome: BackendAnalysisOutcome) { capturedBitmap = null; modelStatus = applyBackendOutcomeSelection(outcome, ::persistSelection) }
    fun applyCourseSample() { capturedBitmap = null; applyCourseSampleSelection(::persistSelection) }
    fun applyEventSample() { capturedBitmap = null; applyEventSampleSelection(::persistSelection) }
    fun updateScreenshotAssist(enabled: Boolean) {
        screenshotAssistSwitchEnabled = enabled
        onScreenshotAssistEnabledChange(enabled)
    }
    fun updateImageCleanupStatus(status: ImageCleanupStatus) {
        sourceImageCleanupStatus = status
        onImageCleanupStatusChange(status)
    }
    fun keepSourceImage() {
        updateImageCleanupStatus(ImageCleanupStatus.USER_KEPT)
        executionResults = executionResults.recordExecutionResult(imageCleanupKeptResult())
    }
    fun requestDeleteSourceImage() {
        updateImageCleanupStatus(ImageCleanupStatus.DELETE_REQUESTED)
        executionResults = executionResults.recordExecutionResult(imageCleanupRequestedResult())
        onDeleteSourceImage(selectedSourceMediaStoreUri)
    }
    fun analyzeWithBackend(input: BackendAnalysisInput) {
        if (!cloudEnhancedEnabled) {
            val fallback = cloudEnhancementDisabledFallback()
            modelStatus = fallback.modelStatus
            captureSource = fallback.captureSource
            todayAgendaState = fallback.todayAgendaState
            return
        }
        val imagePayloadProvider = when {
            input.imageUri != null && input.imageUri == selectedSourceMediaStoreUri -> ({
                onBuildImagePayload(input.imageUri, input.imageSourceType)
            })
            input.imageUri == CAMERA_PREVIEW_IMAGE_URI && capturedBitmap != null -> ({ onBuildBitmapPayload(capturedBitmap!!) })
            else -> null
        }
        val result = runBackendAnalysisAction(
            backendUrl = backendUrl,
            input = input,
            ocrDraft = ocrDraft,
            mainHandler = mainHandler,
            imagePayloadProvider = imagePayloadProvider,
            onOutcome = ::applyBackendOutcome,
        )
        backendUrl = result.endpoint
        modelStatus = result.statusMessage
        todayAgendaState = TodayAgendaState.Error
        onSaveBackendUrl(result.endpoint)
    }
    fun analyzeCurrentDraftWithBackend() {
        val imageUri = selectedSourceMediaStoreUri ?: capturedBitmap?.let { CAMERA_PREVIEW_IMAGE_URI }
        analyzeWithBackend(
            backendAnalysisInputForCurrentDraft(
                captureSource = captureSource,
                fallback = selected,
                imageUri = imageUri,
                allowCloudImage = allowCloudImageForPreference(localMultimodalPreference),
            ),
        )
    }
    fun applyCameraPreview(bitmap: Bitmap) {
        capturedBitmap = bitmap
        applyCameraPreviewSelection(bitmap, ::persistSelection)
        analyzeCurrentDraftWithBackend()
    }
    fun applyGalleryImage(label: String) {
        capturedBitmap = null
        applyGalleryImageSelection(label) { item, source ->
            persistSelection(
                item = item,
                source = source,
                sourceMediaStoreUri = label,
                imageCleanupStatus = ImageCleanupStatus.NOT_REQUESTED,
            )
        }
        analyzeCurrentDraftWithBackend()
    }
    fun applyScreenshotCandidate(candidate: ScreenshotCandidate) {
        capturedBitmap = null
        applyScreenshotCandidateSelection(candidate) { item, source ->
            persistSelection(
                item = item,
                source = source,
                sourceMediaStoreUri = candidate.contentUri,
                imageCleanupStatus = ImageCleanupStatus.NOT_REQUESTED,
            )
        }
        onImportScreenshotCandidate()
        analyzeCurrentDraftWithBackend()
    }
    fun analyzeCourseWithBackend() = analyzeCourseWithBackendAction(::analyzeWithBackend)
    fun analyzeEventWithBackend() = analyzeEventWithBackendAction(::analyzeWithBackend)
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
        selectedSourceMediaStoreUri = null
        sourceImageCleanupStatus = ImageCleanupStatus.NOT_SUPPORTED
        capturedBitmap = null
        modelStatus = cleared.modelStatus
        ocrDraft = cleared.item.rawText
        backendUrl = cleared.backendUrl
        cloudEnhancedEnabled = cleared.cloudEnhancedEnabled
        localMultimodalPreference = LocalMultimodalPreference.CloudFirst
        executionResults = pendingExecutionResults()
        todayAgendaState = cleared.todayAgendaState
    }

    val localMultimodalStatus = LocalMultimodalStatus(
        installState = LocalMultimodalInstallState.NotInstalled,
        preference = localMultimodalPreference,
        cloudEnhancedEnabled = cloudEnhancedEnabled,
    )

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
            selectedSourceMediaStoreUri = null
            sourceImageCleanupStatus = ImageCleanupStatus.NOT_SUPPORTED
            capturedBitmap = null
            captureSource = "手动输入入口：请编辑 OCR 文本草稿后选择后端解析或离线样例。"
        },
        onBackendCourse = ::analyzeCurrentDraftWithBackend,
        onBackendEvent = ::analyzeEventWithBackend,
        onCourse = ::applyCourseSample,
        onEvent = ::applyEventSample,
        cloudEnhancedEnabled = cloudEnhancedEnabled,
        onCloudEnhancedChange = { cloudEnhancedEnabled = it },
        localMultimodalStatus = localMultimodalStatus,
        onLocalMultimodalPreferenceChange = { localMultimodalPreference = it },
        screenshotAssistEnabled = screenshotAssistSwitchEnabled,
        onScreenshotAssistChange = ::updateScreenshotAssist,
        onboardingDismissed = onboardingDismissed,
        onDismissOnboarding = onDismissOnboarding,
        onEnableScreenshotAssistFromOnboarding = {
            screenshotAssistSwitchEnabled = true
            onEnableScreenshotAssistFromOnboarding()
        },
        pendingScreenshotCandidate = pendingScreenshotCandidate,
        onImportScreenshotCandidate = ::applyScreenshotCandidate,
        onIgnoreScreenshotCandidate = onImportScreenshotCandidate,
        visibleScreenCapturePrompt = visibleScreenCapturePrompt,
        onImportVisibleScreenCapture = {
            onVisibleScreenCapturePromptConsumed()
            captureLaunchers.launchGallery()
        },
        onDismissVisibleScreenCapture = onVisibleScreenCapturePromptConsumed,
        onClearLocalData = ::clearLocalDataSelection,
        onReviewed = ::updateReviewedItem,
        sourceImageCleanupStatus = sourceImageCleanupStatus,
        selectedSourceMediaStoreUri = selectedSourceMediaStoreUri,
        onDeleteSourceImage = ::requestDeleteSourceImage,
        onKeepSourceImage = ::keepSourceImage,
        onAddCalendar = { runCalendarExecution(it, executionResults, { next -> executionResults = next }, onAddCalendar) },
        onReminder = { runReminderExecution(it, executionResults, { next -> executionResults = next }, onReminder) },
        onOpenMap = { runMapExecution(it, executionResults, { next -> executionResults = next }, onOpenMap) },
    )
}
private fun InitialTodayState.toTodayAgendaState(): TodayAgendaState =
    if (this == InitialTodayState.Empty) TodayAgendaState.Empty else TodayAgendaState.Ready

private const val CAMERA_PREVIEW_IMAGE_URI = "camera_preview"
