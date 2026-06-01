package cn.shike.app.data

import android.content.Context
import android.content.SharedPreferences
import cn.shike.app.domain.ShikeItem

internal fun legacyInboxPreferences(context: Context): SharedPreferences =
    context.getSharedPreferences(INBOX_PREFERENCES_NAME, Context.MODE_PRIVATE)

internal fun legacyInboxItemFromPreferences(preferences: SharedPreferences): ShikeItem? {
    val title = preferences.getString(KEY_TITLE, null) ?: return null
    val actions = decodeInboxActions(preferences.getString(KEY_ACTIONS, null))
    return ShikeItem(
        title = title,
        scene = preferences.getString(KEY_SCENE, "课程通知") ?: "课程通知",
        time = preferences.getString(KEY_TIME, "待确认") ?: "待确认",
        location = preferences.getString(KEY_LOCATION, "待确认") ?: "待确认",
        status = preferences.getString(KEY_STATUS, "待确认") ?: "待确认",
        actions = actions.ifEmpty { listOf("加入日历", "课前提醒", "打开地图") },
        startEpochMillis = preferences.getLong(KEY_START, sampleCourse().startEpochMillis),
        rawText = sanitizeInboxRawText(preferences.getString(KEY_RAW_TEXT, null)),
    )
}

internal fun legacyInboxCaptureSourceFromPreferences(preferences: SharedPreferences): String =
    sanitizeInboxCaptureSource(preferences.getString(KEY_CAPTURE_SOURCE, null))
