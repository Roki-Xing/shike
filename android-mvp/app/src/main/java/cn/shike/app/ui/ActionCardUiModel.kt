package cn.shike.app.ui

import cn.shike.app.domain.preparationItemsFrom
import cn.shike.app.domain.ShikeItem
import cn.shike.app.domain.taskSummaryFrom
import cn.shike.app.domain.userVisibleEvidenceText
import cn.shike.app.domain.userWarningsFrom

data class ActionCardUiModel(
    val sceneLabel: String,
    val title: String,
    val time: String,
    val location: String,
    val task: String,
    val preparationItems: List<String>,
    val actions: List<String>,
    val risks: List<String>,
    val missingFields: List<String>,
    val userWarnings: List<String>,
    val sourceTextPreview: String,
)

fun actionCardUiModelFrom(item: ShikeItem): ActionCardUiModel {
    val risks = item.rawText.linesByPrefix("风险：").flatMap { it.split("；") }.map { it.trim() }.filter { it.isNotBlank() }
    val missingFields = item.rawText.linesByPrefix("待补：").flatMap { it.split("、") }.map { it.trim() }.filter { it.isNotBlank() }
    val task = taskSummaryFrom(item).cleanUiValue(defaultTaskFor(item))
    return ActionCardUiModel(
        sceneLabel = item.scene.ifBlank { "待确认" },
        title = actionCardTitleFor(item),
        time = item.time.cleanUiValue("待确认"),
        location = item.location.cleanUiValue("待确认"),
        task = task,
        preparationItems = preparationItemsFrom(item),
        actions = item.actions.map { it.cleanUiValue("") }.filter { it.isNotBlank() }.ifEmpty { listOf("稍后确认") },
        risks = risks,
        missingFields = missingFields,
        userWarnings = userWarningsFrom(risks + missingFields),
        sourceTextPreview = userVisibleEvidenceText(item.rawText),
    )
}

private fun String?.cleanUiValue(fallback: String): String {
    val value = this?.trim().orEmpty()
    val cleaned = value
        .split(" / ")
        .map { it.trim() }
        .filter { it.isNotBlank() && !it.equals("null", ignoreCase = true) }
        .joinToString(" / ")
    return cleaned
        .takeUnless { it.isBlank() || it.equals("null", ignoreCase = true) }
        ?: fallback
}

private fun defaultTaskFor(item: ShikeItem): String =
    when {
        "课程" in item.scene -> "上课"
        "活动" in item.scene -> "参加活动"
        else -> "确认后处理"
    }

private fun String.linesByPrefix(prefix: String): List<String> =
    lineSequence()
        .map { it.trim() }
        .filter { it.startsWith(prefix) }
        .map { it.removePrefix(prefix).trim() }
        .filter { it.isNotBlank() }
        .toList()

private fun actionCardTitleFor(item: ShikeItem): String {
    val cleaned = stripPreparationFromTitle(item.title.cleanUiValue("待确认碎片"))
    val shouldNormalizeCourse = "课程" in item.scene && (
        cleaned.length > 14 || cleaned.contains("教室") || cleaned.contains("记得") || cleaned.contains("带")
    )
    if (shouldNormalizeCourse) {
        courseTitleFromEvidence(cleaned + "\n" + item.rawText)?.let { return it }
    }
    return cleaned
}

private fun stripPreparationFromTitle(title: String): String =
    title
        .replace(Regex("[，,。；;\\s]*(记得带|提前准备|提前[一二三四五六七八九十两0-9]+分钟|先去?签到|课前交|不要迟到|带).*$"), "")
        .trim()
        .ifBlank { title.cleanUiValue("待确认碎片") }

private fun courseTitleFromEvidence(text: String): String? {
    Regex("(?<!早)(?<!晚)上([\\u4e00-\\u9fa5A-Za-z0-9]{1,16}?)(?:课|课程|教室|地点|在|，|,|\\s|$)")
        .find(text)
        ?.groupValues
        ?.getOrNull(1)
        ?.trim()
        ?.takeIf { it.isNotBlank() }
        ?.let { return if (it.endsWith("课")) it else "${it}课" }
    Regex("([\\u4e00-\\u9fa5A-Za-z0-9]{1,12})(?:课|课程)")
        .find(text)
        ?.groupValues
        ?.getOrNull(1)
        ?.trim()
        ?.takeIf { it.isNotBlank() }
        ?.let { return if (it.endsWith("课")) it else "${it}课" }
    return null
}
