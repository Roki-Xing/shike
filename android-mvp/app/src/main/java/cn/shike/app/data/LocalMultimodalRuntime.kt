package cn.shike.app.data

import cn.shike.app.domain.ShikeItem
import org.json.JSONObject

data class LocalMultimodalConfig(
    val modelPath: String = "/sdcard/1225",
    val multimodal: Boolean = true,
    val nPredict: Int = 512,
    val nCtx: Int = 2048,
    val nThreads: Int = 4,
    val npuPower: Int = 100,
    val temperature: Float = 0.0f,
    val topP: Float = 1.0f,
    val topK: Int = 1,
)

data class LocalMultimodalRequest(
    val rgbBytes: ByteArray,
    val width: Int,
    val height: Int,
    val prompt: String,
    val schemaJson: String,
    val ocrTextHint: String,
)

sealed class LocalMultimodalAnalysisResult {
    data class Unavailable(val reason: String) : LocalMultimodalAnalysisResult()
    data class SchemaRejected(val reason: String, val item: ShikeItem) : LocalMultimodalAnalysisResult()
    data class NeedsManualReview(
        val item: ShikeItem,
        val source: String,
        val statusMessage: String,
    ) : LocalMultimodalAnalysisResult()
}

interface LocalMultimodalEngine {
    fun init(config: LocalMultimodalConfig): Int
    fun callVit(rgbBytes: ByteArray, width: Int, height: Int): Int
    fun generate(prompt: String): String
    fun release()
}

class LocalMultimodalRuntime(
    private val engine: LocalMultimodalEngine?,
) {
    /**
     * Runs the optional local 3B multimodal path without bypassing confirmation.
     *
     * Args:
     *     request: RGB image bytes, prompt, schema, and OCR hint for local inference.
     *     fallback: Local fallback card used when local output is invalid.
     *
     * Returns:
     *     A local result that is unavailable, schema-rejected, or a pending review card.
     */
    fun analyze(
        request: LocalMultimodalRequest,
        fallback: ShikeItem,
    ): LocalMultimodalAnalysisResult {
        val runtimeEngine = engine ?: return LocalMultimodalAnalysisResult.Unavailable("local_multimodal_sdk_missing")
        return try {
            val config = LocalMultimodalConfig(multimodal = true)
            val initCode = runtimeEngine.init(config)
            if (initCode != 0) {
                schemaRejected(fallback, request.ocrTextHint, "local_init_failed:$initCode")
            } else {
                analyzeInitializedEngine(runtimeEngine, request, fallback)
            }
        } catch (_: Exception) {
            schemaRejected(fallback, request.ocrTextHint, "local_runtime_failed")
        } finally {
            runtimeEngine.release()
        }
    }
}

private fun analyzeInitializedEngine(
    engine: LocalMultimodalEngine,
    request: LocalMultimodalRequest,
    fallback: ShikeItem,
): LocalMultimodalAnalysisResult {
    val vitCode = engine.callVit(request.rgbBytes, request.width, request.height)
    if (vitCode != 0) {
        return schemaRejected(fallback, request.ocrTextHint, "local_vit_failed:$vitCode")
    }
    val generated = engine.generate(promptWithSchema(request))
    val parsed = parseGeneratedJson(generated)
        ?: return schemaRejected(fallback, request.ocrTextHint, "local_schema_rejected")
    if (!looksSchemaValid(parsed)) {
        return schemaRejected(fallback, request.ocrTextHint, "local_schema_rejected")
    }
    val item = itemFromAnalyzeImageJson(parsed, request.ocrTextHint).copy(
        status = "待确认",
        rawText = buildLocalReviewRawText(parsed, request.ocrTextHint),
    )
    return LocalMultimodalAnalysisResult.NeedsManualReview(
        item = item,
        source = "端侧 3B：schema_valid，本地待确认",
        statusMessage = "端侧 3B 已生成草稿，等待用户确认",
    )
}

private fun promptWithSchema(request: LocalMultimodalRequest): String =
    listOf(
        request.prompt,
        "schema=${request.schemaJson}",
        "OCR hint=${request.ocrTextHint}",
        "端侧输出只允许生成待确认草稿，用户确认前不可执行日历、提醒、地图或删除原截图。",
    ).joinToString("\n")

private fun parseGeneratedJson(text: String): JSONObject? {
    val start = text.indexOf('{')
    val end = text.lastIndexOf('}')
    if (start == -1 || end <= start) {
        return null
    }
    return runCatching { JSONObject(text.substring(start, end + 1)) }.getOrNull()
}

private fun looksSchemaValid(json: JSONObject): Boolean {
    val suggestedActionCount = json.optJSONArray("suggested_actions")?.length() ?: 0
    return json.optString("title").isNotBlank()
        && json.optString("scene_type").isNotBlank()
        && suggestedActionCount > 0
}

private fun schemaRejected(
    fallback: ShikeItem,
    ocrTextHint: String,
    reason: String,
): LocalMultimodalAnalysisResult.SchemaRejected =
    LocalMultimodalAnalysisResult.SchemaRejected(
        reason = reason.substringBefore(":"),
        item = fallbackItemForRealDraft(fallback, ocrTextHint).copy(status = "待确认"),
    )

private fun buildLocalReviewRawText(json: JSONObject, ocrTextHint: String): String =
    listOf(
        "端侧 3B：${json.optString("explanation", "已生成结构化草稿")}",
        "用户确认前不可执行日历、提醒、地图或删除原截图。",
        ocrTextHint.takeIf { it.isNotBlank() }?.let { "OCR hint：${redactSensitiveLogText(it)}" },
    ).filterNotNull().joinToString("\n")
