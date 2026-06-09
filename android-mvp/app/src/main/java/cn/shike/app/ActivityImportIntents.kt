package cn.shike.app

import android.content.Intent
import android.net.Uri
import cn.shike.app.data.ScreenshotCandidate
import cn.shike.app.data.screenshotCandidateFromNotificationImport
import cn.shike.app.system.ACTION_IMPORT_SCREENSHOT
import cn.shike.app.system.EXTRA_SCREENSHOT_CREATED_AT_MILLIS
import cn.shike.app.system.EXTRA_SCREENSHOT_DISPLAY_NAME_DIGEST
import cn.shike.app.system.EXTRA_SCREENSHOT_HEIGHT
import cn.shike.app.system.EXTRA_SCREENSHOT_URI
import cn.shike.app.system.EXTRA_SCREENSHOT_WIDTH

fun screenshotCandidateFromImportIntent(intent: Intent?, nowMillis: Long): ScreenshotCandidate? {
    if (intent?.action != ACTION_IMPORT_SCREENSHOT) {
        return null
    }
    return screenshotCandidateFromNotificationImport(
        contentUri = intent.getStringExtra(EXTRA_SCREENSHOT_URI),
        createdAtMillis = intent.getLongExtra(EXTRA_SCREENSHOT_CREATED_AT_MILLIS, 0L),
        width = intent.getIntExtra(EXTRA_SCREENSHOT_WIDTH, 0),
        height = intent.getIntExtra(EXTRA_SCREENSHOT_HEIGHT, 0),
        displayNameDigest = intent.getStringExtra(EXTRA_SCREENSHOT_DISPLAY_NAME_DIGEST),
        nowMillis = nowMillis,
    )
}

fun sharedImageUriFromIntent(intent: Intent): Uri? =
    if (android.os.Build.VERSION.SDK_INT >= 33) {
        intent.getParcelableExtra(Intent.EXTRA_STREAM, Uri::class.java)
    } else {
        @Suppress("DEPRECATION")
        intent.getParcelableExtra(Intent.EXTRA_STREAM) as? Uri
    }

fun sharedTextFromIntent(intent: Intent?): String? =
    intent
        ?.takeIf { it.action == Intent.ACTION_SEND && it.type.orEmpty().startsWith("text/") }
        ?.getStringExtra(Intent.EXTRA_TEXT)
        ?.takeIf { it.isNotBlank() }

fun screenshotCandidateFromSharedImage(uri: Uri, nowMillis: Long): ScreenshotCandidate =
    ScreenshotCandidate(
        contentUri = uri.toString(),
        createdAtMillis = nowMillis,
        width = 0,
        height = 0,
        displayNameDigest = uri.toString().hashCode().toUInt().toString(16),
        sourceLabel = "系统截图分享导入",
    )
