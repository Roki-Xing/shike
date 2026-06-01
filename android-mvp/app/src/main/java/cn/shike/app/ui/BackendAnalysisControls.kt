package cn.shike.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun BackendAnalysisControls(
    cloudEnhancedEnabled: Boolean,
    onBackendCourse: () -> Unit,
    onBackendEvent: () -> Unit,
) {
    Text("后端模型编排", fontWeight = FontWeight.SemiBold, color = Color(0xFF101828))
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
        Button(
            onClick = onBackendCourse,
            enabled = cloudEnhancedEnabled,
            modifier = Modifier.weight(1f),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2563EB)),
        ) { Text("解析当前草稿") }
        Button(
            onClick = onBackendEvent,
            enabled = cloudEnhancedEnabled,
            modifier = Modifier.weight(1f),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFF97316)),
        ) { Text("活动样例解析") }
    }
    if (!cloudEnhancedEnabled) {
        Text("关闭云侧增强时不请求后端；可用离线样例或手动草稿继续。", color = Color(0xFFF97316), fontSize = 12.sp)
    }
}
