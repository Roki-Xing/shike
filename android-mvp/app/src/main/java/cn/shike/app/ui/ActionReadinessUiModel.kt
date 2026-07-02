package cn.shike.app.ui

import cn.shike.app.domain.ShikeItem
import cn.shike.app.domain.preparationItemsFrom

data class ActionReadinessUiModel(
    val completed: Int,
    val total: Int,
    val title: String,
    val subtitle: String,
    val steps: List<ActionReadinessStepUi>,
)

data class ActionReadinessStepUi(
    val label: String,
    val completed: Boolean,
    val helper: String,
)

fun actionReadinessUiModelFrom(
    item: ShikeItem,
    executionResults: List<ExecutionResult> = emptyList(),
): ActionReadinessUiModel {
    val timeReady = item.time.isNotBlank() && item.time != "待确认" && !isAmbiguousTimeText(item.time)
    val locationReady = item.location.isNotBlank() && item.location != "待确认"
    val explicitPreparation = cleanPreparationItems(preparationItemsFrom(item)).isNotEmpty()
    val calendarReady = calendarReadinessDone(item, executionResults, timeReady, locationReady, explicitPreparation)
    val steps = listOf(
        ActionReadinessStepUi(
            label = "时间",
            completed = timeReady,
            helper = if (timeReady) "时间可用，保存前仍可改" else "保存前确认时间",
        ),
        ActionReadinessStepUi(
            label = "地点",
            completed = locationReady,
            helper = if (locationReady) "地点已放进卡片" else "补地点后更完整",
        ),
        ActionReadinessStepUi(
            label = "课前包",
            completed = explicitPreparation,
            helper = if (explicitPreparation) "准备事项已带上" else "可添加准备事项",
        ),
        ActionReadinessStepUi(
            label = "日历",
            completed = calendarReady,
            helper = if (calendarReady) "日历草稿可继续" else "日历待保存",
        ),
    )
    val completed = steps.count { it.completed }
    val subtitle = when {
        completed == steps.size -> "这张卡已经可以安排"
        !locationReady -> "还差地点，补上后更完整"
        !timeReady -> "时间是建议值，保存前确认一下"
        !explicitPreparation -> "可以加一条准备事项"
        else -> "日历待保存"
    }
    return ActionReadinessUiModel(
        completed = completed,
        total = steps.size,
        title = "行动准备度 $completed/${steps.size}",
        subtitle = subtitle,
        steps = steps,
    )
}

private fun calendarReadinessDone(
    item: ShikeItem,
    executionResults: List<ExecutionResult>,
    timeReady: Boolean,
    locationReady: Boolean,
    explicitPreparation: Boolean,
): Boolean {
    val hasRealExecutionState = executionResults.any { it.status != "建议" }
    if (!hasRealExecutionState && executionResults.isEmpty()) {
        return timeReady && locationReady && explicitPreparation && item.title.isNotBlank()
    }
    return executionResults.any { result ->
        result.action == "日历" && (
            result.status != "建议" ||
                result.detail.contains("日历草稿") ||
                result.detail.contains("系统日历") ||
                result.status.contains("已保存")
        )
    }
}
