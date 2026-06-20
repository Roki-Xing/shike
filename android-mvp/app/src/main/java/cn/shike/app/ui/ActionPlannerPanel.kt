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
    SectionCard("行动编排") {
        Column(verticalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
            Text("将执行以下动作", color = Color(0xFF667085), fontSize = 12.sp)
            PlannedActionRow("加入日历", calendarPlanCopy(item))
            PlannedActionRow("设置提醒", reminderPlanCopy(item))
            PlannedActionRow("打开地图", mapPlanCopy(item))
            PlannedActionRow("处理后清理截图", "完成后询问是否移入系统回收站")
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
            if (isConfirmed) "已打开系统日历新增页后仍需你在日历中保存；权限拒绝时会保留行动卡。"
            else "先确认字段；未确认前不会打开外部日历、通知或地图。",
            color = Color(0xFF667085),
            fontSize = 12.sp,
        )
        if (!isConfirmed || item.time == "待确认") {
            Pill("补时间", ShikeColors.BrandSoft, ShikeColors.Brand, modifier = Modifier.fillMaxWidth())
        }
        if (!isConfirmed || item.location == "待确认") {
            Pill("补地点", ShikeColors.BrandSoft, ShikeColors.Brand, modifier = Modifier.fillMaxWidth())
        }
        Pill("存入待确认", Color(0xFFF4F7FA), Color(0xFF344054), Color(0xFFE4E7EC), Modifier.fillMaxWidth())
        if (isConfirmed && selectedSourceMediaStoreUri != null && sourceImageCleanupStatus == ImageCleanupStatus.NOT_REQUESTED) {
            ScreenshotCleanupPrompt(
                status = sourceImageCleanupStatus,
                onDelete = onDeleteSourceImage,
                onKeep = onKeepSourceImage,
            )
        }
        Button(
            onClick = onCompleteArrangement,
            enabled = isConfirmed,
            modifier = Modifier.fillMaxWidth(),
            colors = ButtonDefaults.buttonColors(containerColor = ShikeColors.Brand),
        ) {
            Text("完成安排")
        }
    }
}

@Composable
private fun PlannedActionRow(label: String, detail: String) {
    Column(verticalArrangement = Arrangement.spacedBy(2.dp), modifier = Modifier.fillMaxWidth()) {
        Text("✓ $label", color = ShikeColors.Ink, fontSize = 14.sp)
        Text(detail, color = Color(0xFF667085), fontSize = 12.sp)
    }
}

private fun calendarPlanCopy(item: ShikeItem): String =
    listOf(item.title, item.time, item.location).filter { it.isNotBlank() && it != "待确认" }.joinToString("，").ifBlank { "补充时间后可用" }

private fun reminderPlanCopy(item: ShikeItem): String =
    listOf("课前提醒", item.title).filter { it.isNotBlank() }.joinToString("：")

private fun mapPlanCopy(item: ShikeItem): String =
    item.location.takeIf { it.isNotBlank() && it != "待确认" } ?: "补充地点后可用"
