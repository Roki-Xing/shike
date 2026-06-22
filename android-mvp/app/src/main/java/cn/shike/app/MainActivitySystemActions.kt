package cn.shike.app

import android.Manifest
import androidx.activity.ComponentActivity
import cn.shike.app.data.ImageCleanupStatus
import cn.shike.app.data.loadInitialSelection
import cn.shike.app.data.saveSnapshot
import cn.shike.app.domain.ShikeItem
import cn.shike.app.system.buildCalendarInsertIntent
import cn.shike.app.system.buildMapIntent
import cn.shike.app.system.canPostReminderNotification
import cn.shike.app.system.copyMapLocationFallback
import cn.shike.app.system.SourceImageCleanupManager
import cn.shike.app.system.SourceImageCleanupRequest
import cn.shike.app.system.MapActionMode
import cn.shike.app.system.scheduleReminder
import cn.shike.app.system.startSystemActivitySafely
import cn.shike.app.system.mapActionModeFor

fun ComponentActivity.openCalendarInsert(item: ShikeItem) {
    startSystemActivitySafely(
        context = this,
        intent = buildCalendarInsertIntent(item),
        item = item,
        fallbackSource = "系统日历新增页不可用，已保留行动卡，稍后可手动添加日程。",
        onFallback = ::saveSystemActionFallback,
    )
}

fun MainActivity.requestReminder(item: ShikeItem) {
    if (canPostReminderNotification(this)) {
        saveScheduledReminder(item)
    } else {
        pendingReminderItem = item
        notificationPermission.launch(Manifest.permission.POST_NOTIFICATIONS)
    }
}

fun ComponentActivity.saveReminderPermissionFallback(item: ShikeItem) {
    saveSnapshot(this, item, reminderPermissionFallbackCopyFor(item).source)
}

fun ComponentActivity.saveScheduledReminder(item: ShikeItem) {
    saveSnapshot(this, item, scheduleReminder(this, item))
}

fun ComponentActivity.openMap(item: ShikeItem) {
    when (mapActionModeFor(item.location)) {
        MapActionMode.Disabled -> {
            saveMapFallback(item, "地点不完整，已保留行动卡")
            return
        }
        MapActionMode.CopyOnly -> {
            saveMapFallback(item, "地点像校内教室代码，已复制地点；补充校区后再打开地图")
            return
        }
        MapActionMode.OpenMap -> Unit
    }
    startSystemActivitySafely(
        context = this,
        intent = buildMapIntent(item),
        item = item,
        fallbackSource = "地图应用不可用，已保留地点：${item.location}",
        onFallback = ::saveMapFallback,
    )
}

fun ComponentActivity.saveMapFallback(item: ShikeItem, source: String) {
    saveSystemActionFallback(item, "$source；${copyMapLocationFallback(this, item)}")
}

fun ComponentActivity.saveSystemActionFallback(item: ShikeItem, source: String) {
    saveSnapshot(this, item, source)
}

fun MainActivity.handleImageCleanupStatusFromApp(status: ImageCleanupStatus) {
    if (status == ImageCleanupStatus.DELETE_REQUESTED) {
        saveSnapshot(this, loadSavedItemOrFallback(), "原截图清理：已请求系统确认")
    }
}

fun MainActivity.handleImageCleanupStatusFromSystem(status: ImageCleanupStatus) {
    imageCleanupStatusFromSystem = status
    val source = when (status) {
        ImageCleanupStatus.DELETED -> "原截图清理：已移入系统回收站"
        ImageCleanupStatus.USER_KEPT -> "原截图清理：已保留原图"
        ImageCleanupStatus.NOT_SUPPORTED -> "原截图清理：当前来源不支持移入回收站"
        ImageCleanupStatus.FAILED -> "原截图清理：系统确认未完成"
        else -> return
    }
    saveSnapshot(this, loadSavedItemOrFallback(), source)
}

fun MainActivity.loadSavedItemOrFallback(): ShikeItem =
    loadInitialSelection(this, null).item

fun MainActivity.requestDeleteSourceImage(sourceMediaStoreUri: String?) {
    when (val request = SourceImageCleanupManager(this).requestTrash(sourceMediaStoreUri)) {
        is SourceImageCleanupRequest.SystemTrashConfirmation -> {
            pendingDeleteSourceUri = sourceMediaStoreUri
            handleImageCleanupStatusFromApp(ImageCleanupStatus.DELETE_REQUESTED)
            deleteScreenshotLauncher.launch(
                androidx.activity.result.IntentSenderRequest.Builder(request.intentSender).build(),
            )
        }
        is SourceImageCleanupRequest.NotSupported -> {
            handleImageCleanupStatusFromSystem(request.status)
        }
    }
}
