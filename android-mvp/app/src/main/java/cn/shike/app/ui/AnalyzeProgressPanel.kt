package cn.shike.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

data class AnalyzeProgressState(
    val active: Boolean,
    val currentStepIndex: Int,
    val statusLabel: String,
)

private val AnalyzeSteps = listOf("读取图片", "OCR识别", "结构化解析", "生成行动卡")

fun analyzeProgressStateFor(modelStatus: String, hasPendingImage: Boolean, selectedStatus: String): AnalyzeProgressState {
    val active = hasPendingImage || "解析中" in modelStatus || "待确认" in selectedStatus
    val index = when {
        "图片解析中" in modelStatus -> 1
        "云侧解析中" in modelStatus -> 2
        "待确认" in selectedStatus -> 3
        else -> 0
    }
    return AnalyzeProgressState(
        active = active,
        currentStepIndex = index.coerceIn(0, AnalyzeSteps.lastIndex),
        statusLabel = modelStatus.removePrefix("模型状态：").ifBlank { "等待截图" },
    )
}

@Composable
fun AnalyzeProgressPanel(state: AnalyzeProgressState) {
    if (!state.active) {
        return
    }
    SectionCard("正在把截图变成行动卡") {
        LinearProgressIndicator(
            progress = { (state.currentStepIndex + 1).toFloat() / AnalyzeSteps.size },
            modifier = Modifier.fillMaxWidth(),
            color = ShikeColors.Brand,
        )
        AnalyzeSteps.forEachIndexed { index, step ->
            AnalyzeStepRow(
                label = "${index + 1}/4 $step",
                active = index == state.currentStepIndex,
                done = index < state.currentStepIndex,
            )
        }
        Text(state.statusLabel, style = ShikeTypography.Caption)
    }
}

@Composable
private fun AnalyzeStepRow(label: String, active: Boolean, done: Boolean) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Text(label, style = ShikeTypography.Body.copy(color = if (active) ShikeColors.Brand else ShikeColors.Muted))
        Text(
            when {
                done -> "完成"
                active -> "进行中"
                else -> "等待"
            },
            style = ShikeTypography.Caption.copy(fontWeight = FontWeight.SemiBold),
        )
    }
}
