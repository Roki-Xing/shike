package cn.shike.app

import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import cn.shike.app.data.loadBackendBaseUrl
import cn.shike.app.data.loadInitialSelection
import cn.shike.app.data.loadSavedInboxHistory
import cn.shike.app.data.saveBackendBaseUrl
import cn.shike.app.data.saveSnapshot

fun MainActivity.installShikeContent(sharedText: String?) {
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
                    onAddCalendar = { item -> openCalendarInsert(item) },
                    onReminder = { item -> requestReminder(item) },
                    onOpenMap = { item -> openMap(item) },
                    pendingScreenshotCandidate = pendingScreenshotCandidate,
                    onImportScreenshotCandidate = ::clearPendingScreenshotCandidate,
                    screenshotAssistEnabled = screenshotAssistEnabled,
                    onScreenshotAssistEnabledChange = ::updateScreenshotAssistEnabled,
                    onboardingDismissed = permissionOnboardingDismissed,
                    onDismissOnboarding = ::dismissPermissionOnboarding,
                    onEnableScreenshotAssistFromOnboarding = ::enableScreenshotAssistFromOnboarding,
                    onDeleteSourceImage = ::requestDeleteSourceImage,
                    onBuildImagePayload = ::buildBackendImagePayloadFromUri,
                    onBuildBitmapPayload = ::buildBackendImagePayloadFromBitmap,
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
