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
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import cn.shike.app.domain.ShikeItem

@Composable
fun QuickImportBar(
    onGallery: () -> Unit,
    onCamera: () -> Unit,
    onManualInput: () -> Unit,
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        shape = RoundedCornerShape(16.dp),
        border = BorderStroke(1.dp, ShikeColors.Line),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
    ) {
        Column(modifier = Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text("把截图变成行动卡", color = ShikeColors.Ink, fontSize = 18.sp, fontWeight = FontWeight.Bold)
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                Button(
                    onClick = onGallery,
                    modifier = Modifier.weight(1.2f),
                    colors = ButtonDefaults.buttonColors(containerColor = ShikeColors.Brand),
                ) { Text("导入截图") }
                OutlinedButton(onClick = onCamera, modifier = Modifier.weight(1f)) { Text("拍照") }
                OutlinedButton(onClick = onManualInput, modifier = Modifier.weight(1f)) { Text("手动输入") }
            }
        }
    }
}

@Composable
fun FocusedHomeCard(
    title: String,
    body: String,
    primaryLabel: String,
    secondaryLabel: String,
    onPrimary: () -> Unit,
    onSecondary: () -> Unit,
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        shape = RoundedCornerShape(16.dp),
        border = BorderStroke(1.dp, ShikeColors.Line),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
    ) {
        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            Text(title, color = ShikeColors.Ink, fontSize = 20.sp, fontWeight = FontWeight.Bold)
            Text(body, style = ShikeTypography.Body)
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                Button(
                    onClick = onPrimary,
                    modifier = Modifier.weight(1.2f),
                    colors = ButtonDefaults.buttonColors(containerColor = ShikeColors.Brand),
                ) { Text(primaryLabel) }
                OutlinedButton(onClick = onSecondary, modifier = Modifier.weight(1f)) { Text(secondaryLabel) }
            }
        }
    }
}

@Composable
fun FocusedActionReviewCard(
    item: ShikeItem,
    titlePrefix: String = "今天要处理",
    primaryLabel: String = "确认并安排",
    onPrimary: () -> Unit,
) {
    val preparation = preparationItemsForUi(item)
    val readiness = actionReadinessUiModelFrom(item)
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        shape = RoundedCornerShape(16.dp),
        border = BorderStroke(1.dp, ShikeColors.Line),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
    ) {
        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                Pill(titlePrefix, ShikeColors.BrandSoft, ShikeColors.Brand, modifier = Modifier.weight(1f))
                Pill("准备度 ${readiness.completed}/${readiness.total}", ShikeColors.WarningSoft, ShikeColors.Warning, modifier = Modifier.weight(1f))
            }
            Text(item.title, color = ShikeColors.Ink, fontSize = 21.sp, fontWeight = FontWeight.Bold)
            ActionReadinessBar(readiness, compact = true)
            Text(
                smartActionCardUiModelFrom(item).let { model ->
                    listOf(model.time.value, model.location.value)
                        .filter { it.isNotBlank() && it != "待确认" }
                        .joinToString(" · ")
                        .ifBlank { "时间地点待确认" }
                },
                style = ShikeTypography.Body,
            )
            if (preparation.isNotEmpty()) {
                Text(
                    "课前包：${preparation.joinToString("、")}",
                    color = ShikeColors.Warning,
                    fontSize = 13.sp,
                    fontWeight = FontWeight.SemiBold,
                )
            }
            Button(
                onClick = onPrimary,
                modifier = Modifier.fillMaxWidth(),
                colors = ButtonDefaults.buttonColors(containerColor = ShikeColors.Brand),
            ) { Text(primaryLabel) }
        }
    }
}
