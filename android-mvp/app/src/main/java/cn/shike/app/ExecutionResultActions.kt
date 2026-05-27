package cn.shike.app

import cn.shike.app.domain.ShikeItem
import cn.shike.app.ui.ExecutionResult
import cn.shike.app.ui.calendarExecutionResult
import cn.shike.app.ui.mapExecutionResult
import cn.shike.app.ui.recordExecutionResult
import cn.shike.app.ui.reminderExecutionResult

fun runCalendarExecution(
    item: ShikeItem,
    currentResults: List<ExecutionResult>,
    updateResults: (List<ExecutionResult>) -> Unit,
    action: (ShikeItem) -> Unit,
) {
    runExecution(calendarExecutionResult(), item, currentResults, updateResults, action)
}

fun runReminderExecution(
    item: ShikeItem,
    currentResults: List<ExecutionResult>,
    updateResults: (List<ExecutionResult>) -> Unit,
    action: (ShikeItem) -> Unit,
) {
    runExecution(reminderExecutionResult(item), item, currentResults, updateResults, action)
}

fun runMapExecution(
    item: ShikeItem,
    currentResults: List<ExecutionResult>,
    updateResults: (List<ExecutionResult>) -> Unit,
    action: (ShikeItem) -> Unit,
) {
    runExecution(mapExecutionResult(), item, currentResults, updateResults, action)
}

private fun runExecution(
    result: ExecutionResult,
    item: ShikeItem,
    currentResults: List<ExecutionResult>,
    updateResults: (List<ExecutionResult>) -> Unit,
    action: (ShikeItem) -> Unit,
) {
    updateResults(currentResults.recordExecutionResult(result))
    action(item)
}
