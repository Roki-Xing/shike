package cn.shike.app

import cn.shike.app.data.sampleCourse
import cn.shike.app.system.calendarDraftFrom
import cn.shike.app.system.calendarInsertDescriptionFor
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test
import java.time.Instant

class SystemActionsTest {
    @Test
    fun calendarInsertDescriptionFor_onlyDescribesSystemInsertPage() {
        val description = calendarInsertDescriptionFor(sampleCourse())

        assertTrue(description.contains("打开系统日历新增页"))
        assertTrue(description.contains("由用户在日历中保存"))
        assertFalse(description.contains("确认后写入"))
        assertFalse(description.contains("已保存"))
    }

    @Test
    fun calendarDraftFrom_usesParsedEpochAndDisablesWhenTimeIsMissing() {
        val parsedItem = sampleCourse().copy(
            title = "英语口语课",
            time = "明天早上九点",
            location = "E520",
            startEpochMillis = Instant.parse("2026-06-10T01:00:00Z").toEpochMilli(),
        )

        val draft = calendarDraftFrom(parsedItem)

        assertEquals("英语口语课", draft.title)
        assertEquals(Instant.parse("2026-06-10T01:00:00Z").toEpochMilli(), draft.startAtMillis)
        assertEquals(Instant.parse("2026-06-10T02:00:00Z").toEpochMilli(), draft.endAtMillis)
        assertEquals("E520", draft.location)
        assertNull(draft.disabledReason)
        assertTrue(draft.description.contains("打开系统日历新增页"))

        val missingTimeDraft = calendarDraftFrom(parsedItem.copy(time = "待确认", startEpochMillis = 0L))

        assertNull(missingTimeDraft.startAtMillis)
        assertNull(missingTimeDraft.endAtMillis)
        assertEquals("补充具体时间后可加入日历", missingTimeDraft.disabledReason)
    }
}
