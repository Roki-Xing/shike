package cn.shike.app

import cn.shike.app.domain.ShikeItem
import cn.shike.app.ui.SmartFieldState
import cn.shike.app.ui.cleanPreparationItem
import cn.shike.app.ui.isAmbiguousTimeText
import cn.shike.app.ui.isCampusRoomCode
import cn.shike.app.ui.smartActionCardUiModelFrom
import cn.shike.app.ui.userFacingRiskCopy
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class SmartActionCardUiModelTest {
    @Test
    fun smartActionCard_marksMorningOnlyCourseTimeAsNeedsReview() {
        val item = ShikeItem(
            title = "高数",
            scene = "课程通知",
            time = "今天上午",
            location = "B342",
            status = "待确认",
            actions = listOf("加入日历", "课前提醒", "打开地图"),
            startEpochMillis = 0L,
            rawText = "今天上午 高数在B342",
        )

        val model = smartActionCardUiModelFrom(item)

        assertEquals("高数", model.title)
        assertEquals("课程", model.sceneLabel)
        assertEquals(SmartFieldState.NeedsReview, model.time.state)
        assertEquals(SmartFieldState.Confirmed, model.location.state)
        assertEquals("B342", model.location.value)
        assertTrue(model.time.helper.contains("确认具体开始时间"))
    }

    @Test
    fun smartActionCard_recognizesCampusRoomCodes() {
        assertTrue(isCampusRoomCode("B342"))
        assertTrue(isCampusRoomCode("E520"))
        assertTrue(isCampusRoomCode("B地点303"))
        assertTrue(isCampusRoomCode("二教305"))
    }

    @Test
    fun smartActionCard_marksApproximateNightTimeAsNeedsReview() {
        assertTrue(isAmbiguousTimeText("今天晚上大概九点"))
        val item = ShikeItem(
            title = "晚自习",
            scene = "课程通知",
            time = "今天晚上大概九点",
            location = "B342",
            status = "待确认",
            actions = listOf("加入日历"),
            startEpochMillis = 1777035600000L,
            rawText = "今天晚上大概九点 晚自习 B342",
        )

        val model = smartActionCardUiModelFrom(item)

        assertEquals(SmartFieldState.NeedsReview, model.time.state)
        assertTrue(model.time.value.contains("建议时间"))
    }

    @Test
    fun sanitizer_cleansPreparationQuotesAndRiskCopy() {
        assertEquals("带红领巾", cleanPreparationItem("带红领巾'"))
        assertEquals("可能有截止时间，请确认", userFacingRiskCopy("deadline"))
        assertEquals("地点还没识别到，可以稍后补充", userFacingRiskCopy("missing_location"))
    }
}
