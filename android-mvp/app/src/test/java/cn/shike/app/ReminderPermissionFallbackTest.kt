package cn.shike.app

import cn.shike.app.domain.ShikeItem
import cn.shike.app.ui.reminderExecutionResult
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class ReminderPermissionFallbackTest {
    private val item = ShikeItem(
        title = "AI应用分享会",
        scene = "活动海报",
        time = "4月24日 19:30",
        location = "图书馆报告厅",
        status = "已安排",
        actions = listOf("提醒"),
        startEpochMillis = 1_776_984_600_000L,
        rawText = "AI应用分享会 4月24日19:30 图书馆报告厅",
    )

    @Test
    fun reminderPermissionFallbackCopyFor_namesPermissionBlockedAndKeepsCard() {
        val copy = reminderPermissionFallbackCopyFor(item)

        assertTrue(copy.source.contains(REMINDER_PERMISSION_BLOCKED_STATUS))
        assertTrue(copy.source.contains("已保留「AI应用分享会」行动卡"))
        assertTrue(copy.source.contains("开启通知权限后再安排提醒"))
        assertTrue(copy.executionDetail.contains(REMINDER_PERMISSION_BLOCKED_STATUS))
        assertTrue(copy.executionDetail.contains("已请求本地定时提醒"))
    }

    @Test
    fun reminderExecutionResult_usesSharedPermissionFallbackCopy() {
        val result = reminderExecutionResult(item)

        assertEquals("提醒", result.action)
        assertEquals("已调度", result.status)
        assertTrue(result.detail.contains(REMINDER_PERMISSION_BLOCKED_STATUS))
        assertTrue(result.detail.contains("AI应用分享会"))
    }
}
