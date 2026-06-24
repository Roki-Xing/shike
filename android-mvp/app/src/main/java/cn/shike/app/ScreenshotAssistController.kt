package cn.shike.app

import android.Manifest
import android.os.Handler
import cn.shike.app.data.ScreenshotCandidate
import cn.shike.app.data.saveScreenshotAssistEnabled
import cn.shike.app.system.canPostScreenshotAssistNotification
import cn.shike.app.system.hasScreenshotMediaPermission
import cn.shike.app.system.startScreenshotAssistService
import cn.shike.app.system.stopScreenshotAssistService

class ScreenshotAssistController(
    private val activity: MainActivity,
    @Suppress("UNUSED_PARAMETER")
    private val handler: Handler,
    @Suppress("UNUSED_PARAMETER")
    private val onCandidateVisible: (ScreenshotCandidate) -> Unit,
) {
    fun updateEnabled(enabled: Boolean) {
        activity.screenshotAssistEnabled = enabled
        saveScreenshotAssistEnabled(activity, enabled)
        if (enabled) {
            requestPermissions()
            registerIfAllowed()
        } else {
            unregister()
            activity.handleScreenshotAssistServiceRunningChanged(false)
            stopScreenshotAssistService(activity)
        }
    }

    fun requestPermissions() {
        if (!hasScreenshotMediaPermission(activity)) {
            val permission = if (android.os.Build.VERSION.SDK_INT >= 33) {
                Manifest.permission.READ_MEDIA_IMAGES
            } else {
                Manifest.permission.READ_EXTERNAL_STORAGE
            }
            activity.screenshotMediaPermission.launch(permission)
            return
        }
        requestNotificationPermissionIfNeeded()
    }

    fun requestNotificationPermissionIfNeeded() {
        if (!canPostScreenshotAssistNotification(activity)) {
            activity.screenshotNotificationPermission.launch(Manifest.permission.POST_NOTIFICATIONS)
        }
    }

    fun registerIfAllowed() {
        if (activity.screenshotAssistEnabled && hasScreenshotMediaPermission(activity)) {
            if (canPostScreenshotAssistNotification(activity)) {
                startScreenshotAssistService(activity)
                activity.handleScreenshotAssistServiceRunningChanged(true)
            } else {
                activity.handleScreenshotAssistServiceRunningChanged(false)
            }
        }
    }

    fun register() {
        registerIfAllowed()
    }

    fun unregister() {
        // Activity no longer owns a MediaStore observer; the service keeps running until explicitly disabled.
    }
}
