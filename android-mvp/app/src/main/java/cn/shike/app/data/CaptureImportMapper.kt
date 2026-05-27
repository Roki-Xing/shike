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
)

fun cameraCaptureSource(width: Int, height: Int): String = "相机拍照预览 ${width}x${height}"

fun cameraDraftFromPreview(width: Int, height: Int): CaptureDraft =
    CaptureDraft(
        channel = "camera",
        sourceLabel = cameraCaptureSource(width, height),
        rawText = "相机 OCR 草稿：AI应用分享会 4月24日19:30 图书馆报告厅 报名截止今晚22:00",
    )

fun itemFromCameraDraft(draft: CaptureDraft): ShikeItem =
    sampleEvent().copy(title = "拍照导入的活动海报", rawText = draft.rawText)

fun cameraSelectionFromPreview(width: Int, height: Int): CaptureSelection =
    selectionFromCaptureDraft(cameraDraftFromPreview(width, height))

fun galleryCaptureSource(label: String): String = "相册图片 $label"

fun galleryDraftFromImage(label: String): CaptureDraft =
    CaptureDraft(
        channel = "gallery",
        sourceLabel = galleryCaptureSource(label),
        rawText = "相册 OCR 草稿：高数A班今晚18:30改到B203，作业第5章今晚22:00前提交。",
    )

fun itemFromGalleryDraft(draft: CaptureDraft): ShikeItem =
    sampleCourse().copy(title = "相册导入的课程通知", rawText = draft.rawText)

fun gallerySelectionFromImage(label: String): CaptureSelection =
    selectionFromCaptureDraft(galleryDraftFromImage(label))

fun selectionFromCaptureDraft(draft: CaptureDraft): CaptureSelection {
    val item = if (draft.channel == "camera") itemFromCameraDraft(draft) else itemFromGalleryDraft(draft)
    return CaptureSelection(item = item, source = draft.sourceLabel)
}
