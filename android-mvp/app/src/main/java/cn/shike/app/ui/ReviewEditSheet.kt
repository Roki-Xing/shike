package cn.shike.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import cn.shike.app.domain.ShikeItem

@Composable
fun ReviewEditSheet(
    target: ReviewEditTarget,
    draftTitle: String,
    onTitleChange: (String) -> Unit,
    draftTime: String,
    onTimeChange: (String) -> Unit,
    draftLocation: String,
    onLocationChange: (String) -> Unit,
    draftStatus: String,
    onStatusChange: (String) -> Unit,
    draftPreparation: String,
    onPreparationChange: (String) -> Unit,
    draftSourceText: String,
    onSourceTextChange: (String) -> Unit,
    item: ShikeItem,
    onReviewed: (ShikeItem) -> Unit,
    onRegenerateFromSource: () -> Unit,
) {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        when (target) {
            ReviewEditTarget.All -> {
                FieldEditor(draftTitle, onTitleChange, "任务标题")
                FieldEditor(draftTime, onTimeChange, "时间")
                FieldEditor(draftLocation, onLocationChange, "地点")
                FieldEditor(draftPreparation, onPreparationChange, "准备事项")
                FieldEditor(draftStatus, onStatusChange, "状态")
            }
            ReviewEditTarget.Time -> FieldEditor(draftTime, onTimeChange, "只改时间")
            ReviewEditTarget.Location -> FieldEditor(draftLocation, onLocationChange, "只改地点")
            ReviewEditTarget.Preparation -> FieldEditor(draftPreparation, onPreparationChange, "只改准备事项")
            ReviewEditTarget.SourceText -> {
                FieldEditor(draftSourceText, onSourceTextChange, "修改原文并重新生成", singleLine = false)
                androidx.compose.material3.OutlinedButton(onClick = onRegenerateFromSource, modifier = Modifier.fillMaxWidth()) {
                    Text("重新生成行动卡")
                }
            }
            ReviewEditTarget.None -> Text("选择要修改的字段", style = ShikeTypography.Caption)
        }
        ReviewDecisionActions(
            item = item,
            draftTitle = draftTitle,
            draftTime = draftTime,
            draftLocation = draftLocation,
            draftStatus = draftStatus,
            draftPreparation = draftPreparation,
            onReviewed = onReviewed,
        )
    }
}

@Composable
private fun FieldEditor(
    value: String,
    onValueChange: (String) -> Unit,
    label: String,
    singleLine: Boolean = true,
) {
    OutlinedTextField(
        value = value,
        onValueChange = onValueChange,
        label = { Text(label) },
        modifier = Modifier.fillMaxWidth(),
        singleLine = singleLine,
    )
}
