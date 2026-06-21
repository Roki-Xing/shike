package cn.shike.app.data

import android.content.Context
import android.content.SharedPreferences

private const val SCREENSHOT_ASSIST_PREFERENCES_NAME = "shike_screenshot_assist_state"
internal const val KEY_SCREENSHOT_ASSIST_ENABLED = "screenshot_assist_enabled"
internal const val KEY_LAST_SCREENSHOT_ASSIST_NOTIFIED_URI = "last_screenshot_assist_notified_uri"
const val SCREENSHOT_ASSIST_LOOKBACK_SECONDS = 30L
private const val SCREENSHOT_ASSIST_IMPORT_SOURCE_LABEL = "最近截图助手导入"

data class ScreenshotCandidate(
    val contentUri: String,
    val createdAtMillis: Long,
    val width: Int,
    val height: Int,
    val displayNameDigest: String,
    val sourceLabel: String = "",
)

fun screenshotDisplayNameDigest(displayName: String): String =
    displayName.hashCode().toUInt().toString(16)

fun shouldNotifyScreenshotCandidate(
    candidate: ScreenshotCandidate,
    lastNotifiedContentUri: String?,
): Boolean = candidate.contentUri != lastNotifiedContentUri

fun shouldNotifyScreenshotCandidate(
    preferences: SharedPreferences,
    candidate: ScreenshotCandidate,
): Boolean =
    shouldNotifyScreenshotCandidate(candidate, loadLastScreenshotAssistNotifiedUriFromPreferences(preferences))

fun shouldNotifyScreenshotCandidate(context: Context, candidate: ScreenshotCandidate): Boolean =
    shouldNotifyScreenshotCandidate(screenshotAssistPreferences(context), candidate)

fun recordScreenshotAssistNotified(context: Context, candidate: ScreenshotCandidate) {
    recordScreenshotAssistNotifiedToPreferences(screenshotAssistPreferences(context), candidate)
}

internal fun recordScreenshotAssistNotifiedToPreferences(
    preferences: SharedPreferences,
    candidate: ScreenshotCandidate,
) {
    preferences.edit()
        .putString(KEY_LAST_SCREENSHOT_ASSIST_NOTIFIED_URI, candidate.contentUri)
        .apply()
}

internal fun loadLastScreenshotAssistNotifiedUriFromPreferences(preferences: SharedPreferences): String? =
    preferences.getString(KEY_LAST_SCREENSHOT_ASSIST_NOTIFIED_URI, null)

fun screenshotCandidateFromNotificationImport(
    contentUri: String?,
    createdAtMillis: Long,
    width: Int,
    height: Int,
    displayNameDigest: String?,
    nowMillis: Long,
): ScreenshotCandidate? {
    val uri = contentUri?.takeIf { it.isNotBlank() } ?: return null
    return ScreenshotCandidate(
        contentUri = uri,
        createdAtMillis = createdAtMillis.takeIf { it > 0 } ?: nowMillis,
        width = width.coerceAtLeast(0),
        height = height.coerceAtLeast(0),
        displayNameDigest = displayNameDigest
            ?.takeIf { it.isNotBlank() }
            ?: uri.hashCode().toUInt().toString(16),
        sourceLabel = SCREENSHOT_ASSIST_IMPORT_SOURCE_LABEL,
    )
}

fun loadScreenshotAssistEnabled(context: Context): Boolean =
    loadScreenshotAssistEnabledFromPreferences(screenshotAssistPreferences(context))

fun saveScreenshotAssistEnabled(context: Context, enabled: Boolean) {
    saveScreenshotAssistEnabledToPreferences(screenshotAssistPreferences(context), enabled)
}

fun clearScreenshotAssistPreference(context: Context) {
    clearScreenshotAssistPreferenceFromPreferences(screenshotAssistPreferences(context))
}

internal fun loadScreenshotAssistEnabledFromPreferences(preferences: SharedPreferences): Boolean =
    preferences.getBoolean(KEY_SCREENSHOT_ASSIST_ENABLED, false)

internal fun saveScreenshotAssistEnabledToPreferences(
    preferences: SharedPreferences,
    enabled: Boolean,
) {
    preferences.edit()
        .putBoolean(KEY_SCREENSHOT_ASSIST_ENABLED, enabled)
        .apply()
}

internal fun clearScreenshotAssistPreferenceFromPreferences(preferences: SharedPreferences) {
    preferences.edit()
        .remove(KEY_SCREENSHOT_ASSIST_ENABLED)
        .remove(KEY_LAST_SCREENSHOT_ASSIST_NOTIFIED_URI)
        .apply()
}

fun isLikelyScreenshot(
    displayName: String,
    relativePath: String?,
): Boolean {
    val nameSignal = listOf("Screenshot", "截屏", "屏幕截图").any { token ->
        displayName.contains(token, ignoreCase = true)
    }
    val pathSignal = relativePath?.let { path ->
        listOf("Screenshots", "截屏", "屏幕截图").any { token -> path.contains(token, ignoreCase = true) }
    } ?: false
    return nameSignal || pathSignal
}

private fun screenshotAssistPreferences(context: Context): SharedPreferences =
    context.getSharedPreferences(SCREENSHOT_ASSIST_PREFERENCES_NAME, Context.MODE_PRIVATE)
