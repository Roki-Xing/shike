package cn.shike.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import cn.shike.app.domain.ShikeItem

@Composable
fun ConfirmBanner(
    selected: ShikeItem,
    isConfirmed: Boolean,
    onAddCalendar: (ShikeItem) -> Unit,
    onReminder: (ShikeItem) -> Unit,
    onOpenMap: (ShikeItem) -> Unit,
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = Color(0xFF0F766E)),
        shape = RoundedCornerShape(18.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Column(modifier = Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(3.dp)) {
                    Text("确认后安排", color = Color.White, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                    Text(
                        if (isConfirmed) "当前行动卡已确认，可继续打开系统日历、提醒和路线。" else "请先在下方确认修正，再执行日历、提醒和地图动作。",
                        color = Color.White.copy(alpha = 0.85f),
                        fontSize = 12.sp,
                    )
                }
                Pill(if (isConfirmed) "可执行" else "待确认", Color.White.copy(alpha = 0.16f), Color.White)
            }
            ConfirmBannerActions(
                selected = selected,
                isConfirmed = isConfirmed,
                onAddCalendar = onAddCalendar,
                onReminder = onReminder,
                onOpenMap = onOpenMap,
            )
        }
    }
}
