package cn.shike.app

import cn.shike.app.data.sampleCourse
import cn.shike.app.ui.actionCardUiModelFrom
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Test

class ActionCardUiModelTest {
    @Test
    fun actionCardUiModelFrom_extractsStructuredFieldsAndHidesNullCopy() {
        val item = sampleCourse().copy(
            title = "英语口语课",
            time = "明天早上九点 / null",
            location = "E520",
            actions = listOf("加入日历", "课前提醒", "打开地图"),
            rawText = "云端 AI 解析：从截图提取字段\n任务：上英语口语\n风险：日期来自“明天”，请确认\n待补：reminder_offset",
        )

        val model = actionCardUiModelFrom(item)

        assertEquals("英语口语课", model.title)
        assertEquals("课程通知", model.sceneLabel)
        assertEquals("E520", model.location)
        assertEquals("上英语口语", model.task)
        assertEquals(listOf("加入日历", "课前提醒", "打开地图"), model.actions)
        assertEquals(listOf("日期来自“明天”，请确认"), model.risks)
        assertEquals(listOf("reminder_offset"), model.missingFields)
        assertEquals("明天早上九点", model.time)
        assertFalse(model.time.contains("null", ignoreCase = true))
    }

    @Test
    fun actionCardUiModelFrom_usesCourseTaskFallbackWhenNoTaskEvidence() {
        val model = actionCardUiModelFrom(sampleCourse().copy(rawText = "云端 AI 解析：字段完整"))

        assertEquals("上课", model.task)
    }
}
