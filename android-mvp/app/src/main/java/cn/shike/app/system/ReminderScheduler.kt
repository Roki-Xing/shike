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
private const val KEY_REMINDER_IDS = "scheduled_reminder_ids"
private const val KEY_REMINDER_TITLE_PREFIX = "scheduled_reminder_title_"
private const val KEY_REMINDER_DETAIL_PREFIX = "scheduled_reminder_detail_"
private const val KEY_REMINDER_TRIGGER_PREFIX = "scheduled_reminder_trigger_"
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
    val preferences = context.getSharedPreferences(REMINDER_PREFERENCES_NAME, Context.MODE_PRIVATE)
    migrateLegacyReminderIfNeeded(preferences)
    var restored = false
    loadScheduledRemindersFromPreferences(preferences).forEach { reminder ->
        if (shouldRestoreScheduledReminder(reminder, System.currentTimeMillis())) {
            scheduleReminderPayload(context, reminder)
            restored = true
        } else {
            removeScheduledReminderFromPreferences(preferences, reminder.notificationId)
        }
    }
    return restored
}

/**
 * Cancels the pending system alarm and clears its persisted payload.
 *
 * Args:
 *     context: Android context used to access app-scoped preferences and AlarmManager.
 */
fun cancelScheduledReminder(context: Context) {
    val preferences = context.getSharedPreferences(REMINDER_PREFERENCES_NAME, Context.MODE_PRIVATE)
    migrateLegacyReminderIfNeeded(preferences)
    loadScheduledRemindersFromPreferences(preferences).forEach { reminder ->
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
    clearScheduledReminderFromPreferences(preferences)
}

fun removeScheduledReminder(context: Context, notificationId: Int) {
    removeScheduledReminderFromPreferences(
        context.getSharedPreferences(REMINDER_PREFERENCES_NAME, Context.MODE_PRIVATE),
        notificationId,
    )
}

/**
 * Clears the persisted scheduled reminder after delivery or expiry.
 *
 * Args:
 *     context: Android context used to access app-scoped preferences.
 */
fun clearScheduledReminder(context: Context) {
    clearScheduledReminderFromPreferences(
        context.getSharedPreferences(REMINDER_PREFERENCES_NAME, Context.MODE_PRIVATE),
    )
}

internal fun clearScheduledReminderFromPreferences(preferences: SharedPreferences) {
    migrateLegacyReminderIfNeeded(preferences)
    val ids = reminderIdsFromPreferences(preferences)
    val editor = preferences.edit()
        .remove(KEY_REMINDER_IDS)
        .remove(KEY_SCHEDULED_TITLE)
        .remove(KEY_SCHEDULED_DETAIL)
        .remove(KEY_SCHEDULED_ID)
        .remove(KEY_SCHEDULED_TRIGGER)
    ids.forEach { id ->
        editor
            .remove(KEY_REMINDER_TITLE_PREFIX + id)
            .remove(KEY_REMINDER_DETAIL_PREFIX + id)
            .remove(KEY_REMINDER_TRIGGER_PREFIX + id)
    }
    editor.apply()
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
    addScheduledReminderToPreferences(
        context.getSharedPreferences(REMINDER_PREFERENCES_NAME, Context.MODE_PRIVATE),
        reminder,
    )
}

private fun loadLegacyScheduledReminder(preferences: SharedPreferences): ScheduledReminder? {
    val title = preferences.getString(KEY_SCHEDULED_TITLE, null) ?: return null
    val detail = preferences.getString(KEY_SCHEDULED_DETAIL, null) ?: REMINDER_FALLBACK_DETAIL
    val notificationId = preferences.getInt(KEY_SCHEDULED_ID, title.hashCode())
    val triggerAtMillis = preferences.getLong(KEY_SCHEDULED_TRIGGER, 0L)
    if (triggerAtMillis <= 0L) return null
    return ScheduledReminder(title, detail, notificationId, triggerAtMillis)
}

internal fun addScheduledReminderToPreferences(preferences: SharedPreferences, reminder: ScheduledReminder) {
    migrateLegacyReminderIfNeeded(preferences)
    val ids = reminderIdsFromPreferences(preferences).toMutableSet()
    ids.add(reminder.notificationId)
    preferences.edit()
        .putStringSet(KEY_REMINDER_IDS, ids.map { it.toString() }.toMutableSet())
        .putString(KEY_REMINDER_TITLE_PREFIX + reminder.notificationId, reminder.title)
        .putString(KEY_REMINDER_DETAIL_PREFIX + reminder.notificationId, reminder.detail)
        .putLong(KEY_REMINDER_TRIGGER_PREFIX + reminder.notificationId, reminder.triggerAtMillis)
        .apply()
}

internal fun removeScheduledReminderFromPreferences(preferences: SharedPreferences, notificationId: Int) {
    migrateLegacyReminderIfNeeded(preferences)
    val ids = reminderIdsFromPreferences(preferences).toMutableSet()
    ids.remove(notificationId)
    preferences.edit()
        .putStringSet(KEY_REMINDER_IDS, ids.map { it.toString() }.toMutableSet())
        .remove(KEY_REMINDER_TITLE_PREFIX + notificationId)
        .remove(KEY_REMINDER_DETAIL_PREFIX + notificationId)
        .remove(KEY_REMINDER_TRIGGER_PREFIX + notificationId)
        .apply()
}

internal fun loadScheduledRemindersFromPreferences(preferences: SharedPreferences): List<ScheduledReminder> {
    migrateLegacyReminderIfNeeded(preferences)
    return reminderIdsFromPreferences(preferences).mapNotNull { id ->
        val title = preferences.getString(KEY_REMINDER_TITLE_PREFIX + id, null) ?: return@mapNotNull null
        val detail = preferences.getString(KEY_REMINDER_DETAIL_PREFIX + id, null) ?: REMINDER_FALLBACK_DETAIL
        val triggerAt = preferences.getLong(KEY_REMINDER_TRIGGER_PREFIX + id, 0L)
        if (triggerAt <= 0L) return@mapNotNull null
        ScheduledReminder(title, detail, id, triggerAt)
    }.sortedBy { it.triggerAtMillis }
}

private fun migrateLegacyReminderIfNeeded(preferences: SharedPreferences) {
    if (preferences.getStringSet(KEY_REMINDER_IDS, null) != null) return
    val legacy = loadLegacyScheduledReminder(preferences) ?: return
    val ids = mutableSetOf(legacy.notificationId.toString())
    preferences.edit()
        .putStringSet(KEY_REMINDER_IDS, ids)
        .putString(KEY_REMINDER_TITLE_PREFIX + legacy.notificationId, legacy.title)
        .putString(KEY_REMINDER_DETAIL_PREFIX + legacy.notificationId, legacy.detail)
        .putLong(KEY_REMINDER_TRIGGER_PREFIX + legacy.notificationId, legacy.triggerAtMillis)
        .apply()
}

private fun reminderIdsFromPreferences(preferences: SharedPreferences): Set<Int> =
    preferences.getStringSet(KEY_REMINDER_IDS, mutableSetOf())
        .orEmpty()
        .mapNotNull { it.toIntOrNull() }
        .toSet()

private fun reminderIntent(context: Context, reminder: ScheduledReminder): Intent =
    Intent(context, ReminderReceiver::class.java).apply {
        putExtra(EXTRA_REMINDER_TITLE, reminder.title)
        putExtra(EXTRA_REMINDER_DETAIL, reminder.detail)
        putExtra(EXTRA_REMINDER_ID, reminder.notificationId)
    }
