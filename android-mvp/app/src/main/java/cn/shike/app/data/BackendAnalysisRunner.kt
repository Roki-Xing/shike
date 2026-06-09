package cn.shike.app.data

import cn.shike.app.domain.ShikeItem

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
