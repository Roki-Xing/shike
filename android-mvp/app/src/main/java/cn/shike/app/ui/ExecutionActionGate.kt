package cn.shike.app.ui

import cn.shike.app.domain.ShikeItem

data class ExecutionActionGate(
    val missingTime: Boolean,
    val missingLocation: Boolean,
    val canUseCalendar: Boolean,
    val canUseReminder: Boolean,
    val canUseMap: Boolean,
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
        canUseReminder = isConfirmed,
        canUseMap = isConfirmed && !missingLocation,
    )
}
