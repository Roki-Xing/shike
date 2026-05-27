package cn.shike.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
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
fun ParseConfirmHeader(item: ShikeItem) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.Top,
    ) {
        Column(modifier = Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Text(item.title, fontSize = 17.sp, fontWeight = FontWeight.Bold, color = Color(0xFF101828))
            Text("场景：${item.scene} · 置信度 ${if (item.scene == "课程通知") "0.94" else "0.91"}", color = Color(0xFF667085), fontSize = 12.sp)
        }
        Pill("可编辑", Color(0xFFEAF1FF), Color(0xFF2563EB))
    }
}
