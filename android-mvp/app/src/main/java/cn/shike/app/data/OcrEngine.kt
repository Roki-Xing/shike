package cn.shike.app.data

enum class CaptureSourceType {
    Gallery,
    Camera,
    ShareText,
    Manual,
}

enum class PrivacyLevel {
    Synthetic,
    LocalOnly,
    CloudAllowed,
}

data class CaptureInput(
    val sourceType: CaptureSourceType,
    val sourceLabel: String,
    val localImageUri: String? = null,
    val thumbnailUri: String? = null,
    val manualText: String = "",
    val width: Int? = null,
    val height: Int? = null,
    val allowCloudEnhancement: Boolean = true,
)

data class OcrResult(
    val text: String,
    val confidence: Float,
    val engineName: String,
    val isRedacted: Boolean,
    val imageCleared: Boolean,
    val failureHint: String? = null,
)

interface OcrEngine {
    fun recognize(input: CaptureInput): OcrResult
}

class ManualOcrEngine : OcrEngine {
    override fun recognize(input: CaptureInput): OcrResult =
        OcrResult(
            text = input.manualText,
            confidence = if (input.manualText.isBlank()) 0f else 1f,
            engineName = "manual",
            isRedacted = false,
            imageCleared = input.localImageUri == null,
            failureHint = if (input.manualText.isBlank()) "未识别到稳定文字，可手动粘贴通知内容继续" else null,
        )
}

class MockOcrEngine : OcrEngine {
    override fun recognize(input: CaptureInput): OcrResult =
        when (input.sourceType) {
            CaptureSourceType.Camera, CaptureSourceType.Gallery -> pendingImageOcrResult()
            CaptureSourceType.ShareText, CaptureSourceType.Manual -> ManualOcrEngine().recognize(input)
        }
}

fun pendingImageOcrResult(): OcrResult =
    OcrResult(
        text = "",
        confidence = 0f,
        engineName = "image_pending",
        isRedacted = false,
        imageCleared = false,
        failureHint = "等待云侧图片解析；若识别失败，可手动补充识别到的文字。",
    )

fun captureSourceTypeFromChannel(channel: String): CaptureSourceType =
    when (channel) {
        "camera" -> CaptureSourceType.Camera
        "gallery" -> CaptureSourceType.Gallery
        "share" -> CaptureSourceType.ShareText
        else -> CaptureSourceType.Manual
    }
