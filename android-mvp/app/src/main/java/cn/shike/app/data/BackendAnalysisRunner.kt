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
)

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
        rawText = "${redactSensitiveLogText(textForAnalyze)}\n后端不可用，已回退本地 MockModelAdapter，日志已脱敏。",
        source = "后端失败，回退本地 MockModelAdapter",
        statusMessage = "模型编排：后端失败，已回退本地 mock",
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
        item = fallback.copy(
            status = "待确认",
            rawText = fallbackCopy.rawText,
        ),
        source = fallbackCopy.source,
        statusMessage = fallbackCopy.statusMessage,
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
    sourceType: String,
    ocrDraft: String,
    fallback: ShikeItem,
    deliver: (BackendAnalysisOutcome) -> Unit,
): String {
    val textForAnalyze = backendAnalyzeText(ocrDraft, fallback)
    val endpoint = normalizeBackendUrl(backendUrl)
    Thread {
        val result = runCatching {
            callAnalyzeApi(endpoint, sourceType, textForAnalyze, fallback.scene)
        }
        deliver(
            result.fold(
                onSuccess = ::backendSuccessOutcome,
                onFailure = { backendFailureOutcome(fallback, textForAnalyze) },
            ),
        )
    }.start()
    return endpoint
}
