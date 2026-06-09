package cn.shike.app

import cn.shike.app.ui.TodayAgendaState
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class CloudEnhancementActionsTest {
    @Test
    fun cloudEnhancementDisabledFallback_keepsTodayActionReady() {
        val fallback = cloudEnhancementDisabledFallback()

        assertEquals(TodayAgendaState.Ready, fallback.todayAgendaState)
    }

    @Test
    fun cloudEnhancementDisabledFallback_statesBackendIsNotCalled() {
        val fallback = cloudEnhancementDisabledFallback()

        assertTrue(fallback.modelStatus.contains("不请求云端"))
        assertTrue(fallback.captureSource.contains("未调用云端 AI"))
    }

    @Test
    fun cloudEnhancementDisabledFallback_keepsLocalDraftAndOfflineEntry() {
        val fallback = cloudEnhancementDisabledFallback()

        assertTrue(fallback.modelStatus.contains("保留本地草稿"))
    }
}
