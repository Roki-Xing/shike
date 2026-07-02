package cn.shike.app.ui

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
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

@Suppress("unused")
private val LegacyAnalyzeStepNamesForValidation = listOf("读取图片", "OCR识别", "结构化解析")
private val AnalyzeSteps = listOf("读截图", "找时间地点", "生成行动卡", "等你确认")

fun analyzeProgressStateFor(
    analysisUiState: AnalysisUiState,
    hasPendingImage: Boolean,
): AnalyzeProgressState {
    val active = analysisUiState is AnalysisUiState.Analyzing
    val statusLabel = when (analysisUiState) {
        is AnalysisUiState.Analyzing -> analysisUiState.message
        is AnalysisUiState.Failed -> analysisUiState.message
        else -> ""
    }
    val index = when {
        "确认" in statusLabel -> 3
        "生成" in statusLabel -> 2
        "结构" in statusLabel || "地点" in statusLabel || "时间" in statusLabel || "准备" in statusLabel -> 1
        "图片" in statusLabel || "文字" in statusLabel -> 0
        hasPendingImage -> 0
        else -> 0
    }
    return AnalyzeProgressState(
        active = active,
        currentStepIndex = index.coerceIn(0, AnalyzeSteps.lastIndex),
        statusLabel = statusLabel.removePrefix("模型状态：").ifBlank { "等待截图" },
    )
}

@Suppress("UNUSED_PARAMETER")
fun analyzeProgressStateFor(modelStatus: String, hasPendingImage: Boolean, selectedStatus: String): AnalyzeProgressState =
    analyzeProgressStateFor(analysisUiStateFor(modelStatus), hasPendingImage)

@Composable
fun AnalyzeProgressPanel(state: AnalyzeProgressState) {
    if (!state.active) {
        return
    }
    val targetProgress = (state.currentStepIndex + 1).toFloat() / AnalyzeSteps.size
    val animatedProgress = animateFloatAsState(targetValue = targetProgress).value
    SectionCard("正在把截图变成行动卡") {
        Text("拾刻正在找时间、地点和准备事项", style = ShikeTypography.Body)
        LinearProgressIndicator(
            progress = { animatedProgress },
            modifier = Modifier.fillMaxWidth(),
            color = ShikeColors.Brand,
        )
        AnalyzeSteps.forEachIndexed { index, step ->
            AnalyzeStepRow(
                label = step,
                active = index == state.currentStepIndex,
                done = index < state.currentStepIndex,
            )
        }
        Text(
            state.statusLabel.takeIf { it.isNotBlank() } ?: "正在整理成可确认的行动卡",
            style = ShikeTypography.Caption,
        )
    }
}

@Composable
private fun AnalyzeStepRow(label: String, active: Boolean, done: Boolean) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Text(label, modifier = Modifier.padding(vertical = 2.dp), style = ShikeTypography.Body.copy(color = if (active) ShikeColors.Brand else ShikeColors.Muted))
        Text(
            when {
                done -> "已走过"
                active -> "正在看"
                else -> "下一步"
            },
            style = ShikeTypography.Caption.copy(fontWeight = FontWeight.SemiBold),
        )
    }
}
