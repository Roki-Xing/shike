package cn.shike.app

import cn.shike.app.ui.DEVELOPER_MODE_UNLOCK_TAPS
import cn.shike.app.ui.DeveloperModeState
import cn.shike.app.ui.ShikeMainSection
import cn.shike.app.ui.developerModeStateAfterVersionTap
import cn.shike.app.ui.visibleSectionsForDeveloperMode
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class DeveloperModeUnlockTest {
    @Test
    fun developerModeStateAfterVersionTap_keepsDebugHiddenBeforeFifthTap() {
        val fourthTap = (1 until DEVELOPER_MODE_UNLOCK_TAPS).fold(DeveloperModeState()) { state, _ ->
            developerModeStateAfterVersionTap(state).state
        }

        assertEquals(4, fourthTap.tapCount)
        assertFalse(fourthTap.enabled)
        assertEquals(
            listOf(
                ShikeMainSection.Home,
                ShikeMainSection.Import,
                ShikeMainSection.Inbox,
                ShikeMainSection.Settings,
            ),
            visibleSectionsForDeveloperMode(fourthTap.enabled),
        )
    }

    @Test
    fun developerModeStateAfterVersionTap_unlocksDebugOnFifthTapAndTargetsDebug() {
        val result = (1..DEVELOPER_MODE_UNLOCK_TAPS).fold(
            DeveloperModeState() to ShikeMainSection.Settings,
        ) { (state, _), _ ->
            val next = developerModeStateAfterVersionTap(state)
            next.state to next.targetSection
        }

        assertTrue(result.first.enabled)
        assertEquals(DEVELOPER_MODE_UNLOCK_TAPS, result.first.tapCount)
        assertEquals(ShikeMainSection.Debug, result.second)
        assertEquals(
            listOf(
                ShikeMainSection.Home,
                ShikeMainSection.Import,
                ShikeMainSection.Inbox,
                ShikeMainSection.Settings,
                ShikeMainSection.Debug,
            ),
            visibleSectionsForDeveloperMode(result.first.enabled),
        )
    }

    @Test
    fun developerModeStateAfterVersionTap_keepsUnlockedStateStableAfterExtraTaps() {
        val unlocked = DeveloperModeState(tapCount = DEVELOPER_MODE_UNLOCK_TAPS, enabled = true)

        val result = developerModeStateAfterVersionTap(unlocked)

        assertTrue(result.state.enabled)
        assertEquals(DEVELOPER_MODE_UNLOCK_TAPS, result.state.tapCount)
        assertEquals(ShikeMainSection.Debug, result.targetSection)
    }
}
