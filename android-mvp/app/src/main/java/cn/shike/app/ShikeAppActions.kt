package cn.shike.app

import android.graphics.Bitmap
import android.os.Handler
import cn.shike.app.data.BackendAnalysisInput
import cn.shike.app.data.BackendAnalysisOutcome
import cn.shike.app.data.BackendImagePayload
import cn.shike.app.data.ImageCleanupStatus
import cn.shike.app.data.ScreenshotCandidate
import cn.shike.app.data.buildRuntimeSharedTextSelection
import cn.shike.app.domain.ShikeItem
import cn.shike.app.ui.TodayAgendaState
import cn.shike.app.ui.imageCleanupDeletedResult
import cn.shike.app.ui.imageCleanupFailedResult
import cn.shike.app.ui.imageCleanupKeptResult
import cn.shike.app.ui.imageCleanupRequestedResult
import cn.shike.app.ui.recordExecutionResult

class ShikeAppActions(
    private val state: ShikeAppState,
    private val mainHandler: Handler,
    private val onPersist: (ShikeItem, String) -> Unit,
    private val onSaveBackendUrl: (String) -> Unit,
    private val onClearLocalData: () -> Unit,
    private val onDeleteSourceImage: (String?) -> Unit,
    private val onImageCleanupStatusChange: (ImageCleanupStatus) -> Unit,
    private val onImportScreenshotCandidate: () -> Unit,
    private val onBuildImagePayload: (String, String) -> BackendImagePayload?,
    private val onBuildBitmapPayload: (Bitmap) -> BackendImagePayload?,
) {
    fun consumeImageCleanupStatus(status: ImageCleanupStatus) {
        state.sourceImageCleanupStatus = status
        state.executionResults = when (status) {
            ImageCleanupStatus.DELETED -> state.executionResults.recordExecutionResult(imageCleanupDeletedResult())
            ImageCleanupStatus.FAILED -> state.executionResults.recordExecutionResult(imageCleanupFailedResult())
            else -> state.executionResults
        }
    }

    fun consumeSharedText(text: String?, onConsumed: () -> Unit) {
        val selection = buildRuntimeSharedTextSelection(text) ?: return
        state.capturedBitmap = null
        state.persistSelection(
            item = selection.item,
            source = selection.captureSource,
            imageCleanupStatus = ImageCleanupStatus.NOT_SUPPORTED,
            onPersist = onPersist,
        )
        state.todayAgendaState = selection.todayState.toTodayAgendaState()
        onConsumed()
    }

    fun updateReviewedItem(item: ShikeItem) = state.updateReviewedItem(item, onPersist)

    fun applyBackendOutcome(outcome: BackendAnalysisOutcome) {
        state.applyBackendOutcome(outcome, onPersist)
    }

    fun applyCourseSample() = state.applyCourseSample(onPersist)

    fun applyEventSample() = state.applyEventSample(onPersist)

    fun keepSourceImage() {
        state.sourceImageCleanupStatus = ImageCleanupStatus.USER_KEPT
        onImageCleanupStatusChange(ImageCleanupStatus.USER_KEPT)
        state.executionResults = state.executionResults.recordExecutionResult(imageCleanupKeptResult())
    }

    fun requestDeleteSourceImage() {
        state.sourceImageCleanupStatus = ImageCleanupStatus.DELETE_REQUESTED
        onImageCleanupStatusChange(ImageCleanupStatus.DELETE_REQUESTED)
        state.executionResults = state.executionResults.recordExecutionResult(imageCleanupRequestedResult())
        onDeleteSourceImage(state.selectedSourceMediaStoreUri)
    }

    fun analyzeWithBackend(input: BackendAnalysisInput) {
        if (!state.cloudEnhancedEnabled) {
            val fallback = cloudEnhancementDisabledFallback()
            state.modelStatus = fallback.modelStatus
            state.captureSource = fallback.captureSource
            state.todayAgendaState = fallback.todayAgendaState
            return
        }
        val result = runBackendAnalysisAction(
            backendUrl = state.backendUrl,
            input = input,
            ocrDraft = state.ocrDraft,
            mainHandler = mainHandler,
            imagePayloadProvider = imagePayloadProviderFor(input),
            onOutcome = ::applyBackendOutcome,
        )
        state.backendUrl = result.endpoint
        state.modelStatus = result.statusMessage
        state.todayAgendaState = TodayAgendaState.Error
        onSaveBackendUrl(result.endpoint)
    }

    fun analyzeCurrentDraftWithBackend() = analyzeWithBackend(state.currentBackendInput())

    fun applyCameraPreview(bitmap: Bitmap) {
        state.applyCameraPreview(bitmap, onPersist)
        analyzeCurrentDraftWithBackend()
    }

    fun applyGalleryImage(label: String) {
        state.applyGalleryImage(label, onPersist)
        analyzeCurrentDraftWithBackend()
    }

    fun applyScreenshotCandidate(candidate: ScreenshotCandidate) {
        state.applyScreenshotCandidate(candidate, onPersist)
        onImportScreenshotCandidate()
        analyzeCurrentDraftWithBackend()
    }

    fun analyzeCourseWithBackend() = analyzeCourseWithBackendAction(::analyzeWithBackend)

    fun analyzeEventWithBackend() = analyzeEventWithBackendAction(::analyzeWithBackend)

    fun saveBackendEndpoint() {
        val result = saveBackendEndpointAction(state.backendUrl, onSaveBackendUrl)
        state.backendUrl = result.endpoint
        state.modelStatus = result.statusMessage
    }

    fun clearLocalDataSelection() {
        onClearLocalData()
        state.resetAfterClear(clearedLocalDataState())
    }

    fun onCameraUnavailable() {
        state.captureSource = "错误状态：相机未返回图片，保留当前行动卡。"
        state.todayAgendaState = TodayAgendaState.Error
    }

    fun onCameraPermissionDenied() {
        state.captureSource = "错误状态：相机权限被拒绝，可改用相册或文本分享入口。"
        state.todayAgendaState = TodayAgendaState.Error
    }

    fun onGalleryUnavailable() {
        state.captureSource = "错误状态：未选择图片，保留当前行动卡。"
        state.todayAgendaState = TodayAgendaState.Error
    }

    private fun imagePayloadProviderFor(input: BackendAnalysisInput): (() -> BackendImagePayload?)? =
        when {
            input.imageUri != null && input.imageUri == state.selectedSourceMediaStoreUri -> ({
                onBuildImagePayload(input.imageUri, input.imageSourceType)
            })
            input.imageUri == CAMERA_PREVIEW_IMAGE_URI && state.capturedBitmap != null -> ({
                onBuildBitmapPayload(state.capturedBitmap!!)
            })
            else -> null
        }
}
