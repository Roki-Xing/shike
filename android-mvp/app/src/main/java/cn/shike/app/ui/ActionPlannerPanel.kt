package cn.shike.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import cn.shike.app.data.ImageCleanupStatus
import cn.shike.app.domain.ShikeItem

@Composable
fun ActionPlannerPanel(
    item: ShikeItem,
    isConfirmed: Boolean,
    executionResults: List<ExecutionResult>,
    sourceImageCleanupStatus: ImageCleanupStatus,
    selectedSourceMediaStoreUri: String?,
    onDeleteSourceImage: () -> Unit,
    onKeepSourceImage: () -> Unit,
    onAddCalendar: (ShikeItem) -> Unit,
    onReminder: (ShikeItem) -> Unit,
    onOpenMap: (ShikeItem) -> Unit,
) {
    SectionCard("行动编排") {
        Column(verticalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
            item.actions.take(3).forEach { action ->
                Pill(action, Color(0xFFF4F7FA), Color(0xFF344054), Color(0xFFE4E7EC), Modifier.fillMaxWidth())
            }
        }
        ActionPlannerExecutionControls(
            item = item,
            isConfirmed = isConfirmed,
            executionResults = executionResults,
            onAddCalendar = onAddCalendar,
            onReminder = onReminder,
            onOpenMap = onOpenMap,
        )
        Text(
            if (isConfirmed) "权限拒绝时降级为本地行动卡、应用内倒计时或复制地点。"
            else "先确认字段；未确认前不会打开外部日历、通知或地图。",
            color = Color(0xFF667085),
            fontSize = 12.sp,
        )
        if (isConfirmed && selectedSourceMediaStoreUri != null && sourceImageCleanupStatus == ImageCleanupStatus.NOT_REQUESTED) {
            ScreenshotCleanupPrompt(
                status = sourceImageCleanupStatus,
                onDelete = onDeleteSourceImage,
                onKeep = onKeepSourceImage,
            )
        }
        ExecutionResultPanel(executionResults)
    }
}
