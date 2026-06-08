package cn.shike.app.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class ImagePreprocessPolicyTest {
    @Test
    fun sampleSizeFor_limitsLongEdgeToConfiguredMaximum() {
        assertEquals(2, ImagePreprocessPolicy.sampleSizeFor(width = 3000, height = 1200))
        assertEquals(4, ImagePreprocessPolicy.sampleSizeFor(width = 5000, height = 3800))
        assertEquals(1, ImagePreprocessPolicy.sampleSizeFor(width = 1200, height = 900))
    }

    @Test
    fun outputDimensionsFor_swapsWidthAndHeightForRotatedExifOrientations() {
        assertEquals(
            ImageDimensions(width = 2400, height = 1080),
            ImagePreprocessPolicy.outputDimensionsFor(
                width = 1080,
                height = 2400,
                exifOrientation = ImagePreprocessPolicy.EXIF_ROTATE_90,
            ),
        )
        assertEquals(
            ImageDimensions(width = 2400, height = 1080),
            ImagePreprocessPolicy.outputDimensionsFor(
                width = 1080,
                height = 2400,
                exifOrientation = ImagePreprocessPolicy.EXIF_ROTATE_270,
            ),
        )
        assertEquals(
            ImageDimensions(width = 1080, height = 2400),
            ImagePreprocessPolicy.outputDimensionsFor(
                width = 1080,
                height = 2400,
                exifOrientation = ImagePreprocessPolicy.EXIF_NORMAL,
            ),
        )
    }

    @Test
    fun outputMimeAndDigest_matchBackendImageContract() {
        val digest = ImagePreprocessPolicy.sha256Hex("shike-image".toByteArray())

        assertEquals("image/jpeg", ImagePreprocessPolicy.OUTPUT_MIME)
        assertEquals(64, digest.length)
        assertTrue(digest.all { it in '0'..'9' || it in 'a'..'f' })
    }

    @Test
    fun thumbnailDimensionsFor_limitsLongEdgeWithoutUpscalingSmallImages() {
        assertEquals(
            ImageDimensions(width = 360, height = 180),
            ImagePreprocessPolicy.thumbnailDimensionsFor(width = 1440, height = 720),
        )
        assertEquals(
            ImageDimensions(width = 180, height = 360),
            ImagePreprocessPolicy.thumbnailDimensionsFor(width = 720, height = 1440),
        )
        assertEquals(
            ImageDimensions(width = 320, height = 240),
            ImagePreprocessPolicy.thumbnailDimensionsFor(width = 320, height = 240),
        )
    }

    @Test
    fun mimeForBytes_detectsSupportedImageFormatsByMagicBytes() {
        val jpeg = byteArrayOf(0xFF.toByte(), 0xD8.toByte(), 0xFF.toByte(), 0xE0.toByte())
        val png = byteArrayOf(
            0x89.toByte(),
            0x50,
            0x4E,
            0x47,
            0x0D,
            0x0A,
            0x1A,
            0x0A,
        )
        val webp = "RIFFxxxxWEBP".toByteArray()

        assertEquals("image/jpeg", ImagePreprocessPolicy.mimeForBytes(jpeg))
        assertEquals("image/png", ImagePreprocessPolicy.mimeForBytes(png))
        assertEquals("image/webp", ImagePreprocessPolicy.mimeForBytes(webp))
    }

    @Test
    fun mimeForBytes_rejectsNonImageBytes() {
        val text = "not an image".toByteArray()

        assertEquals(null, ImagePreprocessPolicy.mimeForBytes(text))
    }

    @Test
    fun chromeCropFor_cropsTallScreenshotChromeWithoutChangingWidth() {
        val crop = ImagePreprocessPolicy.chromeCropFor(
            width = 1080,
            height = 2400,
            source = ImagePreprocessSource.SCREENSHOT,
        )

        assertEquals(0, crop.left)
        assertEquals(144, crop.top)
        assertEquals(0, crop.right)
        assertEquals(120, crop.bottom)
        assertEquals(ImageDimensions(width = 1080, height = 2136), crop.outputDimensions)
    }

    @Test
    fun chromeCropFor_doesNotCropCameraImages() {
        val crop = ImagePreprocessPolicy.chromeCropFor(
            width = 1080,
            height = 2400,
            source = ImagePreprocessSource.CAMERA,
        )

        assertEquals(ImageChromeCrop.NONE, crop)
    }

    @Test
    fun chromeCropFor_keepsSmallScreenshotsUsable() {
        val crop = ImagePreprocessPolicy.chromeCropFor(
            width = 320,
            height = 480,
            source = ImagePreprocessSource.SCREENSHOT,
        )

        assertEquals(ImageChromeCrop.NONE, crop)
    }
}
