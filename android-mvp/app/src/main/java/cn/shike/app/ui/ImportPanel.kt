package cn.shike.app.ui

import android.graphics.Bitmap
import androidx.compose.runtime.Composable

@Composable
fun ImportPanel(
    captureSource: String,
    capturedBitmap: Bitmap?,
    modelStatus: String,
    ocrDraft: String,
    onOcrDraftChange: (String) -> Unit,
    cloudEnhancedEnabled: Boolean,
    onGallery: () -> Unit,
    onCamera: () -> Unit,
    onManualInput: () -> Unit,
    onBackendCourse: () -> Unit,
    onBackendEvent: () -> Unit,
) {
    CaptureEntryPanel(
        captureSource = captureSource,
        capturedBitmap = capturedBitmap,
        modelStatus = modelStatus,
        ocrDraft = ocrDraft,
        onOcrDraftChange = onOcrDraftChange,
        cloudEnhancedEnabled = cloudEnhancedEnabled,
        onGallery = onGallery,
        onCamera = onCamera,
        onManualInput = onManualInput,
        onBackendCourse = onBackendCourse,
        onBackendEvent = onBackendEvent,
    )
}
