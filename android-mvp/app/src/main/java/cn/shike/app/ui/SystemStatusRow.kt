package cn.shike.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

@Composable
fun SystemStatusRow() {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Text("10:28", fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = Color(0xFF111827))
        Text("拾刻", fontSize = 12.sp, color = Color(0xFF667085))
        Text("100%", fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = Color(0xFF111827))
    }
}
