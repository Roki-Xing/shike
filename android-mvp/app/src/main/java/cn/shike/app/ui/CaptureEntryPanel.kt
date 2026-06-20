package cn.shike.app.ui

import android.graphics.Bitmap
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun CaptureEntryPanel(
    captureSource: String,
    capturedBitmap: Bitmap?,
    ocrDraft: String,
    onOcrDraftChange: (String) -> Unit,
    onGallery: () -> Unit,
    onCamera: () -> Unit,
    onManualInput: () -> Unit,
) {
    SectionCard("导入") {
        Text("从相册选择截图、拍海报公告，或直接粘贴文字继续。", style = ShikeTypography.Body)
        ImportCaptureActions(
            onGallery = onGallery,
            onCamera = onCamera,
            onManualInput = onManualInput,
        )
        KeyValue("来源", captureSource)
        Text("识别原文默认折叠；生成行动卡后再确认细节。", style = ShikeTypography.Caption)
        OcrDraftEditor(
            ocrDraft = ocrDraft,
            onOcrDraftChange = onOcrDraftChange,
        )
        CapturedImagePreview(capturedBitmap = capturedBitmap)
        Text("AI 解析不可用时也会保留待确认行动卡。", style = ShikeTypography.Caption)
    }
}
