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

enum class TodayAgendaState {
    Ready,
    Empty,
    Error,
}

data class TodayActionItem(
    val title: String,
    val status: String,
    val detailLines: List<String>,
    val footerLabel: String,
    val actionLabel: String,
    val tone: TodayActionTone,
)

enum class TodayActionTone {
    Scheduled,
    DueSoon,
    Pending,
}

fun todayActionItemFrom(item: ShikeItem): TodayActionItem {
    val status = item.status
    val tone = when (status) {
        "已安排" -> TodayActionTone.Scheduled
        "即将截止" -> TodayActionTone.DueSoon
        else -> TodayActionTone.Pending
    }
    val primaryAction = item.actions.firstOrNull().orEmpty()
    val actionLabel = when {
        status == "已安排" && item.actions.any { "地图" in it } -> "查看路线"
        status == "即将截止" -> "查看截止"
        primaryAction.isNotBlank() -> primaryAction
        else -> "查看详情"
    }
    return TodayActionItem(
        title = item.title,
        status = status,
        detailLines = listOf(item.time, item.location),
        footerLabel = "来源：${item.scene} · ${if (status == "已安排") "已确认" else "待用户确认"}",
        actionLabel = actionLabel,
        tone = tone,
    )
}

@Composable
fun HomeAgendaList(
    item: ShikeItem,
    state: TodayAgendaState,
    onGallery: () -> Unit,
    onManualInput: () -> Unit,
) {
    when (state) {
        TodayAgendaState.Empty -> {
            TodayStateCard(
                title = "今日行动台空状态",
                description = "还没有本地收件箱任务。可以从截图、拍照、分享或手动输入开始，不会自动执行日历、提醒或地图动作。",
                tone = Color(0xFF0F766E),
                onGallery = onGallery,
                onManualInput = onManualInput,
            )
            return
        }
        TodayAgendaState.Error -> {
            TodayStateCard(
                title = "今日行动台错误状态",
                description = "本地数据加载失败或后端不可用时，拾刻会保留当前行动卡，并提示改用截图、拍照、分享或手动输入继续。",
                tone = Color(0xFFF97316),
                onGallery = onGallery,
                onManualInput = onManualInput,
            )
            return
        }
        TodayAgendaState.Ready -> Unit
    }

    val todayItem = todayActionItemFrom(item)
    val palette = when (todayItem.tone) {
        TodayActionTone.Scheduled -> TodayActionPalette(
            icon = "今",
            iconBackground = Color(0xFFD9F0EA),
            statusBackground = Color(0xFFE0F5EE),
            color = Color(0xFF0F766E),
        )
        TodayActionTone.DueSoon -> TodayActionPalette(
            icon = "急",
            iconBackground = Color(0xFFFFE8D9),
            statusBackground = Color(0xFFFFF0E5),
            color = Color(0xFFF97316),
        )
        TodayActionTone.Pending -> TodayActionPalette(
            icon = "核",
            iconBackground = Color(0xFFDDEBFF),
            statusBackground = Color(0xFFEAF1FF),
            color = Color(0xFF2563EB),
        )
    }

    AgendaCard(
        iconText = palette.icon,
        iconBackground = palette.iconBackground,
        title = todayItem.title,
        statusText = todayItem.status,
        statusBackground = palette.statusBackground,
        statusColor = palette.color,
        detailLines = todayItem.detailLines,
        footerLabel = todayItem.footerLabel,
        actionLabel = todayItem.actionLabel,
        actionColor = palette.color,
    )
}

@Composable
private fun TodayStateCard(
    title: String,
    description: String,
    tone: Color,
    onGallery: () -> Unit,
    onManualInput: () -> Unit,
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        shape = RoundedCornerShape(16.dp),
        border = BorderStroke(1.dp, Color(0xFFE6EDF1)),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
    ) {
        Column(
            modifier = Modifier.padding(14.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                Text(
                    title,
                    color = Color(0xFF101828),
                    fontSize = 17.sp,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.weight(1f),
                )
                Pill("需导入", Color(0xFFEAF1FF), Color(0xFF2563EB))
            }
            Text(description, color = Color(0xFF667085), fontSize = 12.sp, lineHeight = 18.sp)
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                Button(
                    onClick = onGallery,
                    modifier = Modifier.weight(1.35f),
                    colors = ButtonDefaults.buttonColors(containerColor = tone),
                ) { Text("导入截图") }
                OutlinedButton(onClick = onManualInput, modifier = Modifier.weight(1f)) { Text("手动输入") }
            }
        }
    }
}

private data class TodayActionPalette(
    val icon: String,
    val iconBackground: Color,
    val statusBackground: Color,
    val color: Color,
)
