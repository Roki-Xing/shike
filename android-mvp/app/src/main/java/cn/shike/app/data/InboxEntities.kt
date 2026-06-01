package cn.shike.app.data

import cn.shike.app.domain.ShikeItem

data class InboxItemEntity(
    val id: String,
    val title: String,
    val scene: String,
    val time: String,
    val location: String,
    val status: String,
    val source: String,
    val rawText: String,
    val actionLabels: List<String>,
    val startEpochMillis: Long,
    val updatedEpochMillis: Long,
    val archived: Boolean = false,
)

data class CaptureDraftEntity(
    val id: String,
    val sourceType: String,
    val localImageUri: String?,
    val ocrText: String,
    val createdEpochMillis: Long,
    val privacyLevel: String,
)

data class ActionDraftEntity(
    val id: String,
    val inboxItemId: String,
    val actionType: String,
    val label: String,
    val enabled: Boolean,
)

data class ExecutionResultEntity(
    val id: String,
    val inboxItemId: String,
    val actionType: String,
    val status: String,
    val detail: String,
    val executedEpochMillis: Long,
)

fun inboxItemEntityFrom(
    item: ShikeItem,
    captureSource: String,
    updatedEpochMillis: Long,
): InboxItemEntity =
    InboxItemEntity(
        id = stableInboxItemId(item.title, item.rawText, item.startEpochMillis),
        title = item.title,
        scene = item.scene,
        time = item.time,
        location = item.location,
        status = normalizeInboxStatus(item.status),
        source = sanitizeInboxCaptureSource(captureSource),
        rawText = sanitizeInboxRawText(item.rawText),
        actionLabels = item.actions,
        startEpochMillis = item.startEpochMillis,
        updatedEpochMillis = updatedEpochMillis,
    )

fun shikeItemFromInboxEntity(entity: InboxItemEntity): ShikeItem =
    ShikeItem(
        title = entity.title,
        scene = entity.scene,
        time = entity.time,
        location = entity.location,
        status = normalizeInboxStatus(entity.status),
        actions = entity.actionLabels.ifEmpty { sampleCourse().actions },
        startEpochMillis = entity.startEpochMillis,
        rawText = entity.rawText,
    )

fun normalizeInboxStatus(status: String): String =
    status.takeIf { it in setOf("待确认", "已安排", "即将截止", "已完成", "已忽略") } ?: "待确认"

fun stableInboxItemId(title: String, rawText: String, startEpochMillis: Long): String {
    val source = "$title|$rawText|$startEpochMillis"
    return Integer.toUnsignedString(source.hashCode(), 16)
}
