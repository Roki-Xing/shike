package cn.shike.app.data

import cn.shike.app.domain.ShikeItem

data class BackendAnalysisOutcome(
    val item: ShikeItem,
    val source: String,
    val statusMessage: String,
)

data class BackendFailureFallbackCopy(
    val rawText: String,
    val source: String,
    val statusMessage: String,
)

data class BackendAnalysisInput(
    val sourceType: String,
    val fallback: ShikeItem,
    val imageUri: String? = null,
    val imageSourceType: String = "manual",
    val allowCloudImage: Boolean = true,
) {
    val hasImageForCloudAnalysis: Boolean
        get() = !imageUri.isNullOrBlank()
}

/**
 * Builds the backend-analysis input for the course screenshot demo path.
 *
 * Returns:
 *     Source metadata and fallback item used by `/v1/analyze`.
 */
fun courseBackendAnalysisInput(): BackendAnalysisInput =
    BackendAnalysisInput("screenshot", sampleCourse())

/**
 * Builds the backend-analysis input for the event camera demo path.
 *
 * Returns:
 *     Source metadata and fallback item used by `/v1/analyze`.
 */
fun eventBackendAnalysisInput(): BackendAnalysisInput =
    BackendAnalysisInput("camera", sampleEvent())

fun backendAnalysisInputForCurrentDraft(
    captureSource: String,
    fallback: ShikeItem,
    imageUri: String? = null,
    allowCloudImage: Boolean = true,
): BackendAnalysisInput =
    BackendAnalysisInput(
        sourceType = backendSourceTypeFromCaptureSource(captureSource),
        fallback = fallback,
        imageUri = imageUri,
        imageSourceType = backendImageSourceTypeFromCaptureSource(captureSource),
        allowCloudImage = allowCloudImage,
    )

/**
 * Chooses the editable OCR text sent to the backend.
 *
 * Args:
 *     ocrDraft: User-edited OCR text.
 *     fallback: Local fallback action card.
 *
 * Returns:
 *     Edited OCR text, or the fallback sample text when the draft is blank.
 */
fun backendAnalyzeText(ocrDraft: String, fallback: ShikeItem): String =
    ocrDraft.ifBlank { fallback.rawText }

/**
 * Maps a successful backend item into persisted UI state.
 *
 * Args:
 *     item: Action card returned by `/v1/analyze`.
 *
 * Returns:
 *     UI-ready backend analysis outcome.
 */
fun backendSuccessOutcome(item: ShikeItem): BackendAnalysisOutcome =
    BackendAnalysisOutcome(
        item = item,
        source = "后端 /v1/analyze：${item.scene}",
        statusMessage = "模型编排：后端解析成功",
    )

/**
 * Builds safe user-visible copy for backend failure fallback.
 *
 * Args:
 *     textForAnalyze: OCR text attempted against `/v1/analyze`.
 *
 * Returns:
 *     Redacted raw-text evidence plus source and status copy.
 */
fun backendFailureFallbackCopyFor(textForAnalyze: String): BackendFailureFallbackCopy =
    BackendFailureFallbackCopy(
        rawText = "${redactSensitiveLogText(textForAnalyze)}\n云侧暂不可用，已切换为本地确认，日志已脱敏。",
        source = "云侧解析失败，本地待确认",
        statusMessage = "云侧暂不可用，已切换为本地确认",
    )

/**
 * Maps backend failure into a safe local fallback outcome.
 *
 * Args:
 *     fallback: Local fallback action card.
 *     textForAnalyze: OCR text attempted against the backend.
 *
 * Returns:
 *     UI-ready failure outcome with redacted fallback evidence.
 */
fun backendFailureOutcome(fallback: ShikeItem, textForAnalyze: String): BackendAnalysisOutcome {
    val fallbackCopy = backendFailureFallbackCopyFor(textForAnalyze)
    return BackendAnalysisOutcome(
        item = fallbackItemForRealDraft(fallback, textForAnalyze).copy(
            status = "待确认",
            rawText = fallbackCopy.rawText,
        ),
        source = fallbackCopy.source,
        statusMessage = fallbackCopy.statusMessage,
    )
}

fun backendImageFailureOutcome(fallback: ShikeItem, textForAnalyze: String, reason: String): BackendAnalysisOutcome =
    BackendAnalysisOutcome(
        item = fallbackItemForRealDraft(fallback, textForAnalyze).copy(
            status = "待确认",
            rawText = "${redactSensitiveLogText(textForAnalyze)}\n$reason，已进入本地待确认，日志已脱敏。",
        ),
        source = "云侧图片解析失败，本地待确认",
        statusMessage = "云侧图片理解暂不可用，已进入待确认",
    )

fun backendImageSuccessOutcome(item: ShikeItem): BackendAnalysisOutcome =
    BackendAnalysisOutcome(
        item = item,
        source = "后端 /v2/analyze-image：${item.scene}",
        statusMessage = "模型编排：云侧图片解析成功",
    )

fun backendImageManualReviewOutcome(item: ShikeItem): BackendAnalysisOutcome =
    BackendAnalysisOutcome(
        item = item,
        source = "云侧图片解析失败，本地待确认",
        statusMessage = "云侧图片理解暂不可用，已进入待确认",
    )

fun fallbackItemForRealDraft(fallback: ShikeItem, textForAnalyze: String): ShikeItem {
    val trimmed = textForAnalyze.trim()
    if (trimmed.isBlank()) {
        return fallback
    }
    if ("高数" in trimmed && "B203" !in trimmed && "18:30" !in trimmed && "22:00" !in trimmed) {
        return fallback.copy(
            title = "上高数 A",
            scene = "课程通知",
            time = "今天晚上（需确认具体时间）",
            location = "待补充",
            actions = listOf("先存入待确认"),
            rawText = trimmed,
        )
    }
    return fallback.copy(
        title = trimmed.lineSequence().firstOrNull()?.take(18)?.ifBlank { fallback.title } ?: fallback.title,
        time = "待确认",
        location = "待补充",
        actions = listOf("先存入待确认"),
        rawText = trimmed,
    )
}

/**
 * Runs backend analysis and converts network success or failure into UI-ready state.
 *
 * Args:
 *     backendUrl: User-configured backend base URL.
 *     sourceType: Capture source sent to `/v1/analyze`.
 *     ocrDraft: Editable OCR text from the review panel.
 *     fallback: Local mock item used when the backend is unavailable.
 *     deliver: Callback invoked from the worker thread with the mapped result.
 *
 * Returns:
 *     Normalized backend endpoint persisted by the caller.
 */
fun runBackendAnalysis(
    backendUrl: String,
    input: BackendAnalysisInput,
    ocrDraft: String,
    imagePayloadProvider: (() -> BackendImagePayload?)? = null,
    deliver: (BackendAnalysisOutcome) -> Unit,
): String {
    val textForAnalyze = backendAnalyzeText(ocrDraft, input.fallback)
    val endpoint = normalizeBackendUrl(backendUrl)
    Thread {
        if (imagePayloadProvider != null || input.hasImageForCloudAnalysis) {
            val imagePayload = imagePayloadProvider?.invoke()
            if (imagePayload == null) {
                deliver(backendImageFailureOutcome(input.fallback, textForAnalyze, "图片读取失败"))
                return@Thread
            }
            val result = runCatching {
                callAnalyzeImageApi(
                    backendBaseUrl = endpoint,
                    sourceType = input.imageSourceType,
                    ocrTextHint = textForAnalyze,
                    scene = input.fallback.scene,
                    image = imagePayload,
                    allowCloudImage = input.allowCloudImage,
                )
            }
            deliver(
                result.fold(
                    onSuccess = { outcome -> outcome },
                    onFailure = { backendImageFailureOutcome(input.fallback, textForAnalyze, "云侧图片解析失败") },
                ),
            )
            return@Thread
        }

        val result = runCatching {
            callAnalyzeApi(endpoint, input.sourceType, textForAnalyze, input.fallback.scene)
        }
        deliver(
            result.fold(
                onSuccess = ::backendSuccessOutcome,
                onFailure = { backendFailureOutcome(input.fallback, textForAnalyze) },
            ),
        )
    }.start()
    return endpoint
}
