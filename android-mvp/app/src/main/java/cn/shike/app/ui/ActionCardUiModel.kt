package cn.shike.app.ui

import cn.shike.app.domain.ShikeItem

data class ActionCardUiModel(
    val sceneLabel: String,
    val title: String,
    val time: String,
    val location: String,
    val task: String,
    val actions: List<String>,
    val risks: List<String>,
    val missingFields: List<String>,
)

fun actionCardUiModelFrom(item: ShikeItem): ActionCardUiModel =
    ActionCardUiModel(
        sceneLabel = item.scene.ifBlank { "待确认" },
        title = item.title.cleanUiValue("待确认碎片"),
        time = item.time.cleanUiValue("待确认"),
        location = item.location.cleanUiValue("待确认"),
        task = item.rawText.linesByPrefix("任务：").firstOrNull().cleanUiValue(defaultTaskFor(item)),
        actions = item.actions.map { it.cleanUiValue("") }.filter { it.isNotBlank() }.ifEmpty { listOf("稍后确认") },
        risks = item.rawText.linesByPrefix("风险：").flatMap { it.split("；") }.map { it.trim() }.filter { it.isNotBlank() },
        missingFields = item.rawText.linesByPrefix("待补：").flatMap { it.split("、") }.map { it.trim() }.filter { it.isNotBlank() },
    )

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
