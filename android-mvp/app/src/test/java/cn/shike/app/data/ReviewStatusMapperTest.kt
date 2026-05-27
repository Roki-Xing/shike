package cn.shike.app.data

import org.junit.Assert.assertEquals
import org.junit.Test

class ReviewStatusMapperTest {
    @Test
    fun mapReviewedItemState_confirmedItemBecomesScheduled() {
        val reviewed = mapReviewedItemState(sampleEvent().copy(status = "待确认"))

        assertEquals("已安排", reviewed.item.status)
        assertEquals("模型编排：用户已确认", reviewed.statusMessage)
        assertEquals("AI应用分享会", reviewed.item.title)
    }

    @Test
    fun mapReviewedItemState_ignoredItemStaysIgnored() {
        val ignored = mapReviewedItemState(sampleCourse().copy(status = "已忽略"))

        assertEquals("已忽略", ignored.item.status)
        assertEquals("模型编排：用户已忽略", ignored.statusMessage)
    }

    @Test
    fun mapReviewedItemState_preservesReviewedFields() {
        val item = sampleCourse().copy(
            title = "用户修正后的课程",
            time = "今天 20:00",
            location = "B305",
            status = "低置信度",
        )

        val reviewed = mapReviewedItemState(item)

        assertEquals("用户修正后的课程", reviewed.item.title)
        assertEquals("今天 20:00", reviewed.item.time)
        assertEquals("B305", reviewed.item.location)
        assertEquals("已安排", reviewed.item.status)
    }
}
