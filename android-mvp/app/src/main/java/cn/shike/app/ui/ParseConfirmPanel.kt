package cn.shike.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.unit.dp
import cn.shike.app.domain.ShikeItem

enum class ReviewEditTarget {
    None,
    All,
    Time,
    Location,
    Preparation,
    SourceText,
}

@Composable
fun ParseConfirmPanel(item: ShikeItem, onReviewed: (ShikeItem) -> Unit) {
    var draftTitle by remember(item.title) { mutableStateOf(item.title) }
    var draftTime by remember(item.time) { mutableStateOf(item.time) }
    var draftLocation by remember(item.location) { mutableStateOf(item.location) }
    var draftStatus by remember(item.status) { mutableStateOf(item.status) }
    var draftPreparation by remember(item.rawText) { mutableStateOf(actionCardUiModelFrom(item).preparationItems.joinToString("、")) }
    var draftSourceText by remember(item.rawText) { mutableStateOf(actionCardUiModelFrom(item).sourceTextPreview) }
    val actionCard = actionCardUiModelFrom(item)
    var editTarget by rememberSaveable(item.rawText) { mutableStateOf(ReviewEditTarget.None) }
    var showReason by rememberSaveable(item.rawText) { mutableStateOf(false) }
    var showSourceText by rememberSaveable(item.rawText) { mutableStateOf(false) }
    SectionCard("AI 生成的行动卡") {
        ParseConfirmHeader(item)
        StructuredActionCard(
            model = actionCard,
            onConfirmAndPlan = {
                onReviewed(
                    item.copy(
                        title = draftTitle.ifBlank { item.title },
                        time = draftTime.ifBlank { "待确认" },
                        location = draftLocation.ifBlank { "待确认" },
                        status = draftStatus.ifBlank { "待确认" },
                    )
                )
            },
            onEdit = { editTarget = ReviewEditTarget.All },
            onEditTime = { editTarget = ReviewEditTarget.Time },
            onEditLocation = { editTarget = ReviewEditTarget.Location },
            onEditPreparation = { editTarget = ReviewEditTarget.Preparation },
            onEditSourceText = { editTarget = ReviewEditTarget.SourceText },
        )
        if (editTarget != ReviewEditTarget.None) {
            ReviewEditSheet(
                target = editTarget,
                draftTitle = draftTitle,
                onTitleChange = { draftTitle = it },
                draftTime = draftTime,
                onTimeChange = { draftTime = it },
                draftLocation = draftLocation,
                onLocationChange = { draftLocation = it },
                draftStatus = draftStatus,
                onStatusChange = { draftStatus = it },
                draftPreparation = draftPreparation,
                onPreparationChange = { draftPreparation = it },
                draftSourceText = draftSourceText,
                onSourceTextChange = { draftSourceText = it },
                item = item,
                onReviewed = onReviewed,
                onRegenerateFromSource = {
                    onReviewed(
                        item.copy(
                            title = draftTitle.ifBlank { item.title },
                            time = draftTime.ifBlank { "待确认" },
                            location = draftLocation.ifBlank { "待确认" },
                            status = "待确认",
                            rawText = listOf(
                                draftSourceText.ifBlank { actionCard.sourceTextPreview },
                                "需要确认：已根据修改后的识别文字重新生成，请确认时间、地点和准备事项。",
                            ).joinToString("\n"),
                        )
                    )
                    editTarget = ReviewEditTarget.None
                },
            )
        }
        RiskChecklistPanel(item)
        ExpandableInfoRow(
            label = "为什么这样判断",
            expanded = showReason,
            onToggle = { showReason = !showReason },
            body = actionCard.userWarnings.ifEmpty { listOf("关键字段已可确认，系统动作仍需你确认后执行。") }.joinToString("\n"),
        )
        ExpandableInfoRow(
            label = "查看识别原文",
            expanded = showSourceText,
            onToggle = { showSourceText = !showSourceText },
            body = actionCard.sourceTextPreview.ifBlank { "暂无可展示的识别原文" },
        )
        Text("确认后才会进入日历、提醒和地图安排。", style = ShikeTypography.Caption)
    }
}

@Composable
private fun ExpandableInfoRow(
    label: String,
    expanded: Boolean,
    onToggle: () -> Unit,
    body: String,
) {
    androidx.compose.material3.TextButton(onClick = onToggle) {
        Text(if (expanded) "收起$label" else label)
    }
    if (expanded) {
        Text(body, style = ShikeTypography.Caption)
    }
}
