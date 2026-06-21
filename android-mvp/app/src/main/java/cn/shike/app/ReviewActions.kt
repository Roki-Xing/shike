package cn.shike.app

import cn.shike.app.data.mapReviewedItemState
import cn.shike.app.domain.ShikeItem

fun reviewedItemWithPreparationDraft(
    item: ShikeItem,
    title: String,
    time: String,
    location: String,
    status: String,
    preparation: String,
): ShikeItem =
    item.copy(
        title = title.ifBlank { item.title },
        time = time.ifBlank { "待确认" },
        location = location.ifBlank { "待确认" },
        status = status.ifBlank { "待确认" },
        rawText = item.rawText.withPreparationEvidence(preparation),
    )

fun applyReviewedItemSelection(
    item: ShikeItem,
    persistSelection: (ShikeItem, String) -> Unit,
): String {
    val review = mapReviewedItemState(item)
    val reviewedItem = review.item
    persistSelection(reviewedItem, "用户确认修正：${item.scene}")
    return review.statusMessage
}

private fun String.withPreparationEvidence(preparation: String): String {
    val items = preparation.split('、', ',', '，', ';', '；', '\n')
        .map { it.trim() }
        .filter { it.isNotBlank() }
        .distinct()
    val keptLines = lineSequence()
        .map { it.trim() }
        .filter { it.isNotBlank() }
        .filterNot { it.startsWith("准备：") || it.startsWith("准备事项：") }
        .toMutableList()
    if (items.isNotEmpty()) {
        val insertAt = keptLines.indexOfFirst { it.startsWith("需要确认：") || it.startsWith("风险：") }
            .takeIf { it >= 0 }
            ?: keptLines.size
        keptLines.add(insertAt, "准备：${items.joinToString("、")}")
    }
    return keptLines.joinToString("\n")
}
