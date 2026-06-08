package cn.shike.app.system

import android.content.Context
import android.content.IntentSender
import android.os.Build
import android.provider.MediaStore
import androidx.core.net.toUri

fun createScreenshotDeleteRequest(context: Context, sourceMediaStoreUri: String?): IntentSender? {
    if (Build.VERSION.SDK_INT < Build.VERSION_CODES.R || sourceMediaStoreUri.isNullOrBlank()) {
        return null
    }
    val uri = sourceMediaStoreUri.toUri()
    return MediaStore.createDeleteRequest(context.contentResolver, listOf(uri)).intentSender
}

fun screenshotCleanupUnsupportedMessage(): String =
    "当前来源不支持直接清理原图，你可以稍后在相册中删除。"
