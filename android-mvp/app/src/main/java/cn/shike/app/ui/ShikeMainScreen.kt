package cn.shike.app.ui

import android.graphics.Bitmap
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import cn.shike.app.data.InboxItemEntity
import cn.shike.app.domain.ShikeItem

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
    onClearLocalData: () -> Unit,
    onReviewed: (ShikeItem) -> Unit,
    onAddCalendar: (ShikeItem) -> Unit,
    onReminder: (ShikeItem) -> Unit,
    onOpenMap: (ShikeItem) -> Unit,
) {
    var selectedSection by remember { mutableStateOf(ShikeMainSection.Home) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(ShikeColors.Surface)
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 14.dp, vertical = 12.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        when (selectedSection) {
            ShikeMainSection.Home -> HomeActionScreen(
                selected = selected,
                todayAgendaState = todayAgendaState,
                isConfirmed = isConfirmed,
                onGallery = onGallery,
                onCamera = onCamera,
                onManualInput = onManualInput,
                onAddCalendar = onAddCalendar,
                onReminder = onReminder,
                onOpenMap = onOpenMap,
            )
            ShikeMainSection.Import -> {
                CaptureHubScreen(
                    captureSource = captureSource,
                    capturedBitmap = capturedBitmap,
                    modelStatus = modelStatus,
                    ocrDraft = ocrDraft,
                    onOcrDraftChange = onOcrDraftChange,
                    cloudEnhancedEnabled = cloudEnhancedEnabled,
                    onGallery = onGallery,
                    onCamera = onCamera,
                    onManualInput = onManualInput,
                    onBackendCourse = onBackendCourse,
                    onBackendEvent = onBackendEvent,
                )
                ParseConfirmScreen(selected, onReviewed = onReviewed)
                ActionPlanScreen(selected, isConfirmed, executionResults, onAddCalendar, onReminder, onOpenMap)
            }
            ShikeMainSection.Inbox -> InboxScreen(selected, captureSource, executionResults, inboxHistory)
            ShikeMainSection.Settings -> PrivacySettingsScreen(
                cloudEnhancedEnabled = cloudEnhancedEnabled,
                onCloudEnhancedChange = onCloudEnhancedChange,
                onClearLocalData = onClearLocalData,
                backendUrl = backendUrl,
                onBackendUrlChange = onBackendUrlChange,
                onSaveBackendUrl = onSaveBackendUrl,
            )
            ShikeMainSection.Debug -> DebugDemoScreen(
                backendUrl = backendUrl,
                onBackendUrlChange = onBackendUrlChange,
                onSaveBackendUrl = onSaveBackendUrl,
                onCourse = onCourse,
                onEvent = onEvent,
            )
        }
        BottomNavBar(
            selectedSection = selectedSection,
            onSelected = { selectedSection = it },
        )
    }
}
