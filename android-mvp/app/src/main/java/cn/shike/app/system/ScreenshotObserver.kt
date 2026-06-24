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
import java.util.concurrent.Executor

class ScreenshotObserver(
    private val resolver: ContentResolver,
    handler: Handler,
    private val executor: Executor,
    private val onCandidate: (ScreenshotCandidate) -> Unit,
) : ContentObserver(handler) {
    override fun onChange(selfChange: Boolean, uri: Uri?) {
        super.onChange(selfChange, uri)
        executor.execute {
            queryFromCallbackUriFirst(uri)?.let(onCandidate)
        }
    }

    fun register() {
        resolver.registerContentObserver(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, true, this)
    }

    fun unregister() {
        resolver.unregisterContentObserver(this)
    }

    internal fun queryFromCallbackUriFirst(uri: Uri?): ScreenshotCandidate? {
        if (uri != null && isMediaStoreImageItemUri(uri)) {
            querySpecificImage(uri)?.let { return it }
        }
        return queryRecentScreenshot()
    }

    private fun querySpecificImage(uri: Uri): ScreenshotCandidate? {
        val projection = imageProjection()
        resolver.query(uri, projection.toTypedArray(), null, null, null)?.use { cursor ->
            if (!cursor.moveToFirst()) return null
            return candidateFromCursor(cursor, uri)
        }
        return null
    }

    private fun queryRecentScreenshot(): ScreenshotCandidate? {
        val projection = imageProjection()
        val nowSeconds = System.currentTimeMillis() / 1000
        resolver.query(
            MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
            projection.toTypedArray(),
            "${MediaStore.Images.Media.DATE_ADDED} >= ?",
            arrayOf((nowSeconds - SCREENSHOT_ASSIST_LOOKBACK_SECONDS).toString()),
            "${MediaStore.Images.Media.DATE_ADDED} DESC",
        )?.use { cursor ->
            while (cursor.moveToNext()) {
                candidateFromCursor(cursor)?.let { return it }
            }
        }
        return null
    }

    private fun imageProjection(): MutableList<String> {
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
        return projection
    }

    private fun candidateFromCursor(cursor: android.database.Cursor, sourceUri: Uri? = null): ScreenshotCandidate? {
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
        val displayName = cursor.getString(nameIndex) ?: ""
        val relativePath = pathIndex.takeIf { it >= 0 }?.let { cursor.getString(it) }
        if (!isLikelyScreenshot(displayName, relativePath)) {
            return null
        }
        val contentUri = sourceUri ?: ContentUris.withAppendedId(
            MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
            cursor.getLong(idIndex),
        )
        return ScreenshotCandidate(
            contentUri = contentUri.toString(),
            createdAtMillis = cursor.getLong(dateIndex) * 1000,
            width = cursor.getInt(widthIndex),
            height = cursor.getInt(heightIndex),
            displayNameDigest = screenshotDisplayNameDigest(displayName),
        )
    }
}

internal fun isMediaStoreImageItemUri(uri: Uri): Boolean {
    if (uri.scheme != ContentResolver.SCHEME_CONTENT || uri.authority != MediaStore.AUTHORITY) {
        return false
    }
    val path = uri.path.orEmpty().lowercase()
    return Regex("^/[^/]+/images/media/[0-9]+$").matches(path)
}
