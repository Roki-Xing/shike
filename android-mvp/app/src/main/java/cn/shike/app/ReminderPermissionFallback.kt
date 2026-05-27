package cn.shike.app

import cn.shike.app.domain.ShikeItem

const val REMINDER_PERMISSION_BLOCKED_STATUS = "permission_blocked"

data class ReminderPermissionFallbackCopy(
    val source: String,
    val executionDetail: String,
)

/**
 * Builds the user-visible copy used when notification permission blocks reminders.
 *
 * Args:
 *     item: Confirmed action card that must stay recoverable after permission denial.
 *
 * Returns:
 *     Shared persistence source and execution-result detail for the fallback path.
 */
fun reminderPermissionFallbackCopyFor(item: ShikeItem): ReminderPermissionFallbackCopy {
    val title = item.title.trim().ifBlank { "当前行动卡" }
    return ReminderPermissionFallbackCopy(
        source = "通知权限拒绝 $REMINDER_PERMISSION_BLOCKED_STATUS：已保留「$title」行动卡，稍后可开启通知权限后再安排提醒。",
        executionDetail = "已请求本地定时提醒；通知权限拒绝时进入 $REMINDER_PERMISSION_BLOCKED_STATUS 并保留「$title」行动卡。",
    )
}
