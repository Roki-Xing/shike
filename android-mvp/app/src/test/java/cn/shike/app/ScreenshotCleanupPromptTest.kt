package cn.shike.app

import cn.shike.app.data.ImageCleanupStatus
import cn.shike.app.ui.cleanupStatusLabel
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Test

class ScreenshotCleanupPromptTest {
    @Test
    fun cleanupStatusLabel_usesUserFacingChineseCopy() {
        val labels = ImageCleanupStatus.entries.map { cleanupStatusLabel(it) }

        assertEquals("当前来源不支持删除原图", cleanupStatusLabel(ImageCleanupStatus.NOT_SUPPORTED))
        assertEquals("等待你的选择", cleanupStatusLabel(ImageCleanupStatus.NOT_REQUESTED))
        assertEquals("已选择保留原图", cleanupStatusLabel(ImageCleanupStatus.USER_KEPT))
        assertEquals("正在等待系统确认删除", cleanupStatusLabel(ImageCleanupStatus.DELETE_REQUESTED))
        assertEquals("已删除原截图", cleanupStatusLabel(ImageCleanupStatus.DELETED))
        assertEquals("系统确认未完成", cleanupStatusLabel(ImageCleanupStatus.FAILED))
        assertFalse(labels.any { it.contains("_") })
    }
}
