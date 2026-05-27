package cn.shike.app

import cn.shike.app.data.sampleCourse
import cn.shike.app.data.sampleEvent
import cn.shike.app.domain.ShikeItem
import org.junit.Assert.assertEquals
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
}
