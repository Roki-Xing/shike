package cn.shike.app.domain

data class ShikeItem(
    val title: String,
    val scene: String,
    val time: String,
    val location: String,
    val status: String,
    val actions: List<String>,
    val startEpochMillis: Long,
    val rawText: String,
)

