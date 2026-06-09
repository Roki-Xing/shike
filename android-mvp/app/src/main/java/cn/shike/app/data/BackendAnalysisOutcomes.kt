package cn.shike.app.data

import cn.shike.app.domain.ShikeItem

data class BackendAnalysisOutcome(
    val item: ShikeItem,
    val source: String,
    val statusMessage: String,
)

data class BackendFailureFallbackCopy(
    val rawText: String,
    val source: String,
    val statusMessage: String,
)

fun backendSuccessOutcome(item: ShikeItem): BackendAnalysisOutcome =
    BackendAnalysisOutcome(
        item = item,
        source = "云端 AI 解析：${item.scene}",
        statusMessage = "云端 AI 解析完成",
    )

fun backendFailureFallbackCopyFor(textForAnalyze: String): BackendFailureFallbackCopy =
    BackendFailureFallbackCopy(
        rawText = "${redactSensitiveLogText(textForAnalyze)}\n云侧暂不可用，已切换为本地确认，日志已脱敏。",
        source = "云侧解析失败，本地待确认",
        statusMessage = "云侧暂不可用，已切换为本地确认",
    )

fun backendFailureOutcome(fallback: ShikeItem, textForAnalyze: String): BackendAnalysisOutcome {
    val fallbackCopy = backendFailureFallbackCopyFor(textForAnalyze)
    return BackendAnalysisOutcome(
        item = fallbackItemForRealDraft(fallback, textForAnalyze).copy(
            status = "待确认",
            rawText = fallbackCopy.rawText,
        ),
        source = fallbackCopy.source,
        statusMessage = fallbackCopy.statusMessage,
    )
}

fun backendImageFailureOutcome(fallback: ShikeItem, textForAnalyze: String, reason: String): BackendAnalysisOutcome =
    BackendAnalysisOutcome(
        item = fallbackItemForRealDraft(fallback, textForAnalyze).copy(
            status = "待确认",
            rawText = "${redactSensitiveLogText(textForAnalyze)}\n$reason，已进入本地待确认，日志已脱敏。",
        ),
        source = "云侧图片解析失败，本地待确认",
        statusMessage = "云侧图片理解暂不可用，已进入待确认",
    )

fun backendImageSuccessOutcome(item: ShikeItem): BackendAnalysisOutcome =
    BackendAnalysisOutcome(
        item = item,
        source = "云端图片解析：${item.scene}",
        statusMessage = "云端图片解析完成",
    )

fun backendImageManualReviewOutcome(item: ShikeItem): BackendAnalysisOutcome =
    BackendAnalysisOutcome(
        item = item,
        source = "云侧图片解析失败，本地待确认",
        statusMessage = "云侧图片理解暂不可用，已进入待确认",
    )

fun fallbackItemForRealDraft(fallback: ShikeItem, textForAnalyze: String): ShikeItem {
    val trimmed = textForAnalyze.trim()
    if (trimmed.isBlank()) {
        return fallback
    }
    if ("高数" in trimmed && "B203" !in trimmed && "18:30" !in trimmed && "22:00" !in trimmed) {
        return fallback.copy(
            title = "上高数 A",
            scene = "课程通知",
            time = "今天晚上（需确认具体时间）",
            location = "待补充",
            actions = listOf("先存入待确认"),
            rawText = trimmed,
        )
    }
    return fallback.copy(
        title = trimmed.lineSequence().firstOrNull()?.take(18)?.ifBlank { fallback.title } ?: fallback.title,
        time = "待确认",
        location = "待补充",
        actions = listOf("先存入待确认"),
        rawText = trimmed,
    )
}
