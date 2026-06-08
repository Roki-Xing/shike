package cn.shike.app.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class LocalMultimodalRuntimeTest {
    @Test
    fun analyze_runsInitVitGenerateThenSchemaGateBeforeManualReviewCard() {
        val engine = RecordingLocalMultimodalEngine(
            generatedJson = """
                {
                  "title": "组会改到 B203",
                  "scene_type": "meeting_notice",
                  "confidence": 0.82,
                  "time": {"start_text": "今晚 19:30"},
                  "location": {"raw": "B203"},
                  "suggested_actions": [{"label": "打开日历"}, {"label": "设置提醒"}, {"label": "查看路线"}],
                  "missing_fields": [],
                  "risks": [],
                  "explanation": "端侧 3B 根据图片和 OCR hint 生成草稿"
                }
            """.trimIndent(),
        )
        val runtime = LocalMultimodalRuntime(engine)

        val result = runtime.analyze(
            request = LocalMultimodalRequest(
                rgbBytes = byteArrayOf(1, 2, 3, 4, 5, 6),
                width = 1,
                height = 2,
                prompt = "请只输出 JSON，schema={...}",
                schemaJson = """{"required":["title","scene_type","suggested_actions"]}""",
                ocrTextHint = "组会今晚 19:30 改到 B203",
            ),
            fallback = sampleCourse(),
        )

        assertEquals(
            listOf(
                "init(multimodal=true)",
                "callVit(width=1,height=2,bytes=6)",
                "generate(prompt_has_schema=true)",
            ),
            engine.calls,
        )
        val outcome = result as LocalMultimodalAnalysisResult.NeedsManualReview
        assertEquals("组会改到 B203", outcome.item.title)
        assertEquals("会议通知", outcome.item.scene)
        assertEquals("待确认", outcome.item.status)
        assertEquals("端侧 3B：schema_valid，本地待确认", outcome.source)
        assertEquals("端侧 3B 已生成草稿，等待用户确认", outcome.statusMessage)
        assertTrue(outcome.item.rawText.contains("端侧 3B"))
        assertTrue(outcome.item.rawText.contains("用户确认前不可执行"))
    }

    @Test
    fun analyze_returnsUnavailableWithoutCallingSdkWhenEngineMissing() {
        val runtime = LocalMultimodalRuntime(engine = null)

        val result = runtime.analyze(
            request = LocalMultimodalRequest(
                rgbBytes = byteArrayOf(1, 2, 3),
                width = 1,
                height = 1,
                prompt = "schema={...}",
                schemaJson = """{"type":"object"}""",
                ocrTextHint = "",
            ),
            fallback = sampleCourse(),
        )

        assertEquals(
            LocalMultimodalAnalysisResult.Unavailable("local_multimodal_sdk_missing"),
            result,
        )
    }

    @Test
    fun analyze_rejectsJsonMissingRequiredFieldsAndDoesNotInjectSample() {
        val engine = RecordingLocalMultimodalEngine(generatedJson = """{"title":"只有标题"}""")
        val runtime = LocalMultimodalRuntime(engine)

        val result = runtime.analyze(
            request = LocalMultimodalRequest(
                rgbBytes = byteArrayOf(1, 2, 3),
                width = 1,
                height = 1,
                prompt = "schema={...}",
                schemaJson = """{"required":["title","scene_type","suggested_actions"]}""",
                ocrTextHint = "今天晚上需要上高数A",
            ),
            fallback = sampleCourse(),
        )

        val failure = result as LocalMultimodalAnalysisResult.SchemaRejected
        assertEquals("local_schema_rejected", failure.reason)
        assertEquals("待确认", failure.item.status)
        assertEquals("今天晚上需要上高数A", failure.item.rawText)
        assertTrue("B203" !in failure.item.rawText)
        assertTrue("18:30" !in failure.item.rawText)
        assertTrue("22:00" !in failure.item.rawText)
    }
}

private class RecordingLocalMultimodalEngine(
    private val generatedJson: String,
) : LocalMultimodalEngine {
    val calls = mutableListOf<String>()

    override fun init(config: LocalMultimodalConfig): Int {
        calls += "init(multimodal=${config.multimodal})"
        return 0
    }

    override fun callVit(rgbBytes: ByteArray, width: Int, height: Int): Int {
        calls += "callVit(width=$width,height=$height,bytes=${rgbBytes.size})"
        return 0
    }

    override fun generate(prompt: String): String {
        calls += "generate(prompt_has_schema=${"schema" in prompt})"
        return generatedJson
    }

    override fun release() = Unit
}
