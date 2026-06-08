package cn.shike.app.system

import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.ActivityNotFoundException
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Build
import android.provider.CalendarContract
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.net.toUri
import cn.shike.app.domain.ShikeItem

internal const val REMINDER_CHANNEL_ID = "shike_reminders"

/**
 * Builds the user-visible description for Android's calendar insert page.
 *
 * Args:
 *     item: Confirmed action card.
 *
 * Returns:
 *     Calendar event description that avoids claiming the event was saved.
 */
fun calendarInsertDescriptionFor(item: ShikeItem): String =
    "由拾刻从${item.scene}解析，用户确认后打开系统日历新增页，由用户在日历中保存。"

/**
 * Creates the Android notification channel used by local reminders.
 *
 * Args:
 *     context: Android context used to access system services.
 */
fun createReminderNotificationChannel(context: Context) {
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
        val channel = NotificationChannel(REMINDER_CHANNEL_ID, "拾刻提醒", NotificationManager.IMPORTANCE_DEFAULT)
        val manager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        manager.createNotificationChannel(channel)
    }
}

/**
 * Builds a system calendar insert intent for an action card.
 *
 * Args:
 *     item: Confirmed action card.
 *
 * Returns:
 *     Intent that opens Android's calendar insertion flow.
 */
fun buildCalendarInsertIntent(item: ShikeItem): Intent {
    val startMillis = item.startEpochMillis
    return Intent(Intent.ACTION_INSERT).apply {
        data = CalendarContract.Events.CONTENT_URI
        putExtra(CalendarContract.Events.TITLE, item.title)
        putExtra(CalendarContract.Events.EVENT_LOCATION, item.location)
        putExtra(CalendarContract.EXTRA_EVENT_BEGIN_TIME, startMillis)
        putExtra(CalendarContract.EXTRA_EVENT_END_TIME, startMillis + 60 * 60 * 1000)
        putExtra(CalendarContract.Events.DESCRIPTION, calendarInsertDescriptionFor(item))
    }
}

/**
 * Builds a geo deeplink intent for opening the selected location.
 *
 * Args:
 *     item: Confirmed action card.
 *
 * Returns:
 *     Intent that opens a map app for the card location.
 */
fun buildMapIntent(item: ShikeItem): Intent {
    val uri = "geo:0,0?q=${Uri.encode(item.location)}".toUri()
    return Intent(Intent.ACTION_VIEW, uri)
}

/**
 * Copies a map location when no map app can handle the deeplink.
 *
 * Args:
 *     context: Android context used to access the clipboard service.
 *     item: Current action card.
 *
 * Returns:
 *     Source text persisted with the local fallback snapshot.
 */
fun copyMapLocationFallback(context: Context, item: ShikeItem): String {
    val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
    clipboard.setPrimaryClip(ClipData.newPlainText("拾刻地点", item.location))
    return "已复制地点到剪贴板：${item.location}"
}

/**
 * Starts an external system activity and saves the card on fallback.
 *
 * Args:
 *     context: Android context used to start the activity.
 *     intent: External system intent.
 *     item: Current action card.
 *     fallbackSource: Source text persisted if the external activity cannot open.
 *     onFallback: Persistence callback for the local action-card fallback.
 */
fun startSystemActivitySafely(
    context: Context,
    intent: Intent,
    item: ShikeItem,
    fallbackSource: String,
    onFallback: (ShikeItem, String) -> Unit,
) {
    try {
        context.startActivity(intent)
    } catch (_: ActivityNotFoundException) {
        onFallback(item, fallbackSource)
    } catch (_: SecurityException) {
        onFallback(item, fallbackSource)
    }
}

/**
 * Shows the immediate local reminder notification.
 *
 * Args:
 *     context: Android context used to post the notification.
 *     item: Confirmed action card.
 */
fun showReminderNotification(context: Context, item: ShikeItem) {
    showReminderNotificationPayload(
        context = context,
        notificationId = item.title.hashCode(),
        title = item.title,
        detail = "${item.time} · ${item.location}",
    )
}

/**
 * Shows a local reminder notification from scheduled reminder payload.
 *
 * Args:
 *     context: Android context used to post the notification.
 *     notificationId: Stable notification id.
 *     title: Reminder title.
 *     detail: Reminder detail text.
 */
fun showReminderNotificationPayload(
    context: Context,
    notificationId: Int,
    title: String,
    detail: String,
) {
    val notification = NotificationCompat.Builder(context, REMINDER_CHANNEL_ID)
        .setSmallIcon(android.R.drawable.ic_dialog_info)
        .setContentTitle("拾刻提醒：$title")
        .setContentText(detail)
        .setPriority(NotificationCompat.PRIORITY_DEFAULT)
        .setAutoCancel(true)
        .build()
    try {
        NotificationManagerCompat.from(context).notify(notificationId, notification)
    } catch (_: SecurityException) {
        // Permission may still be denied on Android 13+.
    }
}
