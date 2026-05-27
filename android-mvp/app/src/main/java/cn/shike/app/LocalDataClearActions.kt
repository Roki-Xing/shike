package cn.shike.app

import cn.shike.app.data.DEFAULT_BACKEND_BASE_URL
import cn.shike.app.data.sampleCourse
import cn.shike.app.domain.ShikeItem
import cn.shike.app.ui.TodayAgendaState

data class LocalDataClearState(
    val item: ShikeItem,
    val captureSource: String,
    val modelStatus: String,
    val backendUrl: String,
    val todayAgendaState: TodayAgendaState,
    val cloudEnhancedEnabled: Boolean,
)

fun clearedLocalDataState(): LocalDataClearState {
    val item = sampleCourse()
    return LocalDataClearState(
        item = item,
        captureSource = "数据清除：已一键清除本地收件箱和设置。",
        modelStatus = "本地数据已清除，可重新从截图、拍照、分享或手动输入开始。",
        backendUrl = DEFAULT_BACKEND_BASE_URL,
        todayAgendaState = TodayAgendaState.Empty,
        cloudEnhancedEnabled = true,
    )
}
