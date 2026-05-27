package cn.shike.app

import android.os.Handler
import cn.shike.app.data.BackendAnalysisInput
import cn.shike.app.data.BackendAnalysisOutcome
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
    onOutcome: (BackendAnalysisOutcome) -> Unit,
): BackendAnalysisResult {
    val endpoint = runBackendAnalysis(
        backendUrl = backendUrl,
        sourceType = input.sourceType,
        ocrDraft = ocrDraft,
        fallback = input.fallback,
    ) { outcome ->
        mainHandler.post {
            onOutcome(outcome)
        }
    }
    return BackendAnalysisResult(
        endpoint = endpoint,
        statusMessage = "模型编排：请求后端 /v1/analyze",
    )
}
