package cn.shike.app.domain

private val prepSeparators = Regex("[、/和及与]")
private val prepStopChars = Regex("[，,。；;\\n]")

internal fun parsePreparationItemsFromText(
    text: String,
    isInternalText: (String) -> Boolean,
): List<String> {
    val results = mutableListOf<String>()
    fun add(value: String) {
        cleanPreparationItem(value, isInternalText)?.let { cleaned ->
            if (cleaned !in results) results.add(cleaned)
        }
    }

    Regex("记得带([^，,。；;\\n]+)").findAll(text).forEach { match ->
        expandCarryItems(match.groupValues[1]).forEach(::add)
    }
    Regex("(?:别忘|别忘了)([^，,。；;\\n]+)").findAll(text).forEach { match ->
        val raw = match.groupValues[1].trim()
        when {
            raw == "了" -> Unit
            raw.startsWithAny("带", "打印", "上传", "完成", "准备", "自备", "穿", "看", "发") -> add(raw)
            raw.isNotBlank() -> add("带$raw")
        }
    }
    if ("东西别忘了" in text) add("东西别忘了")
    if ("别迟到" in text) add("别迟到")
    Regex("记得打印([^，,。；;\\n]+)").findAll(text).forEach { add("打印${it.groupValues[1]}") }
    Regex("带([^，,。；;\\n]+)").findAll(text).forEach { expandCarryItems(it.groupValues[1]).forEach(::add) }
    Regex("带上([^，,。；;\\n]+)").findAll(text).forEach { expandCarryItems(it.groupValues[1]).forEach(::add) }
    Regex("先把([^，,。；;\\n]+?)带上").findAll(text).forEach { expandCarryItems(it.groupValues[1]).forEach(::add) }
    Regex("提前准备([^，,。；;\\n]+)").findAll(text).forEach { add("提前准备${it.groupValues[1]}") }
    Regex("准备([0-9一二三四五六七八九十两]+分钟[^，,。；;\\n]+|风险清单|简历|作品集)").findAll(text).forEach {
        add("准备${it.groupValues[1]}")
    }
    Regex("提前把([^，,。；;\\n]+)").findAll(text).forEach { add("提前把${it.groupValues[1]}") }
    Regex("(?:先|提前)(安装好[^，,。；;\\n]+|看[^，,。；;\\n]+|打印[^，,。；;\\n]+|下载[^，,。；;\\n]+|调试[^，,。；;\\n]+)").findAll(text).forEach {
        add(it.groupValues[1])
    }
    Regex("提前[一二三四五六七八九十两0-9]+分钟(?:到达|到|上线|入场)?").findAll(text).forEach { add(it.value) }
    Regex("提前[一二三四五六七八九十两0-9]+(?:小时|分钟)(?:到机场|到站|入会|到达)?").findAll(text).forEach { add(it.value) }
    Regex("先去?签到").findAll(text).forEach { add(it.value) }
    Regex("课前交([^，,。；;\\n]+)").findAll(text).forEach { add("课前交${it.groupValues[1]}") }
    Regex("课前(?:交|提交)([^，,。；;\\n]+)").findAll(text).forEach { add("带${it.groupValues[1]}") }
    Regex("文件名写\\s*([^，,。；;\\n]+)").findAll(text).forEach { add("文件名写${it.groupValues[1]}") }
    Regex("(上传PDF|完成问卷|截图发群里|扫描报名二维码|先加群报名|完成报名|报名)").findAll(text).forEach { add(it.value) }
    if ("录音作业" in text) add("录音作业")
    if ("发QQ群" in text) add("发QQ群")
    Regex("(自备[^，,。；;\\n]+|穿[^，,。；;\\n]+|看PRD第[0-9一二三四五六七八九十]+版|PPT[^，,。；;\\n]*备份)").findAll(text).forEach {
        add(it.value)
    }
    Regex("不要迟到").findAll(text).forEach { add(it.value) }
    Regex("到[^，,。；;\\n]{1,12}集合").findAll(text).forEach { add(it.value) }
    return results
        .filterNot { item -> results.any { other -> other != item && other.contains(item) } }
        .sortedBy { occurrenceIndex(text, it) }
}

private fun expandCarryItems(raw: String): List<String> =
    raw.split(prepSeparators)
        .map { it.trim() }
        .filter { it.isNotBlank() }
        .map { normalizeCarryItem(it) }

private fun normalizeCarryItem(item: String): String =
    if (item.startsWithAny("带", "打印", "上传", "完成", "截图", "扫描", "自备", "穿", "看", "发")) item else "带$item"

private fun cleanPreparationItem(value: String, isInternalText: (String) -> Boolean): String? {
    var cleaned = value
        .replace(prepStopChars, "")
        .trim()
        .trim('：', ':', '。', '，', ',', '；', ';')
        .removeSuffix("带上")
        .trim()
        .replace("PPT存在云盘也备份", "PPT云盘备份")
    while (Regex("\\s*(标题|未分类|AI)\\s*$").containsMatchIn(cleaned)) {
        cleaned = cleaned.replace(Regex("\\s*(标题|未分类|AI)\\s*$"), "").trim()
    }
    if (cleaned.isBlank() || cleaned.length > 24) return null
    if (cleaned in listOf("带上", "带了", "了")) return null
    return cleaned.takeUnless { isInternalText(it.lowercase()) }
}

private fun String.startsWithAny(vararg prefixes: String): Boolean = prefixes.any { startsWith(it) }

private fun occurrenceIndex(text: String, item: String): Int {
    val candidates = listOf(item, item.removePrefix("带").removePrefix("记得"))
    return candidates
        .map { candidate -> text.indexOf(candidate).takeIf { it >= 0 } ?: Int.MAX_VALUE }
        .minOrNull()
        ?: Int.MAX_VALUE
}
