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
        val manual = backendAnalysisInputForCurrentDraft("手动输入：可编辑识别文字后生成行动卡。", sampleCourse())

        assertEquals("share_text", share.sourceType)
        assertEquals("manual", manual.sourceType)
        assertEquals("课程通知", share.fallback.scene)
        assertEquals("课程通知", manual.fallback.scene)
    }

    @Test
    fun backendAnalyzeText_prefersEditedOcrDraftAndDoesNotFallbackToImageSampleRawText() {
        val fallback = sampleCourse()
        val pendingImage = fallback.copy(
            title = "待解析截图",
            scene = "图片导入",
            time = "待确认",
            location = "待确认",
            status = "待确认",
            actions = listOf("先存入待确认"),
            rawText = "",
        )

        assertEquals("用户改过的 OCR 文本", backendAnalyzeText("用户改过的 OCR 文本", fallback))
        assertEquals(fallback.rawText, backendAnalyzeText("   ", fallback))
        assertEquals("", backendAnalyzeText("   ", pendingImage))
    }

    @Test
    fun backendFailureOutcome_redactsSensitiveTextAndKeepsFallbackReviewState() {
        val fallback = sampleCourse().copy(status = "已安排")
        val outcome = backendFailureOutcome(
            fallback = fallback,
            textForAnalyze = "报名联系 13812345678 学号：20260001 电脑 192.168.1.10:8000",
        )

        assertEquals("待确认", outcome.item.status)
        assertEquals("云侧解析失败，本地待确认", outcome.source)
        assertEquals("云侧暂不可用，已切换为本地确认", outcome.statusMessage)
        assertTrue(outcome.item.rawText.contains("[手机号已脱敏]"))
        assertTrue(outcome.item.rawText.contains("学号：[学号已脱敏]"))
        assertTrue(outcome.item.rawText.contains("[局域网地址已脱敏]"))
        assertTrue(outcome.item.rawText.contains("云侧暂不可用，已切换为本地确认"))
        assertFalse(outcome.item.rawText.contains("13812345678"))
        assertFalse(outcome.item.rawText.contains("192.168.1.10"))
    }

    @Test
    fun backendFailureOutcomeForRealMathDraft_doesNotInjectCourseSampleFields() {
        val outcome = backendFailureOutcome(
            fallback = sampleCourse(),
            textForAnalyze = "今天晚上需要上高数A",
        )
        val combined = listOf(
            outcome.item.title,
            outcome.item.time,
            outcome.item.location,
            outcome.item.rawText,
            outcome.source,
            outcome.statusMessage,
        ).joinToString("\n")

        assertEquals("上高数 A", outcome.item.title)
        assertEquals("课程通知", outcome.item.scene)
        assertEquals("今天晚上（需确认具体时间）", outcome.item.time)
        assertEquals("待补充", outcome.item.location)
        assertEquals("待确认", outcome.item.status)
        assertEquals(listOf("先存入待确认"), outcome.item.actions)
        assertEquals("云侧解析失败，本地待确认", outcome.source)
        assertEquals("云侧暂不可用，已切换为本地确认", outcome.statusMessage)
        assertTrue(outcome.item.rawText.contains("今天晚上需要上高数A"))
        assertFalse(combined.contains("B203"))
        assertFalse(combined.contains("18:30"))
        assertFalse(combined.contains("22:00"))
        assertFalse(combined.contains("第5章"))
        assertFalse(combined.contains("MockModelAdapter"))
    }

    @Test
    fun backendFailureFallbackCopyFor_redactsEvidenceBeforeUiPersistence() {
        val copy = backendFailureFallbackCopyFor(
            "活动报名 联系 13900001111 邮箱 demo@example.com 地址 192.168.0.2:8000",
        )

        assertEquals("云侧解析失败，本地待确认", copy.source)
        assertEquals("云侧暂不可用，已切换为本地确认", copy.statusMessage)
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
        assertEquals("云端 AI 解析：活动海报", outcome.source)
        assertEquals("云端 AI 解析完成", outcome.statusMessage)
    }
}
