package cn.shike.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

@Composable
fun OfflineSampleActions(
    onCourse: () -> Unit,
    onEvent: () -> Unit,
) {
    Text("离线兜底样例", fontWeight = FontWeight.SemiBold, color = Color(0xFF101828))
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
        OutlinedButton(onClick = onCourse, modifier = Modifier.weight(1f)) { Text("课程样例") }
        OutlinedButton(onClick = onEvent, modifier = Modifier.weight(1f)) { Text("活动样例") }
    }
}
