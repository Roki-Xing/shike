package cn.shike.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

data class CompletionSummaryState(
    val calendarStatus: String,
    val reminderStatus: String,
    val mapStatus: String,
    val sourceImageStatus: String,
)

fun completionSummaryState(results: List<ExecutionResult>): CompletionSummaryState {
    fun resultFor(action: String): ExecutionResult? =
        results.firstOrNull { it.action == action }

    val calendar = resultFor("日历")
    val reminder = resultFor("提醒")
    val map = resultFor("地图")
    val sourceImage = resultFor("原截图")

    return CompletionSummaryState(
        calendarStatus = when (calendar?.status) {
            "已请求" -> "日历：已打开系统新增页，请在日历中保存"
            null, "待确认" -> "日历：未打开"
            else -> "日历：${calendar.detail}"
        },
        reminderStatus = reminder?.let { "提醒：${it.status}" } ?: "提醒：未设置",
        mapStatus = map?.let { "地图：${it.status}" } ?: "地图：未打开",
        sourceImageStatus = when (sourceImage?.status) {
            "已移入回收站" -> "原截图：已移入回收站"
            "已保留" -> "原截图：已保留"
            "已请求" -> "原截图：等待系统确认"
            "未完成" -> "原截图：未修改"
            else -> "原截图：未处理"
        },
    )
}

@Composable
fun CompletionSummaryScreen(
    results: List<ExecutionResult>,
    onReturnHome: () -> Unit,
) {
    val state = completionSummaryState(results)
    SectionCard("已安排") {
        Column(
            verticalArrangement = Arrangement.spacedBy(10.dp),
            modifier = Modifier.fillMaxWidth(),
        ) {
            Text("这张截图已经完成处理，后续可在今日行动台继续追踪。", color = Color(0xFF667085), fontSize = 12.sp)
            KeyValue("日历", state.calendarStatus.removePrefix("日历："))
            KeyValue("提醒", state.reminderStatus.removePrefix("提醒："))
            KeyValue("地图", state.mapStatus.removePrefix("地图："))
            KeyValue("原截图", state.sourceImageStatus.removePrefix("原截图："))
            ExecutionResultPanel(results)
            Button(
                onClick = onReturnHome,
                modifier = Modifier.fillMaxWidth(),
                colors = ButtonDefaults.buttonColors(containerColor = ShikeColors.Brand),
            ) {
                Text("回到今日行动台")
            }
        }
    }
}
