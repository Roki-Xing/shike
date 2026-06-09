package cn.shike.app.system

data class VisibleScreenCapturePrompt(
    val title: String,
    val body: String,
    val primaryActionLabel: String,
    val secondaryActionLabel: String,
)

fun visibleScreenCapturePrompt(): VisibleScreenCapturePrompt =
    VisibleScreenCapturePrompt(
        title = "检测到当前页面截图",
        body = "Android 只通知当前页面被截图，拾刻不会直接获得图片。请在导入页选择这张截图，解析后可用系统确认移入回收站。",
        primaryActionLabel = "选择截图导入",
        secondaryActionLabel = "先不处理，解析后可移入回收站",
    )
