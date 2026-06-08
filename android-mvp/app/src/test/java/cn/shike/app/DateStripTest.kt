package cn.shike.app

import cn.shike.app.ui.dateStripSubtitle
import cn.shike.app.ui.formatTodayForHome
import java.time.LocalDate
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class DateStripTest {
    @Test
    fun formatTodayForHome_usesInjectedSystemDateWithoutLunarOrFixedDemoDate() {
        val text = formatTodayForHome(LocalDate.of(2026, 6, 8))

        assertEquals("6月8日 星期一", text)
        assertFalse(text.contains("5月24日"))
        assertFalse(text.contains("农历"))
    }

    @Test
    fun dateStripSubtitle_statesDateIsSortingHintNotTaskTime() {
        val subtitle = dateStripSubtitle()

        assertTrue(subtitle.contains("仅用于排序提示"))
        assertTrue(subtitle.contains("不作为任务时间"))
        assertFalse(subtitle.contains("自动当作任务时间"))
    }
}
