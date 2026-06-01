package cn.shike.app.ui

import android.graphics.Bitmap
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun CaptureEntryPanel(
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
    SectionCard("导入") {
        Text("从相册选择通知截图、拍海报公告，或在没有 OCR / OCR 失败时直接粘贴文字继续。", style = ShikeTypography.Body)
        ImportCaptureActions(
            onGallery = onGallery,
            onCamera = onCamera,
            onManualInput = onManualInput,
        )
        KeyValue("本地恢复", "已保存到收件箱缓存")
        KeyValue("采集来源", captureSource)
        KeyValue("模型状态", modelStatus)
        OcrDraftEditor(
            ocrDraft = ocrDraft,
            onOcrDraftChange = onOcrDraftChange,
        )
        CapturedImagePreview(capturedBitmap = capturedBitmap)
        BackendAnalysisControls(
            cloudEnhancedEnabled = cloudEnhancedEnabled,
            onBackendCourse = onBackendCourse,
            onBackendEvent = onBackendEvent,
        )
        Text("云侧不可用时可手动确认继续，后端地址和样例按钮在设置或调试页管理。", style = ShikeTypography.Caption)
    }
}
