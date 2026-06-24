package cn.shike.app.system

import android.content.Context

private const val SCREENSHOT_ASSIST_DIAGNOSTICS_PREFS = "shike_screenshot_assist_diagnostics"
private const val KEY_LAST_DETECTED_AT = "last_detected_at"
private const val KEY_LAST_NOTIFICATION_STATUS = "last_notification_status"
private const val KEY_SERVICE_HEARTBEAT_AT = "service_heartbeat_at"
private const val KEY_OBSERVER_OWNER = "observer_owner"
private const val KEY_OBSERVER_REGISTERED = "observer_registered"
private const val KEY_LAST_STOP_REASON = "last_stop_reason"
private const val SERVICE_HEARTBEAT_FRESH_MS = 20_000L

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
    val prefs = diagnosticsPrefs(context)
    val heartbeatAt = prefs.getLong(KEY_SERVICE_HEARTBEAT_AT, 0L)
    val heartbeatFresh = heartbeatAt > 0 && System.currentTimeMillis() - heartbeatAt <= SERVICE_HEARTBEAT_FRESH_MS
    val observerOwner = prefs.getString(KEY_OBSERVER_OWNER, null)?.takeIf { it.isNotBlank() }
    val observerRegistered = prefs.getBoolean(KEY_OBSERVER_REGISTERED, false)
    val stopReason = prefs.getString(KEY_LAST_STOP_REASON, null)?.takeIf { it.isNotBlank() }
    val healthText = when {
        enabled && heartbeatFresh && observerRegistered -> "运行中（${observerOwner ?: "service"}）"
        enabled && stopReason != null -> "已停止：$stopReason"
        enabled && serviceRunning -> "正在启动，等待服务心跳"
        enabled -> "未运行"
        else -> false.toString()
    }
    return ScreenshotAssistDiagnostics(
        enabled = enabled,
        mediaPermissionGranted = hasScreenshotMediaPermission(context),
        notificationPermissionGranted = canPostScreenshotAssistNotification(context),
        serviceRunning = enabled && heartbeatFresh && observerRegistered,
        lastDetectedAtText = stored.lastDetectedAtText,
        lastNotificationStatus = "${stored.lastNotificationStatus}；后台服务：$healthText",
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

fun recordScreenshotAssistHeartbeat(context: Context, observerOwner: String, observerRegistered: Boolean) {
    diagnosticsPrefs(context).edit()
        .putLong(KEY_SERVICE_HEARTBEAT_AT, System.currentTimeMillis())
        .putString(KEY_OBSERVER_OWNER, observerOwner)
        .putBoolean(KEY_OBSERVER_REGISTERED, observerRegistered)
        .remove(KEY_LAST_STOP_REASON)
        .apply()
}

fun recordScreenshotAssistStopped(context: Context, reason: String) {
    diagnosticsPrefs(context).edit()
        .putBoolean(KEY_OBSERVER_REGISTERED, false)
        .putString(KEY_LAST_STOP_REASON, reason)
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
