package cn.shike.app.ui

import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
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
    var expanded by rememberSaveable { mutableStateOf(false) }
    SectionCard("原图处理") {
        OutlinedButton(onClick = { expanded = !expanded }, modifier = Modifier.fillMaxWidth()) {
            Text(if (expanded) "收起原图处理" else "展开原图处理")
        }
        if (expanded) {
            Text("这张截图已经生成行动卡。你可以保留原图，也可以稍后回相册删除。", style = ShikeTypography.Body)
            Text("如果系统支持，也可以选择是否把原图移入系统回收站；这个移入回收站动作会弹出确认，拾刻不会静默删除。", style = ShikeTypography.Caption)
            KeyValue("当前状态", cleanupStatusLabel(status))
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                OutlinedButton(onClick = onDelete, modifier = Modifier.weight(1f)) {
                    Text("移入系统回收站")
                }
                OutlinedButton(onClick = onKeep, modifier = Modifier.weight(1f)) {
                    Text("保留原图")
                }
            }
        }
    }
}
