package cn.shike.app.ui

import cn.shike.app.domain.ShikeItem

fun modelExplanation(item: ShikeItem): String {
    listOf("云端 AI 解析：").forEach { prefix ->
        val explanation = item.rawText.substringAfter(prefix, missingDelimiterValue = "")
            .lineSequence()
            .firstOrNull()
            ?.takeIf { it.isNotBlank() }
        if (explanation != null) return explanation
    }

    val reason = when {
        "云侧暂不可用" in item.rawText || "AI 暂不可用" in item.rawText -> "AI 暂时没识别成功，截图已保存为待确认。"
        "活动" in item.scene -> "海报包含活动主题、时间、地点或截止信息，适合生成待确认行动卡。"
        "课程" in item.scene -> "文本包含课程、时间、地点或截止事项，适合转成待确认行动卡。"
        else -> "碎片内容包含可追踪信息，需用户确认后再安排后续行动。"
    }
    val confidence = if (item.status == "待确认") "置信度或字段完整性仍需用户确认。" else "关键字段已确认。"
    return "$reason $confidence"
}
