package cn.shike.app

import cn.shike.app.data.sampleCourse
import cn.shike.app.data.sampleEvent
import cn.shike.app.ui.TodayActionTone
import cn.shike.app.ui.todayActionItemFrom
import org.junit.Assert.assertEquals
import org.junit.Test

class TodayActionItemMapperTest {
    @Test
    fun todayActionItemFrom_scheduledItemUsesRouteActionAndConfirmedFooter() {
        val item = sampleCourse().copy(status = "已安排", actions = listOf("加入日历", "打开地图"))

        val today = todayActionItemFrom(item)

        assertEquals(TodayActionTone.Scheduled, today.tone)
        assertEquals("查看路线", today.actionLabel)
        assertEquals("来源：课程通知 · 已确认", today.footerLabel)
        assertEquals(listOf("今天 18:30 / 22:00 截止", "B203"), today.detailLines)
    }

    @Test
    fun todayActionItemFrom_dueSoonItemKeepsDeadlineActionAndReviewFooter() {
        val today = todayActionItemFrom(sampleEvent())

        assertEquals(TodayActionTone.DueSoon, today.tone)
        assertEquals("查看截止", today.actionLabel)
        assertEquals("来源：活动海报 · 待用户确认", today.footerLabel)
    }

    @Test
    fun todayActionItemFrom_pendingItemFallsBackToPrimaryActionOrDetail() {
        val withAction = sampleCourse().copy(status = "待确认", actions = listOf("确认课程"))
        val withoutAction = sampleCourse().copy(status = "待确认", actions = emptyList())

        assertEquals(TodayActionTone.Pending, todayActionItemFrom(withAction).tone)
        assertEquals("确认课程", todayActionItemFrom(withAction).actionLabel)
        assertEquals("查看详情", todayActionItemFrom(withoutAction).actionLabel)
    }
}
