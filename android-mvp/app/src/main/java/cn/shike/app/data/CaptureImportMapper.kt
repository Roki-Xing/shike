package cn.shike.app.data

import cn.shike.app.domain.ShikeItem

data class CaptureSelection(
    val item: ShikeItem,
    val source: String,
)

data class CaptureDraft(
    val channel: String,
    val sourceLabel: String,
    val rawText: String,
    val createdEpochMillis: Long = 0L,
    val id: String = stableInboxItemId(sourceLabel, rawText, createdEpochMillis),
    val sourceType: CaptureSourceType = captureSourceTypeFromChannel(channel),
    val localImageUri: String? = null,
    val ocrText: String = rawText,
    val ocrConfidence: Float = 1f,
    val ocrEngineName: String = "manual",
    val privacyLevel: PrivacyLevel = PrivacyLevel.Synthetic,
    val cloudAllowed: Boolean = true,
    val imageCleared: Boolean = channel == "share",
)

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
    sampleEvent().copy(title = "拍照导入的活动海报", rawText = draft.rawText)

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
    sampleCourse().copy(title = "相册导入的课程通知", rawText = draft.rawText)

fun gallerySelectionFromImage(label: String): CaptureSelection =
    selectionFromCaptureDraft(galleryDraftFromImage(label))

fun selectionFromCaptureDraft(draft: CaptureDraft): CaptureSelection {
    val item = if (draft.channel == "camera") itemFromCameraDraft(draft) else itemFromGalleryDraft(draft)
    return CaptureSelection(item = item, source = draft.sourceLabel)
}

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
        ocrConfidence = result.confidence,
        ocrEngineName = result.engineName,
        privacyLevel = if (input.allowCloudEnhancement) PrivacyLevel.CloudAllowed else PrivacyLevel.LocalOnly,
        cloudAllowed = input.allowCloudEnhancement,
        imageCleared = result.imageCleared,
    )
}
