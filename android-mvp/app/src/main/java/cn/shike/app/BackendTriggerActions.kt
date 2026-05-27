package cn.shike.app

import cn.shike.app.data.BackendAnalysisInput
import cn.shike.app.data.courseBackendAnalysisInput
import cn.shike.app.data.eventBackendAnalysisInput

fun analyzeCourseWithBackendAction(analyzeWithBackend: (BackendAnalysisInput) -> Unit) {
    analyzeWithBackend(courseBackendAnalysisInput())
}

fun analyzeEventWithBackendAction(analyzeWithBackend: (BackendAnalysisInput) -> Unit) {
    analyzeWithBackend(eventBackendAnalysisInput())
}
