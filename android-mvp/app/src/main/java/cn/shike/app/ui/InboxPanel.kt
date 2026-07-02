package cn.shike.app.ui

import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import cn.shike.app.domain.ShikeItem

@Composable
fun InboxPanel(
    item: ShikeItem,
    captureSource: String,
    executionResults: List<ExecutionResult>,
    historyEntries: List<InboxWorkbenchEntry> = emptyList(),
) {
    var selectedStatus by remember(item.status) { mutableStateOf(selectedInboxStatusFor(item.status)) }
    var searchQuery by remember { mutableStateOf("") }
    var isArchived by remember(item.title, item.rawText) { mutableStateOf(false) }
    val currentEntry = inboxWorkbenchEntryFrom(item, captureSource, executionResults)
    val allEntries = (historyEntries + currentEntry).distinctBy { it.archiveKey }
    val summaryStats = inboxSummaryStatsFor(allEntries)
    val archivedKeys = if (isArchived) setOf(currentEntry.archiveKey) else emptySet()
    val visibleEntries = visibleInboxEntries(
        entries = allEntries,
        selectedStatus = selectedStatus,
        query = searchQuery,
        archivedKeys = archivedKeys,
    )

    SectionCard("行动台") {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
        ) {
            summaryStats.forEach { stat ->
                SummaryStat(stat.count, stat.label, Color(0xFF0F766E))
            }
        }
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .horizontalScroll(rememberScrollState()),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            inboxStatusFilters.forEach { status ->
                OutlinedButton(onClick = { selectedStatus = status }) {
                    Text(if (status == selectedStatus) "✓ $status" else status)
                }
            }
        }
        OutlinedTextField(
            value = searchQuery,
            onValueChange = { searchQuery = it },
            label = { Text("搜课程、地点、活动") },
            modifier = Modifier.fillMaxWidth(),
            singleLine = true,
        )
        if (visibleEntries.isEmpty()) {
            KeyValue("筛选结果", "没有匹配的行动卡")
            KeyValue("当前筛选", selectedStatus)
        } else {
            visibleEntries.forEach { entry ->
                InboxWorkbenchRow(
                    entry = entry,
                    isArchived = isArchived && entry.archiveKey == currentEntry.archiveKey,
                    onArchive = { isArchived = true },
                    onRestore = { isArchived = false },
                )
            }
        }
        if (isArchived) {
            InboxArchiveRow(currentEntry, onRestore = { isArchived = false })
        }
    }
}

@Composable
private fun InboxWorkbenchRow(
    entry: InboxWorkbenchEntry,
    isArchived: Boolean,
    onArchive: () -> Unit,
    onRestore: () -> Unit,
) {
    val archiveActionState = inboxArchiveActionStateFor(isArchived)
    var showEvidence by rememberSaveable(entry.archiveKey) { mutableStateOf(false) }
    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
        KeyValue("标题", entry.title)
        KeyValue("时间", if (entry.startEpochMillis > 0L) "今天" else "待确认")
        KeyValue("地点", entry.location.ifBlank { "待确认" })
        KeyValue("状态", entry.status)
        KeyValue("下一步", inboxNextStepFor(entry))
        TextButton(onClick = { showEvidence = !showEvidence }) {
            Text(if (showEvidence) "收起识别依据" else "查看识别依据")
        }
        if (showEvidence) {
            KeyValue("识别原文", entry.rawText.take(36))
            KeyValue("判断依据", entry.explanation.take(42))
            KeyValue("回执", entry.executionSummary)
        }
        KeyValue("归档状态", archiveActionState.statusLabel)
        InboxArchiveActions(
            actionState = archiveActionState,
            onArchive = onArchive,
            onRestore = onRestore,
        )
    }
}

@Composable
private fun InboxArchiveRow(entry: InboxWorkbenchEntry, onRestore: () -> Unit) {
    val archiveActionState = inboxArchiveActionStateFor(isArchived = true)
    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
        KeyValue("归档区", entry.title)
        KeyValue("归档说明", archiveActionState.detailText)
        InboxArchiveActions(actionState = archiveActionState, onArchive = {}, onRestore = onRestore)
    }
}

@Composable
private fun InboxArchiveActions(
    actionState: InboxArchiveActionState,
    onArchive: () -> Unit,
    onRestore: () -> Unit,
) {
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
        OutlinedButton(onClick = onArchive, enabled = actionState.archiveEnabled, modifier = Modifier.weight(1f)) {
            Text("归档")
        }
        OutlinedButton(onClick = onRestore, enabled = actionState.restoreEnabled, modifier = Modifier.weight(1f)) {
            Text("恢复")
        }
    }
}
