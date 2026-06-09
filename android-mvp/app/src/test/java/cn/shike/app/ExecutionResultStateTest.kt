package cn.shike.app

import cn.shike.app.ui.ExecutionResult
import cn.shike.app.ui.calendarExecutionResult
import cn.shike.app.ui.imageCleanupDeletedResult
import cn.shike.app.ui.imageCleanupFailedResult
import cn.shike.app.ui.imageCleanupKeptResult
import cn.shike.app.ui.imageCleanupRequestedResult
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

    @Test
    fun imageCleanupResults_distinguishSystemConfirmationStates() {
        assertEquals("已请求", imageCleanupRequestedResult().status)
        assertTrue(imageCleanupRequestedResult().detail.contains("系统确认"))
        assertEquals("已移入回收站", imageCleanupDeletedResult().status)
        assertTrue(imageCleanupDeletedResult().detail.contains("移入系统回收站"))
        assertEquals("已保留", imageCleanupKeptResult().status)
        assertTrue(imageCleanupKeptResult().detail.contains("用户选择保留"))
        assertEquals("未完成", imageCleanupFailedResult().status)
        assertTrue(imageCleanupFailedResult().detail.contains("未修改原截图"))
    }
}
