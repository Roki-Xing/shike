package cn.shike.app

import cn.shike.app.data.mapReviewedItemState
import cn.shike.app.domain.ShikeItem

fun applyReviewedItemSelection(
    item: ShikeItem,
    persistSelection: (ShikeItem, String) -> Unit,
): String {
    val review = mapReviewedItemState(item)
    val reviewedItem = review.item
    persistSelection(reviewedItem, "用户确认修正：${item.scene}")
    return review.statusMessage
}
