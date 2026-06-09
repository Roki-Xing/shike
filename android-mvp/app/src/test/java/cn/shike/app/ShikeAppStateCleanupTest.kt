package cn.shike.app

import cn.shike.app.data.BackendAnalysisOutcome
import cn.shike.app.data.DEFAULT_BACKEND_BASE_URL
import cn.shike.app.data.ImageCleanupStatus
import cn.shike.app.data.InitialTodayState
import cn.shike.app.data.sampleCourse
import cn.shike.app.domain.ShikeItem
import org.junit.Assert.assertEquals
import org.junit.Test

class ShikeAppStateCleanupTest {
    @Test
    fun applyBackendOutcome_preservesSourceImageCleanupState() {
        val state = cleanupState()
        val persisted = mutableListOf<Pair<ShikeItem, String>>()
        val sourceUri = "content://media/external/images/media/520"

        state.applyGalleryImage(sourceUri) { item, source -> persisted += item to source }
        state.applyBackendOutcome(englishClassOutcome()) { item, source -> persisted += item to source }

        assertEquals(sourceUri, state.selectedSourceMediaStoreUri)
        assertEquals(ImageCleanupStatus.NOT_REQUESTED, state.sourceImageCleanupStatus)
        assertEquals("英语口语课", state.selected.title)
    }

    @Test
    fun updateReviewedItem_preservesSourceImageCleanupStateAfterConfirmation() {
        val state = cleanupState()
        val persisted = mutableListOf<Pair<ShikeItem, String>>()
        val sourceUri = "content://media/external/images/media/303"

        state.applyGalleryImage(sourceUri) { item, source -> persisted += item to source }
        state.updateReviewedItem(state.selected.copy(title = "高数课", status = "待确认")) { item, source ->
            persisted += item to source
        }

        assertEquals(sourceUri, state.selectedSourceMediaStoreUri)
        assertEquals(ImageCleanupStatus.NOT_REQUESTED, state.sourceImageCleanupStatus)
        assertEquals("已安排", state.selected.status)
    }

    private fun cleanupState(): ShikeAppState =
        ShikeAppState(
            initialItem = sampleCourse(),
            initialCaptureSource = "今日行动台空状态",
            initialTodayState = InitialTodayState.Empty,
            initialBackendUrl = DEFAULT_BACKEND_BASE_URL,
            initialInboxHistory = emptyList(),
        )

    private fun englishClassOutcome(): BackendAnalysisOutcome =
        BackendAnalysisOutcome(
            item = sampleCourse().copy(
                title = "英语口语课",
                scene = "课程通知",
                time = "明天 09:00",
                location = "E520",
                status = "待确认",
                rawText = "明天早上九点上英语口语教室E520",
            ),
            source = "云端图片解析：课程通知",
            statusMessage = "云端图片解析完成",
        )
}
