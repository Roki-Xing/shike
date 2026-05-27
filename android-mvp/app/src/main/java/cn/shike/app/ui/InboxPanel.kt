package cn.shike.app.ui

import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import cn.shike.app.domain.ShikeItem

@Composable
fun InboxPanel(item: ShikeItem, captureSource: String, executionResults: List<ExecutionResult>) {
    var selectedStatus by remember(item.status) { mutableStateOf(selectedInboxStatusFor(item.status)) }
    var searchQuery by remember { mutableStateOf("") }
    var isArchived by remember(item.title, item.rawText) { mutableStateOf(false) }
    val currentEntry = inboxWorkbenchEntryFrom(item, captureSource, executionResults)
    val archivedKeys = if (isArchived) setOf(currentEntry.archiveKey) else emptySet()
    val visibleEntries = visibleInboxEntries(
        entries = listOf(currentEntry),
        selectedStatus = selectedStatus,
        query = searchQuery,
        archivedKeys = archivedKeys,
    )

    SectionCard("收件箱状态") {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
        ) {
            SummaryStat("3", "待确认", Color(0xFF0F766E))
            SummaryStat("1", "已安排", Color(0xFFF97316))
            SummaryStat("2", "即将截止", Color(0xFF2563EB))
        }
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .horizontalScroll(rememberScrollState()),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            inboxStatusFilters.forEach { status ->
                OutlinedButton(onClick = { selectedStatus = status }) {
                    androidx.compose.material3.Text(if (status == selectedStatus) "✓ $status" else status)
                }
            }
        }
        OutlinedTextField(
            value = searchQuery,
            onValueChange = { searchQuery = it },
            label = { androidx.compose.material3.Text("搜索标题、地点、来源文本、场景或 OCR 原文") },
            modifier = Modifier.fillMaxWidth(),
            singleLine = true,
        )
        if (visibleEntries.isEmpty()) {
            KeyValue("筛选结果", "没有匹配的收件箱卡片")
            KeyValue("当前筛选", selectedStatus)
        } else {
            visibleEntries.forEach { entry ->
                InboxWorkbenchRow(
                    entry = entry,
                    isArchived = isArchived,
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
    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
        KeyValue("当前卡片", entry.title)
        KeyValue("当前状态", entry.status)
        KeyValue("场景", entry.scene)
        KeyValue("地点", entry.location)
        KeyValue("来源", entry.source)
        KeyValue("OCR 原文", entry.rawText.take(36))
        KeyValue("模型解释", entry.explanation.take(42))
        KeyValue("执行结果", entry.executionSummary)
        KeyValue("归档状态", archiveActionState.statusLabel)
        KeyValue("归档说明", archiveActionState.detailText)
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
            androidx.compose.material3.Text("归档")
        }
        OutlinedButton(onClick = onRestore, enabled = actionState.restoreEnabled, modifier = Modifier.weight(1f)) {
            androidx.compose.material3.Text("恢复")
        }
    }
}
