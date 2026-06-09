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
    Text("生成行动卡", fontWeight = FontWeight.SemiBold, color = Color(0xFF101828))
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
        Button(
            onClick = onBackendCourse,
            enabled = cloudEnhancedEnabled,
            modifier = Modifier.fillMaxWidth(),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2563EB)),
        ) { Text("生成行动卡") }
    }
    if (!cloudEnhancedEnabled) {
        Text("关闭云侧增强时不请求云端；可手动确认并保留行动卡。", color = Color(0xFFF97316), fontSize = 12.sp)
    }
}
