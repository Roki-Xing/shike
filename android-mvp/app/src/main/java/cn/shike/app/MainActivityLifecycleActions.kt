package cn.shike.app

import android.content.Intent
import cn.shike.app.data.ImageCleanupStatus
import cn.shike.app.data.clearBackendBaseUrl
import cn.shike.app.data.clearInboxSnapshot
import cn.shike.app.data.clearScreenshotAssistPreference
import cn.shike.app.data.savePermissionOnboardingDismissed
import cn.shike.app.domain.ShikeItem
import cn.shike.app.system.cancelScheduledReminder
import cn.shike.app.system.startScreenshotAssistService
import cn.shike.app.system.stopScreenshotAssistService
import cn.shike.app.system.visibleScreenCapturePrompt

fun MainActivity.handleNotificationPermissionResult(granted: Boolean) {
    pendingReminderItem?.let { item: ShikeItem ->
        if (granted) {
            saveScheduledReminder(item)
        } else {
            saveReminderPermissionFallback(item)
        }
    }
    pendingReminderItem = null
}

fun MainActivity.clearAllLocalData() {
    cancelScheduledReminder(this)
    clearInboxSnapshot(this)
    clearBackendBaseUrl(this)
    clearScreenshotAssistPreference(this)
    screenshotAssistEnabled = false
    unregisterScreenshotObserver()
    stopScreenshotAssistService(this)
}

fun MainActivity.dismissPermissionOnboarding() {
    permissionOnboardingDismissed = true
    savePermissionOnboardingDismissed(this, true)
}

fun MainActivity.enableScreenshotAssistFromOnboarding() {
    dismissPermissionOnboarding()
    updateScreenshotAssistEnabled(true)
}

fun MainActivity.consumeScreenshotImportIntent(intent: Intent?) {
    pendingScreenshotCandidate = screenshotCandidateFromImportIntent(intent, System.currentTimeMillis())
        ?: pendingScreenshotCandidate
}

fun MainActivity.consumeSharedImageIntent(intent: Intent?) {
    if (intent?.action != Intent.ACTION_SEND || !intent.type.orEmpty().startsWith("image/")) return
    val uri = sharedImageUriFromIntent(intent) ?: return
    try {
        contentResolver.takePersistableUriPermission(uri, Intent.FLAG_GRANT_READ_URI_PERMISSION)
    } catch (_: SecurityException) {
        // Share-sheet URIs may be one-shot grants; decoding remains user-triggered.
    }
    pendingScreenshotCandidate = screenshotCandidateFromSharedImage(uri, System.currentTimeMillis())
}

fun MainActivity.clearPendingSharedText() {
    pendingSharedText = null
}

fun MainActivity.clearPendingScreenshotCandidate() {
    pendingScreenshotCandidate = null
}

fun MainActivity.showVisibleScreenCapturePrompt() {
    visibleScreenCapturePromptState = visibleScreenCapturePrompt()
}

fun MainActivity.clearVisibleScreenCapturePrompt() {
    visibleScreenCapturePromptState = null
}

fun MainActivity.clearImageCleanupStatusFromSystem() {
    imageCleanupStatusFromSystem = null
}

fun MainActivity.updateScreenshotAssistEnabled(enabled: Boolean) {
    screenshotAssistController.updateEnabled(enabled)
}

fun MainActivity.requestScreenshotNotificationPermissionIfNeeded() {
    screenshotAssistController.requestNotificationPermissionIfNeeded()
}

fun MainActivity.registerScreenshotObserverIfAllowed() {
    screenshotAssistController.registerIfAllowed()
}

fun MainActivity.registerScreenshotObserver() {
    screenshotAssistController.register()
}

fun MainActivity.unregisterScreenshotObserver() {
    screenshotAssistController.unregister()
}

fun MainActivity.handleScreenshotMediaPermissionResult(granted: Boolean) {
    if (granted) {
        requestScreenshotNotificationPermissionIfNeeded()
        registerScreenshotObserverIfAllowed()
        startScreenshotAssistService(this)
    } else {
        screenshotAssistEnabled = false
        unregisterScreenshotObserver()
        stopScreenshotAssistService(this)
    }
}
