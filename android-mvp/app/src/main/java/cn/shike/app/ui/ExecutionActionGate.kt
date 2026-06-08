package cn.shike.app.ui

import cn.shike.app.REMINDER_PERMISSION_BLOCKED_STATUS
import cn.shike.app.domain.ShikeItem

data class ExecutionActionGate(
    val missingTime: Boolean,
    val missingLocation: Boolean,
    val canUseCalendar: Boolean,
    val canUseReminder: Boolean,
    val canUseMap: Boolean,
)

data class ExecutionActionButtonLabels(
    val calendar: String,
    val reminder: String,
    val map: String,
)

/**
 * Derives user-confirmed execution gates for sensitive system actions.
 *
 * Args:
 *     item: Current action card.
 *     isConfirmed: Whether the user has confirmed the parsed fields.
 *
 * Returns:
 *     Gate flags shared by the confirmation banner and action planner.
 */
fun executionActionGateFor(item: ShikeItem, isConfirmed: Boolean): ExecutionActionGate {
    val missingTime = item.time.isBlank() || item.time == "待确认"
    val missingLocation = item.location.isBlank() || item.location == "待确认"
    return ExecutionActionGate(
        missingTime = missingTime,
        missingLocation = missingLocation,
        canUseCalendar = isConfirmed && !missingTime,
        canUseReminder = isConfirmed && !missingTime,
        canUseMap = isConfirmed && !missingLocation,
    )
}

/**
 * Derives action button copy from the same confirmation and missing-field gate.
 *
 * Args:
 *     item: Current action card.
 *     isConfirmed: Whether the user has confirmed the parsed fields.
 *
 * Returns:
 *     User-facing labels for calendar, reminder, and map actions.
 */
fun executionActionButtonLabelsFor(
    item: ShikeItem,
    isConfirmed: Boolean,
    executionResults: List<ExecutionResult> = emptyList(),
): ExecutionActionButtonLabels {
    val gate = executionActionGateFor(item, isConfirmed)
    if (!isConfirmed) {
        return ExecutionActionButtonLabels(
            calendar = "先确认字段",
            reminder = "先确认字段",
            map = "先确认字段",
        )
    }
    return ExecutionActionButtonLabels(
        calendar = if (gate.missingTime) "补充时间后可用" else "打开日历",
        reminder = when {
            gate.missingTime -> "补充时间后可用"
            executionResults.hasReminderPermissionBlocked() -> "去开启通知"
            else -> "设置提醒"
        },
        map = if (gate.missingLocation) "补充地点后可用" else "查看路线",
    )
}

private fun List<ExecutionResult>.hasReminderPermissionBlocked(): Boolean =
    any { result ->
        result.action == "提醒" &&
            (result.status == REMINDER_PERMISSION_BLOCKED_STATUS ||
                REMINDER_PERMISSION_BLOCKED_STATUS in result.detail)
    }
