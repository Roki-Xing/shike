package cn.shike.app.ui

import cn.shike.app.domain.ShikeItem
import cn.shike.app.domain.preparationItemsFrom
import cn.shike.app.domain.userVisibleEvidenceText

data class SmartActionCardUiModel(
    val title: String,
    val sceneLabel: String,
    val time: SmartFieldUi,
    val location: SmartFieldUi,
    val preparationItems: List<String>,
    val evidenceText: String,
    val primaryWarning: String?,
    val recommendedActions: List<String>,
)

data class SmartFieldUi(
    val label: String,
    val value: String,
    val state: SmartFieldState,
    val helper: String,
)

enum class SmartFieldState {
    Confirmed,
    NeedsReview,
    Suggested,
    Missing,
}

fun smartActionCardUiModelFrom(item: ShikeItem): SmartActionCardUiModel {
    val legacy = actionCardUiModelFrom(item)
    val time = smartTimeField(item)
    val location = smartLocationField(item)
    val preparation = preparationItemsForUi(item)
    val evidence = userVisibleEvidenceText(item.rawText).ifBlank { item.rawText.trim() }
    val warning = when {
        time.state == SmartFieldState.NeedsReview -> time.helper
        location.state == SmartFieldState.NeedsReview -> location.helper
        else -> null
    }
    return SmartActionCardUiModel(
        title = legacy.title.removeSuffix("课").ifBlank { item.title.ifBlank { "待确认行动卡" } },
        sceneLabel = smartSceneLabel(item.scene),
        time = time,
        location = location,
        preparationItems = preparation,
        evidenceText = evidence,
        primaryWarning = warning,
        recommendedActions = smartRecommendedActions(item, preparation),
    )
}

private fun smartTimeField(item: ShikeItem): SmartFieldUi {
    val value = item.time.trim().ifBlank { "待确认" }
    return when {
        value == "待确认" -> SmartFieldUi("时间", "待确认", SmartFieldState.Missing, "时间还没识别到，可以先存入待确认")
        isAmbiguousTimeText(value) -> SmartFieldUi("时间", "$value · 建议时间", SmartFieldState.NeedsReview, "这是建议时间，保存前请确认具体开始时间")
        item.startEpochMillis > 0L || hasExplicitClock(value) -> SmartFieldUi("时间", value, SmartFieldState.Confirmed, "保存前仍可修改")
        else -> SmartFieldUi("时间", value, SmartFieldState.Suggested, "时间表达不完整，建议保存前确认")
    }
}

private fun smartLocationField(item: ShikeItem): SmartFieldUi {
    val value = item.location.trim().ifBlank { "待确认" }
    return when {
        value == "待确认" -> SmartFieldUi("地点", userFacingLocationText(value), SmartFieldState.Missing, "不影响先保存日历草稿，地点可以稍后补充")
        isCampusRoomCode(value) -> SmartFieldUi("地点", value, SmartFieldState.Confirmed, "疑似校内教室")
        else -> SmartFieldUi("地点", value, SmartFieldState.Confirmed, "已识别到地点")
    }
}

fun isAmbiguousTimeText(value: String): Boolean {
    val normalized = value.trim().replace(" ", "")
    if (normalized.isBlank() || normalized == "待确认") return true
    val approximateLabels = listOf("大概", "左右", "约", "可能", "差不多")
    if (approximateLabels.any { fuzzyLabel -> normalized.contains(fuzzyLabel) }) return true
    if (hasExplicitClock(normalized)) return false
    return listOf(
        "今天上午",
        "今天下午",
        "今天晚上",
        "上午",
        "下午",
        "晚上",
        "今晚",
        "明天上午",
        "明天下午",
        "明天晚上",
        "明早",
        "明晚",
        "下周三下午",
    ).any { coarseTimeLabel -> normalized.contains(coarseTimeLabel) }
}

fun isCampusRoomCode(value: String): Boolean {
    val normalized = value.trim()
        .replace("教室", "")
        .replace("地点", "")
        .replace(" ", "")
    return normalized.matches(Regex("^[A-Za-z]?\\d{2,4}$")) ||
        normalized.matches(Regex("^[A-Za-z]{1,2}\\d{2,4}$")) ||
        normalized.matches(Regex("^[一二三四五六七八九十两0-9]{1,2}教\\d{2,4}$"))
}

private fun hasExplicitClock(value: String): Boolean =
    Regex("(?:[0-2]?\\d[:：][0-5]\\d|[一二三四五六七八九十两0-9]{1,3}点(?:半|[0-9]{1,2}分)?|早[一二三四五六七八九十两0-9]{1,2})").containsMatchIn(value)

private fun smartSceneLabel(scene: String): String =
    when {
        "课程" in scene || "course" in scene -> "课程"
        "考试" in scene || "exam" in scene -> "考试"
        "活动" in scene || "event" in scene -> "活动"
        "会议" in scene || "meeting" in scene -> "会议"
        else -> "待确认"
    }

private fun smartRecommendedActions(item: ShikeItem, preparation: List<String>): List<String> =
    buildList {
        if (!isAmbiguousTimeText(item.time) && item.startEpochMillis > 0L) add("打开日历草稿") else add("确认时间")
        add(if (preparation.isEmpty()) "添加课前包" else "课前包")
        if (isCampusRoomCode(item.location)) add("复制地点") else add("查看路线")
    }

private fun String.shortTimeHint(): String =
    when {
        contains("上午") -> "上午"
        contains("下午") -> "下午"
        contains("今晚") || contains("晚上") -> "晚上"
        else -> this
    }
