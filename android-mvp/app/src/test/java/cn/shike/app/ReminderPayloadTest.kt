package cn.shike.app

import cn.shike.app.data.sampleCourse
import cn.shike.app.system.REMINDER_FALLBACK_DETAIL
import cn.shike.app.system.ScheduledReminder
import cn.shike.app.system.reminderDeliveryPayloadFrom
import cn.shike.app.system.reminderScheduleResultDetail
import cn.shike.app.system.scheduledReminderFrom
import cn.shike.app.system.shouldRestoreScheduledReminder
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class ReminderPayloadTest {
    @Test
    fun scheduledReminderFrom_keepsStablePayloadFields() {
        val item = sampleCourse().copy(
            title = "课程提醒",
            time = "今天 18:30",
            location = "B203",
            startEpochMillis = 1_000_000L,
        )

        val reminder = scheduledReminderFrom(item, nowMillis = 0L)

        assertEquals("课程提醒", reminder.title)
        assertEquals("今天 18:30 · B203", reminder.detail)
        assertEquals("课程提醒".hashCode(), reminder.notificationId)
        assertEquals(100_000L, reminder.triggerAtMillis)
    }

    @Test
    fun scheduledReminderFrom_nearStartUsesOneMinuteFallbackAndResultMode() {
        val item = sampleCourse().copy(
            time = "今天 18:30 / 22:00 截止",
            startEpochMillis = 120_000L,
        )

        val reminder = scheduledReminderFrom(item, nowMillis = 100_000L)

        assertEquals(160_000L, reminder.triggerAtMillis)
        assertTrue(reminderScheduleResultDetail(item, exactScheduled = true).contains("调度模式：精确定时"))
        assertTrue(reminderScheduleResultDetail(item, exactScheduled = false).contains("调度模式：系统普通定时"))
    }

    @Test
    fun shouldRestoreScheduledReminder_rejectsExpiredPayload() {
        val reminder = ScheduledReminder("活动提醒", "图书馆报告厅", 7, 2_000L)

        assertTrue(shouldRestoreScheduledReminder(reminder, nowMillis = 1_999L))
        assertFalse(shouldRestoreScheduledReminder(reminder, nowMillis = 2_000L))
        assertFalse(shouldRestoreScheduledReminder(reminder, nowMillis = 2_001L))
    }

    @Test
    fun reminderDeliveryPayloadFrom_keepsIntentPayloadFields() {
        val payload = reminderDeliveryPayloadFrom(
            title = "面试提醒",
            detail = "明天 09:00 · 腾讯会议",
            notificationId = 42,
        )

        assertEquals("面试提醒", payload?.title)
        assertEquals("明天 09:00 · 腾讯会议", payload?.detail)
        assertEquals(42, payload?.notificationId)
    }

    @Test
    fun reminderDeliveryPayloadFrom_defaultsMissingDetailAndId() {
        val payload = reminderDeliveryPayloadFrom(
            title = "课程提醒",
            detail = null,
            notificationId = null,
        )

        assertEquals("课程提醒", payload?.title)
        assertEquals(REMINDER_FALLBACK_DETAIL, payload?.detail)
        assertEquals("课程提醒".hashCode(), payload?.notificationId)
    }

    @Test
    fun reminderDeliveryPayloadFrom_rejectsMissingOrBlankTitle() {
        assertNull(reminderDeliveryPayloadFrom(title = null, detail = "地点", notificationId = 1))
        assertNull(reminderDeliveryPayloadFrom(title = "", detail = "地点", notificationId = 1))
    }
}
