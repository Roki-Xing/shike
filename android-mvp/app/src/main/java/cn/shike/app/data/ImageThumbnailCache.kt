package cn.shike.app.data

import java.io.File

data class ClearThumbnailCacheResult(
    val deletedFiles: Int,
    val success: Boolean,
)

object ImageThumbnailCache {
    fun cacheThumbnailBytes(
        cacheRoot: File,
        imageSha256: String,
        jpegBytes: ByteArray,
    ): String {
        val directory = File(cacheRoot, ImagePreprocessPolicy.THUMBNAIL_CACHE_DIR)
        if (!directory.exists()) {
            directory.mkdirs()
        }
        val file = File(directory, ImagePreprocessPolicy.thumbnailFileNameFor(imageSha256))
        if (!file.exists()) {
            file.writeBytes(jpegBytes)
        }
        return file.toURI().toString()
    }

    fun clearThumbnailCache(cacheRoot: File): ClearThumbnailCacheResult {
        val directory = File(cacheRoot, ImagePreprocessPolicy.THUMBNAIL_CACHE_DIR)
        if (!directory.exists()) {
            return ClearThumbnailCacheResult(deletedFiles = 0, success = true)
        }
        val deletedFiles = directory.walkTopDown().count { it.isFile }
        val success = directory.deleteRecursively()
        return ClearThumbnailCacheResult(deletedFiles = deletedFiles, success = success && !directory.exists())
    }
}
