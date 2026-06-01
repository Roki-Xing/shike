package cn.shike.app.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class InboxEntitiesTest {
    @Test
    fun syntheticInboxSeed_providesFiftySearchableStatusRecords() {
        val records = syntheticInboxSeed()
        val statuses = records.map { it.status }.toSet()

        assertEquals(50, records.size)
        assertTrue(statuses.containsAll(listOf("待确认", "已安排", "即将截止", "已完成", "已忽略")))
        assertTrue(records.any { it.rawText.contains("OCR 摘要") })
    }

    @Test
    fun inboxItemEntityFrom_redactsSourceAndRawTextAndKeepsActions() {
        val entity = inboxItemEntityFrom(
            item = sampleCourse().copy(rawText = "联系 13812345678 demo@example.com"),
            captureSource = "截图 192.168.1.10:8000",
            updatedEpochMillis = 100L,
        )

        assertEquals(sampleCourse().actions, entity.actionLabels)
        assertEquals("已安排", normalizeInboxStatus(entity.status))
        assertTrue(entity.source.contains("[局域网地址已脱敏]"))
        assertTrue(entity.rawText.contains("[手机号已脱敏]"))
        assertFalse(entity.rawText.contains("13812345678"))
    }

    @Test
    fun shikeItemFromInboxEntity_restoresActionCardShape() {
        val entity = syntheticInboxSeed(1).first().copy(status = "未知")
        val item = shikeItemFromInboxEntity(entity)

        assertEquals(entity.title, item.title)
        assertEquals("待确认", item.status)
        assertEquals(entity.actionLabels, item.actions)
    }
}
