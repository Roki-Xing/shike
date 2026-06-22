package cn.shike.app

import cn.shike.app.ui.ExecutionResult
import cn.shike.app.ui.calendarExecutionResult
import cn.shike.app.ui.completionSummaryState
import cn.shike.app.ui.imageCleanupDeletedResult
import cn.shike.app.ui.imageCleanupKeptResult
import cn.shike.app.ui.mapExecutionResult
import cn.shike.app.ui.reminderExecutionResult
import org.junit.Assert.assertEquals
import org.junit.Test

class CompletionSummaryStateTest {
    @Test
    fun completionSummaryState_prefersRecordedExecutionResults() {
        val state = completionSummaryState(
            listOf(
                calendarExecutionResult(),
                reminderExecutionResult(),
                mapExecutionResult(),
                imageCleanupDeletedResult(),
            ),
        )

        assertEquals("日历：已打开系统新增页，等待你在日历中保存", state.calendarStatus)
        assertEquals("提醒：已调度", state.reminderStatus)
        assertEquals("地图：已打开地图", state.mapStatus)
        assertEquals("原截图：已移入回收站", state.sourceImageStatus)
    }

    @Test
    fun completionSummaryState_handlesKeptSourceImage() {
        val state = completionSummaryState(
            listOf(
                ExecutionResult("日历", "待确认", "确认字段后才会打开系统新增日程页。"),
                imageCleanupKeptResult(),
            ),
        )

        assertEquals("日历：未打开", state.calendarStatus)
        assertEquals("提醒：未设置", state.reminderStatus)
        assertEquals("地图：未打开", state.mapStatus)
        assertEquals("原截图：已保留", state.sourceImageStatus)
    }
}
