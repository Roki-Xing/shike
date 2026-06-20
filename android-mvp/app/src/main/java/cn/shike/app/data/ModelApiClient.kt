package cn.shike.app.data

import cn.shike.app.domain.ShikeItem
import org.json.JSONArray
import org.json.JSONObject
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL
import java.time.ZoneId

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

fun itemFromAnalyzeJson(
    json: JSONObject,
    fallbackText: String,
    referenceNowMillis: Long = System.currentTimeMillis(),
    zoneId: ZoneId = ZoneId.of("Asia/Shanghai"),
): ShikeItem {
    val sceneType = json.safeString("scene_type")
    val scene = when (sceneType) {
        "event_poster" -> "活动海报"
        "course_notice" -> "课程通知"
        else -> "待确认"
    }
    val time = json.optJSONObject("time")
    val location = json.optJSONObject("location")
    val explanation = json.safeString("explanation").ifBlank { fallbackText }
    val timeText = displayTimeFrom(time)
    val preparationItems = preparationItemsFromJson(json)
    val taskSummary = json.optJSONObject("task")?.safeString("summary").orEmpty()
    val reviewTail = listOfNotNull(
        taskSummary.takeIf { it.isNotBlank() }?.let { "任务：$it" },
        preparationItems.takeIf { it.isNotEmpty() }?.let { "准备：${it.joinToString("、")}" },
    ).joinToString("\n")
    return ShikeItem(
        title = json.safeString("title").ifBlank { "待确认碎片" },
        scene = scene,
        time = timeText,
        location = location?.safeString("raw")?.takeIf { it.isNotBlank() } ?: "待确认",
        status = "待确认",
        actions = actionsFromJson(json.optJSONArray("suggested_actions")),
        startEpochMillis = startEpochMillisFromTime(time, fallbackText, referenceNowMillis, zoneId),
        rawText = listOf("云端 AI 解析：$explanation", reviewTail)
            .filter { it.isNotBlank() }
            .joinToString("\n"),
    )
}

fun itemFromAnalyzeImageJson(
    json: JSONObject,
    fallbackText: String,
    referenceNowMillis: Long = System.currentTimeMillis(),
    zoneId: ZoneId = ZoneId.of("Asia/Shanghai"),
): ShikeItem {
    val sceneType = json.safeString("scene_type")
    val scene = when (sceneType) {
        "event_poster" -> "活动海报"
        "course_notice" -> "课程通知"
        "meeting_notice" -> "会议通知"
        "interview_notice" -> "面试通知"
        "assignment_deadline" -> "作业截止"
        "exam_notice" -> "考试通知"
        "travel_ticket" -> "出行票据"
        else -> "待确认"
    }
    val time = json.optJSONObject("time")
    val location = json.optJSONObject("location")
    val task = json.optJSONObject("task")
    val explanation = json.safeString("explanation").ifBlank { fallbackText }
    val taskSummary = task?.safeString("summary").orEmpty()
    val preparationItems = preparationItemsFromJson(json)
    val confirmationItems = confirmationItemsFromJson(json)
    val timeText = displayTimeFrom(time)
    val reviewTail = listOfNotNull(
        taskSummary.takeIf { it.isNotBlank() }?.let { "任务：$it" },
        preparationItems.takeIf { it.isNotEmpty() }?.let { "准备：${it.joinToString("、")}" },
        confirmationItems.takeIf { it.isNotEmpty() }?.let { "需要确认：${it.joinToString("；")}" },
    ).joinToString("\n")
    return ShikeItem(
        title = json.safeString("title").ifBlank { "待确认碎片" },
        scene = scene,
        time = timeText,
        location = location?.safeString("raw")?.takeIf { it.isNotBlank() } ?: "待确认",
        status = "待确认",
        actions = actionsFromJson(json.optJSONArray("suggested_actions")),
        startEpochMillis = startEpochMillisFromTime(time, fallbackText, referenceNowMillis, zoneId),
        rawText = listOf("云端 AI 解析：$explanation", reviewTail)
            .filter { it.isNotBlank() }
            .joinToString("\n"),
    )
}

fun actionsFromJson(actions: JSONArray?): List<String> {
    if (actions == null || actions.length() == 0) {
        return listOf("稍后确认")
    }
    return (0 until actions.length()).mapNotNull { index ->
        actions.optJSONObject(index)?.safeString("label")?.takeIf { it.isNotBlank() }
    }.ifEmpty { listOf("稍后确认") }
}

fun stringsFromJson(values: JSONArray?): List<String> {
    if (values == null || values.length() == 0) {
        return emptyList()
    }
    return (0 until values.length()).mapNotNull { index ->
        values.safeArrayString(index).takeIf { it.isNotBlank() }
    }
}

fun preparationItemsFromJson(json: JSONObject): List<String> {
    val directItems = stringsFromJson(json.optJSONArray("preparation_items"))
    val checklistItems = checklistItemTextsFromJson(json.optJSONArray("checklist_items"))
    return (directItems + checklistItems)
        .map { it.trim() }
        .filter { it.isNotBlank() }
        .distinct()
}

fun confirmationItemsFromJson(json: JSONObject): List<String> {
    "需要确认："
    return confirmationItemsFromModelJson(json, ::stringsFromJson)
}

private fun checklistItemTextsFromJson(values: JSONArray?): List<String> {
    if (values == null || values.length() == 0) {
        return emptyList()
    }
    return (0 until values.length()).mapNotNull { index ->
        values.optJSONObject(index)?.safeString("text")?.takeIf { it.isNotBlank() }
    }
}

fun displayTimeFrom(time: JSONObject?): String =
    listOfNotNull(
        time?.safeString("start_text")?.takeIf { it.isNotBlank() },
        time?.safeString("deadline_text")?.takeIf { it.isNotBlank() },
    ).joinToString(" / ").ifBlank { "待确认" }

fun sceneHint(scene: String): String =
    sceneHintForModel(scene)
