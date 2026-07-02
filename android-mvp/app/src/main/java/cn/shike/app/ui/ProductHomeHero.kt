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
fun ProductHomeHero(
    onGallery: () -> Unit,
    onCamera: () -> Unit,
    onManualInput: () -> Unit,
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        shape = RoundedCornerShape(20.dp),
        border = BorderStroke(1.dp, ShikeColors.Line),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
    ) {
        Column(modifier = Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            Pill("截图变行动卡", ShikeColors.BrandSoft, ShikeColors.Brand, borderColor = null, modifier = Modifier.fillMaxWidth())
            Text("把截图变成今天能做的事", color = ShikeColors.Ink, fontSize = 24.sp, fontWeight = FontWeight.Bold)
            Text(
                "课程变更、活动海报、群通知，交给拾刻生成时间、地点、提醒和准备清单。",
                style = ShikeTypography.Body,
            )
            Button(
                onClick = onGallery,
                modifier = Modifier.fillMaxWidth(),
                colors = ButtonDefaults.buttonColors(containerColor = ShikeColors.Brand),
            ) { Text("导入截图") }
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                OutlinedButton(onClick = onCamera, modifier = Modifier.weight(1f)) { Text("拍照") }
                OutlinedButton(onClick = onManualInput, modifier = Modifier.weight(1f)) { Text("手动输入") }
            }
        }
    }
}

@Composable
fun ProductHomeMiniHeader(
    item: ShikeItem,
    todayAgendaState: TodayAgendaState,
) {
    val state = productHomeStateFor(item, todayAgendaState)
    Column(verticalArrangement = Arrangement.spacedBy(6.dp), modifier = Modifier.fillMaxWidth()) {
        Text(
            when (state) {
                ProductHomeState.NeedsReview -> "现在该做"
                ProductHomeState.Arranged -> "今晚要做"
                ProductHomeState.Empty -> "截图变行动卡"
                ProductHomeState.Active -> "今天要处理"
            },
            color = ShikeColors.Ink,
            fontSize = 20.sp,
            fontWeight = FontWeight.Bold,
        )
        Text(
            when (state) {
                ProductHomeState.NeedsReview -> "先确认这张行动卡，再决定是否打开日历、提醒或地点。"
                ProductHomeState.Arranged -> "安排已准备好，需要时可以回来看下一步。"
                ProductHomeState.Empty -> "导入截图，生成一张待确认行动卡。"
                ProductHomeState.Active -> "把今天的碎片事项继续推进。"
            },
            style = ShikeTypography.Body,
        )
    }
}

@Composable
fun TodayFocusCard(
    selected: ShikeItem,
    todayAgendaState: TodayAgendaState,
    onOpenCurrentAction: () -> Unit,
) {
    val smartCard = smartActionCardUiModelFrom(selected)
    val productState = productHomeStateFor(selected, todayAgendaState)
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        shape = RoundedCornerShape(16.dp),
        border = BorderStroke(1.dp, ShikeColors.Line),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
    ) {
        Column(modifier = Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text(
                if (productState == ProductHomeState.Arranged) "明天第一件事" else "今天要处理",
                color = ShikeColors.Ink,
                fontSize = 17.sp,
                fontWeight = FontWeight.Bold,
            )
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                Pill("待确认 ${if (selected.status == "待确认") "1" else "0"}", ShikeColors.WarningSoft, ShikeColors.Warning, modifier = Modifier.weight(1f))
                Pill("已安排 ${if (selected.status == "已安排") "1" else "0"}", ShikeColors.BrandSoft, ShikeColors.Brand, modifier = Modifier.weight(1f))
            }
            if (todayAgendaState != TodayAgendaState.Empty && selected.title.isNotBlank()) {
                Text(
                    listOf(smartCard.title, smartCard.time.value, smartCard.location.value)
                        .filter { it.isNotBlank() && it != "待确认" }
                        .joinToString(" · "),
                    style = ShikeTypography.Caption,
                )
                OutlinedButton(onClick = onOpenCurrentAction, modifier = Modifier.fillMaxWidth()) {
                    Text(if (selected.status == "待确认") "确认行动卡" else "查看下一步")
                }
            } else {
                Text("还没有需要你处理的卡片。", style = ShikeTypography.Caption)
            }
        }
    }
}
