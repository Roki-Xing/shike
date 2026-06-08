package cn.shike.app.data

import java.io.File
import java.net.URI
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test
import org.junit.rules.TemporaryFolder

class ImageThumbnailCacheTest {
    @get:Rule
    val temporaryFolder = TemporaryFolder()

    @Test
    fun cacheThumbnailBytes_persistsPrivateDigestNamedJpeg() {
        val root = temporaryFolder.newFolder("cache-root")
        val digest = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
        val bytes = byteArrayOf(0xFF.toByte(), 0xD8.toByte(), 0x01, 0x02, 0xFF.toByte(), 0xD9.toByte())

        val uri = ImageThumbnailCache.cacheThumbnailBytes(root, digest, bytes)

        val file = File(URI(uri))
        assertTrue(file.exists())
        assertEquals("shike-image-thumbnails", requireNotNull(file.parentFile).name)
        assertEquals(ImagePreprocessPolicy.thumbnailFileNameFor(digest), file.name)
        assertEquals(bytes.toList(), file.readBytes().toList())
    }

    @Test
    fun cacheThumbnailBytes_reusesExistingFileForSameDigest() {
        val root = temporaryFolder.newFolder("cache-root")
        val digest = "abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789"
        val first = byteArrayOf(0xFF.toByte(), 0xD8.toByte(), 0x11, 0xFF.toByte(), 0xD9.toByte())
        val second = byteArrayOf(0xFF.toByte(), 0xD8.toByte(), 0x22, 0xFF.toByte(), 0xD9.toByte())

        val firstUri = ImageThumbnailCache.cacheThumbnailBytes(root, digest, first)
        val secondUri = ImageThumbnailCache.cacheThumbnailBytes(root, digest, second)

        assertEquals(firstUri, secondUri)
        assertEquals(first.toList(), File(URI(secondUri)).readBytes().toList())
    }
}
