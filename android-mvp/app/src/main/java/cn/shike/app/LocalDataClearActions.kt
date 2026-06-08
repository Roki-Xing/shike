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

data class LocalDataClearConfirmationState(
    val isAwaitingConfirmation: Boolean = false,
)

data class LocalDataClearConfirmationResult(
    val state: LocalDataClearConfirmationState,
    val shouldClearLocalData: Boolean,
)

/**
 * Arms App-internal confirmation for clearing Shike-owned cache only.
 *
 * Args:
 *     state: Current local-data clear confirmation state.
 *
 * Returns:
 *     The next state and whether clearing may run now.
 */
fun requestLocalDataClearConfirmation(
    state: LocalDataClearConfirmationState,
): LocalDataClearConfirmationResult =
    LocalDataClearConfirmationResult(
        state = state.copy(isAwaitingConfirmation = true),
        shouldClearLocalData = false,
    )

/**
 * Cancels the cache-clear prompt without deleting App data.
 *
 * Args:
 *     state: Current local-data clear confirmation state.
 *
 * Returns:
 *     The dismissed state and a false clear flag.
 */
fun cancelLocalDataClearConfirmation(
    state: LocalDataClearConfirmationState,
): LocalDataClearConfirmationResult =
    LocalDataClearConfirmationResult(
        state = state.copy(isAwaitingConfirmation = false),
        shouldClearLocalData = false,
    )

/**
 * Allows cache clearing only after the App confirmation prompt is visible.
 *
 * Args:
 *     state: Current local-data clear confirmation state.
 *
 * Returns:
 *     A dismissed state and whether the caller should clear App-private data.
 */
fun confirmLocalDataClearConfirmation(
    state: LocalDataClearConfirmationState,
): LocalDataClearConfirmationResult =
    LocalDataClearConfirmationResult(
        state = state.copy(isAwaitingConfirmation = false),
        shouldClearLocalData = state.isAwaitingConfirmation,
    )

fun clearedLocalDataState(): LocalDataClearState {
    val item = sampleCourse()
    return LocalDataClearState(
        item = item,
        captureSource = "数据清除：已清除拾刻缓存、本地收件箱和设置。",
        modelStatus = "拾刻缓存已清除，可重新从截图、拍照、分享或手动输入开始。",
        backendUrl = DEFAULT_BACKEND_BASE_URL,
        todayAgendaState = TodayAgendaState.Empty,
        cloudEnhancedEnabled = true,
    )
}
