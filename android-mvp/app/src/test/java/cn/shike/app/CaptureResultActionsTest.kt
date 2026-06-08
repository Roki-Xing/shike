package cn.shike.app

import cn.shike.app.data.ScreenshotCandidate
import cn.shike.app.domain.ShikeItem
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Test

class CaptureResultActionsTest {
    @Test
    fun applyCameraPreviewSizeSelection_persistsCameraDraftAndSource() {
        val persisted = mutableListOf<Pair<ShikeItem, String>>()

        applyCameraPreviewSizeSelection(width = 1080, height = 1440) { item, source ->
            persisted += item to source
        }

        assertEquals("相机拍照预览 1080x1440", persisted.single().second)
        assertEquals("拍照导入的活动海报", persisted.single().first.title)
        assertEquals("活动海报", persisted.single().first.scene)
        assertEquals(
            "相机 OCR 草稿：AI应用分享会 4月24日19:30 图书馆报告厅 报名截止今晚22:00",
            persisted.single().first.rawText,
        )
    }

    @Test
    fun applyGalleryImageSelection_persistsGalleryDraftAndSource() {
        val persisted = mutableListOf<Pair<ShikeItem, String>>()

        applyGalleryImageSelection("course-screenshot.png") { item, source ->
            persisted += item to source
        }

        assertEquals("相册图片 course-screenshot.png", persisted.single().second)
        assertEquals("相册导入的课程通知", persisted.single().first.title)
        assertEquals("课程通知", persisted.single().first.scene)
        assertEquals(
            "相册 OCR 草稿：高数A班今晚18:30改到B203，作业第5章今晚22:00前提交。",
            persisted.single().first.rawText,
        )
    }

    @Test
    fun applyScreenshotCandidateSelection_persistsPendingDraftWithoutSampleFields() {
        val persisted = mutableListOf<Pair<ShikeItem, String>>()
        val candidate = ScreenshotCandidate(
            contentUri = "content://media/external/images/media/42",
            createdAtMillis = 1_777_000_000_000L,
            width = 1260,
            height = 2800,
            displayNameDigest = "abc123",
        )

        applyScreenshotCandidateSelection(candidate) { item, source ->
            persisted += item to source
        }

        val item = persisted.single().first
        assertEquals("截图助手导入 1260x2800", persisted.single().second)
        assertEquals("待解析截图", item.title)
        assertEquals("截图导入", item.scene)
        assertEquals("待确认", item.time)
        assertEquals("待确认", item.location)
        assertEquals("待确认", item.status)
        assertEquals(listOf("先存入待确认"), item.actions)
        assertFalse(item.rawText.contains("B203"))
        assertFalse(item.rawText.contains("18:30"))
        assertFalse(item.rawText.contains("22:00"))
        assertFalse(item.rawText.contains("第5章"))
    }
}
