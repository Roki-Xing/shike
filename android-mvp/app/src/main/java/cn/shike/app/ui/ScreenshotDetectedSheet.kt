package cn.shike.app.ui

import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import cn.shike.app.data.ScreenshotCandidate

@Composable
fun ScreenshotDetectedSheet(
    candidate: ScreenshotCandidate,
    onImport: (ScreenshotCandidate) -> Unit,
    onIgnore: () -> Unit,
) {
    SectionCard("检测到新截图") {
        Text("可能包含课程、活动或截止事项，是否交给拾刻生成行动卡？", style = ShikeTypography.Body)
        KeyValue("图片尺寸", "${candidate.width}x${candidate.height}")
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            OutlinedButton(onClick = { onImport(candidate) }, modifier = Modifier.weight(1f)) {
                Text("交给拾刻")
            }
            OutlinedButton(onClick = onIgnore, modifier = Modifier.weight(1f)) {
                Text("忽略")
            }
        }
    }
}
