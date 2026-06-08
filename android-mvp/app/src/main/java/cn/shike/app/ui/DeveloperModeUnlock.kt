package cn.shike.app.ui

const val DEVELOPER_MODE_UNLOCK_TAPS = 5

data class DeveloperModeState(
    val tapCount: Int = 0,
    val enabled: Boolean = false,
)

data class DeveloperModeTapResult(
    val state: DeveloperModeState,
    val targetSection: ShikeMainSection,
)

fun developerModeStateAfterVersionTap(
    current: DeveloperModeState,
): DeveloperModeTapResult {
    if (current.enabled) {
        return DeveloperModeTapResult(
            state = current.copy(tapCount = DEVELOPER_MODE_UNLOCK_TAPS),
            targetSection = ShikeMainSection.Debug,
        )
    }

    val nextTapCount = (current.tapCount + 1).coerceAtMost(DEVELOPER_MODE_UNLOCK_TAPS)
    val nextState = DeveloperModeState(
        tapCount = nextTapCount,
        enabled = nextTapCount >= DEVELOPER_MODE_UNLOCK_TAPS,
    )
    return DeveloperModeTapResult(
        state = nextState,
        targetSection = if (nextState.enabled) ShikeMainSection.Debug else ShikeMainSection.Settings,
    )
}

fun visibleSectionsForDeveloperMode(enabled: Boolean): List<ShikeMainSection> {
    val ordinarySections = listOf(
        ShikeMainSection.Home,
        ShikeMainSection.Import,
        ShikeMainSection.Inbox,
        ShikeMainSection.Settings,
    )
    return if (enabled) ordinarySections + ShikeMainSection.Debug else ordinarySections
}
