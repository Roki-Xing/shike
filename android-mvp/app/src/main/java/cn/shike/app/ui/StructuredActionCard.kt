package cn.shike.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun StructuredActionCard(
    model: ActionCardUiModel,
    onConfirmAndPlan: (() -> Unit)? = null,
    onEdit: (() -> Unit)? = null,
    onEditTime: (() -> Unit)? = null,
    onEditLocation: (() -> Unit)? = null,
    onEditPreparation: (() -> Unit)? = null,
    onEditSourceText: (() -> Unit)? = null,
) {
    Column(verticalArrangement = Arrangement.spacedBy(12.dp), modifier = Modifier.fillMaxWidth()) {
        ActionCardHero(model, onEditTime, onEditLocation)
        PreparationSection(model.preparationItems, onEditPreparation)
        SuggestedPlanSection(model.actions)
        ConfirmationSection(model.userWarnings)
        FieldEditRow(onEditTime, onEditLocation, onEditPreparation, onEditSourceText)
        if (onConfirmAndPlan != null && onEdit != null) {
            ConfirmActionSection(
                onConfirmAndPlan = onConfirmAndPlan,
                onEdit = onEdit,
            )
        }
    }
}

@Composable
private fun ActionCardHero(
    model: ActionCardUiModel,
    onEditTime: (() -> Unit)?,
    onEditLocation: (() -> Unit)?,
) {
    Column(verticalArrangement = Arrangement.spacedBy(4.dp), modifier = Modifier.fillMaxWidth()) {
        Text("事项", style = ShikeTypography.Caption)
        Text(model.title, color = ShikeColors.Ink, fontSize = 22.sp, fontWeight = FontWeight.Bold)
        Text(
            listOf(model.time, model.location).filter { it.isNotBlank() && it != "待确认" }.joinToString(" · ").ifBlank { "时间地点待确认" },
            style = ShikeTypography.Body,
        )
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
            onEditTime?.let { OutlinedButton(onClick = it, modifier = Modifier.weight(1f)) { Text("改时间") } }
            onEditLocation?.let { OutlinedButton(onClick = it, modifier = Modifier.weight(1f)) { Text("改地点") } }
        }
        Text(model.task, style = ShikeTypography.Caption)
    }
}

@Composable
private fun PreparationSection(items: List<String>, onEditPreparation: (() -> Unit)?) {
    if (items.isEmpty() && onEditPreparation == null) return
    Column(
        verticalArrangement = Arrangement.spacedBy(6.dp),
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .padding(10.dp),
    ) {
        Text("准备事项", color = ShikeColors.Warning, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
        if (items.isEmpty()) {
            Text("暂无准备事项", color = ShikeColors.Muted, fontSize = 13.sp)
        } else {
            items.forEach { Text(it, color = ShikeColors.Ink, fontSize = 14.sp, fontWeight = FontWeight.SemiBold) }
        }
        onEditPreparation?.let {
            OutlinedButton(onClick = it, modifier = Modifier.fillMaxWidth()) { Text("改准备") }
        }
    }
}

@Composable
private fun SuggestedPlanSection(actions: List<String>) {
    Text("建议动作", style = ShikeTypography.Caption)
    ActionPillRow(actions)
}

@Composable
private fun ConfirmationSection(warnings: List<String>) {
    if (warnings.isEmpty()) {
        Text("关键字段已可确认；系统动作仍需用户手动确认。", style = ShikeTypography.Caption)
        return
    }
    Column(verticalArrangement = Arrangement.spacedBy(6.dp), modifier = Modifier.fillMaxWidth()) {
        Text("需要确认", color = ShikeColors.Warning, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
        warnings.take(3).forEach { warning ->
            Text(warning, color = Color(0xFF7C2D12), fontSize = 12.sp)
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

@Composable
private fun FieldEditRow(
    onEditTime: (() -> Unit)?,
    onEditLocation: (() -> Unit)?,
    onEditPreparation: (() -> Unit)?,
    onEditSourceText: (() -> Unit)?,
) {
    if (listOf(onEditTime, onEditLocation, onEditPreparation, onEditSourceText).all { it == null }) return
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
        onEditSourceText?.let {
            OutlinedButton(onClick = it, modifier = Modifier.weight(1f)) { Text("改原文") }
        }
    }
}

@Composable
private fun ConfirmActionSection(
    onConfirmAndPlan: () -> Unit,
    onEdit: () -> Unit,
) {
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
        Button(
            onClick = onConfirmAndPlan,
            modifier = Modifier.weight(1.35f),
            colors = ButtonDefaults.buttonColors(containerColor = ShikeColors.Brand),
        ) {
            Text("确认并安排")
        }
        OutlinedButton(onClick = onEdit, modifier = Modifier.weight(1f)) {
            Text("修改")
        }
    }
}
