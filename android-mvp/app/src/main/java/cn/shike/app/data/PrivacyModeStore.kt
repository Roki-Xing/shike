package cn.shike.app.data

import android.content.Context
import android.content.SharedPreferences
import cn.shike.app.ui.LocalMultimodalPreference

private const val PRIVACY_MODE_PREFERENCES_NAME = "shike_privacy_mode"
private const val KEY_CLOUD_ENHANCED_ENABLED = "cloud_enhanced_enabled"
private const val KEY_LOCAL_MULTIMODAL_PREFERENCE = "local_multimodal_preference"

data class PrivacyModeState(
    val cloudEnhancedEnabled: Boolean,
    val localMultimodalPreference: LocalMultimodalPreference,
)

fun loadPrivacyMode(context: Context): PrivacyModeState =
    loadPrivacyModeFromPreferences(privacyModePreferences(context))

fun savePrivacyMode(
    context: Context,
    cloudEnhancedEnabled: Boolean,
    localMultimodalPreference: LocalMultimodalPreference,
) {
    savePrivacyModeToPreferences(
        preferences = privacyModePreferences(context),
        cloudEnhancedEnabled = cloudEnhancedEnabled,
        localMultimodalPreference = localMultimodalPreference,
    )
}

fun clearPrivacyMode(context: Context) {
    privacyModePreferences(context).edit().clear().apply()
}

internal fun loadPrivacyModeFromPreferences(preferences: SharedPreferences): PrivacyModeState {
    val preference = preferences.getString(KEY_LOCAL_MULTIMODAL_PREFERENCE, null)
        ?.let { runCatching { LocalMultimodalPreference.valueOf(it) }.getOrNull() }
        ?: LocalMultimodalPreference.CloudFirst
    return PrivacyModeState(
        cloudEnhancedEnabled = preferences.getBoolean(KEY_CLOUD_ENHANCED_ENABLED, true),
        localMultimodalPreference = preference,
    )
}

internal fun savePrivacyModeToPreferences(
    preferences: SharedPreferences,
    cloudEnhancedEnabled: Boolean,
    localMultimodalPreference: LocalMultimodalPreference,
) {
    preferences.edit()
        .putBoolean(KEY_CLOUD_ENHANCED_ENABLED, cloudEnhancedEnabled)
        .putString(KEY_LOCAL_MULTIMODAL_PREFERENCE, localMultimodalPreference.name)
        .apply()
}

private fun privacyModePreferences(context: Context): SharedPreferences =
    context.getSharedPreferences(PRIVACY_MODE_PREFERENCES_NAME, Context.MODE_PRIVATE)
