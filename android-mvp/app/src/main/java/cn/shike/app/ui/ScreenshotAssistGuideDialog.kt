package cn.shike.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.unit.dp

@Composable
fun ScreenshotAssistGuideDialog(
    onEnableScreenshotAssist: () -> Unit,
    onDismiss: () -> Unit,
) {
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("开启截图助手") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("截图后，拾刻会提醒你是否生成行动卡。", style = ShikeTypography.Body)
                Text("通知权限：用于截图提醒和到点提醒。", style = ShikeTypography.Caption)
                Text("图片权限：用于识别最近截图，不默认上传原图。", style = ShikeTypography.Caption)
                Text("日历和地图：只在用户确认后打开。", style = ShikeTypography.Caption)
            }
        },
        confirmButton = {
            Button(
                onClick = onEnableScreenshotAssist,
                colors = ButtonDefaults.buttonColors(containerColor = ShikeColors.Brand),
            ) {
                Text("开启截图助手")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("稍后再说")
            }
        },
    )
}
