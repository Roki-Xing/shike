package cn.shike.app.system

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent

class ReminderReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == Intent.ACTION_BOOT_COMPLETED) {
            restoreScheduledReminder(context)
            return
        }

        val payload = reminderDeliveryPayloadFrom(
            title = intent.getStringExtra(EXTRA_REMINDER_TITLE),
            detail = intent.getStringExtra(EXTRA_REMINDER_DETAIL),
            notificationId = if (intent.hasExtra(EXTRA_REMINDER_ID)) {
                intent.getIntExtra(EXTRA_REMINDER_ID, 0)
            } else {
                null
            },
        ) ?: return
        showReminderNotificationPayload(
            context = context,
            notificationId = payload.notificationId,
            title = payload.title,
            detail = payload.detail,
        )
        clearScheduledReminder(context)
    }
}
