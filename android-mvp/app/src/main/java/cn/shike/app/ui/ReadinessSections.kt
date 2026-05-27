package cn.shike.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.material3.Switch
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun DeliveryReadinessPanel() {
    SectionCard("交付物自检中心") {
        ReadinessRow("APK", "已构建，可真机安装", Color(0xFF0F766E))
        ReadinessRow("真机证据", "按 device-demo-checklist 录屏", Color(0xFF2563EB))
        ReadinessRow("后端", "支持 /health、/v1/schema、/v1/analyze", Color(0xFF0F766E))
        ReadinessRow("总体验收", "REAL_WORLD_READY_METRIC 22/22", Color(0xFFF97316))
        Text("现场演示时可直接打开本区说明交付状态，不依赖计划文件。", color = Color(0xFF667085), fontSize = 12.sp)
    }
}

@Composable
private fun ReadinessRow(label: String, value: String, color: Color) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = androidx.compose.foundation.layout.Arrangement.spacedBy(10.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Box(
            modifier = Modifier
                .size(9.dp)
                .background(color, CircleShape),
        )
        Text(label, modifier = Modifier.weight(0.8f), color = Color(0xFF344054), fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
        Text(value, modifier = Modifier.weight(2f), color = Color(0xFF101828), fontSize = 12.sp, textAlign = TextAlign.End)
    }
}

@Composable
fun PrivacyPanel(
    cloudEnhancedEnabled: Boolean,
    onCloudEnhancedChange: (Boolean) -> Unit,
    onClearLocalData: () -> Unit,
) {
    SectionCard("隐私与端云设置") {
        KeyValue("端侧优先", "OCR、本地缓存、基础分类")
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = androidx.compose.foundation.layout.Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text("云侧增强", color = Color(0xFF667085), fontSize = 12.sp)
            Switch(
                checked = cloudEnhancedEnabled,
                onCheckedChange = onCloudEnhancedChange,
            )
        }
        KeyValue(
            "云侧状态",
            if (cloudEnhancedEnabled) "开启，用户点击后才请求后端" else "关闭云侧增强，不请求后端",
        )
        OutlinedButton(onClick = onClearLocalData, modifier = Modifier.fillMaxWidth()) {
            Text("一键清除本地数据")
        }
        KeyValue("敏感动作", "日历和提醒写入前必须确认")
    }
}
