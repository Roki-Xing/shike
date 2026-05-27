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
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
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
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFFF3F8F7))
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 14.dp, vertical = 12.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        SystemStatusRow()
        DashboardHeader()
        DateStrip()
        HomeAgendaList(
            item = selected,
            state = todayAgendaState,
            onGallery = onGallery,
            onCamera = onCamera,
            onManualInput = onManualInput,
        )
        ConfirmBanner(
            selected = selected,
            isConfirmed = isConfirmed,
            onAddCalendar = onAddCalendar,
            onReminder = onReminder,
            onOpenMap = onOpenMap,
        )
        TodaySummaryPanel()
        DemoRoutePanel()
        ImportPanel(
            captureSource = captureSource,
            capturedBitmap = capturedBitmap,
            modelStatus = modelStatus,
            ocrDraft = ocrDraft,
            onOcrDraftChange = onOcrDraftChange,
            backendUrl = backendUrl,
            onBackendUrlChange = onBackendUrlChange,
            onSaveBackendUrl = onSaveBackendUrl,
            cloudEnhancedEnabled = cloudEnhancedEnabled,
            onGallery = onGallery,
            onCamera = onCamera,
            onManualInput = onManualInput,
            onBackendCourse = onBackendCourse,
            onBackendEvent = onBackendEvent,
            onCourse = onCourse,
            onEvent = onEvent,
        )
        ParseConfirmPanel(selected, onReviewed = onReviewed)
        ActionPlannerPanel(selected, isConfirmed, executionResults, onAddCalendar, onReminder, onOpenMap)
        InboxPanel(selected, captureSource, executionResults)
        DeliveryReadinessPanel()
        PrivacyPanel(
            cloudEnhancedEnabled = cloudEnhancedEnabled,
            onCloudEnhancedChange = onCloudEnhancedChange,
            onClearLocalData = onClearLocalData,
        )
        BottomNavBar()
    }
}
