package cn.shike.app

import cn.shike.app.domain.ShikeItem
import cn.shike.app.system.calendarDraftFrom
import cn.shike.app.system.scheduledReminderFrom
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class PreparationCalendarReminderTest {
    @Test
    fun calendarDraft_includesPreparationItemsInDescription() {
        val item = englishCourseWithBookReminder()

        val draft = calendarDraftFrom(item)

        assertTrue(draft.description.contains("来源：拾刻识别"))
        assertTrue(draft.description.contains("任务：上英语口语，记得带书"))
        assertTrue(draft.description.contains("地点：E520"))
        assertTrue(draft.description.contains("准备事项：带书"))
        assertTrue(draft.description.contains("打开系统日历新增页"))
        assertTrue(draft.description.contains("由用户在日历中保存"))
    }

    @Test
    fun scheduledReminder_includesPreparationItemsInDetail() {
        val item = englishCourseWithBookReminder()

        val reminder = scheduledReminderFrom(item, nowMillis = 0L)

        assertEquals("英语口语课 · E520 · 记得带书", reminder.detail)
    }

    private fun englishCourseWithBookReminder(): ShikeItem =
        ShikeItem(
            title = "英语口语课",
            scene = "课程通知",
            time = "明天早上九点",
            location = "E520",
            status = "待确认",
            actions = listOf("加入日历", "课前提醒", "打开地图"),
            startEpochMillis = 1_800_000L,
            rawText = "任务：上英语口语，记得带书",
        )
}
