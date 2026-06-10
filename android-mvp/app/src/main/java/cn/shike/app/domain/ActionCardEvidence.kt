package cn.shike.app.domain

private val prepSeparators = Regex("[、/和及与]")
private val prepStopChars = Regex("[，,。；;\\n]")
private val engineeringWarningTokens = listOf(
    "schema_valid",
    "risk code",
    "/v1/analyze",
    "/v2/analyze-image",
)

/**
 * Extracts preparation items that should travel with the action card.
 *
 * Args:
 *     item: Current action card draft.
 *
 * Returns:
 *     Distinct user-visible preparation items such as `带书`.
 */
fun preparationItemsFrom(item: ShikeItem): List<String> =
    preparationItemsFromText(
        listOf(
            taskSummaryFrom(item),
            item.rawText,
            item.title,
        ).joinToString("\n")
    )

/**
 * Extracts preparation items from OCR or model task text.
 *
 * Args:
 *     text: User-visible evidence text.
 *
 * Returns:
 *     Distinct preparation items, capped to concise display strings.
 */
fun preparationItemsFromText(text: String): List<String> {
    val results = mutableListOf<String>()
    fun add(value: String) {
        cleanPreparationItem(value)?.let { cleaned ->
            if (cleaned !in results) results.add(cleaned)
        }
    }

    Regex("记得带([^，,。；;\\n]+)").findAll(text).forEach { match ->
        expandCarryItems(match.groupValues[1]).forEach(::add)
    }
    Regex("带([^，,。；;\\n]+)").findAll(text).forEach { match ->
        expandCarryItems(match.groupValues[1]).forEach(::add)
    }
    Regex("提前准备([^，,。；;\\n]+)").findAll(text).forEach { match ->
        add("提前准备${match.groupValues[1]}")
    }
    Regex("提前[一二三四五六七八九十两0-9]+分钟(?:到达|到|上线|入场)?").findAll(text).forEach { match ->
        add(match.value)
    }
    Regex("先去?签到").findAll(text).forEach { match ->
        add(match.value)
    }
    Regex("课前交([^，,。；;\\n]+)").findAll(text).forEach { match ->
        add("课前交${match.groupValues[1]}")
    }
    Regex("不要迟到").findAll(text).forEach { match ->
        add(match.value)
    }
    Regex("到[^，,。；;\\n]{1,12}集合").findAll(text).forEach { match ->
        add(match.value)
    }
    return results.sortedBy { occurrenceIndex(text, it) }
}

/**
 * Builds the reminder detail shown in local notifications.
 *
 * Args:
 *     item: Confirmed action card.
 *
 * Returns:
 *     Compact reminder detail that includes preparation items when present.
 */
fun reminderDetailFor(item: ShikeItem): String {
    val preparation = preparationItemsFrom(item)
    return if (preparation.isEmpty()) {
        listOf(item.time, item.location).filterUsableParts().joinToString(" · ")
    } else {
        listOf(item.title, item.location, reminderPreparationCopy(preparation)).filterUsableParts().joinToString(" · ")
    }
}

/**
 * Reads the task summary from the model evidence block.
 *
 * Args:
 *     item: Current action card draft.
 *
 * Returns:
 *     Task summary or an empty string when no summary exists.
 */
fun taskSummaryFrom(item: ShikeItem): String =
    item.rawText.lineSequence()
        .map { it.trim() }
        .firstOrNull { it.startsWith("任务：") }
        ?.removePrefix("任务：")
        ?.trim()
        .orEmpty()

/**
 * Maps internal risk and missing-field tokens to user-facing confirmation copy.
 *
 * Args:
 *     rawWarnings: Internal risk/missing-field strings.
 *
 * Returns:
 *     User-facing warnings without provider/schema/debug tokens.
 */
fun userWarningsFrom(rawWarnings: List<String>): List<String> {
    val results = mutableListOf<String>()
    rawWarnings.forEach { warning ->
        userWarningCopyFor(warning)?.let { copy ->
            if (copy !in results) results.add(copy)
        }
    }
    return results
}

/**
 * Removes backend/debug lines from OCR text shown in ordinary UI.
 *
 * Args:
 *     text: Raw evidence or editable OCR draft.
 *
 * Returns:
 *     User-facing OCR text only.
 */
fun userVisibleEvidenceText(text: String): String =
    text.lineSequence()
        .map { it.trim() }
        .filter { it.isNotBlank() }
        .filterNot { line ->
            val lower = line.lowercase()
            lower.startsWith("云端 ai 解析")
                || lower.startsWith("后端")
                || engineeringWarningTokens.any { token -> lower.contains(token) }
                || lower.contains("manual_review")
                || lower.contains("provider")
        }
        .joinToString("\n")

private fun expandCarryItems(raw: String): List<String> =
    raw.split(prepSeparators)
        .map { it.trim() }
        .filter { it.isNotBlank() }
        .map { if (it.startsWith("带")) it else "带$it" }

private fun cleanPreparationItem(value: String): String? {
    val cleaned = value
        .replace(prepStopChars, "")
        .trim()
        .trim('：', ':', '。', '，', ',', '；', ';')
    if (cleaned.isBlank() || cleaned.length > 24) return null
    val lower = cleaned.lowercase()
    if (engineeringWarningTokens.any { lower.contains(it) } || lower.contains("provider") || lower.contains("manual_review")) {
        return null
    }
    return cleaned
}

private fun reminderPreparationCopy(items: List<String>): String =
    items.joinToString("，") { item ->
        if (item.startsWith("带")) "记得$item" else item
    }

private fun List<String>.filterUsableParts(): List<String> =
    map { it.trim() }
        .filter { it.isNotBlank() && it != "待确认" && !it.equals("null", ignoreCase = true) }

private fun userWarningCopyFor(raw: String): String? {
    val warning = raw.trim().trim('：', ':', '。', '，', ',', '；', ';')
    if (warning.isBlank()) return null
    val lower = warning.lowercase()
    if (engineeringWarningTokens.any { lower.contains(it) }) return null
    return when {
        lower == "relative_time" || "相对时间" in warning || "明天" in warning || "今晚" in warning ->
            "时间来自“明天/今晚”等相对表达，请确认日期"
        lower == "location_low_confidence" || "地点识别" in warning ->
            "地点识别不够确定，请确认"
        lower == "missing_location" || lower == "location" ->
            "还缺地点，暂不能打开地图"
        lower == "missing_exact_time" || lower == "exact_start_time" || lower == "time" ->
            "还缺具体时间，暂不能加入日历"
        lower.contains("provider_error") || lower.contains("provider") || "ai" in lower && "不可用" in warning ->
            "AI 暂时不可用，已保留待确认卡"
        lower.contains("manual_review") ->
            "待你确认"
        "_" in warning && warning.none { it in '\u4e00'..'\u9fff' } ->
            null
        else -> warning
    }
}

private fun occurrenceIndex(text: String, item: String): Int {
    val candidates = listOf(item, item.removePrefix("带").removePrefix("记得"))
    return candidates
        .map { candidate -> text.indexOf(candidate).takeIf { it >= 0 } ?: Int.MAX_VALUE }
        .minOrNull()
        ?: Int.MAX_VALUE
}
