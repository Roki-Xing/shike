package cn.shike.app.ui

sealed class AnalysisUiState {
    data object Idle : AnalysisUiState()
    data class Analyzing(val message: String) : AnalysisUiState()
    data object Reviewing : AnalysisUiState()
    data object Planning : AnalysisUiState()
    data class Failed(val message: String) : AnalysisUiState()
}

fun analysisUiStateFor(modelStatus: String): AnalysisUiState {
    val copy = modelStatus.trim()
    return when {
        copy.contains("解析中") || copy.contains("正在解析") -> AnalysisUiState.Analyzing(copy)
        copy.contains("失败") || copy.contains("暂不可用") || copy.contains("没识别成功") -> AnalysisUiState.Failed(copy)
        copy.contains("已存入待确认") -> AnalysisUiState.Reviewing
        else -> AnalysisUiState.Idle
    }
}
