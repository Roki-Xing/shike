package cn.shike.app.data

import cn.shike.app.domain.ShikeItem

const val DEFAULT_BACKEND_BASE_URL = "https://roky.chat"

fun sampleCourse() = ShikeItem(
    title = "高数A班教室变更",
    scene = "课程通知",
    time = "今天 18:30 / 22:00 截止",
    location = "B203",
    status = "已安排",
    actions = listOf("加入日历", "课前提醒", "打开地图"),
    startEpochMillis = 1777036200000L,
    rawText = "高数A班今晚18:30改到B203，作业第5章今晚22:00前提交。",
)

fun sampleEvent() = ShikeItem(
    title = "AI应用分享会",
    scene = "活动海报",
    time = "4月24日 19:30 / 22:00 报名截止",
    location = "图书馆报告厅",
    status = "即将截止",
    actions = listOf("加入活动日历", "报名截止提醒", "打开活动地点"),
    startEpochMillis = 1777039800000L,
    rawText = "AI应用分享会 4月24日19:30 图书馆报告厅 报名截止今晚22:00",
)
