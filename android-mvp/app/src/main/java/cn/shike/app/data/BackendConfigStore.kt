package cn.shike.app.data

import android.content.Context

private const val BACKEND_PREFERENCES_NAME = "shike_backend_config"
private const val KEY_BACKEND_BASE_URL = "backend_base_url"
private const val LEGACY_EMULATOR_BACKEND_BASE_URL = "http://10.0.2.2:8000"

/**
 * Saves a normalized backend base URL for emulator and real-device demos.
 *
 * Args:
 *     context: Android context used to open app-scoped preferences.
 *     url: User-entered backend URL.
 */
fun saveBackendBaseUrl(context: Context, url: String) {
    context.getSharedPreferences(BACKEND_PREFERENCES_NAME, Context.MODE_PRIVATE)
        .edit()
        .putString(KEY_BACKEND_BASE_URL, normalizeBackendUrl(url))
        .apply()
}

/**
 * Normalizes a backend URL from the UI and persists it through the supplied saver.
 *
 * Args:
 *     backendUrl: User-entered backend URL.
 *     save: Persistence callback owned by the Android shell.
 *
 * Returns:
 *     The normalized backend URL that should be reflected in UI state.
 */
fun saveBackendUrlFromInput(backendUrl: String, save: (String) -> Unit): String {
    val normalizedUrl = normalizeBackendUrl(backendUrl)
    save(normalizedUrl)
    return normalizedUrl
}

/**
 * Loads the configured backend base URL.
 *
 * Args:
 *     context: Android context used to open app-scoped preferences.
 *
 * Returns:
 *     The saved backend URL, or the emulator default.
 */
fun loadBackendBaseUrl(context: Context): String {
    val preferences = context.getSharedPreferences(BACKEND_PREFERENCES_NAME, Context.MODE_PRIVATE)
    val savedUrl = preferences.getString(KEY_BACKEND_BASE_URL, null)
    val backendUrl = migrateLegacyBackendBaseUrl(savedUrl)
    if (savedUrl == LEGACY_EMULATOR_BACKEND_BASE_URL) {
        preferences.edit().putString(KEY_BACKEND_BASE_URL, backendUrl).apply()
    }
    return backendUrl
}

/**
 * Migrates old emulator-only defaults to the deployed HTTPS backend.
 *
 * Args:
 *     savedUrl: Persisted backend URL, if any.
 *
 * Returns:
 *     A usable backend URL for the current build.
 */
fun migrateLegacyBackendBaseUrl(savedUrl: String?): String =
    when (savedUrl) {
        null, "" -> DEFAULT_BACKEND_BASE_URL
        LEGACY_EMULATOR_BACKEND_BASE_URL -> DEFAULT_BACKEND_BASE_URL
        else -> savedUrl
    }

/**
 * Clears the persisted backend endpoint override.
 *
 * Args:
 *     context: Android context used to open app-scoped preferences.
 */
fun clearBackendBaseUrl(context: Context) {
    context.getSharedPreferences(BACKEND_PREFERENCES_NAME, Context.MODE_PRIVATE)
        .edit()
        .remove(KEY_BACKEND_BASE_URL)
        .apply()
}
