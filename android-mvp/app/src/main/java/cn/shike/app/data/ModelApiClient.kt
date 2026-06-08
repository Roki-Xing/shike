package cn.shike.app.data

import cn.shike.app.domain.ShikeItem
import org.json.JSONArray
import org.json.JSONObject
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URI
import java.net.URL
import java.time.LocalDate

data class BackendImagePayload(
    val dataUrl: String,
    val mime: String,
    val width: Int,
    val height: Int,
    val sha256: String,
)

fun callAnalyzeApi(backendBaseUrl: String, sourceType: String, ocrText: String, scene: String): ShikeItem {
    val connection = (URL("${normalizeBackendUrl(backendBaseUrl)}/v1/analyze").openConnection() as HttpURLConnection).apply {
        requestMethod = "POST"
        connectTimeout = 8000
        readTimeout = 60000
        setRequestProperty("Content-Type", "application/json; charset=utf-8")
        doOutput = true
    }
    val payload = buildAnalyzeRequestPayload(
        inputId = "android-demo-${System.currentTimeMillis()}",
        sourceType = sourceType,
        ocrText = ocrText,
        scene = scene,
    )
    OutputStreamWriter(connection.outputStream, Charsets.UTF_8).use { writer ->
        writer.write(payload.toString())
    }
    if (connection.responseCode !in 200..299) {
        throw IllegalStateException("Analyze failed: HTTP ${connection.responseCode}")
    }
    val body = connection.inputStream.bufferedReader(Charsets.UTF_8).use { it.readText() }
    return itemFromAnalyzeJson(JSONObject(body), ocrText)
}

fun buildAnalyzeRequestPayload(inputId: String, sourceType: String, ocrText: String, scene: String): JSONObject =
    JSONObject()
        .put("input_id", inputId)
        .put("source_type", sourceType)
        .put("ocr_text", ocrText)
        .put("scene_hint", sceneHint(scene))
        .put("locale", "zh-CN")
        .put("user_timezone", "Asia/Shanghai")

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

fun itemFromAnalyzeJson(json: JSONObject, fallbackText: String): ShikeItem {
    val sceneType = json.optString("scene_type")
    val scene = when (sceneType) {
        "event_poster" -> "活动海报"
        "course_notice" -> "课程通知"
        else -> "待确认"
    }
    val time = json.optJSONObject("time")
    val location = json.optJSONObject("location")
    return ShikeItem(
        title = json.optString("title", "待确认碎片"),
        scene = scene,
        time = listOfNotNull(
            time?.optString("start_text")?.takeIf { it.isNotBlank() },
            time?.optString("deadline_text")?.takeIf { it.isNotBlank() },
        ).joinToString(" / ").ifBlank { "待确认" },
        location = location?.optString("raw")?.takeIf { it.isNotBlank() } ?: "待确认",
        status = "待确认",
        actions = actionsFromJson(json.optJSONArray("suggested_actions")),
        startEpochMillis = when (sceneType) {
            "event_poster" -> sampleEvent().startEpochMillis
            else -> sampleCourse().startEpochMillis
        },
        rawText = "后端 /v1/analyze：${json.optString("explanation", fallbackText)}",
    )
}

fun itemFromAnalyzeImageJson(json: JSONObject, fallbackText: String): ShikeItem {
    val sceneType = json.optString("scene_type")
    val scene = when (sceneType) {
        "event_poster" -> "活动海报"
        "course_notice" -> "课程通知"
        "meeting_notice" -> "会议通知"
        "assignment_deadline" -> "作业截止"
        "exam_notice" -> "考试通知"
        "travel_ticket" -> "出行票据"
        else -> "待确认"
    }
    val time = json.optJSONObject("time")
    val location = json.optJSONObject("location")
    val explanation = json.optString("explanation", fallbackText)
    val risks = stringsFromJson(json.optJSONArray("risks")).joinToString("；")
    val missingFields = stringsFromJson(json.optJSONArray("missing_fields")).joinToString("、")
    val reviewTail = listOfNotNull(
        risks.takeIf { it.isNotBlank() }?.let { "风险：$it" },
        missingFields.takeIf { it.isNotBlank() }?.let { "待补：$it" },
    ).joinToString("\n")
    return ShikeItem(
        title = json.optString("title", "待确认碎片"),
        scene = scene,
        time = listOfNotNull(
            time?.optString("start_text")?.takeIf { it.isNotBlank() },
            time?.optString("deadline_text")?.takeIf { it.isNotBlank() },
        ).joinToString(" / ").ifBlank { "待确认" },
        location = location?.optString("raw")?.takeIf { it.isNotBlank() } ?: "待确认",
        status = "待确认",
        actions = actionsFromJson(json.optJSONArray("suggested_actions")),
        startEpochMillis = when (sceneType) {
            "event_poster" -> sampleEvent().startEpochMillis
            else -> sampleCourse().startEpochMillis
        },
        rawText = listOf("后端 /v2/analyze-image：$explanation", reviewTail)
            .filter { it.isNotBlank() }
            .joinToString("\n"),
    )
}

fun actionsFromJson(actions: JSONArray?): List<String> {
    if (actions == null || actions.length() == 0) {
        return listOf("稍后确认")
    }
    return (0 until actions.length()).mapNotNull { index ->
        actions.optJSONObject(index)?.optString("label")?.takeIf { it.isNotBlank() }
    }.ifEmpty { listOf("稍后确认") }
}

fun stringsFromJson(values: JSONArray?): List<String> {
    if (values == null || values.length() == 0) {
        return emptyList()
    }
    return (0 until values.length()).mapNotNull { index ->
        values.optString(index).takeIf { it.isNotBlank() }
    }
}

fun sceneHint(scene: String): String =
    when {
        "活动" in scene -> "event_poster"
        "作业" in scene || "截止" in scene -> "assignment_deadline"
        "会议" in scene || "周会" in scene || "例会" in scene -> "meeting_notice"
        "面试" in scene || "笔试" in scene -> "interview_notice"
        "出行" in scene || "车票" in scene || "高铁" in scene || "航班" in scene -> "travel_ticket"
        else -> "course_notice"
    }

fun normalizeBackendUrl(url: String): String {
    val trimmed = url.trim()
    if (trimmed.isBlank()) return DEFAULT_BACKEND_BASE_URL

    val withScheme =
        if (trimmed.startsWith("http://") || trimmed.startsWith("https://")) trimmed
        else "http://$trimmed"

    val uri = runCatching { URI(withScheme) }.getOrNull()
    val host = uri?.host
    val port = uri?.port ?: -1
    if (uri == null || host.isNullOrBlank()) {
        return withScheme.trimEnd('/')
    }

    val base = buildString {
        append(uri.scheme)
        append("://")
        append(host)
        if (port != -1) {
            append(":")
            append(port)
        }
    }
    return base.trimEnd('/')
}
