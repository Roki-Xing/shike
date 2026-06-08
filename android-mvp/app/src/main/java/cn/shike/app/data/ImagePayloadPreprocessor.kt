package cn.shike.app.data

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Matrix
import android.media.ExifInterface
import android.util.Base64
import java.io.ByteArrayInputStream
import java.io.ByteArrayOutputStream
import java.io.File

data class ImagePreprocessResult(
    val payload: BackendImagePayload,
    val thumbnailUri: String?,
)

object ImagePayloadPreprocessor {
    fun fromBytes(
        bytes: ByteArray,
        source: ImagePreprocessSource = ImagePreprocessSource.PHOTO_PICKER,
    ): BackendImagePayload? =
        fromBytesWithThumbnail(bytes = bytes, source = source, thumbnailCacheRoot = null)?.payload

    fun fromBytesWithThumbnail(
        bytes: ByteArray,
        source: ImagePreprocessSource = ImagePreprocessSource.PHOTO_PICKER,
        thumbnailCacheRoot: File? = null,
    ): ImagePreprocessResult? {
        if (ImagePreprocessPolicy.mimeForBytes(bytes) == null) {
            return null
        }
        val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
        BitmapFactory.decodeByteArray(bytes, 0, bytes.size, bounds)
        if (bounds.outWidth <= 0 || bounds.outHeight <= 0) {
            return null
        }
        val decodeOptions = BitmapFactory.Options().apply {
            inSampleSize = ImagePreprocessPolicy.sampleSizeFor(bounds.outWidth, bounds.outHeight)
        }
        val decoded = BitmapFactory.decodeByteArray(bytes, 0, bytes.size, decodeOptions) ?: return null
        return fromBitmapWithThumbnail(
            bitmap = decoded,
            exifOrientation = readExifOrientation(bytes),
            source = source,
            thumbnailCacheRoot = thumbnailCacheRoot,
        )
    }

    fun fromBitmap(
        bitmap: Bitmap,
        exifOrientation: Int = ImagePreprocessPolicy.EXIF_NORMAL,
        source: ImagePreprocessSource = ImagePreprocessSource.CAMERA,
    ): BackendImagePayload? =
        fromBitmapWithThumbnail(
            bitmap = bitmap,
            exifOrientation = exifOrientation,
            source = source,
            thumbnailCacheRoot = null,
        )?.payload

    fun fromBitmapWithThumbnail(
        bitmap: Bitmap,
        exifOrientation: Int = ImagePreprocessPolicy.EXIF_NORMAL,
        source: ImagePreprocessSource = ImagePreprocessSource.CAMERA,
        thumbnailCacheRoot: File? = null,
    ): ImagePreprocessResult? {
        val normalized = normalizedBitmap(bitmap, exifOrientation)
        val cropped = cropChromeIfNeeded(normalized, source)
        val output = ByteArrayOutputStream()
        if (!cropped.compress(Bitmap.CompressFormat.JPEG, ImagePreprocessPolicy.JPEG_QUALITY, output)) {
            return null
        }
        val jpegBytes = output.toByteArray()
        val sha256 = ImagePreprocessPolicy.sha256Hex(jpegBytes)
        val encoded = Base64.encodeToString(jpegBytes, Base64.NO_WRAP)
        val thumbnailUri = thumbnailCacheRoot?.let { cacheRoot ->
            buildThumbnailBytes(cropped)?.let { thumbnailBytes ->
                ImageThumbnailCache.cacheThumbnailBytes(cacheRoot, sha256, thumbnailBytes)
            }
        }
        return ImagePreprocessResult(
            payload = BackendImagePayload(
                dataUrl = "data:image/jpeg;base64,$encoded",
                mime = ImagePreprocessPolicy.OUTPUT_MIME,
                width = cropped.width.coerceAtLeast(1),
                height = cropped.height.coerceAtLeast(1),
                sha256 = sha256,
            ),
            thumbnailUri = thumbnailUri,
        )
    }

    private fun readExifOrientation(bytes: ByteArray): Int =
        runCatching {
            ExifInterface(ByteArrayInputStream(bytes)).getAttributeInt(
                ExifInterface.TAG_ORIENTATION,
                ImagePreprocessPolicy.EXIF_NORMAL,
            )
        }.getOrDefault(ImagePreprocessPolicy.EXIF_NORMAL)

    private fun normalizedBitmap(bitmap: Bitmap, exifOrientation: Int): Bitmap {
        val rotation = when (exifOrientation) {
            ImagePreprocessPolicy.EXIF_ROTATE_90 -> 90f
            ImagePreprocessPolicy.EXIF_ROTATE_180 -> 180f
            ImagePreprocessPolicy.EXIF_ROTATE_270 -> 270f
            else -> 0f
        }
        if (rotation == 0f) {
            return bitmap
        }
        val matrix = Matrix().apply { postRotate(rotation) }
        return Bitmap.createBitmap(bitmap, 0, 0, bitmap.width, bitmap.height, matrix, true)
    }

    private fun cropChromeIfNeeded(bitmap: Bitmap, source: ImagePreprocessSource): Bitmap {
        val crop = ImagePreprocessPolicy.chromeCropFor(
            width = bitmap.width,
            height = bitmap.height,
            source = source,
        )
        if (crop == ImageChromeCrop.NONE) {
            return bitmap
        }
        return Bitmap.createBitmap(
            bitmap,
            crop.left,
            crop.top,
            crop.outputDimensions.width,
            crop.outputDimensions.height,
        )
    }

    private fun buildThumbnailBytes(bitmap: Bitmap): ByteArray? {
        val dimensions = ImagePreprocessPolicy.thumbnailDimensionsFor(bitmap.width, bitmap.height)
        val thumbnail = if (dimensions.width == bitmap.width && dimensions.height == bitmap.height) {
            bitmap
        } else {
            Bitmap.createScaledBitmap(bitmap, dimensions.width, dimensions.height, true)
        }
        val output = ByteArrayOutputStream()
        if (!thumbnail.compress(Bitmap.CompressFormat.JPEG, ImagePreprocessPolicy.JPEG_QUALITY, output)) {
            return null
        }
        return output.toByteArray()
    }
}
