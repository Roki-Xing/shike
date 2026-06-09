package cn.shike.app

import android.content.Context
import android.graphics.Bitmap
import android.net.Uri
import cn.shike.app.data.BackendImagePayload
import cn.shike.app.data.ImagePayloadPreprocessor
import cn.shike.app.data.ImagePreprocessSource

fun Context.buildBackendImagePayloadFromUri(uriText: String, sourceType: String): BackendImagePayload? {
    val uri = runCatching { Uri.parse(uriText) }.getOrNull() ?: return null
    val bytes = contentResolver.openInputStream(uri)?.use { stream ->
        stream.readBytes()
    } ?: return null
    return ImagePayloadPreprocessor.fromBytesWithThumbnail(
        bytes = bytes,
        source = imagePreprocessSourceFromBackendSource(sourceType),
        thumbnailCacheRoot = cacheDir,
    )?.payload
}

fun Context.buildBackendImagePayloadFromBitmap(bitmap: Bitmap): BackendImagePayload? =
    ImagePayloadPreprocessor.fromBitmapWithThumbnail(
        bitmap = bitmap,
        thumbnailCacheRoot = cacheDir,
    )?.payload

private fun imagePreprocessSourceFromBackendSource(sourceType: String): ImagePreprocessSource =
    when (sourceType) {
        "screenshot_share", "recent_screenshot_assist" -> ImagePreprocessSource.SCREENSHOT
        else -> ImagePreprocessSource.PHOTO_PICKER
    }
