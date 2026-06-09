package cn.shike.app.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.json.JSONArray
import org.json.JSONObject
import org.json.JSONObject.NULL
import org.junit.Test

class AnalyzeImageApiClientTest {
    @Test
    fun buildAnalyzeImageRequestPayload_includesImageOcrHintAndUserContext() {
        val payload = buildAnalyzeImageRequestPayload(
            inputId = "android-image-1",
            sourceType = "photo_picker",
            ocrTextHint = "海报：周五 19:30 图书馆报告厅",
            scene = "活动海报",
            currentDate = "2026-06-06",
            image = BackendImagePayload(
                dataUrl = "data:image/jpeg;base64,ZmFrZQ==",
                mime = "image/jpeg",
                width = 1080,
                height = 2400,
                sha256 = "abc123",
            ),
        )

        assertEquals("android-image-1", payload.getString("input_id"))
        assertEquals("photo_picker", payload.getString("source_type"))
        assertEquals("海报：周五 19:30 图书馆报告厅", payload.getString("ocr_text_hint"))
        assertEquals("2026-06-06", payload.getString("current_date"))
        assertEquals("Asia/Shanghai", payload.getString("user_timezone"))
        assertEquals("zh-CN", payload.getString("locale"))
        assertEquals("event_poster", payload.getString("scene_hint"))
        assertTrue(payload.getBoolean("allow_cloud_image"))

        val image = payload.getJSONObject("image")
        assertEquals("data:image/jpeg;base64,ZmFrZQ==", image.getString("data_url"))
        assertEquals("image/jpeg", image.getString("mime"))
        assertEquals(1080, image.getInt("width"))
        assertEquals(2400, image.getInt("height"))
        assertEquals("abc123", image.getString("sha256"))
    }

    @Test
    fun buildAnalyzeImageRequestPayload_canDisableCloudImageUpload() {
        val payload = buildAnalyzeImageRequestPayload(
            inputId = "android-image-no-cloud",
            sourceType = "screenshot_share",
            ocrTextHint = "今晚18:30 项目讨论 B203",
            scene = "课程通知",
            currentDate = "2026-06-06",
            image = BackendImagePayload(
                dataUrl = "data:image/jpeg;base64,ZmFrZQ==",
                mime = "image/jpeg",
                width = 1080,
                height = 2400,
                sha256 = "abc123",
            ),
            allowCloudImage = false,
        )

        assertFalse(payload.getBoolean("allow_cloud_image"))
    }

    @Test
    fun backendAnalysisInputForCurrentDraft_keepsImageUriForV2Route() {
        val input = backendAnalysisInputForCurrentDraft(
            captureSource = "相册图片 content://media/external/images/media/42",
            fallback = sampleCourse(),
            imageUri = "content://media/external/images/media/42",
        )

        assertEquals("screenshot", input.sourceType)
        assertEquals("content://media/external/images/media/42", input.imageUri)
        assertEquals("/v2/analyze-image", backendAnalysisPathFor(input))
        assertEquals("photo_picker", backendImageSourceTypeFromCaptureSource("相册图片 content://media/external/images/media/42"))
    }

    @Test
    fun backendAnalysisPathFor_textOnlyDraftStaysOnV1() {
        val input = backendAnalysisInputForCurrentDraft(
            captureSource = "手动输入：可编辑识别文字后生成行动卡。",
            fallback = sampleCourse(),
            imageUri = null,
        )

        assertEquals("/v1/analyze", backendAnalysisPathFor(input))
        assertFalse(input.hasImageForCloudAnalysis)
    }

    @Test
    fun itemFromAnalyzeImageJson_omitsJsonNullDeadlineAndKeepsStructuredFields() {
        val item = itemFromAnalyzeImageJson(
            JSONObject()
                .put("scene_type", "course_notice")
                .put("title", "英语口语课")
                .put("time", JSONObject().put("start_text", "明天早上九点").put("deadline_text", NULL))
                .put("location", JSONObject().put("raw", "E520"))
                .put("task", JSONObject().put("summary", "上英语口语").put("priority", "medium").put("topic", "course"))
                .put(
                    "suggested_actions",
                    JSONArray()
                        .put(JSONObject().put("label", "加入日历"))
                        .put(JSONObject().put("label", "课前提醒"))
                        .put(JSONObject().put("label", "打开地图")),
                )
                .put("missing_fields", JSONArray().put("reminder_offset"))
                .put("risks", JSONArray().put("日期来自“明天”，请确认"))
                .put("explanation", "从 OCR 证据提取课程、时间和地点"),
            fallbackText = "明天早上九点上英语口语教室E520",
        )

        assertEquals("英语口语课", item.title)
        assertEquals("课程通知", item.scene)
        assertEquals("明天早上九点", item.time)
        assertFalse(item.time.contains("null"))
        assertEquals("E520", item.location)
        assertEquals(listOf("加入日历", "课前提醒", "打开地图"), item.actions)
        assertTrue(item.rawText.contains("任务：上英语口语"))
        assertTrue(item.rawText.contains("风险：日期来自“明天”，请确认"))
        assertTrue(item.rawText.contains("待补：reminder_offset"))
    }
}
