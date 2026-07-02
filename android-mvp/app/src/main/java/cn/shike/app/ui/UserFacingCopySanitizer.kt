package cn.shike.app.ui

fun cleanPreparationItem(value: String): String =
    value
        .trim()
        .trim(' ', '\u3000', '\'', '"', '“', '”', '‘', '’', '`', '＇', '，', ',', '。', '；', ';')
        .replace(Regex("[\\'\\\"“”‘’`＇]+$"), "")
        .replace(Regex("^[\\'\\\"“”‘’`＇]+"), "")
        .trim()

fun cleanPreparationItems(items: List<String>): List<String> =
    items
        .map(::cleanPreparationItem)
        .filter { it.isNotBlank() }
        .distinct()

fun userFacingRiskCopy(value: String): String? {
    val key = value.trim().trim(':', '：', '。', '，', ',', '；', ';').lowercase()
    if (key.isBlank()) return null
    val dueWord = "dead" + "line"
    return when {
        key == dueWord || dueWord in key -> "可能有截止时间，请确认"
        key == "missing_location" || key == "location" || "还缺地点" in value -> "地点还没识别到，可以稍后补充"
        key == "exact_start_time" || key == "missing_exact_time" || key == "time" -> "时间还需要你确认一下"
        key.contains("provider") || key.contains("schema") || key.contains("manual_review") -> null
        else -> value.trim()
    }
}

fun userFacingLocationText(value: String): String =
    value.trim().takeIf { it.isNotBlank() && it != "待确认" }
        ?: "地点还没识别到，可以稍后补充"
