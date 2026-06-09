package cn.shike.app.data

import cn.shike.app.domain.ShikeItem

data class CaptureSelection(
    val item: ShikeItem,
    val source: String,
)

enum class ImageCleanupStatus {
    NOT_REQUESTED,
    NOT_SUPPORTED,
    USER_KEPT,
    DELETE_REQUESTED,
    DELETED,
    FAILED,
}

enum class ScreenshotDeleteState {
    NotAvailable,
    NotRequested,
    RequestingSystemConfirmation,
    Deleted,
    Denied,
    Failed,
}

data class CaptureDraft(
    val channel: String,
    val sourceLabel: String,
    val rawText: String,
    val createdEpochMillis: Long = 0L,
    val id: String = stableInboxItemId(sourceLabel, rawText, createdEpochMillis),
    val sourceType: CaptureSourceType = captureSourceTypeFromChannel(channel),
    val localImageUri: String? = null,
    val sourceMediaStoreUri: String? = localImageUri,
    val thumbnailUri: String? = null,
    val ocrText: String = rawText,
    val ocrConfidence: Float = 1f,
    val ocrEngineName: String = "manual",
    val privacyLevel: PrivacyLevel = PrivacyLevel.Synthetic,
    val cloudAllowed: Boolean = true,
    val imageCleared: Boolean = channel == "share",
    val imageCleanupStatus: ImageCleanupStatus =
        if (sourceMediaStoreUri == null) ImageCleanupStatus.NOT_SUPPORTED else ImageCleanupStatus.NOT_REQUESTED,
) {
    val canDeleteOriginal: Boolean
        get() = sourceMediaStoreUri != null

    val deleteState: ScreenshotDeleteState
        get() {
            if (!canDeleteOriginal) {
                return ScreenshotDeleteState.NotAvailable
            }
            return when (imageCleanupStatus) {
                ImageCleanupStatus.NOT_SUPPORTED -> ScreenshotDeleteState.NotAvailable
                ImageCleanupStatus.NOT_REQUESTED -> ScreenshotDeleteState.NotRequested
                ImageCleanupStatus.USER_KEPT -> ScreenshotDeleteState.Denied
                ImageCleanupStatus.DELETE_REQUESTED -> ScreenshotDeleteState.RequestingSystemConfirmation
                ImageCleanupStatus.DELETED -> ScreenshotDeleteState.Deleted
                ImageCleanupStatus.FAILED -> ScreenshotDeleteState.Failed
            }
        }
}

fun cameraCaptureSource(width: Int, height: Int): String = "相机拍照预览 ${width}x${height}"

fun cameraDraftFromPreview(width: Int, height: Int): CaptureDraft =
    captureDraftFromInput(
        CaptureInput(
            sourceType = CaptureSourceType.Camera,
            sourceLabel = cameraCaptureSource(width, height),
            width = width,
            height = height,
        ),
        MockOcrEngine(),
    )

fun itemFromCameraDraft(draft: CaptureDraft): ShikeItem =
    pendingImageItem(
        title = "待解析照片",
        scene = "拍照导入",
        rawText = draft.rawText,
        startEpochMillis = draft.createdEpochMillis,
    )

fun cameraSelectionFromPreview(width: Int, height: Int): CaptureSelection =
    selectionFromCaptureDraft(cameraDraftFromPreview(width, height))

fun galleryCaptureSource(label: String): String = "相册图片 $label"

fun galleryDraftFromImage(label: String): CaptureDraft =
    captureDraftFromInput(
        CaptureInput(
            sourceType = CaptureSourceType.Gallery,
            sourceLabel = galleryCaptureSource(label),
            localImageUri = label,
        ),
        MockOcrEngine(),
    )

fun itemFromGalleryDraft(draft: CaptureDraft): ShikeItem =
    pendingImageItem(
        title = "待解析截图",
        scene = "图片导入",
        rawText = draft.rawText,
        startEpochMillis = draft.createdEpochMillis,
    )

fun gallerySelectionFromImage(label: String): CaptureSelection =
    selectionFromCaptureDraft(galleryDraftFromImage(label))

fun screenshotCaptureSource(candidate: ScreenshotCandidate): String =
    candidate.sourceLabel.takeIf { it.isNotBlank() } ?: "截图助手导入 ${candidate.width}x${candidate.height}"

fun itemFromScreenshotCandidate(candidate: ScreenshotCandidate): ShikeItem =
    pendingImageItem(
        title = "待解析截图",
        scene = "截图导入",
        startEpochMillis = candidate.createdAtMillis,
        rawText = "截图助手导入：将生成行动卡，可在识别到的文字中校对后重试。",
    )

fun screenshotSelectionFromCandidate(candidate: ScreenshotCandidate): CaptureSelection =
    CaptureSelection(
        item = itemFromScreenshotCandidate(candidate),
        source = screenshotCaptureSource(candidate),
    )

fun selectionFromCaptureDraft(draft: CaptureDraft): CaptureSelection {
    val item = when (draft.channel) {
        "camera" -> itemFromCameraDraft(draft)
        "gallery" -> itemFromGalleryDraft(draft)
        else -> pendingImageItem(
            title = "待确认碎片",
            scene = "待确认",
            rawText = draft.rawText,
            startEpochMillis = draft.createdEpochMillis,
        )
    }
    return CaptureSelection(item = item, source = draft.sourceLabel)
}

fun pendingImageItem(
    title: String,
    scene: String,
    rawText: String,
    startEpochMillis: Long,
): ShikeItem =
    ShikeItem(
        title = title,
        scene = scene,
        time = "待确认",
        location = "待确认",
        status = "待确认",
        actions = listOf("先存入待确认"),
        startEpochMillis = startEpochMillis,
        rawText = rawText,
    )

fun backendSourceTypeFromCaptureSource(captureSource: String): String =
    when {
        "相机" in captureSource || "拍照" in captureSource -> "camera"
        "分享" in captureSource -> "share_text"
        "手动输入" in captureSource -> "manual"
        else -> "screenshot"
    }

fun captureDraftFromInput(input: CaptureInput, engine: OcrEngine): CaptureDraft {
    val result = engine.recognize(input)
    return CaptureDraft(
        channel = when (input.sourceType) {
            CaptureSourceType.Camera -> "camera"
            CaptureSourceType.Gallery -> "gallery"
            CaptureSourceType.ShareText -> "share"
            CaptureSourceType.Manual -> "manual"
        },
        sourceLabel = input.sourceLabel,
        rawText = result.text,
        localImageUri = input.localImageUri,
        sourceMediaStoreUri = input.localImageUri,
        thumbnailUri = input.thumbnailUri,
        ocrConfidence = result.confidence,
        ocrEngineName = result.engineName,
        privacyLevel = if (input.allowCloudEnhancement) PrivacyLevel.CloudAllowed else PrivacyLevel.LocalOnly,
        cloudAllowed = input.allowCloudEnhancement,
        imageCleared = result.imageCleared,
    )
}
