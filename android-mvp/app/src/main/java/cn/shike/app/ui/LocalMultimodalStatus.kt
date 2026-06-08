package cn.shike.app.ui

enum class LocalMultimodalInstallState {
    NotInstalled,
    Available,
    InitFailed,
}

enum class LocalMultimodalPreference {
    CloudFirst,
    LocalPreferred,
}

fun allowCloudImageForPreference(preference: LocalMultimodalPreference): Boolean =
    preference == LocalMultimodalPreference.CloudFirst

data class LocalMultimodalStatus(
    val installState: LocalMultimodalInstallState,
    val preference: LocalMultimodalPreference,
    val cloudEnhancedEnabled: Boolean,
    val lastErrorCode: Int? = null,
)

data class LocalMultimodalUiState(
    val statusLabel: String,
    val routeLabel: String,
    val detail: String,
)

/**
 * Maps the local 3B multimodal runtime boundary into safe user-facing copy.
 *
 * Args:
 *     status: Current local model install, preference, and cloud availability state.
 *
 * Returns:
 *     Copy that does not claim the local model is usable until runtime state proves it.
 */
fun localMultimodalUiState(status: LocalMultimodalStatus): LocalMultimodalUiState {
    return when (status.installState) {
        LocalMultimodalInstallState.NotInstalled -> LocalMultimodalUiState(
            statusLabel = "端侧模型：未安装",
            routeLabel = "云端优先",
            detail = "当前 APK 不打包模型，不会假装可用；截图解析优先走云端增强或本地草稿确认。",
        )
        LocalMultimodalInstallState.Available -> availableLocalMultimodalUiState(status)
        LocalMultimodalInstallState.InitFailed -> LocalMultimodalUiState(
            statusLabel = "端侧模型：初始化失败",
            routeLabel = "不可用，转人工确认",
            detail = "初始化失败${status.lastErrorCode?.let { "，错误码 $it" } ?: ""}；端侧输出仍必须过同一 JSON Schema，再由用户确认。",
        )
    }
}

private fun availableLocalMultimodalUiState(status: LocalMultimodalStatus): LocalMultimodalUiState {
    if (!status.cloudEnhancedEnabled) {
        return LocalMultimodalUiState(
            statusLabel = "端侧模型：可用",
            routeLabel = "云端关闭，端侧接管",
            detail = "云端关闭后才允许端侧接管；输出仍进入同一确认和执行闸门。",
        )
    }
    if (status.preference == LocalMultimodalPreference.LocalPreferred) {
        return LocalMultimodalUiState(
            statusLabel = "端侧模型：可用",
            routeLabel = "端侧优先",
            detail = "用户选择端侧模式时优先本地推理，云端仅作为用户确认后的增强路径。",
        )
    }
    return LocalMultimodalUiState(
        statusLabel = "端侧模型：可用",
        routeLabel = "云端优先",
        detail = "云端优先；端侧仅在云端不可用时再启用，并保持同一 JSON Schema。",
    )
}
