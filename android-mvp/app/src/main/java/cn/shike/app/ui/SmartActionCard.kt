package cn.shike.app.ui

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun SmartActionCard(
    model: SmartActionCardUiModel,
    onConfirmAndPlan: () -> Unit,
    onEditTime: () -> Unit,
    onEditLocation: () -> Unit,
    onEditPreparation: () -> Unit,
    onEditSourceText: () -> Unit,
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        shape = RoundedCornerShape(18.dp),
        border = BorderStroke(1.dp, ShikeColors.Line),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
    ) {
        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                Pill(model.sceneLabel, ShikeColors.BrandSoft, ShikeColors.Brand, borderColor = null, modifier = Modifier.weight(1f))
                Pill("待你确认", ShikeColors.WarningSoft, ShikeColors.Warning, borderColor = null, modifier = Modifier.weight(1f))
            }
            Text(model.title, color = ShikeColors.Ink, fontSize = 23.sp, fontWeight = FontWeight.Bold)
            model.primaryWarning?.let { Text(it, color = ShikeColors.Warning, fontSize = 12.sp, fontWeight = FontWeight.SemiBold) }
            SmartFieldBlock(model.time)
            SmartFieldBlock(model.location)
            ClassPrepPack(model.preparationItems, onEditPreparation)
            EvidenceFold(model.evidenceText, onEditSourceText)
            Button(
                onClick = onConfirmAndPlan,
                modifier = Modifier.fillMaxWidth(),
                colors = ButtonDefaults.buttonColors(containerColor = ShikeColors.Brand),
            ) { Text("确认并安排") }
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                OutlinedButton(onClick = onEditTime, modifier = Modifier.weight(1f)) { Text("改时间") }
                OutlinedButton(onClick = onEditLocation, modifier = Modifier.weight(1f)) { Text("补地点") }
                OutlinedButton(onClick = onEditPreparation, modifier = Modifier.weight(1f)) { Text("改准备") }
            }
        }
    }
}

@Composable
private fun SmartFieldBlock(field: SmartFieldUi) {
    Column(verticalArrangement = Arrangement.spacedBy(4.dp), modifier = Modifier.fillMaxWidth()) {
        Row(horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
            Text(field.label, style = ShikeTypography.Caption)
            Pill(field.state.copyText(), field.state.background(), field.state.contentColor(), borderColor = null, modifier = Modifier)
        }
        Text(field.value, color = ShikeColors.Ink, fontSize = 15.sp, fontWeight = FontWeight.SemiBold)
        Text(field.helper, style = ShikeTypography.Caption)
    }
}

@Composable
private fun ClassPrepPack(items: List<String>, onEditPreparation: () -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(6.dp), modifier = Modifier.fillMaxWidth()) {
        Text("课前包", color = ShikeColors.Ink, fontSize = 14.sp, fontWeight = FontWeight.Bold)
        if (items.isEmpty()) {
            Text("可添加准备事项", style = ShikeTypography.Caption)
        } else {
            val visibleItems = cleanPreparationItems(items).take(3)
            Row(horizontalArrangement = Arrangement.spacedBy(6.dp), modifier = Modifier.fillMaxWidth()) {
                visibleItems.forEach { item ->
                    Pill(item, ShikeColors.BrandSoft, ShikeColors.Brand, modifier = Modifier.weight(1f))
                }
                repeat((3 - visibleItems.size).coerceAtLeast(0)) {
                    Pill("可补充", ShikeColors.WarningSoft, ShikeColors.Warning, modifier = Modifier.weight(1f))
                }
            }
        }
    }
}

@Composable
private fun EvidenceFold(evidence: String, onEditSourceText: () -> Unit) {
    var expanded by rememberSaveable(evidence) { mutableStateOf(false) }
    val firstLine = evidence.lineSequence().firstOrNull().orEmpty().take(32)
    Column(verticalArrangement = Arrangement.spacedBy(4.dp), modifier = Modifier.fillMaxWidth()) {
        Text("从文字中看到：${firstLine.ifBlank { "暂无识别原文" }}", style = ShikeTypography.Caption)
        TextButton(onClick = { expanded = !expanded }) {
            Text(if (expanded) "收起依据" else "展开依据")
        }
        if (expanded) {
            Text(evidence.ifBlank { "暂无可展示的识别原文" }, style = ShikeTypography.Caption)
            OutlinedButton(onClick = onEditSourceText, modifier = Modifier.fillMaxWidth()) { Text("改原文") }
        }
    }
}

private fun SmartFieldState.copyText(): String = when (this) {
    SmartFieldState.Confirmed -> "已识别"
    SmartFieldState.NeedsReview -> "建议时间"
    SmartFieldState.Suggested -> "建议"
    SmartFieldState.Missing -> "可补充"
}

private fun SmartFieldState.background(): Color = when (this) {
    SmartFieldState.Confirmed -> ShikeColors.BrandSoft
    SmartFieldState.NeedsReview -> ShikeColors.WarningSoft
    SmartFieldState.Suggested -> Color(0xFFF4F7FA)
    SmartFieldState.Missing -> Color(0xFFF4F7FA)
}

private fun SmartFieldState.contentColor(): Color = when (this) {
    SmartFieldState.Confirmed -> ShikeColors.Brand
    SmartFieldState.NeedsReview -> ShikeColors.Warning
    SmartFieldState.Suggested -> ShikeColors.Muted
    SmartFieldState.Missing -> ShikeColors.Muted
}
