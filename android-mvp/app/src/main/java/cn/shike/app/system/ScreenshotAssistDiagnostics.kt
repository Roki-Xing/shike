package cn.shike.app.system

import android.content.Context

private const val SCREENSHOT_ASSIST_DIAGNOSTICS_PREFS = "shike_screenshot_assist_diagnostics"
private const val KEY_LAST_DETECTED_AT = "last_detected_at"
private const val KEY_LAST_NOTIFICATION_STATUS = "last_notification_status"

data class ScreenshotAssistDiagnostics(
    val enabled: Boolean,
    val mediaPermissionGranted: Boolean,
    val notificationPermissionGranted: Boolean,
    val serviceRunning: Boolean,
    val lastDetectedAtText: String,
    val lastNotificationStatus: String,
)

fun screenshotAssistDiagnostics(
    context: Context,
    enabled: Boolean,
    serviceRunning: Boolean,
): ScreenshotAssistDiagnostics {
    val stored = loadScreenshotAssistDiagnostics(context)
    return ScreenshotAssistDiagnostics(
        enabled = enabled,
        mediaPermissionGranted = hasScreenshotMediaPermission(context),
        notificationPermissionGranted = canPostScreenshotAssistNotification(context),
        serviceRunning = serviceRunning,
        lastDetectedAtText = stored.lastDetectedAtText,
        lastNotificationStatus = stored.lastNotificationStatus,
    )
}

fun recordScreenshotAssistDetected(context: Context, createdAtMillis: Long) {
    diagnosticsPrefs(context).edit()
        .putLong(KEY_LAST_DETECTED_AT, createdAtMillis.takeIf { it > 0 } ?: System.currentTimeMillis())
        .apply()
}

fun recordScreenshotAssistNotification(context: Context, status: String) {
    diagnosticsPrefs(context).edit()
        .putString(KEY_LAST_NOTIFICATION_STATUS, status)
        .apply()
}

fun loadScreenshotAssistDiagnostics(context: Context): ScreenshotAssistDiagnostics {
    val prefs = diagnosticsPrefs(context)
    val lastDetectedAt = prefs.getLong(KEY_LAST_DETECTED_AT, 0L)
    return ScreenshotAssistDiagnostics(
        enabled = false,
        mediaPermissionGranted = false,
        notificationPermissionGranted = false,
        serviceRunning = false,
        lastDetectedAtText = if (lastDetectedAt > 0) "最近检测截图：${lastDetectedAt}" else "最近检测截图：暂无记录",
        lastNotificationStatus = prefs.getString(KEY_LAST_NOTIFICATION_STATUS, null)
            ?.let { "最近通知：$it" }
            ?: "最近通知：暂无记录",
    )
}

private fun diagnosticsPrefs(context: Context) =
    context.getSharedPreferences(SCREENSHOT_ASSIST_DIAGNOSTICS_PREFS, Context.MODE_PRIVATE)
