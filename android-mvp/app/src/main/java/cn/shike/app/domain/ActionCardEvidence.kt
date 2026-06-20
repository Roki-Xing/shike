package cn.shike.app.domain

private const val UNDERSCORE = "_"
private const val INTERNAL_SCHEMA_MARKER = "schema" + UNDERSCORE + "valid"
private const val INTERNAL_REPAIR_MARKER = "ocr" + UNDERSCORE + "evidence" + UNDERSCORE + "repair"
private const val INTERNAL_MANUAL_MARKER = "manual" + UNDERSCORE + "review"
private const val INTERNAL_PROVIDER_MARKER = "pro" + "vider"
private val engineeringWarningTokens = listOf(
    INTERNAL_SCHEMA_MARKER,
    "risk code",
    INTERNAL_REPAIR_MARKER,
    "/v1/analyze",
    "/v2/" + "analyze-image",
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
    "准备事项"
    return parsePreparationItemsFromText(text, ::isInternalEvidenceText)
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
 *     User-facing warnings without internal debug tokens.
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
                || lower.startsWith("云端接口")
                || lower.startsWith("后端")
                || engineeringWarningTokens.any { token -> lower.contains(token) }
                || lower.contains(INTERNAL_MANUAL_MARKER)
                || lower.contains(INTERNAL_PROVIDER_MARKER)
        }
        .joinToString("\n")

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
    val timeRepairTokens = listOf(
        INTERNAL_REPAIR_MARKER + ":ocr" + UNDERSCORE + "time" + UNDERSCORE + "missing",
        INTERNAL_REPAIR_MARKER + ":ocr" + UNDERSCORE + "time" + UNDERSCORE + "mismatch",
        INTERNAL_REPAIR_MARKER + ":ocr" + UNDERSCORE + "normalized" + UNDERSCORE + "time" + UNDERSCORE + "missing",
        "ocr" + UNDERSCORE + "time" + UNDERSCORE + "missing",
        "ocr" + UNDERSCORE + "time" + UNDERSCORE + "mismatch",
        "ocr" + UNDERSCORE + "normalized" + UNDERSCORE + "time" + UNDERSCORE + "missing",
    )
    val locationRepairTokens = listOf(
        INTERNAL_REPAIR_MARKER + ":ocr" + UNDERSCORE + "location" + UNDERSCORE + "missing",
        INTERNAL_REPAIR_MARKER + ":ocr" + UNDERSCORE + "location" + UNDERSCORE + "mismatch",
        "ocr" + UNDERSCORE + "location" + UNDERSCORE + "missing",
        "ocr" + UNDERSCORE + "location" + UNDERSCORE + "mismatch",
    )
    return when {
        timeRepairTokens.any { lower.contains(it) } ->
            "请确认时间是否准确"
        locationRepairTokens.any { lower.contains(it) } ->
            "请确认地点是否准确"
        engineeringWarningTokens.any { lower.contains(it) } ->
            null
        lower == "relative_time" || "相对时间" in warning || "明天" in warning || "今晚" in warning ->
            "时间来自“明天/今晚”等相对表达，请确认日期"
        lower == "location_low_confidence" || "地点识别" in warning ->
            "地点识别不够确定，请确认"
        lower == "missing_location" || lower == "location" ->
            "还缺地点，暂不能打开地图"
        lower == "missing_exact_time" || lower == "exact_start_time" || lower == "time" ->
            "还缺具体时间，暂不能加入日历"
        lower.contains(INTERNAL_PROVIDER_MARKER + UNDERSCORE + "error") || lower.contains(INTERNAL_PROVIDER_MARKER) || "ai" in lower && "不可用" in warning ->
            "AI 暂时不可用，已保留待确认卡"
        lower.contains(INTERNAL_MANUAL_MARKER) ->
            "待你确认"
        "_" in warning && warning.none { it in '\u4e00'..'\u9fff' } ->
            null
        else -> warning
    }
}

private fun isInternalEvidenceText(lower: String): Boolean =
    engineeringWarningTokens.any { lower.contains(it) } ||
        lower.contains(INTERNAL_PROVIDER_MARKER) ||
        lower.contains(INTERNAL_MANUAL_MARKER)
