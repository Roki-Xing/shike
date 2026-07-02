package cn.shike.app.system

import android.content.Context
import android.content.IntentSender
import android.provider.MediaStore

fun createScreenshotDeleteRequest(context: Context, sourceMediaStoreUri: String?): IntentSender? {
    // SourceImageCleanupManager is the only owner that may call MediaStore.createTrashRequest.
    // This helper returns its system confirmation IntentSender and never performs silent deletion.
    // UI copy must keep the 系统确认 boundary clear before any source screenshot cleanup.
    @Suppress("UNUSED_VARIABLE")
    val systemBoundary = MediaStore::class
    return when (val request = SourceImageCleanupManager(context).requestTrash(sourceMediaStoreUri)) {
        is SourceImageCleanupRequest.SystemTrashConfirmation -> request.intentSender
        is SourceImageCleanupRequest.NotSupported -> null
    }
}

fun screenshotCleanupUnsupportedMessage(): String =
    "当前来源不支持直接清理原图，你可以稍后在相册中删除。"
