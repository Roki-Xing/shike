package cn.shike.app

import cn.shike.app.domain.ShikeItem
import cn.shike.app.ui.actionCardUiModelFrom
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class FlexibleActionCardTest {
    @Test
    fun actionCardUiModel_extractsPreparationAndKeepsItOutOfTitle() {
        val item = ShikeItem(
            title = "明天早上九点上英语口语教室E520，记得带书",
            scene = "课程通知",
            time = "明天早上九点 / null",
            location = "E520",
            status = "待确认",
            actions = listOf("加入日历", "课前提醒", "打开地图"),
            startEpochMillis = 1_800_000L,
            rawText = """
                OCR原文：明天早上九点上英语口语教室E520，记得带书
                任务：上英语口语，记得带书
                风险：relative_time；schema_valid；provider_error
                待补：manual_review
            """.trimIndent(),
        )

        val model = actionCardUiModelFrom(item)

        assertEquals("英语口语课", model.title)
        assertEquals(listOf("带书"), model.preparationItems)
        assertFalse(model.title.contains("记得带书"))
        assertFalse(model.time.contains("null", ignoreCase = true))
        assertTrue(model.userWarnings.contains("时间来自“明天/今晚”等相对表达，请确认日期"))
        assertTrue(model.userWarnings.contains("AI 暂时不可用，已保留待确认卡"))
        assertTrue(model.userWarnings.contains("待你确认"))
        assertFalse(model.userWarnings.any { it.contains("schema_valid") || it.contains("provider_error") || it.contains("manual_review") })
    }

    @Test
    fun actionCardUiModel_extractsCommonFlexiblePreparationItems() {
        val cases = listOf(
            "今晚七点组会腾讯会议，提前准备周报" to listOf("提前准备周报"),
            "明天下午三点实验课，带实验报告和学生证" to listOf("带实验报告", "带学生证"),
            "周五十点面试，提前十分钟上线" to listOf("提前十分钟上线"),
            "下周一早八到北门集合，先去签到" to listOf("到北门集合", "先去签到"),
        )

        cases.forEach { (text, expected) ->
            val item = ShikeItem(
                title = text,
                scene = "待确认",
                time = "待确认",
                location = "待确认",
                status = "待确认",
                actions = listOf("稍后确认"),
                startEpochMillis = 0L,
                rawText = "任务：$text",
            )

            assertEquals(expected, actionCardUiModelFrom(item).preparationItems)
        }
    }
}
