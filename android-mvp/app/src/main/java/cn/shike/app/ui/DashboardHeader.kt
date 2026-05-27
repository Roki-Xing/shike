package cn.shike.app.ui

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun DashboardHeader() {
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Text(
            text = "拾刻",
            modifier = Modifier.weight(1f),
            color = Color(0xFF0F766E),
            fontSize = 22.sp,
            fontWeight = FontWeight.Bold,
        )
        Text(
            text = "今日行动台",
            modifier = Modifier.weight(1f),
            textAlign = TextAlign.Center,
            color = Color(0xFF101828),
            fontSize = 17.sp,
            fontWeight = FontWeight.SemiBold,
        )
        Box(
            modifier = Modifier.weight(1f),
            contentAlignment = Alignment.CenterEnd,
        ) {
            DashboardNotificationBadge()
        }
    }
}
