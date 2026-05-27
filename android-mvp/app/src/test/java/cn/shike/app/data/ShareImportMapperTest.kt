package cn.shike.app.data

import org.junit.Assert.assertEquals
import org.junit.Test

class ShareImportMapperTest {
    @Test
    fun sharedTextCaptureDraft_keepsShareChannelAndRawText() {
        val draft = sharedTextCaptureDraft("活动报名今晚截止")

        assertEquals("share", draft.channel)
        assertEquals("系统分享文本", draft.sourceLabel)
        assertEquals("活动报名今晚截止", draft.rawText)
    }

    @Test
    fun itemFromSharedText_blankTextFallsBackToCourseSample() {
        val item = itemFromSharedText("   ")

        assertEquals("高数A班教室变更", item.title)
        assertEquals("课程通知", item.scene)
    }

    @Test
    fun itemFromSharedText_activityTextMapsToEventReviewCard() {
        val raw = "AI应用分享会活动 4月24日19:30 图书馆报告厅"

        val item = itemFromSharedText(raw)

        assertEquals("分享导入的活动", item.title)
        assertEquals("活动海报", item.scene)
        assertEquals(raw, item.rawText)
    }

    @Test
    fun itemFromSharedText_courseTextMapsToCourseReviewCard() {
        val raw = "高数A班今晚18:30改到B203"

        val item = itemFromSharedText(raw)

        assertEquals("分享导入的课程通知", item.title)
        assertEquals("课程通知", item.scene)
        assertEquals(raw, item.rawText)
    }
}
