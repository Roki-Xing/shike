package cn.shike.app.system

import cn.shike.app.domain.ShikeItem
import cn.shike.app.domain.reminderDetailFor
import kotlin.math.max

private const val REMINDER_LEAD_MILLIS = 15 * 60 * 1000L
private const val MINIMUM_FUTURE_DELAY_MILLIS = 60 * 1000L
const val REMINDER_FALLBACK_DETAIL = "请查看拾刻行动卡。"

data class ScheduledReminder(
    val title: String,
    val detail: String,
    val notificationId: Int,
    val triggerAtMillis: Long,
)

data class ReminderDeliveryPayload(
    val title: String,
    val detail: String,
    val notificationId: Int,
)

/**
 * Builds the persisted reminder payload for a confirmed action card.
 *
 * Args:
 *     item: Confirmed action card.
 *     nowMillis: Current wall-clock time.
 *
 * Returns:
 *     Stable reminder payload used by AlarmManager and reboot recovery.
 */
fun scheduledReminderFrom(item: ShikeItem, nowMillis: Long): ScheduledReminder =
    ScheduledReminder(
        title = item.title,
        detail = reminderDetailFor(item),
        notificationId = item.title.hashCode(),
        triggerAtMillis = scheduledReminderTriggerAtMillis(item.startEpochMillis, nowMillis),
    )

/**
 * Builds the user-visible result text after reminder scheduling.
 *
 * Args:
 *     item: Confirmed action card.
 *     exactScheduled: Whether the exact alarm API accepted the request.
 *
 * Returns:
 *     Execution-result detail shown in the action planner.
 */
fun reminderScheduleResultDetail(item: ShikeItem, exactScheduled: Boolean): String {
    val mode = if (exactScheduled) "精确定时" else "系统普通定时"
    return "已调度本地定时提醒：${item.time} 前约15分钟；若时间已临近，将在1分钟后提醒。调度模式：$mode。"
}

/**
 * Decides whether a persisted reminder should be restored.
 *
 * Args:
 *     reminder: Persisted reminder payload.
 *     nowMillis: Current wall-clock time.
 *
 * Returns:
 *     True when the trigger is still in the future.
 */
fun shouldRestoreScheduledReminder(reminder: ScheduledReminder, nowMillis: Long): Boolean =
    reminder.triggerAtMillis > nowMillis

/**
 * Builds the notification payload delivered by `ReminderReceiver`.
 *
 * Args:
 *     title: Title read from the alarm intent.
 *     detail: Detail read from the alarm intent.
 *     notificationId: Optional stable notification id read from the alarm intent.
 *
 * Returns:
 *     Notification payload, or null when the required title is missing.
 */
fun reminderDeliveryPayloadFrom(title: String?, detail: String?, notificationId: Int?): ReminderDeliveryPayload? {
    val safeTitle = title?.takeIf { it.isNotBlank() } ?: return null
    return ReminderDeliveryPayload(
        title = safeTitle,
        detail = detail?.takeIf { it.isNotBlank() } ?: REMINDER_FALLBACK_DETAIL,
        notificationId = notificationId ?: safeTitle.hashCode(),
    )
}

private fun scheduledReminderTriggerAtMillis(startEpochMillis: Long, nowMillis: Long): Long =
    max(nowMillis + MINIMUM_FUTURE_DELAY_MILLIS, startEpochMillis - REMINDER_LEAD_MILLIS)
