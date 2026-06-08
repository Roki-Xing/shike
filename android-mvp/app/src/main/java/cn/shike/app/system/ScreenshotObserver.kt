package cn.shike.app.system

import android.content.ContentResolver
import android.content.ContentUris
import android.database.ContentObserver
import android.net.Uri
import android.os.Build
import android.os.Handler
import android.provider.MediaStore
import cn.shike.app.data.ScreenshotCandidate
import cn.shike.app.data.SCREENSHOT_ASSIST_LOOKBACK_SECONDS
import cn.shike.app.data.isLikelyScreenshot
import cn.shike.app.data.screenshotDisplayNameDigest

class ScreenshotObserver(
    private val resolver: ContentResolver,
    handler: Handler,
    private val onCandidate: (ScreenshotCandidate) -> Unit,
) : ContentObserver(handler) {
    override fun onChange(selfChange: Boolean, uri: Uri?) {
        super.onChange(selfChange, uri)
        queryRecentScreenshot()?.let(onCandidate)
    }

    fun register() {
        resolver.registerContentObserver(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, true, this)
    }

    fun unregister() {
        resolver.unregisterContentObserver(this)
    }

    private fun queryRecentScreenshot(): ScreenshotCandidate? {
        val projection = mutableListOf(
            MediaStore.Images.Media._ID,
            MediaStore.Images.Media.DISPLAY_NAME,
            MediaStore.Images.Media.DATE_ADDED,
            MediaStore.Images.Media.WIDTH,
            MediaStore.Images.Media.HEIGHT,
        )
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            projection += MediaStore.Images.Media.RELATIVE_PATH
        }
        val nowSeconds = System.currentTimeMillis() / 1000
        resolver.query(
            MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
            projection.toTypedArray(),
            "${MediaStore.Images.Media.DATE_ADDED} >= ?",
            arrayOf((nowSeconds - SCREENSHOT_ASSIST_LOOKBACK_SECONDS).toString()),
            "${MediaStore.Images.Media.DATE_ADDED} DESC",
        )?.use { cursor ->
            val idIndex = cursor.getColumnIndexOrThrow(MediaStore.Images.Media._ID)
            val nameIndex = cursor.getColumnIndexOrThrow(MediaStore.Images.Media.DISPLAY_NAME)
            val dateIndex = cursor.getColumnIndexOrThrow(MediaStore.Images.Media.DATE_ADDED)
            val widthIndex = cursor.getColumnIndexOrThrow(MediaStore.Images.Media.WIDTH)
            val heightIndex = cursor.getColumnIndexOrThrow(MediaStore.Images.Media.HEIGHT)
            val pathIndex = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                cursor.getColumnIndex(MediaStore.Images.Media.RELATIVE_PATH)
            } else {
                -1
            }
            while (cursor.moveToNext()) {
                val displayName = cursor.getString(nameIndex) ?: ""
                val relativePath = pathIndex.takeIf { it >= 0 }?.let { cursor.getString(it) }
                val width = cursor.getInt(widthIndex)
                val height = cursor.getInt(heightIndex)
                if (isLikelyScreenshot(displayName, relativePath)) {
                    val id = cursor.getLong(idIndex)
                    return ScreenshotCandidate(
                        contentUri = ContentUris.withAppendedId(
                            MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
                            id,
                        ).toString(),
                        createdAtMillis = cursor.getLong(dateIndex) * 1000,
                        width = width,
                        height = height,
                        displayNameDigest = screenshotDisplayNameDigest(displayName),
                    )
                }
            }
        }
        return null
    }
}
