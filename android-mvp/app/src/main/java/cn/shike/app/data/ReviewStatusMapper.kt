package cn.shike.app.data

import cn.shike.app.domain.ShikeItem

data class ReviewedItemState(
    val item: ShikeItem,
    val statusMessage: String,
)

/**
 * Maps a manually reviewed item into persisted item state and model status copy.
 *
 * Args:
 *     item: User-edited item returned from the review panel.
 *
 * Returns:
 *     The item to persist and the model status message shown in the import panel.
 */
fun mapReviewedItemState(item: ShikeItem): ReviewedItemState {
    val reviewedItem = if (item.status == "已忽略") item else item.copy(status = "已安排")
    val statusMessage = if (reviewedItem.status == "已忽略") {
        "模型编排：用户已忽略"
    } else {
        "模型编排：用户已确认"
    }
    return ReviewedItemState(reviewedItem, statusMessage)
}
