package cn.shike.app.system

import android.content.ContentResolver
import android.content.Context
import android.content.IntentSender
import android.os.Build
import android.provider.MediaStore
import androidx.core.net.toUri
import cn.shike.app.data.ImageCleanupStatus

sealed class SourceImageCleanupRequest {
    data class SystemTrashConfirmation(val intentSender: IntentSender) : SourceImageCleanupRequest()
    data class NotSupported(val status: ImageCleanupStatus = ImageCleanupStatus.NOT_SUPPORTED) : SourceImageCleanupRequest()
}

class SourceImageCleanupManager(
    private val context: Context,
) {
    fun canTrash(uri: String?): Boolean =
        Build.VERSION.SDK_INT >= Build.VERSION_CODES.R && isMediaStoreUri(uri)

    fun requestTrash(uri: String?): SourceImageCleanupRequest {
        if (!canTrash(uri)) {
            return SourceImageCleanupRequest.NotSupported()
        }
        val mediaUri = uri!!.toUri()
        return runCatching {
            SourceImageCleanupRequest.SystemTrashConfirmation(
                MediaStore.createTrashRequest(
                    context.contentResolver,
                    listOf(mediaUri),
                    true,
                ).intentSender,
            )
        }.getOrElse {
            SourceImageCleanupRequest.NotSupported(ImageCleanupStatus.FAILED)
        }
    }
}

fun isMediaStoreUri(uri: String?): Boolean =
    uri
        ?.takeIf { it.isNotBlank() }
        ?.let { value ->
            val prefix = "${ContentResolver.SCHEME_CONTENT}://${MediaStore.AUTHORITY}/"
            value.startsWith(prefix)
        } ?: false
