package cn.shike.app.ui

import cn.shike.app.domain.ShikeItem
import cn.shike.app.domain.preparationItemsFrom

fun preparationItemsForUi(item: ShikeItem): List<String> {
    val modelItems = cleanPreparationItems(preparationItemsFrom(item))
    if (modelItems.isNotEmpty()) return modelItems
    return defaultPreparationSuggestionsFor(item)
}

fun defaultPreparationSuggestionsFor(item: ShikeItem): List<String> {
    val text = listOf(item.title, item.scene, item.rawText).joinToString(" ")
    val suggestions = when {
        text.containsAny("考试", "测验", "准考证") ->
            listOf("带准考证", "带文具", "提前到场")
        text.containsAny("班会", "会议", "汇报", "面试") ->
            listOf("准备发言", "带记录本", "提前10分钟到")
        text.containsAny("活动", "报名", "社团") ->
            listOf("确认报名", "带证件", "提前签到")
        text.containsAny("高数", "课程", "上课", "教室", "课") ->
            listOf("带课本", "带作业", "提前10分钟到")
        else -> emptyList()
    }
    return cleanPreparationItems(suggestions)
}

private fun String.containsAny(vararg words: String): Boolean =
    words.any { word -> contains(word) }
