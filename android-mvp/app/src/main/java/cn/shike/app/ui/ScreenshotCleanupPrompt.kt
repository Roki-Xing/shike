package cn.shike.app.ui

import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import cn.shike.app.data.ImageCleanupStatus

fun cleanupStatusLabel(status: ImageCleanupStatus): String =
    when (status) {
        ImageCleanupStatus.NOT_SUPPORTED -> "当前来源不支持直接移入回收站"
        ImageCleanupStatus.NOT_REQUESTED -> "等待你的选择"
        ImageCleanupStatus.USER_KEPT -> "已选择保留原图"
        ImageCleanupStatus.DELETE_REQUESTED -> "正在等待系统确认"
        ImageCleanupStatus.DELETED -> "已移入系统回收站"
        ImageCleanupStatus.FAILED -> "系统确认未完成"
    }

@Composable
fun ScreenshotCleanupPrompt(
    status: ImageCleanupStatus,
    onDelete: () -> Unit,
    onKeep: () -> Unit,
) {
    SectionCard("处理原截图") {
        Text("这张截图已经生成行动卡，是否把原图移入系统回收站？系统会弹出确认，拾刻不会静默删除。", style = ShikeTypography.Body)
        KeyValue("当前状态", cleanupStatusLabel(status))
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            OutlinedButton(onClick = onDelete, modifier = Modifier.weight(1f)) {
                Text("移入回收站")
            }
            OutlinedButton(onClick = onKeep, modifier = Modifier.weight(1f)) {
                Text("保留原图")
            }
        }
    }
}
