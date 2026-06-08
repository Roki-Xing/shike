package cn.shike.app.data

import java.security.MessageDigest
import kotlin.math.roundToInt

data class ImageDimensions(
    val width: Int,
    val height: Int,
)

data class ImageChromeCrop(
    val left: Int,
    val top: Int,
    val right: Int,
    val bottom: Int,
    val outputDimensions: ImageDimensions,
) {
    companion object {
        val NONE = ImageChromeCrop(
            left = 0,
            top = 0,
            right = 0,
            bottom = 0,
            outputDimensions = ImageDimensions(width = 0, height = 0),
        )
    }
}

enum class ImagePreprocessSource {
    SCREENSHOT,
    PHOTO_PICKER,
    CAMERA,
}

object ImagePreprocessPolicy {
    const val MAX_EDGE = 1600
    const val THUMBNAIL_MAX_EDGE = 360
    const val THUMBNAIL_CACHE_DIR = "shike-image-thumbnails"
    const val JPEG_QUALITY = 82
    const val OUTPUT_MIME = "image/jpeg"
    const val EXIF_NORMAL = 1
    const val EXIF_ROTATE_90 = 6
    const val EXIF_ROTATE_180 = 3
    const val EXIF_ROTATE_270 = 8

    fun sampleSizeFor(width: Int, height: Int, maxEdge: Int = MAX_EDGE): Int {
        var sample = 1
        while (width / sample > maxEdge || height / sample > maxEdge) {
            sample *= 2
        }
        return sample
    }

    fun outputDimensionsFor(width: Int, height: Int, exifOrientation: Int): ImageDimensions =
        when (exifOrientation) {
            EXIF_ROTATE_90, EXIF_ROTATE_270 -> ImageDimensions(width = height, height = width)
            else -> ImageDimensions(width = width, height = height)
        }

    fun thumbnailDimensionsFor(
        width: Int,
        height: Int,
        maxEdge: Int = THUMBNAIL_MAX_EDGE,
    ): ImageDimensions {
        val longEdge = maxOf(width, height)
        if (longEdge <= maxEdge) {
            return ImageDimensions(width = width, height = height)
        }
        val scale = maxEdge.toDouble() / longEdge.toDouble()
        return ImageDimensions(
            width = (width * scale).roundToInt().coerceAtLeast(1),
            height = (height * scale).roundToInt().coerceAtLeast(1),
        )
    }

    fun thumbnailFileNameFor(sha256: String): String = "${sha256.lowercase()}-thumb.jpg"

    fun chromeCropFor(
        width: Int,
        height: Int,
        source: ImagePreprocessSource,
    ): ImageChromeCrop {
        if (source != ImagePreprocessSource.SCREENSHOT || width < 640 || height < 1000) {
            return ImageChromeCrop.NONE
        }
        if (height < width * 16 / 10) {
            return ImageChromeCrop.NONE
        }
        val top = height * 6 / 100
        val bottom = height * 5 / 100
        val croppedHeight = height - top - bottom
        if (croppedHeight <= 0) {
            return ImageChromeCrop.NONE
        }
        return ImageChromeCrop(
            left = 0,
            top = top,
            right = 0,
            bottom = bottom,
            outputDimensions = ImageDimensions(width = width, height = croppedHeight),
        )
    }

    fun mimeForBytes(bytes: ByteArray): String? =
        when {
            bytes.size >= 3 &&
                bytes[0].toInt() and 0xFF == 0xFF &&
                bytes[1].toInt() and 0xFF == 0xD8 &&
                bytes[2].toInt() and 0xFF == 0xFF -> "image/jpeg"
            bytes.size >= 8 &&
                bytes[0].toInt() and 0xFF == 0x89 &&
                bytes[1] == 0x50.toByte() &&
                bytes[2] == 0x4E.toByte() &&
                bytes[3] == 0x47.toByte() &&
                bytes[4] == 0x0D.toByte() &&
                bytes[5] == 0x0A.toByte() &&
                bytes[6] == 0x1A.toByte() &&
                bytes[7] == 0x0A.toByte() -> "image/png"
            bytes.size >= 12 &&
                bytes[0] == 'R'.code.toByte() &&
                bytes[1] == 'I'.code.toByte() &&
                bytes[2] == 'F'.code.toByte() &&
                bytes[3] == 'F'.code.toByte() &&
                bytes[8] == 'W'.code.toByte() &&
                bytes[9] == 'E'.code.toByte() &&
                bytes[10] == 'B'.code.toByte() &&
                bytes[11] == 'P'.code.toByte() -> "image/webp"
            else -> null
        }

    fun sha256Hex(bytes: ByteArray): String {
        val digest = MessageDigest.getInstance("SHA-256").digest(bytes)
        return digest.joinToString("") { "%02x".format(it) }
    }
}
