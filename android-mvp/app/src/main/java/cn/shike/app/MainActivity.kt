package cn.shike.app

import android.Manifest
import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import androidx.activity.ComponentActivity
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import cn.shike.app.data.ImageCleanupStatus
import cn.shike.app.data.ScreenshotCandidate
import cn.shike.app.data.loadPermissionOnboardingDismissed
import cn.shike.app.data.loadScreenshotAssistEnabled
import cn.shike.app.domain.ShikeItem
import cn.shike.app.system.createReminderNotificationChannel
import cn.shike.app.system.createScreenshotAssistNotificationChannel
import cn.shike.app.system.ScreenCaptureCallbackHelper
import cn.shike.app.system.VisibleScreenCapturePrompt
import cn.shike.app.system.restoreScheduledReminder

class MainActivity : ComponentActivity() {
    internal var pendingReminderItem: ShikeItem? = null
    private val mainHandler = Handler(Looper.getMainLooper())
    internal val screenshotAssistController by lazy {
        ScreenshotAssistController(
            activity = this,
            handler = mainHandler,
            onCandidateVisible = { candidate -> pendingScreenshotCandidate = candidate },
        )
    }
    internal var pendingDeleteSourceUri: String? = null
    private val screenCaptureCallbackHelper by lazy { ScreenCaptureCallbackHelper(this, ::showVisibleScreenCapturePrompt) }
    internal var pendingScreenshotCandidate by mutableStateOf<ScreenshotCandidate?>(null)
    internal var visibleScreenCapturePromptState by mutableStateOf<VisibleScreenCapturePrompt?>(null)
    internal var pendingSharedText by mutableStateOf<String?>(null)
    internal var screenshotAssistEnabled by mutableStateOf(false)
    internal var imageCleanupStatusFromSystem by mutableStateOf<ImageCleanupStatus?>(null)
    internal var permissionOnboardingDismissed by mutableStateOf(false)

    internal val notificationPermission = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted ->
        handleNotificationPermissionResult(granted)
    }

    internal val screenshotNotificationPermission = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) {
        registerScreenshotObserverIfAllowed()
    }

    internal val screenshotMediaPermission = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted -> handleScreenshotMediaPermissionResult(granted) }

    internal val deleteScreenshotLauncher = registerForActivityResult(
        ActivityResultContracts.StartIntentSenderForResult()
    ) { result ->
        val nextStatus = if (result.resultCode == RESULT_OK) {
            ImageCleanupStatus.DELETED
        } else {
            ImageCleanupStatus.FAILED
        }
        handleImageCleanupStatusFromSystem(nextStatus)
        pendingDeleteSourceUri = null
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
        enableEdgeToEdge()
        createReminderNotificationChannel(this)
        createScreenshotAssistNotificationChannel(this)
        restoreScheduledReminder(this)
        consumeScreenshotImportIntent(intent)
        consumeSharedImageIntent(intent)
        val sharedText = sharedTextFromIntent(intent)
        screenshotAssistEnabled = loadScreenshotAssistEnabled(this)
        permissionOnboardingDismissed = loadPermissionOnboardingDismissed(this)
        registerScreenshotObserverIfAllowed()
        installShikeContent(sharedText)
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        consumeScreenshotImportIntent(intent)
        consumeSharedImageIntent(intent)
        pendingSharedText = sharedTextFromIntent(intent)
    }

    override fun onStart() {
        super.onStart()
        screenCaptureCallbackHelper.register()
    }

    override fun onStop() {
        screenCaptureCallbackHelper.unregister()
        super.onStop()
    }

    override fun onDestroy() {
        unregisterScreenshotObserver()
        super.onDestroy()
    }
}
