package cn.shike.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun AgendaCardHeader(
    iconText: String,
    iconBackground: Color,
    title: String,
    statusText: String,
    statusBackground: Color,
    statusColor: Color,
    detailLines: List<String>,
    actionColor: Color,
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(10.dp),
        verticalAlignment = Alignment.Top,
    ) {
        Box(
            modifier = Modifier
                .size(42.dp)
                .background(iconBackground, CircleShape),
            contentAlignment = Alignment.Center,
        ) {
            Text(iconText, color = actionColor, fontSize = 16.sp, fontWeight = FontWeight.Bold)
        }
        Column(
            modifier = Modifier.weight(1f),
            verticalArrangement = Arrangement.spacedBy(4.dp),
        ) {
            Text(
                title,
                color = Color(0xFF101828),
                fontSize = 17.sp,
                fontWeight = FontWeight.Bold,
            )
            detailLines.forEach { line ->
                Text(line, color = Color(0xFF667085), fontSize = 12.sp)
            }
        }
        Pill(statusText, statusBackground, statusColor)
    }
}
