package cn.shike.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun PermissionOnboarding(
    onEnableScreenshotAssist: () -> Unit,
    onDismiss: () -> Unit,
) {
    SectionCard("开始使用拾刻") {
        Text(
            "拾刻只在你主动导入或开启截图助手后解析内容；系统动作都需要用户确认后执行。",
            style = ShikeTypography.Body,
        )
        Column(verticalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
            PermissionOnboardingRow("通知权限", "用于截图后提醒你是否交给拾刻，也用于到点提醒。")
            PermissionOnboardingRow("图片权限", "仅在你开启截图助手后观察最近截图，不默认上传原图。")
            PermissionOnboardingRow("相机权限", "用于拍海报、公告或课堂通知，点击拍照时才申请。")
            PermissionOnboardingRow("日历", "用户确认后打开系统日历新增页，由你在日历中保存。")
            PermissionOnboardingRow("地图", "用户确认地点后打开地图；地图不可用时复制地点。")
        }
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
            Button(
                onClick = onEnableScreenshotAssist,
                modifier = Modifier.weight(1.25f),
                colors = ButtonDefaults.buttonColors(containerColor = ShikeColors.Brand),
            ) {
                Text("开启截图助手")
            }
            OutlinedButton(onClick = onDismiss, modifier = Modifier.weight(1f)) {
                Text("稍后再说")
            }
        }
    }
}

@Composable
private fun PermissionOnboardingRow(label: String, detail: String) {
    KeyValue(label, detail)
}
