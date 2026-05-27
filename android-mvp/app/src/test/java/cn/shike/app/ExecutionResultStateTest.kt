package cn.shike.app

import cn.shike.app.ui.ExecutionResult
import cn.shike.app.ui.calendarExecutionResult
import cn.shike.app.ui.mapExecutionResult
import cn.shike.app.ui.pendingExecutionResults
import cn.shike.app.ui.recordExecutionResult
import cn.shike.app.ui.reminderExecutionResult
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class ExecutionResultStateTest {
    @Test
    fun pendingExecutionResults_startsAllActionsInConfirmationState() {
        val pending = pendingExecutionResults()

        assertEquals(listOf("日历", "提醒", "地图"), pending.map { it.action })
        assertEquals(listOf("待确认", "待确认", "待确认"), pending.map { it.status })
        assertTrue(pending[0].detail.contains("确认字段后"))
        assertTrue(pending[1].detail.contains("调度本地定时提醒"))
        assertTrue(pending[2].detail.contains("确认地点后"))
    }

    @Test
    fun recordExecutionResult_replacesOnlyMatchingActionAndAppendsLatestResult() {
        val current = pendingExecutionResults().recordExecutionResult(calendarExecutionResult())

        val next = current.recordExecutionResult(ExecutionResult("日历", "已保存", "用户在系统日历中保存。"))

        assertEquals(listOf("提醒", "地图", "日历"), next.map { it.action })
        assertEquals("已保存", next.last().status)
        assertEquals("用户在系统日历中保存。", next.last().detail)
    }

    @Test
    fun executionResultFactories_keepPermissionAndFallbackWording() {
        assertEquals("已请求", calendarExecutionResult().status)
        assertTrue(calendarExecutionResult().detail.contains("系统日历"))
        assertEquals("已调度", reminderExecutionResult().status)
        assertTrue(reminderExecutionResult().detail.contains("permission_blocked"))
        assertEquals("已请求", mapExecutionResult().status)
        assertTrue(mapExecutionResult().detail.contains("地图不可用"))
    }
}
