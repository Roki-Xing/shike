package cn.shike.app

import cn.shike.app.data.sampleCourse
import cn.shike.app.data.sampleEvent
import cn.shike.app.domain.preparationItemsFrom
import cn.shike.app.domain.ShikeItem
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class ReviewActionsTest {
    @Test
    fun applyReviewedItemSelection_persistsConfirmedItemAndSource() {
        val persisted = mutableListOf<Pair<ShikeItem, String>>()
        val item = sampleEvent().copy(status = "待确认")

        val status = applyReviewedItemSelection(item) { savedItem, source ->
            persisted += savedItem to source
        }

        assertEquals("模型编排：用户已确认", status)
        assertEquals("已安排", persisted.single().first.status)
        assertEquals("AI应用分享会", persisted.single().first.title)
        assertEquals("用户确认修正：活动海报", persisted.single().second)
    }

    @Test
    fun applyReviewedItemSelection_persistsIgnoredItemAndSource() {
        val persisted = mutableListOf<Pair<ShikeItem, String>>()
        val item = sampleCourse().copy(status = "已忽略")

        val status = applyReviewedItemSelection(item) { savedItem, source ->
            persisted += savedItem to source
        }

        assertEquals("模型编排：用户已忽略", status)
        assertEquals(item, persisted.single().first)
        assertEquals("用户确认修正：课程通知", persisted.single().second)
    }

    @Test
    fun reviewedItemWithPreparationDraft_persistsPreparationAsStructuredEvidence() {
        val item = sampleCourse().copy(
            title = "高数A考试",
            rawText = "任务：高数A考试\n准备：带书",
        )

        val reviewed = reviewedItemWithPreparationDraft(
            item = item,
            title = "高数A考试",
            time = "今晚 21:00",
            location = "B336",
            status = "待确认",
            preparation = "带准考证、带2B铅笔",
        )

        assertEquals(listOf("带准考证", "带2B铅笔"), preparationItemsFrom(reviewed))
        assertTrue(reviewed.rawText.contains("准备：带准考证、带2B铅笔"))
        assertTrue(reviewed.rawText.contains("任务：高数A考试"))
    }
}
