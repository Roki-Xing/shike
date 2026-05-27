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

        assertTrue(state.captureSource.contains("已一键清除本地收件箱和设置"))
        assertTrue(state.modelStatus.contains("重新从截图、拍照、分享或手动输入开始"))
    }
}
