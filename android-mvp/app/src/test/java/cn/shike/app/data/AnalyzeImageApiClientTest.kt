package cn.shike.app.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
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
            captureSource = "手动输入入口：请编辑 OCR 文本草稿后选择后端解析或离线样例。",
            fallback = sampleCourse(),
            imageUri = null,
        )

        assertEquals("/v1/analyze", backendAnalysisPathFor(input))
        assertFalse(input.hasImageForCloudAnalysis)
    }
}
