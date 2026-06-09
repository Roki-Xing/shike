package cn.shike.app.data

import org.json.JSONObject
import java.time.Instant
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.LocalTime
import java.time.ZoneId
import java.time.ZonedDateTime
import java.time.format.DateTimeFormatter
import java.time.format.DateTimeParseException

fun startEpochMillisFromTime(
    time: JSONObject?,
    fallbackText: String,
    referenceNowMillis: Long = System.currentTimeMillis(),
    zoneId: ZoneId = ZoneId.of("Asia/Shanghai"),
): Long {
    if (time == null) {
        return parseRelativeChineseTime(fallbackText, referenceNowMillis, zoneId) ?: 0L
    }
    val normalized = listOf(
        time.normalizedString("normalized_start"),
        time.normalizedString("start_at"),
        time.normalizedString("start_time"),
    ).firstOrNull { it.isNotBlank() }
    parseNormalizedEpoch(normalized)?.let { return it }

    val evidenceText = listOf(
        time.normalizedString("start_text"),
        time.normalizedString("raw"),
        fallbackText,
    ).filter { it.isNotBlank() }.joinToString(" ")
    return parseRelativeChineseTime(evidenceText, referenceNowMillis, zoneId) ?: 0L
}

private fun parseNormalizedEpoch(value: String?): Long? {
    val text = value?.trim().orEmpty()
    if (text.isBlank()) {
        return null
    }
    return runCatching { Instant.parse(text).toEpochMilli() }.getOrNull()
        ?: runCatching { ZonedDateTime.parse(text).toInstant().toEpochMilli() }.getOrNull()
        ?: runCatching {
            LocalDateTime.parse(text, DateTimeFormatter.ISO_LOCAL_DATE_TIME)
                .atZone(ZoneId.of("Asia/Shanghai"))
                .toInstant()
                .toEpochMilli()
        }.getOrNull()
}

private fun parseRelativeChineseTime(text: String, referenceNowMillis: Long, zoneId: ZoneId): Long? {
    val compact = text.trim()
    if (compact.isBlank()) {
        return null
    }
    parseExplicitDateTime(compact, zoneId)?.let { return it }

    val referenceDate = Instant.ofEpochMilli(referenceNowMillis).atZone(zoneId).toLocalDate()
    val date = when {
        "后天" in compact -> referenceDate.plusDays(2)
        "明天" in compact || "明日" in compact -> referenceDate.plusDays(1)
        "今天" in compact || "今晚" in compact || "早上" in compact || "上午" in compact ||
            "中午" in compact || "下午" in compact || "晚上" in compact -> referenceDate
        else -> return null
    }
    val localTime = parseChineseClock(compact) ?: return null
    return LocalDateTime.of(date, localTime).atZone(zoneId).toInstant().toEpochMilli()
}

private fun parseExplicitDateTime(text: String, zoneId: ZoneId): Long? {
    val match = Regex("""(\d{4})[-年](\d{1,2})[-月](\d{1,2})[日号]?\s*(上午|早上|中午|下午|晚上|今晚)?\s*(\d{1,2})(?::|点|：)(\d{1,2})?""")
        .find(text)
        ?: return null
    val year = match.groupValues[1].toInt()
    val month = match.groupValues[2].toInt()
    val day = match.groupValues[3].toInt()
    val period = match.groupValues[4]
    val hour = normalizeHour(match.groupValues[5].toInt(), period)
    val minute = match.groupValues[6].takeIf { it.isNotBlank() }?.toInt() ?: 0
    return try {
        LocalDateTime.of(LocalDate.of(year, month, day), LocalTime.of(hour, minute))
            .atZone(zoneId)
            .toInstant()
            .toEpochMilli()
    } catch (_: DateTimeParseException) {
        null
    } catch (_: RuntimeException) {
        null
    }
}

private fun parseChineseClock(text: String): LocalTime? {
    val numeric = Regex("""(上午|早上|中午|下午|晚上|今晚)?\s*(\d{1,2})(?::|点|：)(\d{1,2})?""").find(text)
    if (numeric != null) {
        val period = numeric.groupValues[1]
        val hour = normalizeHour(numeric.groupValues[2].toInt(), period.ifBlank { periodFromText(text) })
        val minute = numeric.groupValues[3].takeIf { it.isNotBlank() }?.toInt() ?: 0
        return runCatching { LocalTime.of(hour, minute) }.getOrNull()
    }

    val chinese = Regex("""(上午|早上|中午|下午|晚上|今晚)?\s*([零一二两三四五六七八九十]{1,3})点(半|[零一二三四五六七八九十]{1,3}分?)?""").find(text)
        ?: return null
    val period = chinese.groupValues[1]
    val hourValue = chineseNumberToInt(chinese.groupValues[2]) ?: return null
    val minuteValue = when (val minuteText = chinese.groupValues[3]) {
        "" -> 0
        "半" -> 30
        else -> chineseNumberToInt(minuteText.removeSuffix("分")) ?: 0
    }
    return runCatching { LocalTime.of(normalizeHour(hourValue, period.ifBlank { periodFromText(text) }), minuteValue) }.getOrNull()
}

private fun periodFromText(text: String): String =
    when {
        "今晚" in text -> "晚上"
        "晚上" in text -> "晚上"
        "下午" in text -> "下午"
        "中午" in text -> "中午"
        "上午" in text -> "上午"
        "早上" in text -> "早上"
        else -> ""
    }

private fun normalizeHour(hour: Int, period: String): Int =
    when {
        (period == "下午" || period == "晚上" || period == "今晚") && hour in 1..11 -> hour + 12
        period == "中午" && hour in 1..10 -> hour + 12
        else -> hour
    }

private fun chineseNumberToInt(text: String): Int? {
    if (text.isBlank()) {
        return null
    }
    val digits = mapOf(
        '零' to 0,
        '一' to 1,
        '二' to 2,
        '两' to 2,
        '三' to 3,
        '四' to 4,
        '五' to 5,
        '六' to 6,
        '七' to 7,
        '八' to 8,
        '九' to 9,
    )
    if (text == "十") {
        return 10
    }
    if (text.startsWith("十")) {
        return 10 + (digits[text.last()] ?: 0)
    }
    if ("十" in text) {
        val parts = text.split("十")
        val tens = digits[parts.first().firstOrNull()] ?: return null
        val ones = parts.getOrNull(1)?.firstOrNull()?.let { digits[it] } ?: 0
        return tens * 10 + ones
    }
    return text.fold(0) { acc, c ->
        val digit = digits[c] ?: return null
        acc * 10 + digit
    }
}

private fun JSONObject.normalizedString(key: String): String {
    if (!has(key) || isNull(key)) {
        return ""
    }
    return optString(key)
        .trim()
        .takeUnless { it.equals("null", ignoreCase = true) }
        .orEmpty()
}
