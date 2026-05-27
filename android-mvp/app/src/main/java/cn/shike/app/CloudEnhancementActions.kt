package cn.shike.app

import cn.shike.app.ui.TodayAgendaState

data class CloudEnhancementFallback(
    val modelStatus: String,
    val captureSource: String,
    val todayAgendaState: TodayAgendaState,
)

fun cloudEnhancementDisabledFallback(): CloudEnhancementFallback =
    CloudEnhancementFallback(
        modelStatus = "关闭云侧增强：不请求后端，保留本地草稿和离线样例入口。",
        captureSource = "关闭云侧增强：本次未调用后端 /v1/analyze。",
        todayAgendaState = TodayAgendaState.Ready,
    )
