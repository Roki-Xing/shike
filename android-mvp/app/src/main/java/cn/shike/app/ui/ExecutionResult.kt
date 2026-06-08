package cn.shike.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import cn.shike.app.domain.ShikeItem
import cn.shike.app.reminderPermissionFallbackCopyFor

data class ExecutionResult(
    val action: String,
    val status: String,
    val detail: String,
)

fun pendingExecutionResults(): List<ExecutionResult> = listOf(
    ExecutionResult("日历", "待确认", "确认字段后才会打开系统新增日程页。"),
    ExecutionResult("提醒", "待确认", "确认字段后才会调度本地定时提醒。"),
    ExecutionResult("地图", "待确认", "确认地点后才会打开地图路线。"),
)

fun List<ExecutionResult>.recordExecutionResult(result: ExecutionResult): List<ExecutionResult> =
    filterNot { it.action == result.action } + result

fun calendarExecutionResult(): ExecutionResult =
    ExecutionResult("日历", "已请求", "已打开系统新增页，需用户在系统日历中保存。")

fun reminderExecutionResult(item: ShikeItem? = null): ExecutionResult =
    ExecutionResult(
        "提醒",
        "已调度",
        item?.let { reminderPermissionFallbackCopyFor(it).executionDetail }
            ?: "已请求本地定时提醒；通知权限拒绝时进入 permission_blocked 并保留行动卡。",
    )

fun mapExecutionResult(): ExecutionResult =
    ExecutionResult("地图", "已请求", "已打开地图 deeplink；地图不可用时保留地点。")

fun imageCleanupRequestedResult(): ExecutionResult =
    ExecutionResult("原截图", "已请求", "已打开系统确认页；用户确认后才会删除系统相册原截图。")

fun imageCleanupDeletedResult(): ExecutionResult =
    ExecutionResult("原截图", "已删除", "系统已确认，原截图已删除。")

fun imageCleanupKeptResult(): ExecutionResult =
    ExecutionResult("原截图", "已保留", "用户选择保留原截图，拾刻不会修改相册。")

fun imageCleanupFailedResult(): ExecutionResult =
    ExecutionResult("原截图", "未完成", "系统确认未完成或来源不支持，未修改原截图。")

@Composable
fun ExecutionResultPanel(results: List<ExecutionResult>) {
    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
        results.forEach { result ->
            Pill(
                "${result.action} · ${result.status}",
                Color(0xFFF4F7FA),
                Color(0xFF344054),
                Color(0xFFE4E7EC),
            )
            KeyValue("${result.action}执行结果", result.detail)
        }
    }
}
