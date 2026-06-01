package cn.shike.app

import cn.shike.app.data.backendAnalyzeText
import cn.shike.app.data.backendAnalysisInputForCurrentDraft
import cn.shike.app.data.backendFailureFallbackCopyFor
import cn.shike.app.data.backendFailureOutcome
import cn.shike.app.data.backendSuccessOutcome
import cn.shike.app.data.sampleCourse
import cn.shike.app.data.sampleEvent
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class BackendAnalysisRunnerTest {
    @Test
    fun backendAnalysisInputForCurrentDraft_usesCaptureSourceSpecificBackendType() {
        val share = backendAnalysisInputForCurrentDraft("文本分享入口（待确认，未落盘）", sampleCourse())
        val manual = backendAnalysisInputForCurrentDraft("手动输入入口：请编辑 OCR 文本草稿后选择后端解析或离线样例。", sampleCourse())

        assertEquals("share_text", share.sourceType)
        assertEquals("manual", manual.sourceType)
        assertEquals("课程通知", share.fallback.scene)
        assertEquals("课程通知", manual.fallback.scene)
    }

    @Test
    fun backendAnalyzeText_prefersEditedOcrDraftAndFallsBackToSampleRawText() {
        val fallback = sampleCourse()

        assertEquals("用户改过的 OCR 文本", backendAnalyzeText("用户改过的 OCR 文本", fallback))
        assertEquals(fallback.rawText, backendAnalyzeText("   ", fallback))
    }

    @Test
    fun backendFailureOutcome_redactsSensitiveTextAndKeepsFallbackReviewState() {
        val fallback = sampleCourse().copy(status = "已安排")
        val outcome = backendFailureOutcome(
            fallback = fallback,
            textForAnalyze = "报名联系 13812345678 学号：20260001 电脑 192.168.1.10:8000",
        )

        assertEquals("待确认", outcome.item.status)
        assertEquals("后端失败，回退本地 MockModelAdapter", outcome.source)
        assertEquals("模型编排：后端失败，已回退本地 mock", outcome.statusMessage)
        assertTrue(outcome.item.rawText.contains("[手机号已脱敏]"))
        assertTrue(outcome.item.rawText.contains("学号：[学号已脱敏]"))
        assertTrue(outcome.item.rawText.contains("[局域网地址已脱敏]"))
        assertTrue(outcome.item.rawText.contains("后端不可用，已回退本地 MockModelAdapter"))
        assertFalse(outcome.item.rawText.contains("13812345678"))
        assertFalse(outcome.item.rawText.contains("192.168.1.10"))
    }

    @Test
    fun backendFailureFallbackCopyFor_redactsEvidenceBeforeUiPersistence() {
        val copy = backendFailureFallbackCopyFor(
            "活动报名 联系 13900001111 邮箱 demo@example.com 地址 192.168.0.2:8000",
        )

        assertEquals("后端失败，回退本地 MockModelAdapter", copy.source)
        assertEquals("模型编排：后端失败，已回退本地 mock", copy.statusMessage)
        assertTrue(copy.rawText.contains("[手机号已脱敏]"))
        assertTrue(copy.rawText.contains("[邮箱已脱敏]"))
        assertTrue(copy.rawText.contains("[局域网地址已脱敏]"))
        assertTrue(copy.rawText.contains("日志已脱敏"))
        assertFalse(copy.rawText.contains("13900001111"))
        assertFalse(copy.rawText.contains("demo@example.com"))
        assertFalse(copy.rawText.contains("192.168.0.2"))
    }

    @Test
    fun backendSuccessOutcome_preservesReturnedItemAndBackendSource() {
        val item = sampleEvent().copy(title = "后端解析活动")

        val outcome = backendSuccessOutcome(item)

        assertEquals(item, outcome.item)
        assertEquals("后端 /v1/analyze：活动海报", outcome.source)
        assertEquals("模型编排：后端解析成功", outcome.statusMessage)
    }
}
