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
}
