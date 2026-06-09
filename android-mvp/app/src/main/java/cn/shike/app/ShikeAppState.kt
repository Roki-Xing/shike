package cn.shike.app

import android.graphics.Bitmap
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import cn.shike.app.data.BackendAnalysisInput
import cn.shike.app.data.BackendAnalysisOutcome
import cn.shike.app.data.ImageCleanupStatus
import cn.shike.app.data.InboxItemEntity
import cn.shike.app.data.InitialTodayState
import cn.shike.app.data.ScreenshotCandidate
import cn.shike.app.data.backendAnalysisInputForCurrentDraft
import cn.shike.app.data.inboxItemEntityFrom
import cn.shike.app.domain.ShikeItem
import cn.shike.app.ui.LocalMultimodalPreference
import cn.shike.app.ui.TodayAgendaState
import cn.shike.app.ui.allowCloudImageForPreference
import cn.shike.app.ui.pendingExecutionResults

class ShikeAppState(
    initialItem: ShikeItem,
    initialCaptureSource: String,
    initialTodayState: InitialTodayState,
    initialBackendUrl: String,
    initialInboxHistory: List<InboxItemEntity>,
) {
    var selected by mutableStateOf(initialItem)
    var isConfirmed by mutableStateOf(initialItem.status == "已安排")
    var captureSource by mutableStateOf(initialCaptureSource)
    var selectedSourceMediaStoreUri by mutableStateOf<String?>(null)
    var sourceImageCleanupStatus by mutableStateOf(ImageCleanupStatus.NOT_SUPPORTED)
    var capturedBitmap by mutableStateOf<Bitmap?>(null)
    var modelStatus by mutableStateOf("等待导入")
    var ocrDraft by mutableStateOf(initialItem.rawText)
    var backendUrl by mutableStateOf(initialBackendUrl)
    var executionResults by mutableStateOf(pendingExecutionResults())
    var todayAgendaState by mutableStateOf(initialTodayState.toTodayAgendaState())
    var cloudEnhancedEnabled by mutableStateOf(true)
    var localMultimodalPreference by mutableStateOf(LocalMultimodalPreference.CloudFirst)
    var inboxHistory by mutableStateOf(initialInboxHistory)

    fun persistSelection(
        item: ShikeItem,
        source: String,
        sourceMediaStoreUri: String? = null,
        imageCleanupStatus: ImageCleanupStatus =
            if (sourceMediaStoreUri == null) ImageCleanupStatus.NOT_SUPPORTED else ImageCleanupStatus.NOT_REQUESTED,
        onPersist: (ShikeItem, String) -> Unit,
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

    fun applyBackendOutcome(outcome: BackendAnalysisOutcome, persist: (ShikeItem, String) -> Unit) {
        val sourceMediaStoreUri = selectedSourceMediaStoreUri
        val imageCleanupStatus = persistedImageCleanupStatus(sourceMediaStoreUri)
        capturedBitmap = null
        modelStatus = applyBackendOutcomeSelection(outcome) { item, source ->
            persistSelection(
                item = item,
                source = source,
                sourceMediaStoreUri = sourceMediaStoreUri,
                imageCleanupStatus = imageCleanupStatus,
                onPersist = persist,
            )
        }
    }

    fun updateReviewedItem(item: ShikeItem, persist: (ShikeItem, String) -> Unit) {
        val sourceMediaStoreUri = selectedSourceMediaStoreUri
        val imageCleanupStatus = persistedImageCleanupStatus(sourceMediaStoreUri)
        modelStatus = applyReviewedItemSelection(item) { next, source ->
            persistSelection(
                item = next,
                source = source,
                sourceMediaStoreUri = sourceMediaStoreUri,
                imageCleanupStatus = imageCleanupStatus,
                onPersist = persist,
            )
        }
    }

    fun applyCourseSample(persist: (ShikeItem, String) -> Unit) {
        capturedBitmap = null
        applyCourseSampleSelection { item, source -> persistSelection(item, source, onPersist = persist) }
    }

    fun applyEventSample(persist: (ShikeItem, String) -> Unit) {
        capturedBitmap = null
        applyEventSampleSelection { item, source -> persistSelection(item, source, onPersist = persist) }
    }

    fun resetAfterClear(cleared: LocalDataClearState) {
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
}

private fun ShikeAppState.persistedImageCleanupStatus(sourceMediaStoreUri: String?): ImageCleanupStatus =
    if (sourceMediaStoreUri == null) ImageCleanupStatus.NOT_SUPPORTED else sourceImageCleanupStatus

fun ShikeAppState.currentBackendInput(): BackendAnalysisInput {
    val imageUri = selectedSourceMediaStoreUri ?: capturedBitmap?.let { CAMERA_PREVIEW_IMAGE_URI }
    return backendAnalysisInputForCurrentDraft(
        captureSource = captureSource,
        fallback = selected,
        imageUri = imageUri,
        allowCloudImage = allowCloudImageForPreference(localMultimodalPreference),
    )
}

fun ShikeAppState.applyCameraPreview(bitmap: Bitmap, persist: (ShikeItem, String) -> Unit) {
    capturedBitmap = bitmap
    applyCameraPreviewSelection(bitmap) { item, source -> persistSelection(item, source, onPersist = persist) }
}

fun ShikeAppState.applyGalleryImage(label: String, persist: (ShikeItem, String) -> Unit) {
    capturedBitmap = null
    applyGalleryImageSelection(label) { item, source ->
        persistSelection(
            item = item,
            source = source,
            sourceMediaStoreUri = label,
            imageCleanupStatus = ImageCleanupStatus.NOT_REQUESTED,
            onPersist = persist,
        )
    }
}

fun ShikeAppState.applyScreenshotCandidate(candidate: ScreenshotCandidate, persist: (ShikeItem, String) -> Unit) {
    capturedBitmap = null
    applyScreenshotCandidateSelection(candidate) { item, source ->
        persistSelection(
            item = item,
            source = source,
            sourceMediaStoreUri = candidate.contentUri,
            imageCleanupStatus = ImageCleanupStatus.NOT_REQUESTED,
            onPersist = persist,
        )
    }
}

const val CAMERA_PREVIEW_IMAGE_URI = "camera_preview"

@Composable
fun rememberShikeAppState(
    initialItem: ShikeItem,
    initialCaptureSource: String,
    initialTodayState: InitialTodayState,
    initialBackendUrl: String,
    initialInboxHistory: List<InboxItemEntity>,
): ShikeAppState =
    remember {
        ShikeAppState(initialItem, initialCaptureSource, initialTodayState, initialBackendUrl, initialInboxHistory)
    }

fun InitialTodayState.toTodayAgendaState(): TodayAgendaState =
    if (this == InitialTodayState.Empty) TodayAgendaState.Empty else TodayAgendaState.Ready
