package cn.shike.app.data

import android.content.SharedPreferences

class InMemorySharedPreferences : SharedPreferences {
    private val data: MutableMap<String, Any?> = linkedMapOf()

    override fun getAll(): MutableMap<String, *> = LinkedHashMap(data)

    override fun getString(key: String, defValue: String?): String? =
        (data[key] as? String) ?: defValue

    override fun getStringSet(key: String, defValues: MutableSet<String>?): MutableSet<String>? {
        @Suppress("UNCHECKED_CAST")
        return (data[key] as? MutableSet<String>)?.toMutableSet() ?: defValues
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
            puts[key] = values?.toMutableSet()
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
