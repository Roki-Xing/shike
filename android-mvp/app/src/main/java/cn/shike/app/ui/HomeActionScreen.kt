package cn.shike.app.ui

import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import cn.shike.app.data.ScreenshotCandidate
import cn.shike.app.domain.ShikeItem
import cn.shike.app.system.VisibleScreenCapturePrompt

enum class ImportFlowState {
    Idle,
    Detected,
    Analyzing,
    Reviewing,
    Planning,
    Completed,
}

fun importFlowStateFor(
    selected: ShikeItem,
    todayAgendaState: TodayAgendaState,
    modelStatus: String,
    pendingScreenshotCandidate: ScreenshotCandidate?,
    visibleScreenCapturePrompt: VisibleScreenCapturePrompt?,
): ImportFlowState =
    importFlowStateFor(
        selected = selected,
        todayAgendaState = todayAgendaState,
        analysisUiState = analysisUiStateFor(modelStatus),
        pendingScreenshotCandidate = pendingScreenshotCandidate,
        visibleScreenCapturePrompt = visibleScreenCapturePrompt,
    )

fun importFlowStateFor(
    selected: ShikeItem,
    todayAgendaState: TodayAgendaState,
    analysisUiState: AnalysisUiState,
    pendingScreenshotCandidate: ScreenshotCandidate?,
    visibleScreenCapturePrompt: VisibleScreenCapturePrompt?,
): ImportFlowState =
    when {
        pendingScreenshotCandidate != null || visibleScreenCapturePrompt != null -> ImportFlowState.Detected
        analysisUiState is AnalysisUiState.Analyzing -> ImportFlowState.Analyzing
        selected.status == "待确认" -> ImportFlowState.Reviewing
        selected.status == "已安排" -> ImportFlowState.Completed
        todayAgendaState == TodayAgendaState.Empty -> ImportFlowState.Idle
        else -> ImportFlowState.Reviewing
    }

@Composable
fun HomeActionScreen(
    selected: ShikeItem,
    todayAgendaState: TodayAgendaState,
    onGallery: () -> Unit,
    onCamera: () -> Unit,
    onManualInput: () -> Unit,
    onOpenCurrentAction: () -> Unit,
    onboardingDismissed: Boolean,
    onDismissOnboarding: () -> Unit,
    onEnableScreenshotAssistFromOnboarding: () -> Unit,
    analysisUiState: AnalysisUiState,
    pendingScreenshotCandidate: ScreenshotCandidate?,
    onImportScreenshotCandidate: (ScreenshotCandidate) -> Unit,
    onIgnoreScreenshotCandidate: () -> Unit,
    visibleScreenCapturePrompt: VisibleScreenCapturePrompt?,
    onImportVisibleScreenCapture: () -> Unit,
    onDismissVisibleScreenCapture: () -> Unit,
) {
    var showScreenshotAssistGuide by remember { mutableStateOf(false) }
    val requestScreenshotAssist = {
        if (onboardingDismissed) {
            onEnableScreenshotAssistFromOnboarding()
        } else {
            showScreenshotAssistGuide = true
        }
    }
    val flowState = importFlowStateFor(
        selected = selected,
        todayAgendaState = todayAgendaState,
        analysisUiState = analysisUiState,
        pendingScreenshotCandidate = pendingScreenshotCandidate,
        visibleScreenCapturePrompt = visibleScreenCapturePrompt,
    )
    val productHomeState = productHomeStateFor(selected, todayAgendaState)
    if (productHomeState == ProductHomeState.Empty && flowState == ImportFlowState.Idle) {
        ProductHomeHero(
            onGallery = onGallery,
            onCamera = onCamera,
            onManualInput = onManualInput,
        )
    } else {
        ProductHomeMiniHeader(selected, todayAgendaState)
    }
    when (flowState) {
        ImportFlowState.Idle -> FocusedHomeCard(
            title = "今天还没有待处理截图",
            body = "把截图交给拾刻，生成第一张行动卡。",
            primaryLabel = "开启截图助手",
            secondaryLabel = "手动输入",
            onPrimary = requestScreenshotAssist,
            onSecondary = onManualInput,
        )
        ImportFlowState.Detected -> ScreenshotPromptEntry(
            pendingScreenshotCandidate = pendingScreenshotCandidate,
            onImportScreenshotCandidate = onImportScreenshotCandidate,
            onIgnoreScreenshotCandidate = onIgnoreScreenshotCandidate,
            visibleScreenCapturePrompt = visibleScreenCapturePrompt,
            onImportVisibleScreenCapture = onImportVisibleScreenCapture,
            onDismissVisibleScreenCapture = onDismissVisibleScreenCapture,
        )
        ImportFlowState.Analyzing -> FocusedHomeCard(
            title = "正在把截图变成行动卡",
            body = "读取截图文字、找时间地点，再生成待确认的行动卡。",
            primaryLabel = "查看导入",
            secondaryLabel = "手动输入",
            onPrimary = onGallery,
            onSecondary = onManualInput,
        )
        ImportFlowState.Reviewing, ImportFlowState.Planning -> FocusedActionReviewCard(
            item = selected,
            titlePrefix = "今天要处理",
            onPrimary = onOpenCurrentAction,
        )
        ImportFlowState.Completed -> {
            TodayFocusCard(
                selected = selected,
                todayAgendaState = todayAgendaState,
                onOpenCurrentAction = onOpenCurrentAction,
            )
            FocusedActionReviewCard(
                item = selected,
                titlePrefix = "今晚要做",
                primaryLabel = "查看下一步",
                onPrimary = onOpenCurrentAction,
            )
        }
    }
    if (showScreenshotAssistGuide) {
        ScreenshotAssistGuideDialog(
            onEnableScreenshotAssist = {
                showScreenshotAssistGuide = false
                onEnableScreenshotAssistFromOnboarding()
            },
            onDismiss = {
                showScreenshotAssistGuide = false
                onDismissOnboarding()
            },
        )
    }
}

@Composable
private fun ScreenshotPromptEntry(
    pendingScreenshotCandidate: ScreenshotCandidate?,
    onImportScreenshotCandidate: (ScreenshotCandidate) -> Unit,
    onIgnoreScreenshotCandidate: () -> Unit,
    visibleScreenCapturePrompt: VisibleScreenCapturePrompt?,
    onImportVisibleScreenCapture: () -> Unit,
    onDismissVisibleScreenCapture: () -> Unit,
) {
    visibleScreenCapturePrompt?.let { prompt ->
        FocusedHomeCard(
            title = "检测到新截图",
            body = prompt.body,
            primaryLabel = "交给拾刻",
            secondaryLabel = "忽略",
            onPrimary = onImportVisibleScreenCapture,
            onSecondary = onDismissVisibleScreenCapture,
        )
    }
    pendingScreenshotCandidate?.let { candidate ->
        FocusedHomeCard(
            title = "检测到新截图",
            body = "可能包含课程、考试或截止事项。",
            primaryLabel = "交给拾刻",
            secondaryLabel = "忽略",
            onPrimary = { onImportScreenshotCandidate(candidate) },
            onSecondary = onIgnoreScreenshotCandidate,
        )
    }
}
