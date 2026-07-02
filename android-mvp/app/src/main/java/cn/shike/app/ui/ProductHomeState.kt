package cn.shike.app.ui

import cn.shike.app.domain.ShikeItem

enum class ProductHomeState {
    Empty,
    NeedsReview,
    Arranged,
    Active,
}

fun productHomeStateFor(item: ShikeItem, todayAgendaState: TodayAgendaState): ProductHomeState =
    when {
        todayAgendaState == TodayAgendaState.Empty || item.title.isBlank() -> ProductHomeState.Empty
        item.status == "待确认" -> ProductHomeState.NeedsReview
        item.status == "已安排" -> ProductHomeState.Arranged
        else -> ProductHomeState.Active
    }
