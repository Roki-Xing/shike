package cn.shike.app

import cn.shike.app.ui.AnalysisUiState
import cn.shike.app.ui.ImportFlowState
import cn.shike.app.ui.ImportRouteStage
import cn.shike.app.ui.analysisUiStateFor
import cn.shike.app.ui.importFlowStageFor
import cn.shike.app.ui.importFlowStateFor
import cn.shike.app.ui.TodayAgendaState
import cn.shike.app.data.sampleCourse
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Test

class AnalysisUiStateTest {
    @Test
    fun analysisUiStateFor_keepsFlowLogicAwayFromDisplayCopy() {
        val analyzing = AnalysisUiState.Analyzing("正在把截图变成行动卡")

        assertEquals(
            ImportRouteStage.Analyzing,
            importFlowStageFor(analyzing, selectedStatus = "待确认", isConfirmed = false),
        )
        assertEquals(
            ImportRouteStage.Reviewing,
            importFlowStageFor(AnalysisUiState.Reviewing, selectedStatus = "待确认", isConfirmed = false),
        )
    }

    @Test
    fun analysisUiStateFor_mapsLegacyStatusAtTheBoundaryOnly() {
        val failed = analysisUiStateFor("AI 暂时没识别成功，截图已保存为待确认")

        assertEquals(AnalysisUiState.Failed::class, failed::class)
        assertFalse(failed is AnalysisUiState.Analyzing)
    }

    @Test
    fun homeFlowState_usesAnalysisUiStateInsteadOfParsingModelCopy() {
        val state = importFlowStateFor(
            selected = sampleCourse().copy(status = "待确认"),
            todayAgendaState = TodayAgendaState.Ready,
            analysisUiState = AnalysisUiState.Analyzing("后台处理中，文案可调整"),
            pendingScreenshotCandidate = null,
            visibleScreenCapturePrompt = null,
        )

        assertEquals(ImportFlowState.Analyzing, state)
    }
}
