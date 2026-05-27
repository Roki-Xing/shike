package cn.shike.app.data

import android.content.SharedPreferences
import cn.shike.app.system.clearScheduledReminderFromPreferences
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class LocalPersistenceBoundaryTest {
    @Test
    fun clearingInboxSnapshot_doesNotEraseBackendOverrideOrReminderPayload() {
        val inboxPreferences = InMemorySharedPreferences()
        val backendPreferences = InMemorySharedPreferences()
        val reminderPreferences = InMemorySharedPreferences()

        inboxPreferences.edit()
            .putString("title", "高数A班教室变更")
            .putString("raw_text", "raw")
            .apply()
        backendPreferences.edit()
            .putString("backend_base_url", "http://127.0.0.1:8000")
            .apply()
        reminderPreferences.edit()
            .putString("scheduled_reminder_title", "提醒标题")
            .putString("scheduled_reminder_detail", "提醒详情")
            .putInt("scheduled_reminder_id", 42)
            .putLong("scheduled_reminder_trigger_at_millis", 1234L)
            .apply()

        clearInboxSnapshotFromPreferences(inboxPreferences)

        assertNull(inboxPreferences.getString("title", null))
        assertNull(inboxPreferences.getString("raw_text", null))
        assertEquals("http://127.0.0.1:8000", backendPreferences.getString("backend_base_url", null))
        assertEquals("提醒标题", reminderPreferences.getString("scheduled_reminder_title", null))

        clearScheduledReminderFromPreferences(reminderPreferences)

        assertNull(reminderPreferences.getString("scheduled_reminder_title", null))
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
            private var clearAll: Boolean = false

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
                clearAll = true
            }

            override fun commit(): Boolean {
                apply()
                return true
            }

            override fun apply() {
                if (clearAll) {
                    data.clear()
                }
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
                clearAll = false
            }
        }
    }
}
