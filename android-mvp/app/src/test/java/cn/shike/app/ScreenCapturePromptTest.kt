package cn.shike.app

import cn.shike.app.system.visibleScreenCapturePrompt
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Assert.assertFalse
import org.junit.Test

class ScreenCapturePromptTest {
    @Test
    fun visibleScreenCapturePrompt_keepsAndroidCallbackBoundaryHonest() {
        val prompt = visibleScreenCapturePrompt()

        assertEquals("检测到当前页面截图", prompt.title)
        assertTrue(prompt.body.contains("不会直接获得图片"))
        assertTrue(prompt.body.contains("导入页选择这张截图"))
        assertTrue(prompt.secondaryActionLabel.contains("移入回收站"))
        assertFalse(prompt.body.contains("后台监听"))
        assertFalse(prompt.body.contains("全局监听"))
        assertFalse(prompt.body.contains("自动读取"))
    }
}
