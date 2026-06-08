package cn.shike.app

import cn.shike.app.data.sampleCourse
import cn.shike.app.system.calendarInsertDescriptionFor
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class SystemActionsTest {
    @Test
    fun calendarInsertDescriptionFor_onlyDescribesSystemInsertPage() {
        val description = calendarInsertDescriptionFor(sampleCourse())

        assertTrue(description.contains("打开系统日历新增页"))
        assertTrue(description.contains("由用户在日历中保存"))
        assertFalse(description.contains("确认后写入"))
        assertFalse(description.contains("已保存"))
    }
}
