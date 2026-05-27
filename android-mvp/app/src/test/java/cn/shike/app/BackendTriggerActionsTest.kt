package cn.shike.app

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class BackendTriggerActionsTest {
    @Test
    fun analyzeCourseWithBackendAction_dispatchesCourseScreenshotInput() {
        val dispatched = mutableListOf<cn.shike.app.data.BackendAnalysisInput>()

        analyzeCourseWithBackendAction(dispatched::add)

        assertEquals(1, dispatched.size)
        assertEquals("screenshot", dispatched.single().sourceType)
        assertEquals("课程通知", dispatched.single().fallback.scene)
        assertTrue(dispatched.single().fallback.rawText.contains("高数A班"))
    }

    @Test
    fun analyzeEventWithBackendAction_dispatchesEventCameraInput() {
        val dispatched = mutableListOf<cn.shike.app.data.BackendAnalysisInput>()

        analyzeEventWithBackendAction(dispatched::add)

        assertEquals(1, dispatched.size)
        assertEquals("camera", dispatched.single().sourceType)
        assertEquals("活动海报", dispatched.single().fallback.scene)
        assertTrue(dispatched.single().fallback.rawText.contains("AI应用分享会"))
    }
}
