package cn.shike.app.data

import cn.shike.app.domain.ShikeItem

fun sharedTextCaptureDraft(text: String?): CaptureDraft =
    CaptureDraft(
        channel = "share",
        sourceLabel = "系统分享文本",
        rawText = text.orEmpty(),
    )

/**
 * Maps Android share-sheet text into the initial review card.
 *
 * Args:
 *     text: Text received from `Intent.EXTRA_TEXT`.
 *
 * Returns:
 *     A course or event sample seeded with the shared raw text.
 */
fun itemFromSharedText(text: String?): ShikeItem {
    val draft = sharedTextCaptureDraft(text)
    if (draft.rawText.isBlank()) {
        return sampleCourse()
    }
    return when {
        "活动" in draft.rawText || "分享会" in draft.rawText -> sampleEvent().copy(title = "分享导入的活动", rawText = draft.rawText)
        else -> sampleCourse().copy(title = "分享导入的课程通知", rawText = draft.rawText)
    }
}
