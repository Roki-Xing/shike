package cn.shike.app.system

import android.content.Context
import android.content.IntentSender

fun createScreenshotDeleteRequest(context: Context, sourceMediaStoreUri: String?): IntentSender? {
    return when (val request = SourceImageCleanupManager(context).requestTrash(sourceMediaStoreUri)) {
        is SourceImageCleanupRequest.SystemTrashConfirmation -> request.intentSender
        is SourceImageCleanupRequest.NotSupported -> null
    }
}

fun screenshotCleanupUnsupportedMessage(): String =
    "当前来源不支持直接清理原图，你可以稍后在相册中删除。"
