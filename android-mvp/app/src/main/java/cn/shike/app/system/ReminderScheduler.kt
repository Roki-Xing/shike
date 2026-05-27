package cn.shike.app.system

import android.app.AlarmManager
import android.app.PendingIntent
import android.content.Context
import android.content.SharedPreferences
import android.content.Intent
import android.os.Build
import cn.shike.app.domain.ShikeItem

private const val REMINDER_PREFERENCES_NAME = "shike_reminder_state"
private const val KEY_SCHEDULED_TITLE = "scheduled_reminder_title"
private const val KEY_SCHEDULED_DETAIL = "scheduled_reminder_detail"
private const val KEY_SCHEDULED_ID = "scheduled_reminder_id"
private const val KEY_SCHEDULED_TRIGGER = "scheduled_reminder_trigger_at_millis"
internal const val EXTRA_REMINDER_TITLE = "cn.shike.app.extra.REMINDER_TITLE"
internal const val EXTRA_REMINDER_DETAIL = "cn.shike.app.extra.REMINDER_DETAIL"
internal const val EXTRA_REMINDER_ID = "cn.shike.app.extra.REMINDER_ID"

/**
 * Schedules a real local reminder alarm for a confirmed action card.
 *
 * Args:
 *     context: Android context used to access AlarmManager.
 *     item: Confirmed action card.
 *
 * Returns:
 *     Human-readable schedule detail for execution-result display and logs.
 */
fun scheduleReminder(context: Context, item: ShikeItem): String {
    val reminder = scheduledReminderFrom(item, System.currentTimeMillis())
    val exactScheduled = scheduleReminderPayload(context, reminder)
    persistScheduledReminder(context, reminder)
    return reminderScheduleResultDetail(item, exactScheduled)
}

/**
 * Restores a pending reminder after app start or device reboot.
 *
 * Args:
 *     context: Android context used to access app-scoped preferences and AlarmManager.
 *
 * Returns:
 *     True when a non-expired reminder was restored into AlarmManager.
 */
fun restoreScheduledReminder(context: Context): Boolean {
    val reminder = loadScheduledReminder(context) ?: return false
    if (!shouldRestoreScheduledReminder(reminder, System.currentTimeMillis())) {
        clearScheduledReminder(context)
        return false
    }
    scheduleReminderPayload(context, reminder)
    return true
}

/**
 * Cancels the pending system alarm and clears its persisted payload.
 *
 * Args:
 *     context: Android context used to access app-scoped preferences and AlarmManager.
 */
fun cancelScheduledReminder(context: Context) {
    val reminder = loadScheduledReminder(context)
    if (reminder != null) {
        val pendingIntent = PendingIntent.getBroadcast(
            context,
            reminder.notificationId,
            reminderIntent(context, reminder),
            PendingIntent.FLAG_NO_CREATE or PendingIntent.FLAG_IMMUTABLE,
        )
        if (pendingIntent != null) {
            val alarmManager = context.getSystemService(Context.ALARM_SERVICE) as AlarmManager
            alarmManager.cancel(pendingIntent)
            pendingIntent.cancel()
        }
    }
    clearScheduledReminder(context)
}

/**
 * Clears the persisted scheduled reminder after delivery or expiry.
 *
 * Args:
 *     context: Android context used to access app-scoped preferences.
 */
fun clearScheduledReminder(context: Context) {
    context.getSharedPreferences(REMINDER_PREFERENCES_NAME, Context.MODE_PRIVATE).edit()
        .remove(KEY_SCHEDULED_TITLE)
        .remove(KEY_SCHEDULED_DETAIL)
        .remove(KEY_SCHEDULED_ID)
        .remove(KEY_SCHEDULED_TRIGGER)
        .apply()
}

internal fun clearScheduledReminderFromPreferences(preferences: SharedPreferences) {
    preferences.edit()
        .remove(KEY_SCHEDULED_TITLE)
        .remove(KEY_SCHEDULED_DETAIL)
        .remove(KEY_SCHEDULED_ID)
        .remove(KEY_SCHEDULED_TRIGGER)
        .apply()
}

private fun scheduleReminderPayload(context: Context, reminder: ScheduledReminder): Boolean {
    val alarmManager = context.getSystemService(Context.ALARM_SERVICE) as AlarmManager
    val pendingIntent = PendingIntent.getBroadcast(
        context,
        reminder.notificationId,
        reminderIntent(context, reminder),
        PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE,
    )
    if (canScheduleExactReminder(alarmManager)) {
        try {
            alarmManager.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, reminder.triggerAtMillis, pendingIntent)
            return true
        } catch (_: SecurityException) {
            // Android exact-alarm policy may change after capability checks; keep a usable fallback.
        }
    }
    alarmManager.set(AlarmManager.RTC_WAKEUP, reminder.triggerAtMillis, pendingIntent)
    return false
}

private fun canScheduleExactReminder(alarmManager: AlarmManager): Boolean =
    Build.VERSION.SDK_INT < Build.VERSION_CODES.S || alarmManager.canScheduleExactAlarms()

private fun persistScheduledReminder(context: Context, reminder: ScheduledReminder) {
    context.getSharedPreferences(REMINDER_PREFERENCES_NAME, Context.MODE_PRIVATE).edit()
        .putString(KEY_SCHEDULED_TITLE, reminder.title)
        .putString(KEY_SCHEDULED_DETAIL, reminder.detail)
        .putInt(KEY_SCHEDULED_ID, reminder.notificationId)
        .putLong(KEY_SCHEDULED_TRIGGER, reminder.triggerAtMillis)
        .apply()
}

private fun loadScheduledReminder(context: Context): ScheduledReminder? {
    val preferences = context.getSharedPreferences(REMINDER_PREFERENCES_NAME, Context.MODE_PRIVATE)
    val title = preferences.getString(KEY_SCHEDULED_TITLE, null) ?: return null
    val detail = preferences.getString(KEY_SCHEDULED_DETAIL, null) ?: REMINDER_FALLBACK_DETAIL
    val notificationId = preferences.getInt(KEY_SCHEDULED_ID, title.hashCode())
    val triggerAtMillis = preferences.getLong(KEY_SCHEDULED_TRIGGER, 0L)
    if (triggerAtMillis <= 0L) return null
    return ScheduledReminder(title, detail, notificationId, triggerAtMillis)
}

private fun reminderIntent(context: Context, reminder: ScheduledReminder): Intent =
    Intent(context, ReminderReceiver::class.java).apply {
        putExtra(EXTRA_REMINDER_TITLE, reminder.title)
        putExtra(EXTRA_REMINDER_DETAIL, reminder.detail)
        putExtra(EXTRA_REMINDER_ID, reminder.notificationId)
    }
