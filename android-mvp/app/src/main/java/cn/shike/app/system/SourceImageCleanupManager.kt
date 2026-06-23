package cn.shike.app.system

import android.content.ContentResolver
import android.content.Context
import android.content.IntentSender
import android.os.Build
import android.provider.MediaStore
import androidx.core.net.toUri
import cn.shike.app.data.ImageCleanupStatus

enum class SourceUriCapability {
    STANDARD_MEDIASTORE_ITEM,
    PHOTO_PICKER_PROXY,
    DOCUMENT_URI,
    SHARED_PROVIDER,
    APP_TEMP_FILE,
    UNKNOWN,
}

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
    sourceUriCapabilityFor(uri) == SourceUriCapability.STANDARD_MEDIASTORE_ITEM

fun sourceUriCapabilityFor(uri: String?): SourceUriCapability {
    if (uri.isNullOrBlank()) return SourceUriCapability.UNKNOWN
    val value = uri.trim()
    val lower = value.lowercase()
    val mediaPrefix = "${ContentResolver.SCHEME_CONTENT}://${MediaStore.AUTHORITY}/"
    return when {
        lower.startsWith(mediaPrefix) && "/picker/" in lower ->
            SourceUriCapability.PHOTO_PICKER_PROXY
        lower.startsWith(mediaPrefix) && isConcreteMediaImageItem(lower.removePrefix(mediaPrefix)) ->
            SourceUriCapability.STANDARD_MEDIASTORE_ITEM
        lower.startsWith(mediaPrefix) ->
            SourceUriCapability.UNKNOWN
        lower.startsWith("${ContentResolver.SCHEME_CONTENT}://") && "documents" in lower.substringBefore('/', missingDelimiterValue = lower) ->
            SourceUriCapability.DOCUMENT_URI
        lower.startsWith("${ContentResolver.SCHEME_CONTENT}://") ->
            SourceUriCapability.SHARED_PROVIDER
        lower.startsWith("${ContentResolver.SCHEME_FILE}:") ->
            SourceUriCapability.APP_TEMP_FILE
        else ->
            SourceUriCapability.UNKNOWN
    }
}

private fun isConcreteMediaImageItem(path: String): Boolean =
    Regex("^[^/]+/images/media/[0-9]+$").matches(path)
