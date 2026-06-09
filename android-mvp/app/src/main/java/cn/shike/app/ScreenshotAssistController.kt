package cn.shike.app

import android.Manifest
import android.os.Handler
import cn.shike.app.data.ScreenshotCandidate
import cn.shike.app.data.saveScreenshotAssistEnabled
import cn.shike.app.data.shouldNotifyScreenshotCandidate
import cn.shike.app.system.ScreenshotObserver
import cn.shike.app.system.canPostScreenshotAssistNotification
import cn.shike.app.system.hasScreenshotMediaPermission
import cn.shike.app.system.showScreenshotDetectedNotification
import cn.shike.app.system.startScreenshotAssistService
import cn.shike.app.system.stopScreenshotAssistService

class ScreenshotAssistController(
    private val activity: MainActivity,
    private val handler: Handler,
    private val onCandidateVisible: (ScreenshotCandidate) -> Unit,
) {
    private var observer: ScreenshotObserver? = null
    private var observed = false
    private var lastNotifiedScreenshotUri: String? = null

    fun updateEnabled(enabled: Boolean) {
        activity.screenshotAssistEnabled = enabled
        saveScreenshotAssistEnabled(activity, enabled)
        if (enabled) {
            requestPermissions()
            registerIfAllowed()
        } else {
            unregister()
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
            register()
            if (canPostScreenshotAssistNotification(activity)) {
                startScreenshotAssistService(activity)
            }
        }
    }

    fun register() {
        if (observed) return
        observer = ScreenshotObserver(
            resolver = activity.contentResolver,
            handler = handler,
            onCandidate = ::onScreenshotCandidate,
        ).also { screenshotObserver ->
            screenshotObserver.register()
            observed = true
        }
    }

    fun unregister() {
        observer?.unregister()
        observer = null
        observed = false
    }

    private fun onScreenshotCandidate(candidate: ScreenshotCandidate) {
        if (!shouldNotifyScreenshotCandidate(candidate, lastNotifiedScreenshotUri)) return
        lastNotifiedScreenshotUri = candidate.contentUri
        onCandidateVisible(candidate)
        showScreenshotDetectedNotification(activity, candidate)
    }
}
