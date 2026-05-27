package cn.shike.app

import cn.shike.app.data.BackendAnalysisOutcome
import cn.shike.app.data.redactSensitiveLogText
import cn.shike.app.domain.ShikeItem

private const val DEFAULT_BACKEND_SOURCE = "后端 /v1/analyze：结果待确认"
private const val DEFAULT_BACKEND_STATUS = "模型编排：后端结果待确认"

fun applyBackendOutcomeSelection(
    outcome: BackendAnalysisOutcome,
    persistSelection: (ShikeItem, String) -> Unit,
): String {
    persistSelection(outcome.item, sanitizeBackendOutcomeSource(outcome.source))
    return sanitizeBackendOutcomeStatus(outcome.statusMessage)
}

/**
 * Sanitizes the backend outcome source before UI persistence.
 *
 * Args:
 *     source: Backend or fallback source label.
 *
 * Returns:
 *     Non-blank source text with sensitive tokens redacted.
 */
fun sanitizeBackendOutcomeSource(source: String?): String =
    redactSensitiveLogText(source.orEmpty().trim())
        .ifBlank { DEFAULT_BACKEND_SOURCE }

/**
 * Sanitizes the backend status copy before it is shown in the UI.
 *
 * Args:
 *     statusMessage: Backend status text or fallback status text.
 *
 * Returns:
 *     Non-blank status text with sensitive tokens redacted.
 */
fun sanitizeBackendOutcomeStatus(statusMessage: String?): String =
    redactSensitiveLogText(statusMessage.orEmpty().trim())
        .ifBlank { DEFAULT_BACKEND_STATUS }
