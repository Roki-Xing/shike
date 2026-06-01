package cn.shike.app.data

import android.content.Context
import android.content.SharedPreferences
import cn.shike.app.domain.ShikeItem

internal const val INBOX_PREFERENCES_NAME = "shike_inbox_state"
private const val ACTION_SEPARATOR = "|"
private const val DEFAULT_CAPTURE_SOURCE = "尚未采集图片，已加载离线样例。"
private const val DEFAULT_RAW_TEXT = "已从本地缓存恢复。"
internal const val KEY_TITLE = "title"
internal const val KEY_SCENE = "scene"
internal const val KEY_TIME = "time"
internal const val KEY_LOCATION = "location"
internal const val KEY_STATUS = "status"
internal const val KEY_ACTIONS = "actions"
internal const val KEY_START = "start_epoch_millis"
internal const val KEY_RAW_TEXT = "raw_text"
internal const val KEY_CAPTURE_SOURCE = "capture_source"

private fun preferences(context: Context): SharedPreferences =
    legacyInboxPreferences(context)

/**
 * Saves the current inbox action card as the restart restore snapshot.
 *
 * Args:
 *     context: Android context used to open app-scoped preferences.
 *     item: Current action card to restore after restart.
 *     captureSource: Human-readable source text shown in the import panel.
 */
fun saveSnapshot(context: Context, item: ShikeItem, captureSource: String) {
    upsertInboxItem(
        context,
        inboxItemEntityFrom(
            item = item,
            captureSource = captureSource,
            updatedEpochMillis = System.currentTimeMillis(),
        ),
    )
    preferences(context).edit()
        .putString(KEY_TITLE, item.title)
        .putString(KEY_SCENE, item.scene)
        .putString(KEY_TIME, item.time)
        .putString(KEY_LOCATION, item.location)
        .putString(KEY_STATUS, item.status)
        .putString(KEY_ACTIONS, encodeInboxActions(item.actions))
        .putLong(KEY_START, item.startEpochMillis)
        .putString(KEY_RAW_TEXT, sanitizeInboxRawText(item.rawText))
        .putString(KEY_CAPTURE_SOURCE, sanitizeInboxCaptureSource(captureSource))
        .apply()
}

/**
 * Clears the cached inbox snapshot stored in inbox-scoped SharedPreferences.
 *
 * Args:
 *     context: Android context used to open app-scoped preferences.
 */
fun clearLocalData(context: Context) {
    preferences(context).edit().clear().apply()
}

/**
 * Clears only the cached inbox snapshot.
 *
 * Note:
 * - Backend config and reminder scheduling state are persisted separately and should not be cleared here.
 * - This makes "清空收件箱缓存" semantics predictable without wiping other local settings.
 */
fun clearInboxSnapshot(context: Context) {
    clearInboxHistory(context)
    preferences(context).edit()
        .remove(KEY_TITLE)
        .remove(KEY_SCENE)
        .remove(KEY_TIME)
        .remove(KEY_LOCATION)
        .remove(KEY_STATUS)
        .remove(KEY_ACTIONS)
        .remove(KEY_START)
        .remove(KEY_RAW_TEXT)
        .remove(KEY_CAPTURE_SOURCE)
        .apply()
}

internal fun clearInboxSnapshotFromPreferences(preferences: SharedPreferences) {
    preferences.edit()
        .remove(KEY_TITLE)
        .remove(KEY_SCENE)
        .remove(KEY_TIME)
        .remove(KEY_LOCATION)
        .remove(KEY_STATUS)
        .remove(KEY_ACTIONS)
        .remove(KEY_START)
        .remove(KEY_RAW_TEXT)
        .remove(KEY_CAPTURE_SOURCE)
        .apply()
}

/**
 * Loads the last confirmed inbox card snapshot.
 *
 * Args:
 *     context: Android context used to open app-scoped preferences.
 *
 * Returns:
 *     A saved `ShikeItem`, or null when no snapshot exists yet.
 */
fun loadSavedItem(context: Context): ShikeItem? {
    loadInboxHistory(context, limit = 1).firstOrNull()?.let { return shikeItemFromInboxEntity(it) }
    return legacyInboxItemFromPreferences(preferences(context))
}

/**
 * Loads the last capture source label shown after an app restart.
 *
 * Args:
 *     context: Android context used to open app-scoped preferences.
 *
 * Returns:
 *     A saved source label, or the offline sample fallback label.
 */
fun loadSavedCaptureSource(context: Context): String =
    loadInboxHistory(context, limit = 1).firstOrNull()?.source
        ?: legacyInboxCaptureSourceFromPreferences(preferences(context))

fun loadSavedInboxHistory(context: Context): List<InboxItemEntity> =
    loadInboxHistory(context).ifEmpty {
        legacyInboxItemFromPreferences(preferences(context))?.let { saved ->
            listOf(
                inboxItemEntityFrom(
                    item = saved,
                    captureSource = preferences(context).getString(KEY_CAPTURE_SOURCE, null).orEmpty(),
                    updatedEpochMillis = System.currentTimeMillis(),
                ),
            )
        } ?: emptyList()
    }

fun loadSavedCaptureSourceFromPreferences(context: Context): String =
    legacyInboxCaptureSourceFromPreferences(preferences(context))

/**
 * Encodes action labels for the local inbox snapshot.
 *
 * Args:
 *     actions: Current action-card labels.
 *
 * Returns:
 *     A compact string safe for the existing SharedPreferences snapshot.
 */
fun encodeInboxActions(actions: List<String>): String =
    actions
        .map { it.trim() }
        .filter { it.isNotBlank() }
        .map { it.replace(ACTION_SEPARATOR, " ") }
        .joinToString(ACTION_SEPARATOR)

/**
 * Decodes action labels from the local inbox snapshot.
 *
 * Args:
 *     encoded: Stored action string from SharedPreferences.
 *
 * Returns:
 *     Sanitized action labels, or default course actions when none are stored.
 */
fun decodeInboxActions(encoded: String?): List<String> =
    encoded
        ?.split(ACTION_SEPARATOR)
        ?.map { it.trim() }
        ?.filter { it.isNotBlank() }
        ?.ifEmpty { null }
        ?: sampleCourse().actions

/**
 * Sanitizes the capture source label before local persistence or restart restore.
 *
 * Args:
 *     captureSource: Source label from image, camera, share, backend, or local fallback.
 *
 * Returns:
 *     A non-blank source label with sensitive tokens redacted.
 */
fun sanitizeInboxCaptureSource(captureSource: String?): String =
    redactSensitiveLogText(captureSource.orEmpty().trim())
        .ifBlank { DEFAULT_CAPTURE_SOURCE }

/**
 * Sanitizes raw OCR text before local persistence or restart restore.
 *
 * Args:
 *     rawText: OCR, backend, share, or fallback text attached to the action card.
 *
 * Returns:
 *     A non-blank raw-text snapshot with sensitive tokens redacted.
 */
fun sanitizeInboxRawText(rawText: String?): String =
    redactSensitiveLogText(rawText.orEmpty().trim())
        .ifBlank { DEFAULT_RAW_TEXT }
