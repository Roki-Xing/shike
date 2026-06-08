package cn.shike.app

import cn.shike.app.data.DEFAULT_BACKEND_BASE_URL
import cn.shike.app.ui.TodayAgendaState
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class LocalDataClearActionsTest {
    @Test
    fun clearedLocalDataState_resetsToCourseSampleAndEmptyTodayState() {
        val state = clearedLocalDataState()

        assertEquals("高数A班教室变更", state.item.title)
        assertEquals("课程通知", state.item.scene)
        assertEquals("已安排", state.item.status)
        assertEquals(TodayAgendaState.Empty, state.todayAgendaState)
    }

    @Test
    fun clearedLocalDataState_resetsBackendUrlToDefault() {
        val state = clearedLocalDataState()

        assertEquals(DEFAULT_BACKEND_BASE_URL, state.backendUrl)
    }

    @Test
    fun clearedLocalDataState_restoresCloudEnhancementToDefaultEnabled() {
        val state = clearedLocalDataState()

        assertTrue(state.cloudEnhancedEnabled)
    }

    @Test
    fun clearedLocalDataState_explainsSafeRestartPath() {
        val state = clearedLocalDataState()

        assertTrue(state.captureSource.contains("已清除拾刻缓存"))
        assertTrue(state.modelStatus.contains("重新从截图、拍照、分享或手动输入开始"))
    }

    @Test
    fun requestLocalDataClearConfirmation_requiresSecondAppConfirmation() {
        val result = requestLocalDataClearConfirmation(LocalDataClearConfirmationState())

        assertTrue(result.state.isAwaitingConfirmation)
        assertEquals(false, result.shouldClearLocalData)
    }

    @Test
    fun cancelLocalDataClearConfirmation_keepsCacheAndDismissesPrompt() {
        val result = cancelLocalDataClearConfirmation(LocalDataClearConfirmationState(isAwaitingConfirmation = true))

        assertEquals(LocalDataClearConfirmationState(), result.state)
        assertEquals(false, result.shouldClearLocalData)
    }

    @Test
    fun confirmLocalDataClearConfirmation_onlyClearsAfterPromptIsVisible() {
        val coldResult = confirmLocalDataClearConfirmation(LocalDataClearConfirmationState())
        val armedResult = confirmLocalDataClearConfirmation(LocalDataClearConfirmationState(isAwaitingConfirmation = true))

        assertEquals(false, coldResult.shouldClearLocalData)
        assertEquals(LocalDataClearConfirmationState(), coldResult.state)
        assertEquals(true, armedResult.shouldClearLocalData)
        assertEquals(LocalDataClearConfirmationState(), armedResult.state)
    }
}
