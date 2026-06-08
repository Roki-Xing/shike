package cn.shike.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import cn.shike.app.domain.ShikeItem

@Composable
fun ParseConfirmPanel(item: ShikeItem, onReviewed: (ShikeItem) -> Unit) {
    var draftTitle by remember(item.title) { mutableStateOf(item.title) }
    var draftTime by remember(item.time) { mutableStateOf(item.time) }
    var draftLocation by remember(item.location) { mutableStateOf(item.location) }
    var draftStatus by remember(item.status) { mutableStateOf(item.status) }
    SectionCard("AI 解析确认") {
        ParseConfirmHeader(item)
        OutlinedTextField(
            value = draftTitle,
            onValueChange = { draftTitle = it },
            label = { Text("任务标题") },
            modifier = Modifier.fillMaxWidth(),
        )
        OutlinedTextField(
            value = draftTime,
            onValueChange = { draftTime = it },
            label = { Text("时间") },
            modifier = Modifier.fillMaxWidth(),
        )
        OutlinedTextField(
            value = draftLocation,
            onValueChange = { draftLocation = it },
            label = { Text("地点") },
            modifier = Modifier.fillMaxWidth(),
        )
        OutlinedTextField(
            value = draftStatus,
            onValueChange = { draftStatus = it },
            label = { Text("状态") },
            modifier = Modifier.fillMaxWidth(),
        )
        KeyValue("来源文本", item.rawText.take(28))
        KeyValue("模型解释", modelExplanation(item).take(42))
        RiskChecklistPanel(item)
        ReviewDecisionActions(
            item = item,
            draftTitle = draftTitle,
            draftTime = draftTime,
            draftLocation = draftLocation,
            draftStatus = draftStatus,
            onReviewed = onReviewed,
        )
        Text("低置信度或字段缺失时保持待人工确认；确认并安排后才建议执行日历、提醒和地图动作。", color = Color(0xFFF97316), fontSize = 12.sp)
    }
}
