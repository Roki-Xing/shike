package cn.shike.app.data

import java.io.File

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
}
