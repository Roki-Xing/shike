package cn.shike.app

import cn.shike.app.data.sampleCourse
import cn.shike.app.data.sampleEvent
import cn.shike.app.domain.ShikeItem

fun applyCourseSampleSelection(persistSelection: (ShikeItem, String) -> Unit) {
    persistSelection(sampleCourse(), "离线样例：课程通知截图")
}

fun applyEventSampleSelection(persistSelection: (ShikeItem, String) -> Unit) {
    persistSelection(sampleEvent(), "离线样例：活动海报拍照")
}
