package cn.shike.app.system

import org.junit.Assert.assertEquals
import org.junit.Test

class SourceImageCleanupManagerTest {
    @Test
    fun isMediaStoreUri_acceptsOnlySystemMediaContentUris() {
        assertEquals(true, isMediaStoreUri("content://media/external/images/media/42"))
        assertEquals(false, isMediaStoreUri("content://com.example.provider/image/42"))
        assertEquals(false, isMediaStoreUri("file:/private-cache/shike-image-thumbnails/thumb-42.jpg"))
        assertEquals(false, isMediaStoreUri(null))
    }
}
