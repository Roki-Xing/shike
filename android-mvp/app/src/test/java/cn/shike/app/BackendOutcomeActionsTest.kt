package cn.shike.app

import cn.shike.app.data.BackendAnalysisOutcome
import cn.shike.app.data.sampleCourse
import cn.shike.app.data.sampleEvent
import cn.shike.app.domain.ShikeItem
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class BackendOutcomeActionsTest {
    @Test
    fun applyBackendOutcomeSelection_persistsBackendItemAndSource() {
        val persisted = mutableListOf<Pair<ShikeItem, String>>()
        val item = sampleEvent().copy(title = "后端解析活动")
        val outcome = BackendAnalysisOutcome(
            item = item,
            source = "后端 /v1/analyze：活动海报",
            statusMessage = "模型编排：后端解析成功",
        )

        val status = applyBackendOutcomeSelection(outcome) { savedItem, source ->
            persisted += savedItem to source
        }

        assertEquals("模型编排：后端解析成功", status)
        assertEquals(listOf(item to "后端 /v1/analyze：活动海报"), persisted)
    }

    @Test
    fun applyBackendOutcomeSelection_preservesFallbackStatusMessage() {
        val persisted = mutableListOf<Pair<ShikeItem, String>>()
        val item = sampleCourse().copy(
            status = "待确认",
            rawText = "脱敏后的 OCR 文本\n云侧暂不可用，已切换为本地确认，日志已脱敏。",
        )
        val outcome = BackendAnalysisOutcome(
            item = item,
            source = "云侧解析失败，本地待确认",
            statusMessage = "云侧暂不可用，已切换为本地确认",
        )

        val status = applyBackendOutcomeSelection(outcome) { savedItem, source ->
            persisted += savedItem to source
        }

        assertEquals("云侧暂不可用，已切换为本地确认", status)
        assertEquals(listOf(item to "云侧解析失败，本地待确认"), persisted)
    }

    @Test
    fun sanitizeBackendOutcomeCopy_redactsSensitiveTokensAndFallsBackToDefaults() {
        val persisted = mutableListOf<Pair<ShikeItem, String>>()
        val item = sampleEvent().copy(title = "后端返回活动")
        val outcome = BackendAnalysisOutcome(
            item = item,
            source = " 后端 13812345678 demo@example.com ",
            statusMessage = " 模型 学号：2026123456 10.0.2.2:8000 ",
        )

        val status = applyBackendOutcomeSelection(outcome) { savedItem, source ->
            persisted += savedItem to source
        }

        assertEquals(item, persisted.single().first)
        assertTrue(persisted.single().second.contains("[手机号已脱敏]"))
        assertTrue(persisted.single().second.contains("[邮箱已脱敏]"))
        assertTrue(status.contains("学号：[学号已脱敏]"))
        assertTrue(status.contains("[局域网地址已脱敏]"))
        assertFalse(persisted.single().second.contains("13812345678"))
        assertFalse(persisted.single().second.contains("demo@example.com"))
        assertFalse(status.contains("2026123456"))
        assertFalse(status.contains("10.0.2.2"))
        assertEquals("云侧解析结果待确认", sanitizeBackendOutcomeSource("  "))
        assertEquals("云侧解析结果待确认", sanitizeBackendOutcomeStatus(null))
    }
}
