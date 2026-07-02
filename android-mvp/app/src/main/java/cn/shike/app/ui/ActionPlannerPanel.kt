package cn.shike.app.ui

import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
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
    onCompleteArrangement: () -> Unit,
) {
    val calendarDraftOpened = executionResults.any { it.action == "日历" && it.status != "建议" }
    SectionCard("下一步，先完成这 2 件") {
        ActionReadinessBar(actionReadinessUiModelFrom(item, executionResults))
        Text("先保存日历草稿，再按需要开启提醒或处理地点。", color = Color(0xFF667085), style = ShikeTypography.Caption)
        ActionPlannerExecutionControls(
            item = item,
            isConfirmed = isConfirmed,
            executionResults = executionResults,
            onAddCalendar = onAddCalendar,
            onReminder = onReminder,
            onOpenMap = onOpenMap,
        )
        if (calendarDraftOpened) {
            CalendarDraftReceipt(onSaved = onCompleteArrangement)
        }
        OutlinedButton(
            onClick = {},
            modifier = Modifier.fillMaxWidth(),
        ) {
            Text("先存入待确认")
        }
        if (isConfirmed && selectedSourceMediaStoreUri != null && sourceImageCleanupStatus == ImageCleanupStatus.NOT_REQUESTED) {
            ScreenshotCleanupPrompt(
                status = sourceImageCleanupStatus,
                onDelete = onDeleteSourceImage,
                onKeep = onKeepSourceImage,
            )
        }
        Text(
            if (isConfirmed) "外部动作都由你点击触发；失败时会保留行动卡。"
            else "先确认字段；未确认前不会打开外部日历、通知或地图。",
            color = Color(0xFF667085),
            style = ShikeTypography.Caption,
        )
    }
}
