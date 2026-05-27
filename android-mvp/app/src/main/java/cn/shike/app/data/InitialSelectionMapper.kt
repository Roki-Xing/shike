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
    val importedItem = itemFromSharedText(sharedText)
    if (!sharedText.isNullOrBlank()) {
        return InitialSelection(
            item = importedItem,
            captureSource = "文本分享入口（待确认，未落盘）",
            todayState = InitialTodayState.Ready,
        )
    }
    return InitialSelection(
        item = savedItem ?: importedItem,
        captureSource = if (savedItem == null) {
            "今日行动台空状态：尚无本地收件箱任务，可从截图、拍照、分享或手动输入开始。"
        } else {
            savedCaptureSource ?: "尚未采集图片，已加载离线样例。"
        },
        todayState = if (savedItem == null) InitialTodayState.Empty else InitialTodayState.Ready,
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
