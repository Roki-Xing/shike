package cn.shike.app.ui

import android.graphics.Bitmap
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawing
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import cn.shike.app.data.ImageCleanupStatus
import cn.shike.app.data.InboxItemEntity
import cn.shike.app.data.ScreenshotCandidate
import cn.shike.app.domain.ShikeItem
import cn.shike.app.system.VisibleScreenCapturePrompt

@Composable
fun ShikeMainScreen(
    selected: ShikeItem,
    todayAgendaState: TodayAgendaState,
    executionResults: List<ExecutionResult>,
    isConfirmed: Boolean,
    captureSource: String,
    capturedBitmap: Bitmap?,
    modelStatus: String,
    ocrDraft: String,
    onOcrDraftChange: (String) -> Unit,
    backendUrl: String,
    inboxHistory: List<InboxItemEntity>,
    onBackendUrlChange: (String) -> Unit,
    onSaveBackendUrl: () -> Unit,
    onGallery: () -> Unit,
    onCamera: () -> Unit,
    onManualInput: () -> Unit,
    onBackendCourse: () -> Unit,
    onBackendEvent: () -> Unit,
    onCourse: () -> Unit,
    onEvent: () -> Unit,
    cloudEnhancedEnabled: Boolean,
    onCloudEnhancedChange: (Boolean) -> Unit,
    localMultimodalStatus: LocalMultimodalStatus,
    onLocalMultimodalPreferenceChange: (LocalMultimodalPreference) -> Unit,
    screenshotAssistEnabled: Boolean,
    onScreenshotAssistChange: (Boolean) -> Unit,
    onboardingDismissed: Boolean,
    onDismissOnboarding: () -> Unit,
    onEnableScreenshotAssistFromOnboarding: () -> Unit,
    pendingScreenshotCandidate: ScreenshotCandidate?,
    onImportScreenshotCandidate: (ScreenshotCandidate) -> Unit,
    onIgnoreScreenshotCandidate: () -> Unit,
    visibleScreenCapturePrompt: VisibleScreenCapturePrompt?,
    onImportVisibleScreenCapture: () -> Unit,
    onDismissVisibleScreenCapture: () -> Unit,
    onClearLocalData: () -> Unit,
    onReviewed: (ShikeItem) -> Unit,
    sourceImageCleanupStatus: ImageCleanupStatus,
    selectedSourceMediaStoreUri: String?,
    onDeleteSourceImage: () -> Unit,
    onKeepSourceImage: () -> Unit,
    onAddCalendar: (ShikeItem) -> Unit,
    onReminder: (ShikeItem) -> Unit,
    onOpenMap: (ShikeItem) -> Unit,
) {
    var selectedSection by remember {
        mutableStateOf(ShikeMainSection.Home)
    }
    var developerModeState by remember { mutableStateOf(DeveloperModeState()) }

    Scaffold(
        modifier = Modifier
            .fillMaxSize()
            .background(ShikeColors.Surface),
        containerColor = ShikeColors.Surface,
        contentWindowInsets = WindowInsets.safeDrawing,
        bottomBar = {
            BottomNavBar(
                selectedSection = selectedSection,
                onSelected = { selectedSection = it },
                modifier = Modifier
                    .fillMaxWidth()
                    .navigationBarsPadding()
                    .padding(horizontal = 14.dp, vertical = 8.dp),
            )
        },
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(ShikeColors.Surface)
                .verticalScroll(rememberScrollState())
                .padding(padding)
                .padding(horizontal = 14.dp, vertical = 12.dp),
            verticalArrangement = ShikeSpacing.Screen,
        ) {
            when (selectedSection) {
                ShikeMainSection.Home -> HomeRouteContent(
                    selected, todayAgendaState, modelStatus,
                    pendingScreenshotCandidate, visibleScreenCapturePrompt, onboardingDismissed,
                    onGallery, onManualInput,
                    onDismissOnboarding, onEnableScreenshotAssistFromOnboarding,
                    onImportScreenshotCandidate, onIgnoreScreenshotCandidate,
                    onImportVisibleScreenCapture, onDismissVisibleScreenCapture,
                )
                ShikeMainSection.Import -> ImportRouteContent(
                    selected, executionResults, isConfirmed, captureSource, capturedBitmap,
                    modelStatus, ocrDraft, cloudEnhancedEnabled, pendingScreenshotCandidate,
                    visibleScreenCapturePrompt, sourceImageCleanupStatus, selectedSourceMediaStoreUri,
                    onOcrDraftChange, onGallery, onCamera, onManualInput, onBackendCourse,
                    onBackendEvent, onImportScreenshotCandidate, onIgnoreScreenshotCandidate,
                    onImportVisibleScreenCapture, onDismissVisibleScreenCapture, onReviewed,
                    onDeleteSourceImage, onKeepSourceImage, onAddCalendar, onReminder, onOpenMap,
                )
                ShikeMainSection.Inbox -> InboxScreen(selected, captureSource, executionResults, inboxHistory)
                ShikeMainSection.Settings -> PrivacySettingsScreen(
                    cloudEnhancedEnabled = cloudEnhancedEnabled,
                    onCloudEnhancedChange = onCloudEnhancedChange,
                    localMultimodalStatus = localMultimodalStatus,
                    onLocalMultimodalPreferenceChange = onLocalMultimodalPreferenceChange,
                    screenshotAssistEnabled = screenshotAssistEnabled,
                    onScreenshotAssistChange = onScreenshotAssistChange,
                    onClearLocalData = onClearLocalData,
                    developerModeState = developerModeState,
                    onVersionTap = {
                        val result = developerModeStateAfterVersionTap(developerModeState)
                        developerModeState = result.state
                        selectedSection = result.targetSection
                    },
                )
                ShikeMainSection.Debug -> DebugDemoScreen(
                    backendUrl = backendUrl,
                    onBackendUrlChange = onBackendUrlChange,
                    onSaveBackendUrl = onSaveBackendUrl,
                    onCourse = onCourse,
                    onEvent = onEvent,
                    localMultimodalStatus = localMultimodalStatus,
                )
            }
            Spacer(Modifier.height(112.dp))
        }
    }
}
