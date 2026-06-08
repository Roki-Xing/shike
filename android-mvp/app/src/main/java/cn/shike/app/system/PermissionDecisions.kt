package cn.shike.app.system

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.os.Build
import androidx.core.content.ContextCompat

/**
 * Checks whether the camera preview flow can launch immediately.
 *
 * Args:
 *     context: Android context used to inspect runtime permissions.
 *
 * Returns:
 *     True when `Manifest.permission.CAMERA` is already granted.
 */
fun hasCameraPermission(context: Context): Boolean =
    ContextCompat.checkSelfPermission(context, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED

/**
 * Checks whether a reminder notification can be posted without a new prompt.
 *
 * Args:
 *     context: Android context used to inspect runtime permissions.
 *
 * Returns:
 *     True on Android versions before runtime notification permission, or when
 *     `Manifest.permission.POST_NOTIFICATIONS` is granted.
 */
fun canPostReminderNotification(context: Context): Boolean =
    Build.VERSION.SDK_INT < 33 ||
        ContextCompat.checkSelfPermission(
            context,
            Manifest.permission.POST_NOTIFICATIONS,
        ) == PackageManager.PERMISSION_GRANTED

fun canPostScreenshotAssistNotification(context: Context): Boolean =
    canPostReminderNotification(context)

fun hasScreenshotMediaPermission(context: Context): Boolean {
    val permission = if (Build.VERSION.SDK_INT >= 33) {
        Manifest.permission.READ_MEDIA_IMAGES
    } else {
        Manifest.permission.READ_EXTERNAL_STORAGE
    }
    return ContextCompat.checkSelfPermission(context, permission) == PackageManager.PERMISSION_GRANTED
}
