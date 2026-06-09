package cn.shike.app

import cn.shike.app.ui.TodayAgendaState

data class CloudEnhancementFallback(
    val modelStatus: String,
    val captureSource: String,
    val todayAgendaState: TodayAgendaState,
)

fun cloudEnhancementDisabledFallback(): CloudEnhancementFallback =
    CloudEnhancementFallback(
        modelStatus = "关闭云侧增强：不请求云端，保留本地草稿。",
        captureSource = "关闭云侧增强：本次未调用云端 AI。",
        todayAgendaState = TodayAgendaState.Ready,
    )
