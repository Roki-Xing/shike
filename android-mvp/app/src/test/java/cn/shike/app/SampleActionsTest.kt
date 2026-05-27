package cn.shike.app

import cn.shike.app.data.sampleCourse
import cn.shike.app.data.sampleEvent
import cn.shike.app.domain.ShikeItem
import org.junit.Assert.assertEquals
import org.junit.Test

class SampleActionsTest {
    @Test
    fun applyCourseSampleSelection_persistsCourseSampleWithSource() {
        val persisted = mutableListOf<Pair<ShikeItem, String>>()

        applyCourseSampleSelection { item, source ->
            persisted += item to source
        }

        assertEquals(listOf(sampleCourse() to "离线样例：课程通知截图"), persisted)
    }

    @Test
    fun applyEventSampleSelection_persistsEventSampleWithSource() {
        val persisted = mutableListOf<Pair<ShikeItem, String>>()

        applyEventSampleSelection { item, source ->
            persisted += item to source
        }

        assertEquals(listOf(sampleEvent() to "离线样例：活动海报拍照"), persisted)
    }
}
