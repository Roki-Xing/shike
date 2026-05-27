package cn.shike.app

import android.Manifest
import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import cn.shike.app.data.loadBackendBaseUrl
import cn.shike.app.data.loadInitialSelection
import cn.shike.app.data.clearInboxSnapshot
import cn.shike.app.data.clearBackendBaseUrl
import cn.shike.app.data.saveBackendBaseUrl
import cn.shike.app.data.saveSnapshot
import cn.shike.app.domain.ShikeItem
import cn.shike.app.system.buildCalendarInsertIntent
import cn.shike.app.system.buildMapIntent
import cn.shike.app.system.canPostReminderNotification
import cn.shike.app.system.cancelScheduledReminder
import cn.shike.app.system.copyMapLocationFallback
import cn.shike.app.system.createReminderNotificationChannel
import cn.shike.app.system.restoreScheduledReminder
import cn.shike.app.system.scheduleReminder
import cn.shike.app.system.startSystemActivitySafely

class MainActivity : ComponentActivity() {
    private var pendingReminderItem: ShikeItem? = null

    private val notificationPermission = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted ->
        handleNotificationPermissionResult(granted)
    }

    private fun handleNotificationPermissionResult(granted: Boolean) {
        pendingReminderItem?.let { item ->
            if (granted) {
                saveScheduledReminder(item)
            } else {
                saveReminderPermissionFallback(item)
            }
        }
        pendingReminderItem = null
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        createReminderNotificationChannel(this)
        restoreScheduledReminder(this)
        val sharedText = intent?.takeIf { it.action == Intent.ACTION_SEND }
            ?.getStringExtra(Intent.EXTRA_TEXT)
        setContent {
            MaterialTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    val initialSelection = loadInitialSelection(this, sharedText)
                    ShikeApp(
                        initialItem = initialSelection.item,
                        initialCaptureSource = initialSelection.captureSource,
                        initialTodayState = initialSelection.todayState,
                        initialBackendUrl = loadBackendBaseUrl(this),
                        onPersist = { item, source -> saveSnapshot(this, item, source) },
                        onSaveBackendUrl = { url -> saveBackendBaseUrl(this, url) },
                        onClearLocalData = ::clearAllLocalData,
                        onAddCalendar = ::openCalendarInsert,
                        onReminder = ::requestReminder,
                        onOpenMap = ::openMap,
                    )
                }
            }
        }
    }

    private fun clearAllLocalData() {
        cancelScheduledReminder(this)
        clearInboxSnapshot(this)
        clearBackendBaseUrl(this)
    }

    private fun openCalendarInsert(item: ShikeItem) {
        startSystemActivitySafely(
            context = this,
            intent = buildCalendarInsertIntent(item),
            item = item,
            fallbackSource = "系统日历不可用，已保留行动卡，稍后可手动添加日程。",
            onFallback = ::saveSystemActionFallback,
        )
    }

    private fun requestReminder(item: ShikeItem) {
        if (canPostReminderNotification(this)) {
            saveScheduledReminder(item)
        } else {
            requestNotificationPermissionFor(item)
        }
    }

    private fun requestNotificationPermissionFor(item: ShikeItem) {
        pendingReminderItem = item
        notificationPermission.launch(Manifest.permission.POST_NOTIFICATIONS)
    }

    private fun saveReminderPermissionFallback(item: ShikeItem) {
        saveSnapshot(this, item, reminderPermissionFallbackCopyFor(item).source)
    }

    private fun saveScheduledReminder(item: ShikeItem) {
        saveSnapshot(this, item, scheduleReminder(this, item))
    }

    private fun openMap(item: ShikeItem) {
        startSystemActivitySafely(
            context = this,
            intent = buildMapIntent(item),
            item = item,
            fallbackSource = "地图应用不可用，已保留地点：${item.location}",
            onFallback = ::saveMapFallback,
        )
    }

    private fun saveMapFallback(item: ShikeItem, source: String) {
        saveSystemActionFallback(item, "$source；${copyMapLocationFallback(this, item)}")
    }

    private fun saveSystemActionFallback(item: ShikeItem, source: String) {
        saveSnapshot(this, item, source)
    }

}
