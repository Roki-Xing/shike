package cn.shike.app

import cn.shike.app.domain.ShikeItem
import cn.shike.app.ui.calendarExecutionResult
import cn.shike.app.ui.pendingExecutionResults
import cn.shike.app.ui.recordExecutionResult
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class ExecutionResultActionsTest {
    private val item = ShikeItem(
        title = "AI应用分享会",
        scene = "活动海报",
        time = "4月24日 19:30",
        location = "图书馆报告厅",
        status = "待确认",
        actions = listOf("日历", "提醒", "地图"),
        startEpochMillis = 1_776_984_600_000L,
        rawText = "AI应用分享会 4月24日19:30 图书馆报告厅",
    )

    @Test
    fun runCalendarExecution_recordsResultBeforeSystemAction() {
        val events = mutableListOf<String>()
        var updated = emptyList<cn.shike.app.ui.ExecutionResult>()

        runCalendarExecution(
            item = item,
            currentResults = pendingExecutionResults(),
            updateResults = { next ->
                updated = next
                events += "update:${next.last().action}:${next.last().status}"
            },
            action = { executed ->
                events += "action:${executed.title}"
            },
        )

        assertEquals(listOf("update:日历:已请求", "action:AI应用分享会"), events)
        assertEquals(listOf("提醒", "地图", "日历"), updated.map { it.action })
        assertEquals("待确认", updated[0].status)
        assertEquals("已请求", updated.last().status)
    }

    @Test
    fun runReminderExecution_recordsPermissionAwareReminderResult() {
        var updated = emptyList<cn.shike.app.ui.ExecutionResult>()
        var executedItem: ShikeItem? = null

        runReminderExecution(
            item = item,
            currentResults = pendingExecutionResults(),
            updateResults = { next -> updated = next },
            action = { executed -> executedItem = executed },
        )

        assertEquals(item, executedItem)
        assertEquals(listOf("日历", "地图", "提醒"), updated.map { it.action })
        assertEquals("已调度", updated.last().status)
        assertTrue(updated.last().detail.contains("permission_blocked"))
    }

    @Test
    fun runMapExecution_preservesExistingCalendarResult() {
        val current = pendingExecutionResults().recordExecutionResult(calendarExecutionResult())
        var updated = emptyList<cn.shike.app.ui.ExecutionResult>()

        runMapExecution(
            item = item,
            currentResults = current,
            updateResults = { next -> updated = next },
            action = {},
        )

        assertEquals(listOf("提醒", "日历", "地图"), updated.map { it.action })
        assertEquals("已请求", updated.first { it.action == "日历" }.status)
        assertEquals("已请求", updated.first { it.action == "地图" }.status)
    }
}
