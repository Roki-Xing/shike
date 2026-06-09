package cn.shike.app.data

import android.content.Context

private const val PERMISSION_ONBOARDING_PREFERENCES_NAME = "shike_permission_onboarding"
private const val KEY_PERMISSION_ONBOARDING_DISMISSED = "permission_onboarding_dismissed"

/**
 * Loads whether the user has already seen the first-run permission guide.
 *
 * Args:
 *     context: Android context used to open app-scoped preferences.
 *
 * Returns:
 *     True when the onboarding has been dismissed.
 */
fun loadPermissionOnboardingDismissed(context: Context): Boolean =
    context.getSharedPreferences(PERMISSION_ONBOARDING_PREFERENCES_NAME, Context.MODE_PRIVATE)
        .getBoolean(KEY_PERMISSION_ONBOARDING_DISMISSED, false)

/**
 * Persists the first-run permission guide dismissed state.
 *
 * Args:
 *     context: Android context used to open app-scoped preferences.
 *     dismissed: Whether the onboarding should stay hidden on next launch.
 */
fun savePermissionOnboardingDismissed(context: Context, dismissed: Boolean) {
    context.getSharedPreferences(PERMISSION_ONBOARDING_PREFERENCES_NAME, Context.MODE_PRIVATE)
        .edit()
        .putBoolean(KEY_PERMISSION_ONBOARDING_DISMISSED, dismissed)
        .apply()
}
