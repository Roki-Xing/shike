package cn.shike.app

import android.os.Handler
import cn.shike.app.data.BackendAnalysisInput
import cn.shike.app.data.BackendAnalysisOutcome
import cn.shike.app.data.BackendImagePayload
import cn.shike.app.data.backendAnalysisPathFor
import cn.shike.app.data.backendAnalysisPathForImage
import cn.shike.app.data.runBackendAnalysis

data class BackendAnalysisResult(
    val endpoint: String,
    val statusMessage: String,
)

fun runBackendAnalysisAction(
    backendUrl: String,
    input: BackendAnalysisInput,
    ocrDraft: String,
    mainHandler: Handler,
    imagePayloadProvider: (() -> BackendImagePayload?)? = null,
    onOutcome: (BackendAnalysisOutcome) -> Unit,
): BackendAnalysisResult {
    val endpoint = runBackendAnalysis(
        backendUrl = backendUrl,
        input = input,
        ocrDraft = ocrDraft,
        imagePayloadProvider = imagePayloadProvider,
    ) { outcome ->
        mainHandler.post {
            onOutcome(outcome)
        }
    }
    return BackendAnalysisResult(
        endpoint = endpoint,
        statusMessage = if (backendAnalysisPathFor(input) == backendAnalysisPathForImage()) "AI 正在解析图片" else "AI 正在解析文字",
    )
}
