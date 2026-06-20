package cn.shike.app.ui

import android.graphics.Bitmap
import androidx.compose.runtime.Composable

@Composable
fun ImportPanel(
    captureSource: String,
    capturedBitmap: Bitmap?,
    ocrDraft: String,
    onOcrDraftChange: (String) -> Unit,
    onGallery: () -> Unit,
    onCamera: () -> Unit,
    onManualInput: () -> Unit,
) {
    CaptureEntryPanel(
        captureSource = captureSource,
        capturedBitmap = capturedBitmap,
        ocrDraft = ocrDraft,
        onOcrDraftChange = onOcrDraftChange,
        onGallery = onGallery,
        onCamera = onCamera,
        onManualInput = onManualInput,
    )
}
