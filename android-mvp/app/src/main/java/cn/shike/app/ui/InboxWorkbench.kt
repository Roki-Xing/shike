package cn.shike.app.ui

import cn.shike.app.domain.ShikeItem

const val inboxAllStatusFilter = "全部"

val inboxStatusFilters = listOf(inboxAllStatusFilter, "待确认", "已安排", "即将截止", "已完成", "已忽略")

data class InboxWorkbenchEntry(
    val title: String,
    val status: String,
    val scene: String,
    val location: String,
    val source: String,
    val rawText: String,
    val explanation: String,
    val executionSummary: String,
    val startEpochMillis: Long,
) {
    val archiveKey: String = "$title\n$rawText"

    fun matches(query: String): Boolean {
        val normalized = query.trim()
        if (normalized.isBlank()) {
            return true
        }
        return listOf(title, status, scene, location, source, rawText, explanation, executionSummary).any {
            it.contains(normalized, ignoreCase = true)
        }
    }
}

data class InboxArchiveActionState(
    val archiveEnabled: Boolean,
    val restoreEnabled: Boolean,
    val statusLabel: String,
    val detailText: String,
)

/**
 * Builds the inbox workbench entry from the current action card.
 *
 * Args:
 *     item: Current action card.
 *     source: Capture or backend source label.
 *     executionResults: Latest execution results for the card.
 *
 * Returns:
 *     Searchable inbox workbench entry.
 */
fun inboxWorkbenchEntryFrom(
    item: ShikeItem,
    source: String,
    executionResults: List<ExecutionResult>,
): InboxWorkbenchEntry =
    InboxWorkbenchEntry(
        title = item.title,
        status = item.status,
        scene = item.scene,
        location = item.location,
        source = source,
        rawText = item.rawText,
        explanation = modelExplanation(item),
        executionSummary = executionResults.joinToString("；") { "${it.action}:${it.status}" },
        startEpochMillis = item.startEpochMillis,
    )

/**
 * Normalizes the selected inbox status to a supported filter.
 *
 * Args:
 *     status: Current action card status.
 *
 * Returns:
 *     The status when supported, otherwise the pending-review filter.
 */
fun selectedInboxStatusFor(status: String): String =
    status.takeIf { it in inboxStatusFilters } ?: "待确认"

/**
 * Filters visible inbox entries by archive state, status, and search query.
 *
 * Args:
 *     entries: Candidate inbox entries.
 *     selectedStatus: Current status filter.
 *     query: User search query.
 *     archivedKeys: Archive keys hidden from the active inbox.
 *
 * Returns:
 *     Entries visible in the active inbox list.
 */
fun visibleInboxEntries(
    entries: List<InboxWorkbenchEntry>,
    selectedStatus: String,
    query: String,
    archivedKeys: Set<String>,
): List<InboxWorkbenchEntry> =
    entries.filter { entry ->
        entry.archiveKey !in archivedKeys &&
            (selectedStatus == inboxAllStatusFilter || entry.status == selectedStatus) &&
            entry.matches(query)
    }.sortedWith(compareBy<InboxWorkbenchEntry> { inboxStatusPriority(it.status) }
        .thenBy { it.startEpochMillis }
        .thenBy { it.title })

/**
 * Gives daily-tracking priority to urgent and review-needed inbox states.
 *
 * Args:
 *     status: Inbox card status.
 *
 * Returns:
 *     Lower value means the card appears earlier in the inbox list.
 */
fun inboxStatusPriority(status: String): Int =
    when (status) {
        "即将截止" -> 0
        "待确认" -> 1
        "已安排" -> 2
        "已完成" -> 3
        "已忽略" -> 4
        else -> 5
    }

/**
 * Derives the archive and restore affordances for the current inbox card.
 *
 * Args:
 *     isArchived: Whether the current card is hidden from the active inbox list.
 *
 * Returns:
 *     Button enablement and visible status copy for archive/restore controls.
 */
fun inboxArchiveActionStateFor(isArchived: Boolean): InboxArchiveActionState =
    if (isArchived) {
        InboxArchiveActionState(
            archiveEnabled = false,
            restoreEnabled = true,
            statusLabel = "已归档",
            detailText = "已归档但未删除，恢复后回到状态筛选结果。",
        )
    } else {
        InboxArchiveActionState(
            archiveEnabled = true,
            restoreEnabled = false,
            statusLabel = "收件箱内",
            detailText = "当前卡片保留在状态筛选结果，可归档但不会删除原始信息。",
        )
    }
