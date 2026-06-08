package cn.shike.app.data

import android.content.SharedPreferences
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class ScreenshotCandidateStoreTest {
    @Test
    fun isLikelyScreenshot_acceptsScreenshotNameOrPathSignals() {
        assertTrue(
            isLikelyScreenshot(
                displayName = "Screenshot_20260607-101500.png",
                relativePath = "Pictures/Camera/",
            ),
        )
        assertTrue(
            isLikelyScreenshot(
                displayName = "IMG_20260607_101500.jpg",
                relativePath = "Pictures/Screenshots/",
            ),
        )
        assertTrue(
            isLikelyScreenshot(
                displayName = "屏幕截图_20260607.png",
                relativePath = "Pictures/Camera/",
            ),
        )
    }

    @Test
    fun isLikelyScreenshot_rejectsScreenSizedImagesWithoutScreenshotSignals() {
        assertFalse(
            isLikelyScreenshot(
                displayName = "IMG_20260607_101500.jpg",
                relativePath = "Pictures/Camera/",
            ),
        )
    }

    @Test
    fun screenshotDisplayNameDigest_isStableAndDoesNotExposeTheName() {
        val digest = screenshotDisplayNameDigest("Screenshot_20260607-101500.png")

        assertEquals(digest, screenshotDisplayNameDigest("Screenshot_20260607-101500.png"))
        assertFalse(digest.contains("Screenshot"))
        assertFalse(digest.contains("20260607"))
    }

    @Test
    fun shouldNotifyScreenshotCandidate_rejectsDuplicateContentUri() {
        val candidate = ScreenshotCandidate(
            contentUri = "content://media/external/images/media/42",
            createdAtMillis = 1_786_789_000_000,
            width = 1080,
            height = 2400,
            displayNameDigest = "abc123",
        )

        assertTrue(shouldNotifyScreenshotCandidate(candidate, lastNotifiedContentUri = null))
        assertTrue(shouldNotifyScreenshotCandidate(candidate, lastNotifiedContentUri = "content://media/external/images/media/41"))
        assertFalse(shouldNotifyScreenshotCandidate(candidate, lastNotifiedContentUri = candidate.contentUri))
    }

    @Test
    fun screenshotAssistLookbackWindow_matchesAndroid16Guide() {
        assertEquals(30L, SCREENSHOT_ASSIST_LOOKBACK_SECONDS)
    }

    @Test
    fun screenshotCandidateFromNotificationImport_preservesCandidateMetadata() {
        val candidate = screenshotCandidateFromNotificationImport(
            contentUri = "content://media/external/images/media/42",
            createdAtMillis = 1_786_789_000_000,
            width = 1080,
            height = 2400,
            displayNameDigest = "abc123",
            nowMillis = 1_786_789_999_000,
        )

        requireNotNull(candidate)
        assertEquals("content://media/external/images/media/42", candidate.contentUri)
        assertEquals(1_786_789_000_000, candidate.createdAtMillis)
        assertEquals(1080, candidate.width)
        assertEquals(2400, candidate.height)
        assertEquals("abc123", candidate.displayNameDigest)
        assertEquals("最近截图助手导入", candidate.sourceLabel)
    }

    @Test
    fun screenshotAssistPreference_persistsAcrossRestartAndCanBeCleared() {
        val preferences = InMemorySharedPreferences()

        assertFalse(loadScreenshotAssistEnabledFromPreferences(preferences))

        saveScreenshotAssistEnabledToPreferences(preferences, enabled = true)

        assertTrue(loadScreenshotAssistEnabledFromPreferences(preferences))

        clearScreenshotAssistPreferenceFromPreferences(preferences)

        assertFalse(loadScreenshotAssistEnabledFromPreferences(preferences))
        assertNull(preferences.getAll()[KEY_SCREENSHOT_ASSIST_ENABLED])
    }

    private class InMemorySharedPreferences : SharedPreferences {
        private val data: MutableMap<String, Any?> = linkedMapOf()

        override fun getAll(): MutableMap<String, *> = LinkedHashMap(data)

        override fun getString(key: String, defValue: String?): String? =
            (data[key] as? String) ?: defValue

        override fun getStringSet(key: String, defValues: MutableSet<String>?): MutableSet<String>? {
            @Suppress("UNCHECKED_CAST")
            return (data[key] as? MutableSet<String>) ?: defValues
        }

        override fun getInt(key: String, defValue: Int): Int =
            (data[key] as? Int) ?: defValue

        override fun getLong(key: String, defValue: Long): Long =
            (data[key] as? Long) ?: defValue

        override fun getFloat(key: String, defValue: Float): Float =
            (data[key] as? Float) ?: defValue

        override fun getBoolean(key: String, defValue: Boolean): Boolean =
            (data[key] as? Boolean) ?: defValue

        override fun contains(key: String): Boolean = data.containsKey(key)

        override fun edit(): SharedPreferences.Editor = Editor(data)

        override fun registerOnSharedPreferenceChangeListener(listener: SharedPreferences.OnSharedPreferenceChangeListener) = Unit

        override fun unregisterOnSharedPreferenceChangeListener(listener: SharedPreferences.OnSharedPreferenceChangeListener) = Unit

        private class Editor(private val data: MutableMap<String, Any?>) : SharedPreferences.Editor {
            private val removals: MutableSet<String> = linkedSetOf()
            private val puts: MutableMap<String, Any?> = linkedMapOf()

            override fun putString(key: String, value: String?): SharedPreferences.Editor = apply {
                puts[key] = value
            }

            override fun putStringSet(key: String, values: MutableSet<String>?): SharedPreferences.Editor = apply {
                puts[key] = values
            }

            override fun putInt(key: String, value: Int): SharedPreferences.Editor = apply {
                puts[key] = value
            }

            override fun putLong(key: String, value: Long): SharedPreferences.Editor = apply {
                puts[key] = value
            }

            override fun putFloat(key: String, value: Float): SharedPreferences.Editor = apply {
                puts[key] = value
            }

            override fun putBoolean(key: String, value: Boolean): SharedPreferences.Editor = apply {
                puts[key] = value
            }

            override fun remove(key: String): SharedPreferences.Editor = apply {
                removals.add(key)
            }

            override fun clear(): SharedPreferences.Editor = apply {
                data.clear()
            }

            override fun commit(): Boolean {
                apply()
                return true
            }

            override fun apply() {
                removals.forEach { data.remove(it) }
                puts.forEach { (key, value) ->
                    if (value == null) {
                        data.remove(key)
                    } else {
                        data[key] = value
                    }
                }
                removals.clear()
                puts.clear()
            }
        }
    }
}
