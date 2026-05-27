package cn.shike.app.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class InitialSelectionMapperTest {
    @Test
    fun buildInitialSelection_sharedTextWinsOverSavedSnapshot() {
        val saved = sampleCourse().copy(title = "本地缓存课程")

        val selection = buildInitialSelection(
            sharedText = "AI应用分享会 今晚 19:30 图书馆报告厅",
            savedItem = saved,
            savedCaptureSource = "本地缓存入口",
        )

        assertEquals("分享导入的活动", selection.item.title)
        assertEquals("活动海报", selection.item.scene)
        assertEquals("文本分享入口（待确认，未落盘）", selection.captureSource)
        assertEquals(InitialTodayState.Ready, selection.todayState)
        assertTrue(selection.item.rawText.contains("AI应用分享会"))
    }

    @Test
    fun buildInitialSelection_savedSnapshotRestoresReadyState() {
        val saved = sampleEvent().copy(title = "已恢复的活动")

        val selection = buildInitialSelection(
            sharedText = null,
            savedItem = saved,
            savedCaptureSource = "上次拍照导入",
        )

        assertEquals(saved, selection.item)
        assertEquals("上次拍照导入", selection.captureSource)
        assertEquals(InitialTodayState.Ready, selection.todayState)
    }

    @Test
    fun buildInitialSelection_noShareNoSavedShowsEmptyState() {
        val selection = buildInitialSelection(
            sharedText = "   ",
            savedItem = null,
            savedCaptureSource = null,
        )

        assertEquals(sampleCourse(), selection.item)
        assertTrue(selection.captureSource.contains("今日行动台空状态"))
        assertTrue(selection.captureSource.contains("截图、拍照、分享或手动输入"))
        assertEquals(InitialTodayState.Empty, selection.todayState)
    }
}
