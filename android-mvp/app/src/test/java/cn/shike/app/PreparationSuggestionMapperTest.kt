package cn.shike.app

import cn.shike.app.domain.ShikeItem
import cn.shike.app.ui.defaultPreparationSuggestionsFor
import cn.shike.app.ui.preparationItemsForUi
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class PreparationSuggestionMapperTest {
    @Test
    fun meetingFallbackDoesNotShowCourseItems() {
        val suggestions = defaultPreparationSuggestionsFor(item(title = "班级班会", scene = "会议"))

        assertTrue("准备发言" in suggestions)
        assertFalse("带课本" in suggestions)
        assertFalse("带作业" in suggestions)
    }

    @Test
    fun courseFallbackCanShowCourseItems() {
        val suggestions = defaultPreparationSuggestionsFor(item(title = "高数", scene = "课程"))

        assertTrue("带课本" in suggestions)
        assertTrue("带作业" in suggestions)
    }

    @Test
    fun examFallbackShowsExamItems() {
        val suggestions = defaultPreparationSuggestionsFor(item(title = "高数考试", scene = "考试"))

        assertTrue("带准考证" in suggestions)
        assertTrue("带文具" in suggestions)
    }

    @Test
    fun modelPreparationItemsWinOverFallbackAndAreCleaned() {
        val result = preparationItemsForUi(item(title = "班级班会", scene = "会议", raw = "明天班会记得带红领巾'"))

        assertEquals(listOf("带红领巾"), result)
    }

    private fun item(
        title: String,
        scene: String,
        raw: String = "$title $scene",
    ) = ShikeItem(
        title = title,
        scene = scene,
        time = "明天早八",
        location = "B342",
        status = "待确认",
        actions = emptyList(),
        startEpochMillis = 1777000000000L,
        rawText = raw,
    )
}
