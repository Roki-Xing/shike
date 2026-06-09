package cn.shike.app.system

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import cn.shike.app.data.ScreenshotCandidate

const val SCREENSHOT_ASSIST_CHANNEL_ID = "shike_screenshot_assist"
const val ACTION_IMPORT_SCREENSHOT = "cn.shike.app.action.IMPORT_SCREENSHOT"
const val EXTRA_SCREENSHOT_URI = "cn.shike.app.extra.SCREENSHOT_URI"
const val EXTRA_SCREENSHOT_CREATED_AT_MILLIS = "cn.shike.app.extra.SCREENSHOT_CREATED_AT_MILLIS"
const val EXTRA_SCREENSHOT_WIDTH = "cn.shike.app.extra.SCREENSHOT_WIDTH"
const val EXTRA_SCREENSHOT_HEIGHT = "cn.shike.app.extra.SCREENSHOT_HEIGHT"
const val EXTRA_SCREENSHOT_DISPLAY_NAME_DIGEST = "cn.shike.app.extra.SCREENSHOT_DISPLAY_NAME_DIGEST"

fun createScreenshotAssistNotificationChannel(context: Context) {
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
        val channel = NotificationChannel(
            SCREENSHOT_ASSIST_CHANNEL_ID,
            "拾刻截图助手",
            NotificationManager.IMPORTANCE_HIGH,
        )
        val manager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        manager.createNotificationChannel(channel)
    }
}

fun showScreenshotDetectedNotification(context: Context, candidate: ScreenshotCandidate) {
    val launchIntent = context.packageManager.getLaunchIntentForPackage(context.packageName)
        ?: Intent(Intent.ACTION_MAIN)
    launchIntent.action = ACTION_IMPORT_SCREENSHOT
    launchIntent.putExtra(EXTRA_SCREENSHOT_URI, candidate.contentUri)
    launchIntent.putExtra(EXTRA_SCREENSHOT_CREATED_AT_MILLIS, candidate.createdAtMillis)
    launchIntent.putExtra(EXTRA_SCREENSHOT_WIDTH, candidate.width)
    launchIntent.putExtra(EXTRA_SCREENSHOT_HEIGHT, candidate.height)
    launchIntent.putExtra(EXTRA_SCREENSHOT_DISPLAY_NAME_DIGEST, candidate.displayNameDigest)
    val pendingIntent = PendingIntent.getActivity(
        context,
        candidate.contentUri.hashCode(),
        launchIntent,
        PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE,
    )
    val notification = NotificationCompat.Builder(context, SCREENSHOT_ASSIST_CHANNEL_ID)
        .setSmallIcon(android.R.drawable.ic_menu_upload)
        .setContentTitle("检测到截图，是否交给拾刻？")
        .setContentText("点击后生成可确认的行动卡。")
        .setPriority(NotificationCompat.PRIORITY_HIGH)
        .setContentIntent(pendingIntent)
        .setAutoCancel(true)
        .build()
    try {
        NotificationManagerCompat.from(context).notify(candidate.contentUri.hashCode(), notification)
    } catch (_: SecurityException) {
        // Notification permission may be denied on Android 13+.
    }
}
