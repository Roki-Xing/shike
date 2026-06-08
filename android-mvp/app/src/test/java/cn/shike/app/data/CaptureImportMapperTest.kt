package cn.shike.app.data

import org.junit.Assert.assertEquals
import org.junit.Test

class CaptureImportMapperTest {
    @Test
    fun cameraSelectionFromPreview_mapsPreviewToEventDraft() {
        val selection = cameraSelectionFromPreview(width = 1080, height = 1440)

        assertEquals("相机拍照预览 1080x1440", selection.source)
        assertEquals("拍照导入的活动海报", selection.item.title)
        assertEquals("活动海报", selection.item.scene)
        assertEquals("相机 OCR 草稿：AI应用分享会 4月24日19:30 图书馆报告厅 报名截止今晚22:00", selection.item.rawText)
    }

    @Test
    fun gallerySelectionFromImage_mapsImageLabelToCourseDraft() {
        val selection = gallerySelectionFromImage("course-screenshot.png")

        assertEquals("相册图片 course-screenshot.png", selection.source)
        assertEquals("相册导入的课程通知", selection.item.title)
        assertEquals("课程通知", selection.item.scene)
        assertEquals("相册 OCR 草稿：高数A班今晚18:30改到B203，作业第5章今晚22:00前提交。", selection.item.rawText)
    }

    @Test
    fun screenshotSelectionFromCandidate_keepsAssistantDraftPendingAndSampleFree() {
        val selection = screenshotSelectionFromCandidate(
            ScreenshotCandidate(
                contentUri = "content://media/external/images/media/99",
                createdAtMillis = 1_777_000_000_000L,
                width = 1260,
                height = 2800,
                displayNameDigest = "digest",
            )
        )

        assertEquals("截图助手导入 1260x2800", selection.source)
        assertEquals("待解析截图", selection.item.title)
        assertEquals("截图导入", selection.item.scene)
        assertEquals("待确认", selection.item.time)
        assertEquals("待确认", selection.item.location)
        assertEquals("待确认", selection.item.status)
        assertEquals("截图助手导入：将自动请求云侧解析，可在 OCR 文本草稿中校对后重试。", selection.item.rawText)
    }

    @Test
    fun selectionFromCaptureDraft_routesOnlyCameraDraftToEventSample() {
        val customDraft = CaptureDraft(
            channel = "share",
            sourceLabel = "系统分享文本",
            rawText = "高数A班今晚18:30改到B203",
        )

        val selection = selectionFromCaptureDraft(customDraft)

        assertEquals("系统分享文本", selection.source)
        assertEquals("相册导入的课程通知", selection.item.title)
        assertEquals("高数A班今晚18:30改到B203", selection.item.rawText)
    }

    @Test
    fun captureDraftFromInput_preservesOriginalAndThumbnailUrisSeparately() {
        val draft = captureDraftFromInput(
            input = CaptureInput(
                sourceType = CaptureSourceType.Gallery,
                sourceLabel = "相册图片 course-screenshot.png",
                localImageUri = "content://media/external/images/media/42",
                thumbnailUri = "file:/private-cache/shike-image-thumbnails/thumb-42.jpg",
            ),
            engine = MockOcrEngine(),
        )

        assertEquals("content://media/external/images/media/42", draft.localImageUri)
        assertEquals("content://media/external/images/media/42", draft.sourceMediaStoreUri)
        assertEquals("file:/private-cache/shike-image-thumbnails/thumb-42.jpg", draft.thumbnailUri)
        assertEquals(true, draft.canDeleteOriginal)
        assertEquals(ScreenshotDeleteState.NotRequested, draft.deleteState)
        assertEquals(ImageCleanupStatus.NOT_REQUESTED, draft.imageCleanupStatus)
    }

    @Test
    fun captureDraftFromInput_keepsCameraThumbnailOutOfOriginalMediaUri() {
        val draft = captureDraftFromInput(
            input = CaptureInput(
                sourceType = CaptureSourceType.Camera,
                sourceLabel = "相机拍照预览 1080x1440",
                thumbnailUri = "file:/private-cache/shike-image-thumbnails/camera-thumb.jpg",
            ),
            engine = MockOcrEngine(),
        )

        assertEquals(null, draft.localImageUri)
        assertEquals(null, draft.sourceMediaStoreUri)
        assertEquals("file:/private-cache/shike-image-thumbnails/camera-thumb.jpg", draft.thumbnailUri)
        assertEquals(false, draft.canDeleteOriginal)
        assertEquals(ScreenshotDeleteState.NotAvailable, draft.deleteState)
        assertEquals(ImageCleanupStatus.NOT_SUPPORTED, draft.imageCleanupStatus)
    }

    @Test
    fun captureDraftDeleteState_tracksSystemConfirmationStates() {
        val requesting = CaptureDraft(
            channel = "gallery",
            sourceLabel = "相册图片 course-screenshot.png",
            rawText = "OCR 草稿",
            localImageUri = "content://media/external/images/media/42",
            imageCleanupStatus = ImageCleanupStatus.DELETE_REQUESTED,
        )
        val deleted = requesting.copy(imageCleanupStatus = ImageCleanupStatus.DELETED)
        val failed = requesting.copy(imageCleanupStatus = ImageCleanupStatus.FAILED)

        assertEquals(true, requesting.canDeleteOriginal)
        assertEquals(ScreenshotDeleteState.RequestingSystemConfirmation, requesting.deleteState)
        assertEquals(ScreenshotDeleteState.Deleted, deleted.deleteState)
        assertEquals(ScreenshotDeleteState.Failed, failed.deleteState)
    }

    @Test
    fun backendSourceTypeFromCaptureSource_mapsAllProductEntrypoints() {
        assertEquals("screenshot", backendSourceTypeFromCaptureSource("相册图片 course-screenshot.png"))
        assertEquals("screenshot", backendSourceTypeFromCaptureSource("截图助手导入 1260x2800"))
        assertEquals("camera", backendSourceTypeFromCaptureSource("相机拍照预览 1080x1440"))
        assertEquals("share_text", backendSourceTypeFromCaptureSource("文本分享入口（待确认，未落盘）"))
        assertEquals("manual", backendSourceTypeFromCaptureSource("手动输入入口：请编辑 OCR 文本草稿后选择后端解析或离线样例。"))
    }
}
