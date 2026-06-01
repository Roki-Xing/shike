package cn.shike.app.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class OcrEngineTest {
    @Test
    fun manualOcrEngine_keepsUserTextAndReportsBlankFailure() {
        val manual = ManualOcrEngine()
        val ok = manual.recognize(
            CaptureInput(
                sourceType = CaptureSourceType.Manual,
                sourceLabel = "手动输入",
                manualText = "高数A班今晚18:30改到B203",
                allowCloudEnhancement = false,
            ),
        )
        val blank = manual.recognize(CaptureInput(sourceType = CaptureSourceType.Manual, sourceLabel = "手动输入"))

        assertEquals("manual", ok.engineName)
        assertEquals(1f, ok.confidence)
        assertEquals("高数A班今晚18:30改到B203", ok.text)
        assertEquals(0f, blank.confidence)
        assertTrue(blank.failureHint.orEmpty().contains("手动粘贴"))
    }

    @Test
    fun mockOcrEngine_producesGalleryAndCameraDraftText() {
        val engine = MockOcrEngine()
        val camera = engine.recognize(CaptureInput(sourceType = CaptureSourceType.Camera, sourceLabel = "相机"))
        val gallery = engine.recognize(CaptureInput(sourceType = CaptureSourceType.Gallery, sourceLabel = "相册"))

        assertEquals("mock", camera.engineName)
        assertTrue(camera.text.contains("AI应用分享会"))
        assertTrue(gallery.text.contains("高数A班"))
        assertTrue(gallery.confidence > 0.8f)
    }

    @Test
    fun captureDraftFromInput_recordsOcrMetadataAndPrivacyChoice() {
        val draft = captureDraftFromInput(
            input = CaptureInput(
                sourceType = CaptureSourceType.ShareText,
                sourceLabel = "系统分享文本",
                manualText = "活动报名今晚截止",
                allowCloudEnhancement = false,
            ),
            engine = ManualOcrEngine(),
        )

        assertEquals("share", draft.channel)
        assertEquals(CaptureSourceType.ShareText, draft.sourceType)
        assertEquals("活动报名今晚截止", draft.ocrText)
        assertEquals(PrivacyLevel.LocalOnly, draft.privacyLevel)
        assertEquals("manual", draft.ocrEngineName)
        assertFalse(draft.cloudAllowed)
        assertTrue(draft.imageCleared)
        assertNotEquals("", draft.id)
    }
}
