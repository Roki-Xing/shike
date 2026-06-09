package cn.shike.app.data

import org.json.JSONArray
import org.json.JSONObject
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL
import java.time.LocalDate

data class BackendImagePayload(
    val dataUrl: String,
    val mime: String,
    val width: Int,
    val height: Int,
    val sha256: String,
)

fun callAnalyzeImageApi(
    backendBaseUrl: String,
    sourceType: String,
    ocrTextHint: String,
    scene: String,
    image: BackendImagePayload,
    allowCloudImage: Boolean = true,
): BackendAnalysisOutcome {
    val connection = (URL("${normalizeBackendUrl(backendBaseUrl)}${backendAnalysisPathForImage()}").openConnection() as HttpURLConnection).apply {
        requestMethod = "POST"
        connectTimeout = 8000
        readTimeout = 60000
        setRequestProperty("Content-Type", "application/json; charset=utf-8")
        doOutput = true
    }
    val payload = buildAnalyzeImageRequestPayload(
        inputId = "android-image-${System.currentTimeMillis()}",
        sourceType = sourceType,
        ocrTextHint = ocrTextHint,
        scene = scene,
        currentDate = LocalDate.now().toString(),
        image = image,
        allowCloudImage = allowCloudImage,
    )
    OutputStreamWriter(connection.outputStream, Charsets.UTF_8).use { writer ->
        writer.write(payload.toString())
    }
    if (connection.responseCode !in 200..299) {
        throw IllegalStateException("Analyze image failed: HTTP ${connection.responseCode}")
    }
    val body = connection.inputStream.bufferedReader(Charsets.UTF_8).use { it.readText() }
    val item = itemFromAnalyzeImageJson(JSONObject(body), ocrTextHint)
    return if (item.rawText.contains("manual_review", ignoreCase = true) || item.scene == "待确认") {
        backendImageManualReviewOutcome(item)
    } else {
        backendImageSuccessOutcome(item)
    }
}

fun buildAnalyzeImageRequestPayload(
    inputId: String,
    sourceType: String,
    ocrTextHint: String,
    scene: String,
    currentDate: String,
    image: BackendImagePayload,
    allowCloudImage: Boolean = true,
): JSONObject =
    JSONObject()
        .put("input_id", inputId)
        .put("source_type", sourceType)
        .put("image", JSONObject()
            .put("data_url", image.dataUrl)
            .put("mime", image.mime)
            .put("width", image.width.coerceAtLeast(1))
            .put("height", image.height.coerceAtLeast(1))
            .put("sha256", image.sha256))
        .put("ocr_text_hint", ocrTextHint)
        .put("ocr_blocks", JSONArray())
        .put("user_timezone", "Asia/Shanghai")
        .put("current_date", currentDate)
        .put("locale", "zh-CN")
        .put("scene_hint", sceneHint(scene))
        .put("allow_cloud_image", allowCloudImage)

fun backendAnalysisPathFor(input: BackendAnalysisInput): String =
    if (input.hasImageForCloudAnalysis) backendAnalysisPathForImage() else "/v1/analyze"

fun backendAnalysisPathForImage(): String = "/v2/analyze-image"

fun backendImageSourceTypeFromCaptureSource(captureSource: String): String =
    when {
        "相机" in captureSource || "拍照" in captureSource -> "camera"
        "分享" in captureSource -> "screenshot_share"
        "截图助手" in captureSource -> "recent_screenshot_assist"
        "手动输入" in captureSource -> "manual"
        else -> "photo_picker"
    }
