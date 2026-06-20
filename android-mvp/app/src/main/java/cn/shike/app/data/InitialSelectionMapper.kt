package cn.shike.app.data

import android.content.Context
import cn.shike.app.domain.ShikeItem

enum class InitialTodayState {
    Ready,
    Empty,
}

data class InitialSelection(
    val item: ShikeItem,
    val captureSource: String,
    val todayState: InitialTodayState,
)

/**
 * Builds the initial review card from share input and optional cached inbox data.
 *
 * Args:
 *     sharedText: Optional text received from the Android share sheet.
 *     savedItem: Optional cached inbox snapshot loaded by the caller.
 *     savedCaptureSource: Optional cached source label for the saved snapshot.
 *
 * Returns:
 *     The initial action card and source label shown by the import panel.
 */
fun buildInitialSelection(
    sharedText: String?,
    savedItem: ShikeItem?,
    savedCaptureSource: String?,
): InitialSelection {
    buildRuntimeSharedTextSelection(sharedText)?.let { selection ->
        return selection
    }
    val importedItem = itemFromSharedText(sharedText)
    return InitialSelection(
        item = savedItem ?: importedItem.copy(
            rawText = listOf(
                "今天还没有待处理事项",
                "把截图交给拾刻，生成第一张行动卡",
            ).joinToString("\n"),
        ),
        captureSource = if (savedItem == null) {
            "今天还没有待处理事项：把截图交给拾刻，生成第一张行动卡。"
        } else {
            savedCaptureSource ?: "已恢复上次保存的行动卡。"
        },
        todayState = if (savedItem == null) InitialTodayState.Empty else InitialTodayState.Ready,
    )
}

/**
 * Builds a ready review card from text received while the app is already open.
 *
 * Args:
 *     sharedText: Optional text received from a new `Intent.ACTION_SEND` event.
 *
 * Returns:
 *     A ready text-share selection, or null when the incoming text is blank.
 */
fun buildRuntimeSharedTextSelection(sharedText: String?): InitialSelection? {
    if (sharedText.isNullOrBlank()) {
        return null
    }
    return InitialSelection(
        item = itemFromSharedText(sharedText),
        captureSource = "文本分享入口（待确认，未落盘）",
        todayState = InitialTodayState.Ready,
    )
}

/**
 * Builds the initial review card from share input or the cached inbox snapshot.
 *
 * Args:
 *     context: Android context used to load the local inbox snapshot.
 *     sharedText: Optional text received from the Android share sheet.
 *
 * Returns:
 *     The initial action card and source label shown by the import panel.
 */
fun loadInitialSelection(context: Context, sharedText: String?): InitialSelection {
    val savedItem = loadSavedItem(context)
    val savedCaptureSource = if (savedItem == null) null else loadSavedCaptureSource(context)
    return buildInitialSelection(sharedText, savedItem, savedCaptureSource)
}
