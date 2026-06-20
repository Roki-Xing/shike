package cn.shike.app.system

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import androidx.core.app.NotificationManagerCompat

class ScreenshotDismissReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent?) {
        if (intent?.action != ACTION_IGNORE_SCREENSHOT) return
        val contentUri = intent.getStringExtra(EXTRA_SCREENSHOT_URI).orEmpty()
        if (contentUri.isBlank()) return
        NotificationManagerCompat.from(context).cancel(contentUri.hashCode())
    }
}
