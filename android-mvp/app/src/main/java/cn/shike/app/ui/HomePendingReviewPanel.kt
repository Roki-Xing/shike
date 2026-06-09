package cn.shike.app.ui

import androidx.compose.runtime.Composable
import cn.shike.app.domain.ShikeItem

@Composable
fun HomePendingReviewPanel(selected: ShikeItem) {
    val hasMissingField = selected.time == "待确认" || selected.location == "待确认" || selected.status == "待确认"
    SectionCard("待确认") {
        if (hasMissingField) {
            KeyValue("当前卡片", selected.title)
            KeyValue("需要确认", listOf(selected.time, selected.location, selected.status).filter { it == "待确认" }.size.toString())
            ShikeStatusPill("在识别结果中补齐字段", ShikeColors.WarningSoft, ShikeColors.Warning)
        } else {
            KeyValue("当前状态", "暂无待确认")
            KeyValue("下一步", "可继续处理行动编排")
        }
    }
}
