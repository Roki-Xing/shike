package cn.shike.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import cn.shike.app.domain.ShikeItem

@Composable
fun ActionPlannerExecutionControls(
    item: ShikeItem,
    isConfirmed: Boolean,
    executionResults: List<ExecutionResult>,
    onAddCalendar: (ShikeItem) -> Unit,
    onReminder: (ShikeItem) -> Unit,
    onOpenMap: (ShikeItem) -> Unit,
) {
    val gate = executionActionGateFor(item, isConfirmed)
    val labels = executionActionButtonLabelsFor(item, isConfirmed, executionResults)
    val locationMissing = item.location.isBlank() || item.location == "待确认"
    Column(verticalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
        PlannerStepBlock(
            title = "1. 保存日历草稿",
            status = if (gate.canUseCalendar) "这是建议时间，保存前请确认" else "确认具体时间后再保存更稳妥",
        ) {
            Button(
                onClick = { onAddCalendar(item) },
                enabled = gate.canUseCalendar,
                modifier = Modifier.fillMaxWidth(),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF0F766E)),
            ) { Text(if (gate.canUseCalendar) "打开日历草稿" else labels.calendar) }
        }
        PlannerStepBlock(
            title = "2. 开启提醒",
            status = if (gate.canUseReminder) "保存日历后，可以设置提前提醒" else "确认时间后可开启",
        ) {
            OutlinedButton(onClick = { onReminder(item) }, enabled = gate.canUseReminder, modifier = Modifier.fillMaxWidth()) {
                Text(labels.reminder)
            }
        }
        if (locationMissing) {
            PlannerStepBlock(
                title = "地点",
                status = "地点还没识别到，不影响先保存日历草稿",
            ) {
                OutlinedButton(onClick = {}, enabled = false, modifier = Modifier.fillMaxWidth()) {
                    Text("补地点")
                }
            }
        } else {
            PlannerStepBlock(
                title = "地点",
                status = locationPlannerStatus(item),
            ) {
                OutlinedButton(onClick = { onOpenMap(item) }, enabled = gate.canUseMap, modifier = Modifier.fillMaxWidth()) {
                    Text(labels.map)
                }
            }
        }
    }
}

@Composable
private fun PlannerStepBlock(title: String, status: String, action: @Composable () -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(5.dp), modifier = Modifier.fillMaxWidth()) {
        Text(title, color = ShikeColors.Ink, fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
        Text(status, style = ShikeTypography.Caption)
        action()
    }
}

@Composable
fun CalendarDraftReceipt(
    onSaved: () -> Unit,
) {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
        Text("日历草稿已打开，请确认你是否已在系统日历里保存", color = ShikeColors.Ink, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
            Button(onClick = onSaved, modifier = Modifier.weight(1f), colors = ButtonDefaults.buttonColors(containerColor = ShikeColors.Brand)) {
                Text("我已保存")
            }
            OutlinedButton(onClick = {}, modifier = Modifier.weight(1f)) {
                Text("还没保存")
            }
        }
    }
}

private fun locationPlannerStatus(item: ShikeItem): String =
    when {
        isCampusRoomCode(item.location) -> "${item.location} 是校内教室，建议先复制地点"
        else -> "可查看路线；失败时会复制地点并保留行动卡"
    }
