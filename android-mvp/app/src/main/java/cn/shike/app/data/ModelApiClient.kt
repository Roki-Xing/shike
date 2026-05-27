package cn.shike.app.data

import cn.shike.app.domain.ShikeItem
import org.json.JSONArray
import org.json.JSONObject
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URI
import java.net.URL

fun callAnalyzeApi(backendBaseUrl: String, sourceType: String, ocrText: String, scene: String): ShikeItem {
    val connection = (URL("${normalizeBackendUrl(backendBaseUrl)}/v1/analyze").openConnection() as HttpURLConnection).apply {
        requestMethod = "POST"
        connectTimeout = 1500
        readTimeout = 2500
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

fun actionsFromJson(actions: JSONArray?): List<String> {
    if (actions == null || actions.length() == 0) {
        return listOf("稍后确认")
    }
    return (0 until actions.length()).mapNotNull { index ->
        actions.optJSONObject(index)?.optString("label")?.takeIf { it.isNotBlank() }
    }.ifEmpty { listOf("稍后确认") }
}

fun sceneHint(scene: String): String =
    if ("活动" in scene) "event_poster" else "course_notice"

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
