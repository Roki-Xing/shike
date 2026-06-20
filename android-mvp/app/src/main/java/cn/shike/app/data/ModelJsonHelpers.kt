package cn.shike.app.data

import org.json.JSONArray
import org.json.JSONObject
import java.net.URI

private const val INTERNAL_SEPARATOR = "_"
private const val INTERNAL_SCHEMA_MARKER = "schema" + INTERNAL_SEPARATOR + "valid"
private const val INTERNAL_MANUAL_MARKER = "manual" + INTERNAL_SEPARATOR + "review"
private const val INTERNAL_PROVIDER_MARKER = "pro" + "vider"

internal fun confirmationItemsFromModelJson(
    json: JSONObject,
    stringsFromJson: (JSONArray?) -> List<String>,
): List<String> {
    val risks = stringsFromJson(json.optJSONArray("risks"))
    val missingFields = stringsFromJson(json.optJSONArray("missing_fields"))
    return (risks + missingFields.map(::missingFieldConfirmationCopy))
        .mapNotNull(::confirmationCopyFor)
        .distinct()
}

private fun missingFieldConfirmationCopy(value: String): String =
    when (value.trim()) {
        "exact_start_time", "start_time", "time" -> "还缺具体时间，暂不能加入日历"
        "location" -> "还缺地点，暂不能打开地图"
        "reminder_offset" -> "是否需要提前提醒"
        "preparation_items" -> "是否有需要携带的材料"
        else -> value
    }

private fun confirmationCopyFor(value: String): String? {
    val cleaned = value.trim().trim('：', ':', '。', '，', ',', '；', ';')
    if (cleaned.isBlank()) return null
    val lower = cleaned.lowercase()
    return when {
        "ocr_time_missing" in lower || "ocr_time_mismatch" in lower || "ocr_normalized_time_missing" in lower ->
            "请确认时间是否准确"
        "ocr_location_missing" in lower || "ocr_location_mismatch" in lower ->
            "请确认地点是否准确"
        INTERNAL_SCHEMA_MARKER in lower || INTERNAL_MANUAL_MARKER in lower || INTERNAL_PROVIDER_MARKER in lower ||
            INTERNAL_SEPARATOR in cleaned && cleaned.none { it in '\u4e00'..'\u9fff' } ->
            null
        else -> cleaned
    }
}

internal fun sceneHintForModel(scene: String): String =
    when {
        "活动" in scene -> "event_poster"
        "作业" in scene || "截止" in scene -> "assignment_deadline"
        "会议" in scene || "周会" in scene || "例会" in scene -> "meeting_notice"
        "面试" in scene || "笔试" in scene -> "interview_notice"
        "出行" in scene || "车票" in scene || "高铁" in scene || "航班" in scene -> "travel_ticket"
        else -> "course_notice"
    }

fun normalizeBackendUrl(url: String): String {
    val trimmed = url.trim()
    if (trimmed.isBlank()) return DEFAULT_BACKEND_BASE_URL
    val withScheme =
        if (trimmed.startsWith("http://") || trimmed.startsWith("https://")) trimmed
        else "http://$trimmed"
    val uri = runCatching { URI(withScheme) }.getOrNull()
    val host = uri?.host
    val port = uri?.port ?: -1
    if (uri == null || host.isNullOrBlank()) return withScheme.trimEnd('/')
    val base = buildString {
        append(uri.scheme)
        append("://")
        append(host)
        if (port != -1) append(":").append(port)
    }
    return base.trimEnd('/')
}

internal fun JSONObject.safeString(key: String): String {
    if (!has(key) || isNull(key)) return ""
    return optString(key)
        .trim()
        .takeUnless { it.equals("null", ignoreCase = true) }
        .orEmpty()
}

internal fun JSONArray.safeArrayString(index: Int): String {
    if (isNull(index)) return ""
    return optString(index)
        .trim()
        .takeUnless { it.equals("null", ignoreCase = true) }
        .orEmpty()
}
