package cn.shike.app

import android.Manifest
import android.content.Intent
import android.graphics.Bitmap
import android.net.Uri
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import androidx.activity.result.IntentSenderRequest
import androidx.activity.ComponentActivity
import androidx.activity.enableEdgeToEdge
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import cn.shike.app.data.ImageCleanupStatus
import cn.shike.app.data.BackendImagePayload
import cn.shike.app.data.ImagePayloadPreprocessor
import cn.shike.app.data.ImagePreprocessSource
import cn.shike.app.data.ScreenshotCandidate
import cn.shike.app.data.clearScreenshotAssistPreference
import cn.shike.app.data.loadPermissionOnboardingDismissed
import cn.shike.app.data.loadBackendBaseUrl
import cn.shike.app.data.loadSavedInboxHistory
import cn.shike.app.data.loadInitialSelection
import cn.shike.app.data.loadScreenshotAssistEnabled
import cn.shike.app.data.savePermissionOnboardingDismissed
import cn.shike.app.data.saveScreenshotAssistEnabled
import cn.shike.app.data.shouldNotifyScreenshotCandidate
import cn.shike.app.data.clearInboxSnapshot
import cn.shike.app.data.clearBackendBaseUrl
import cn.shike.app.data.saveBackendBaseUrl
import cn.shike.app.data.saveSnapshot
import cn.shike.app.data.screenshotCandidateFromNotificationImport
import cn.shike.app.domain.ShikeItem
import cn.shike.app.system.buildCalendarInsertIntent
import cn.shike.app.system.buildMapIntent
import cn.shike.app.system.canPostReminderNotification
import cn.shike.app.system.canPostScreenshotAssistNotification
import cn.shike.app.system.cancelScheduledReminder
import cn.shike.app.system.copyMapLocationFallback
import cn.shike.app.system.createReminderNotificationChannel
import cn.shike.app.system.createScreenshotAssistNotificationChannel
import cn.shike.app.system.createScreenshotDeleteRequest
import cn.shike.app.system.hasScreenshotMediaPermission
import cn.shike.app.system.ACTION_IMPORT_SCREENSHOT
import cn.shike.app.system.EXTRA_SCREENSHOT_CREATED_AT_MILLIS
import cn.shike.app.system.EXTRA_SCREENSHOT_DISPLAY_NAME_DIGEST
import cn.shike.app.system.EXTRA_SCREENSHOT_HEIGHT
import cn.shike.app.system.EXTRA_SCREENSHOT_URI
import cn.shike.app.system.EXTRA_SCREENSHOT_WIDTH
import cn.shike.app.system.ScreenshotObserver
import cn.shike.app.system.ScreenCaptureCallbackHelper
import cn.shike.app.system.VisibleScreenCapturePrompt
import cn.shike.app.system.restoreScheduledReminder
import cn.shike.app.system.scheduleReminder
import cn.shike.app.system.showScreenshotDetectedNotification
import cn.shike.app.system.startSystemActivitySafely
import cn.shike.app.system.visibleScreenCapturePrompt

class MainActivity : ComponentActivity() {
    private var pendingReminderItem: ShikeItem? = null
    private val mainHandler = Handler(Looper.getMainLooper())
    private var screenshotObserver: ScreenshotObserver? = null
    private var observedScreenshotAssistEnabled = false
    private var pendingDeleteSourceUri: String? = null
    private var lastNotifiedScreenshotUri: String? = null
    private val screenCaptureCallbackHelper by lazy { ScreenCaptureCallbackHelper(this, ::showVisibleScreenCapturePrompt) }
    private var pendingScreenshotCandidate by mutableStateOf<ScreenshotCandidate?>(null)
    private var visibleScreenCapturePromptState by mutableStateOf<VisibleScreenCapturePrompt?>(null)
    private var pendingSharedText by mutableStateOf<String?>(null)
    private var screenshotAssistEnabled by mutableStateOf(false)
    private var imageCleanupStatusFromSystem by mutableStateOf<ImageCleanupStatus?>(null)
    private var permissionOnboardingDismissed by mutableStateOf(false)

    private val notificationPermission = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted ->
        handleNotificationPermissionResult(granted)
    }

    private val screenshotNotificationPermission = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) {
        registerScreenshotObserverIfAllowed()
    }

    private val screenshotMediaPermission = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted ->
        if (granted) {
            requestScreenshotNotificationPermissionIfNeeded()
            registerScreenshotObserverIfAllowed()
        } else {
            screenshotAssistEnabled = false
            unregisterScreenshotObserver()
        }
    }

    private val deleteScreenshotLauncher = registerForActivityResult(
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
        val sharedText = sharedTextFrom(intent)
        screenshotAssistEnabled = loadScreenshotAssistEnabled(this)
        permissionOnboardingDismissed = loadPermissionOnboardingDismissed(this)
        registerScreenshotObserverIfAllowed()
        setContent {
            MaterialTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    val initialSelection = loadInitialSelection(this, sharedText)
                    ShikeApp(
                        initialItem = initialSelection.item,
                        initialCaptureSource = initialSelection.captureSource,
                        initialTodayState = initialSelection.todayState,
                        initialBackendUrl = loadBackendBaseUrl(this),
                        initialInboxHistory = loadSavedInboxHistory(this),
                        onPersist = { item, source -> saveSnapshot(this, item, source) },
                        onSaveBackendUrl = { url -> saveBackendBaseUrl(this, url) },
                        onClearLocalData = ::clearAllLocalData,
                        onAddCalendar = ::openCalendarInsert,
                        onReminder = ::requestReminder,
                        onOpenMap = ::openMap,
                        pendingScreenshotCandidate = pendingScreenshotCandidate,
                        onImportScreenshotCandidate = ::clearPendingScreenshotCandidate,
                        screenshotAssistEnabled = screenshotAssistEnabled,
                        onScreenshotAssistEnabledChange = ::updateScreenshotAssistEnabled,
                        onboardingDismissed = permissionOnboardingDismissed,
                        onDismissOnboarding = ::dismissPermissionOnboarding,
                        onEnableScreenshotAssistFromOnboarding = ::enableScreenshotAssistFromOnboarding,
                        onDeleteSourceImage = ::requestDeleteSourceImage,
                        onBuildImagePayload = ::buildImagePayloadFromUri,
                        onBuildBitmapPayload = ::buildImagePayloadFromBitmap,
                        visibleScreenCapturePrompt = visibleScreenCapturePromptState,
                        onVisibleScreenCapturePromptConsumed = ::clearVisibleScreenCapturePrompt,
                        pendingSharedText = pendingSharedText,
                        onPendingSharedTextConsumed = ::clearPendingSharedText,
                        onImageCleanupStatusChange = ::handleImageCleanupStatusFromApp,
                        imageCleanupStatusFromSystem = imageCleanupStatusFromSystem,
                        onImageCleanupStatusConsumed = ::clearImageCleanupStatusFromSystem,
                    )
                }
            }
        }
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        consumeScreenshotImportIntent(intent)
        consumeSharedImageIntent(intent)
        pendingSharedText = sharedTextFrom(intent)
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

    private fun clearAllLocalData() {
        cancelScheduledReminder(this)
        clearInboxSnapshot(this)
        clearBackendBaseUrl(this)
        clearScreenshotAssistPreference(this)
        screenshotAssistEnabled = false
        unregisterScreenshotObserver()
    }

    private fun dismissPermissionOnboarding() {
        permissionOnboardingDismissed = true
        savePermissionOnboardingDismissed(this, true)
    }

    private fun enableScreenshotAssistFromOnboarding() {
        dismissPermissionOnboarding()
        updateScreenshotAssistEnabled(true)
    }

    private fun consumeScreenshotImportIntent(intent: Intent?) {
        if (intent?.action != ACTION_IMPORT_SCREENSHOT) {
            return
        }
        pendingScreenshotCandidate = screenshotCandidateFromNotificationImport(
            contentUri = intent.getStringExtra(EXTRA_SCREENSHOT_URI),
            createdAtMillis = intent.getLongExtra(EXTRA_SCREENSHOT_CREATED_AT_MILLIS, 0L),
            width = intent.getIntExtra(EXTRA_SCREENSHOT_WIDTH, 0),
            height = intent.getIntExtra(EXTRA_SCREENSHOT_HEIGHT, 0),
            displayNameDigest = intent.getStringExtra(EXTRA_SCREENSHOT_DISPLAY_NAME_DIGEST),
            nowMillis = System.currentTimeMillis(),
        )
    }

    private fun consumeSharedImageIntent(intent: Intent?) {
        if (intent?.action != Intent.ACTION_SEND || !intent.type.orEmpty().startsWith("image/")) {
            return
        }
        val uri = sharedImageUriFrom(intent) ?: return
        try {
            contentResolver.takePersistableUriPermission(uri, Intent.FLAG_GRANT_READ_URI_PERMISSION)
        } catch (_: SecurityException) {
            // Some share-sheet URIs are one-shot grants. Keep the import draft; decoding remains user-triggered.
        }
        pendingScreenshotCandidate = ScreenshotCandidate(
            contentUri = uri.toString(),
            createdAtMillis = System.currentTimeMillis(),
            width = 0,
            height = 0,
            displayNameDigest = uri.toString().hashCode().toUInt().toString(16),
            sourceLabel = "系统截图分享导入",
        )
    }

    private fun buildImagePayloadFromUri(uriText: String, sourceType: String): BackendImagePayload? {
        val uri = runCatching { Uri.parse(uriText) }.getOrNull() ?: return null
        val bytes = contentResolver.openInputStream(uri)?.use { stream ->
            stream.readBytes()
        } ?: return null
        return ImagePayloadPreprocessor.fromBytesWithThumbnail(
            bytes = bytes,
            source = imagePreprocessSourceFromBackendSource(sourceType),
            thumbnailCacheRoot = cacheDir,
        )?.payload
    }

    private fun buildImagePayloadFromBitmap(bitmap: Bitmap): BackendImagePayload? =
        ImagePayloadPreprocessor.fromBitmapWithThumbnail(
            bitmap = bitmap,
            thumbnailCacheRoot = cacheDir,
        )?.payload

    private fun imagePreprocessSourceFromBackendSource(sourceType: String): ImagePreprocessSource =
        when (sourceType) {
            "screenshot_share", "recent_screenshot_assist" -> ImagePreprocessSource.SCREENSHOT
            else -> ImagePreprocessSource.PHOTO_PICKER
        }

    private fun sharedImageUriFrom(intent: Intent): Uri? =
        if (android.os.Build.VERSION.SDK_INT >= 33) {
            intent.getParcelableExtra(Intent.EXTRA_STREAM, Uri::class.java)
        } else {
            @Suppress("DEPRECATION")
            intent.getParcelableExtra(Intent.EXTRA_STREAM) as? Uri
        }

    private fun sharedTextFrom(intent: Intent?): String? =
        intent
            ?.takeIf { it.action == Intent.ACTION_SEND && it.type.orEmpty().startsWith("text/") }
            ?.getStringExtra(Intent.EXTRA_TEXT)
            ?.takeIf { it.isNotBlank() }

    private fun clearPendingSharedText() {
        pendingSharedText = null
    }

    private fun updateScreenshotAssistEnabled(enabled: Boolean) {
        screenshotAssistEnabled = enabled
        saveScreenshotAssistEnabled(this, enabled)
        if (enabled) {
            requestScreenshotAssistPermissions()
            registerScreenshotObserverIfAllowed()
        } else {
            unregisterScreenshotObserver()
        }
    }

    private fun requestScreenshotAssistPermissions() {
        if (!hasScreenshotMediaPermission(this)) {
            val permission = if (android.os.Build.VERSION.SDK_INT >= 33) {
                Manifest.permission.READ_MEDIA_IMAGES
            } else {
                Manifest.permission.READ_EXTERNAL_STORAGE
            }
            screenshotMediaPermission.launch(permission)
            return
        }
        requestScreenshotNotificationPermissionIfNeeded()
    }

    private fun requestScreenshotNotificationPermissionIfNeeded() {
        if (!canPostScreenshotAssistNotification(this)) {
            screenshotNotificationPermission.launch(Manifest.permission.POST_NOTIFICATIONS)
        }
    }

    private fun registerScreenshotObserverIfAllowed() {
        if (screenshotAssistEnabled && hasScreenshotMediaPermission(this)) {
            registerScreenshotObserver()
        }
    }

    private fun registerScreenshotObserver() {
        if (observedScreenshotAssistEnabled) {
            return
        }
        screenshotObserver = ScreenshotObserver(
            resolver = contentResolver,
            handler = mainHandler,
            onCandidate = ::onScreenshotCandidate,
        ).also { observer ->
            observer.register()
            observedScreenshotAssistEnabled = true
        }
    }

    private fun unregisterScreenshotObserver() {
        screenshotObserver?.unregister()
        screenshotObserver = null
        observedScreenshotAssistEnabled = false
    }

    private fun onScreenshotCandidate(candidate: ScreenshotCandidate) {
        if (!shouldNotifyScreenshotCandidate(candidate, lastNotifiedScreenshotUri)) {
            return
        }
        lastNotifiedScreenshotUri = candidate.contentUri
        pendingScreenshotCandidate = candidate
        showScreenshotDetectedNotification(this, candidate)
    }

    private fun clearPendingScreenshotCandidate() {
        pendingScreenshotCandidate = null
    }

    private fun showVisibleScreenCapturePrompt() {
        visibleScreenCapturePromptState = visibleScreenCapturePrompt()
    }

    private fun clearVisibleScreenCapturePrompt() {
        visibleScreenCapturePromptState = null
    }

    private fun requestDeleteSourceImage(sourceMediaStoreUri: String?) {
        val sender = createScreenshotDeleteRequest(this, sourceMediaStoreUri)
        if (sender == null) {
            handleImageCleanupStatusFromSystem(ImageCleanupStatus.FAILED)
            return
        }
        pendingDeleteSourceUri = sourceMediaStoreUri
        handleImageCleanupStatusFromApp(ImageCleanupStatus.DELETE_REQUESTED)
        deleteScreenshotLauncher.launch(IntentSenderRequest.Builder(sender).build())
    }

    private fun handleImageCleanupStatusFromApp(status: ImageCleanupStatus) {
        if (status == ImageCleanupStatus.DELETE_REQUESTED) {
            saveSnapshot(this, loadSavedItemOrFallback(), "原截图清理：已请求系统确认")
        }
    }

    private fun handleImageCleanupStatusFromSystem(status: ImageCleanupStatus) {
        imageCleanupStatusFromSystem = status
        val source = when (status) {
            ImageCleanupStatus.DELETED -> "原截图清理：已移入系统回收站"
            ImageCleanupStatus.FAILED -> "原截图清理：系统确认未完成"
            else -> return
        }
        saveSnapshot(this, loadSavedItemOrFallback(), source)
    }

    private fun clearImageCleanupStatusFromSystem() {
        imageCleanupStatusFromSystem = null
    }

    private fun loadSavedItemOrFallback(): ShikeItem =
        loadInitialSelection(this, null).item

    private fun openCalendarInsert(item: ShikeItem) {
        startSystemActivitySafely(
            context = this,
            intent = buildCalendarInsertIntent(item),
            item = item,
            fallbackSource = "系统日历新增页不可用，已保留行动卡，稍后可手动添加日程。",
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
