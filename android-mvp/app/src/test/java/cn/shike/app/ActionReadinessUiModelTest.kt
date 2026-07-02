package cn.shike.app

import cn.shike.app.domain.ShikeItem
import cn.shike.app.ui.ExecutionResult
import cn.shike.app.ui.actionReadinessUiModelFrom
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class ActionReadinessUiModelTest {
    @Test
    fun actionReadinessUiModelFrom_clearCourseCardIsReadyToArrangeBeforeExecution() {
        val item = courseItem(time = "明天早八", location = "B342", raw = "明天早八 高数 B342 记得带书")

        val model = actionReadinessUiModelFrom(item)

        assertEquals("行动准备度 4/4", model.title)
        assertEquals("这张卡已经可以安排", model.subtitle)
        assertTrue(model.steps.first { it.label == "时间" }.completed)
        assertTrue(model.steps.first { it.label == "地点" }.completed)
        assertTrue(model.steps.first { it.label == "课前包" }.completed)
    }

    @Test
    fun actionReadinessUiModelFrom_ambiguousTimeNeedsReview() {
        val item = courseItem(time = "今天晚上大概九点", location = "B342", raw = "今天晚上大概九点 高数 B342 记得带书")

        val model = actionReadinessUiModelFrom(item)

        assertFalse(model.steps.first { it.label == "时间" }.completed)
        assertEquals("时间是建议值，保存前确认一下", model.subtitle)
    }

    @Test
    fun actionReadinessUiModelFrom_missingLocationUsesGentleCopy() {
        val item = courseItem(time = "明天早八", location = "待确认", raw = "明天早八 高数 记得带书")

        val model = actionReadinessUiModelFrom(item)

        assertFalse(model.steps.first { it.label == "地点" }.completed)
        assertEquals("还差地点，补上后更完整", model.subtitle)
    }

    @Test
    fun actionReadinessUiModelFrom_calendarIsCompleteAfterDraftOpened() {
        val item = courseItem(time = "明天早八", location = "B342", raw = "明天早八 高数 B342 记得带书")

        val model = actionReadinessUiModelFrom(
            item,
            executionResults = listOf(ExecutionResult("日历", "待用户保存", "已打开日历草稿，等你在系统日历里保存。")),
        )

        assertTrue(model.steps.first { it.label == "日历" }.completed)
    }

    private fun courseItem(time: String, location: String, raw: String) = ShikeItem(
        title = "高数",
        scene = "课程",
        time = time,
        location = location,
        status = "待确认",
        actions = listOf("打开日历草稿"),
        startEpochMillis = 1777000000000L,
        rawText = raw,
    )
}
