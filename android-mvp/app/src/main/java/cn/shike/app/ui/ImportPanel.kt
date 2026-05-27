package cn.shike.app.ui

import android.graphics.Bitmap
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.sp

@Composable
fun ImportPanel(
    captureSource: String,
    capturedBitmap: Bitmap?,
    modelStatus: String,
    ocrDraft: String,
    onOcrDraftChange: (String) -> Unit,
    backendUrl: String,
    onBackendUrlChange: (String) -> Unit,
    onSaveBackendUrl: () -> Unit,
    cloudEnhancedEnabled: Boolean,
    onGallery: () -> Unit,
    onCamera: () -> Unit,
    onManualInput: () -> Unit,
    onBackendCourse: () -> Unit,
    onBackendEvent: () -> Unit,
    onCourse: () -> Unit,
    onEvent: () -> Unit,
) {
    SectionCard("采集与解析") {
        Text("相册截图 / 拍照导入 / 文本分享", color = Color(0xFF667085), fontSize = 12.sp)
        KeyValue("本地恢复", "已保存到收件箱缓存")
        ImportCaptureActions(
            onGallery = onGallery,
            onCamera = onCamera,
            onManualInput = onManualInput,
        )
        Text("OCR 失败、无文字或低质量图片时，可手动继续编辑草稿并解析。", color = Color(0xFFF97316), fontSize = 12.sp)
        KeyValue("采集来源", captureSource)
        KeyValue("模型状态", modelStatus)
        BackendEndpointControls(
            backendUrl = backendUrl,
            onBackendUrlChange = onBackendUrlChange,
            onSaveBackendUrl = onSaveBackendUrl,
        )
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
        Text("服务不可用时自动回退本地 MockModelAdapter；后端失败，回退本地 MockModelAdapter。", color = Color(0xFF667085), fontSize = 12.sp)
        OfflineSampleActions(
            onCourse = onCourse,
            onEvent = onEvent,
        )
    }
}
