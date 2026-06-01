package cn.shike.app.data

fun syntheticInboxSeed(count: Int = 50, baseEpochMillis: Long = sampleCourse().startEpochMillis): List<InboxItemEntity> {
    val statuses = listOf("待确认", "已安排", "即将截止", "已完成", "已忽略")
    val scenes = listOf("课程通知", "活动海报", "作业截止", "会议通知", "出行提醒")
    return (0 until count).map { index ->
        val status = statuses[index % statuses.size]
        val scene = scenes[index % scenes.size]
        InboxItemEntity(
            id = "seed-${index + 1}",
            title = "收件箱样例 ${index + 1}",
            scene = scene,
            time = "2026-05-${(index % 28) + 1} 18:30",
            location = if (index % 4 == 0) "待确认" else "B${200 + index}",
            status = status,
            source = if (index % 2 == 0) "相册截图" else "文本分享",
            rawText = "$scene OCR 摘要 ${index + 1}",
            actionLabels = listOf("加入日历", "本地提醒", "打开地图"),
            startEpochMillis = baseEpochMillis + index * 3_600_000L,
            updatedEpochMillis = baseEpochMillis + index * 60_000L,
            archived = false,
        )
    }
}
