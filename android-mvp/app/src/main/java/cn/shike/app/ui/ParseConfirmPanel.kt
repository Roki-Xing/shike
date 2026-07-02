package cn.shike.app.ui

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.slideInVertically
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.unit.dp
import cn.shike.app.reviewedItemWithPreparationDraft
import cn.shike.app.domain.ShikeItem
import kotlinx.coroutines.delay

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
    val smartCard = smartActionCardUiModelFrom(item)
    val readiness = actionReadinessUiModelFrom(item)
    var editTarget by rememberSaveable(item.rawText) { mutableStateOf(ReviewEditTarget.None) }
    var showReason by rememberSaveable(item.rawText) { mutableStateOf(false) }
    var showSourceText by rememberSaveable(item.rawText) { mutableStateOf(false) }
    var showGeneratedHint by rememberSaveable(item.rawText) { mutableStateOf(true) }
    LaunchedEffect(item.rawText) {
        showGeneratedHint = true
        delay(1000)
        showGeneratedHint = false
    }
    SectionCard("生成的行动卡") {
        ParseConfirmHeader(item)
        AnimatedVisibility(visible = showGeneratedHint, enter = fadeIn()) {
            Text("行动卡已生成", color = ShikeColors.Brand, style = ShikeTypography.Caption)
        }
        ActionReadinessBar(readiness)
        AnimatedVisibility(visible = true, enter = fadeIn() + slideInVertically { it / 6 }) {
            SmartActionCard(
                model = smartCard,
                onConfirmAndPlan = {
                    onReviewed(
                        reviewedItemWithPreparationDraft(
                            item = item,
                            title = draftTitle,
                            time = draftTime,
                            location = draftLocation,
                            status = draftStatus,
                            preparation = draftPreparation,
                        )
                    )
                },
                onEditTime = { editTarget = ReviewEditTarget.Time },
                onEditLocation = { editTarget = ReviewEditTarget.Location },
                onEditPreparation = { editTarget = ReviewEditTarget.Preparation },
                onEditSourceText = { editTarget = ReviewEditTarget.SourceText },
            )
        }
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
                        reviewedItemWithPreparationDraft(
                            item = item.copy(
                                rawText = listOf(
                                    draftSourceText.ifBlank { actionCard.sourceTextPreview },
                                    "需要确认：已根据修改后的识别文字重新生成，请确认时间、地点和准备事项。",
                                ).joinToString("\n"),
                            ),
                            title = draftTitle,
                            time = draftTime,
                            location = draftLocation,
                            status = "待确认",
                            preparation = draftPreparation,
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
