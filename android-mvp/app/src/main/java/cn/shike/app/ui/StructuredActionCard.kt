package cn.shike.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun StructuredActionCard(model: ActionCardUiModel) {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
        KeyValue("课程/事项", model.sceneLabel)
        KeyValue("时间", model.time)
        KeyValue("地点", model.location)
        KeyValue("任务", model.task)
        ActionPillRow(model.actions)
        if (model.risks.isNotEmpty()) {
            KeyValue("风险", model.risks.joinToString("；"))
        }
        if (model.missingFields.isNotEmpty()) {
            KeyValue("缺失项", model.missingFields.joinToString("、"))
        }
        if (model.risks.isEmpty() && model.missingFields.isEmpty()) {
            Text("关键字段已可确认；系统动作仍需用户手动确认。", style = ShikeTypography.Caption)
        }
    }
}

@Composable
private fun ActionPillRow(actions: List<String>) {
    Row(horizontalArrangement = Arrangement.spacedBy(6.dp), modifier = Modifier.fillMaxWidth()) {
        actions.take(3).forEach { action ->
            Pill(
                label = action,
                background = ShikeColors.BrandSoft,
                contentColor = ShikeColors.Brand,
                modifier = Modifier.weight(1f),
            )
        }
    }
}
