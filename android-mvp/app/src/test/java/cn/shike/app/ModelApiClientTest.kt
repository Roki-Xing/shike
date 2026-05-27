package cn.shike.app

import cn.shike.app.data.actionsFromJson
import cn.shike.app.data.buildAnalyzeRequestPayload
import cn.shike.app.data.itemFromAnalyzeJson
import cn.shike.app.data.normalizeBackendUrl
import cn.shike.app.data.sampleCourse
import cn.shike.app.data.sampleEvent
import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class ModelApiClientTest {
    @Test
    fun buildAnalyzeRequestPayload_keepsBackendContractFields() {
        val payload = buildAnalyzeRequestPayload(
            inputId = "android-demo-test",
            sourceType = "screenshot",
            ocrText = "周五 18:30 B203 高数A班调课",
            scene = "课程通知",
        )

        assertEquals("android-demo-test", payload.getString("input_id"))
        assertEquals("screenshot", payload.getString("source_type"))
        assertEquals("周五 18:30 B203 高数A班调课", payload.getString("ocr_text"))
        assertEquals("course_notice", payload.getString("scene_hint"))
        assertEquals("zh-CN", payload.getString("locale"))
        assertEquals("Asia/Shanghai", payload.getString("user_timezone"))
    }

    @Test
    fun itemFromAnalyzeJson_courseNoticeCombinesTimeLocationAndActions() {
        val json = JSONObject()
            .put("scene_type", "course_notice")
            .put("title", "高数A班调课")
            .put("time", JSONObject().put("start_text", "今天 18:30").put("deadline_text", "22:00 截止"))
            .put("location", JSONObject().put("raw", "B203"))
            .put(
                "suggested_actions",
                JSONArray()
                    .put(JSONObject().put("label", "加入日历"))
                    .put(JSONObject().put("label", "课前提醒")),
            )
            .put("explanation", "识别为课程通知，时间和地点完整")

        val item = itemFromAnalyzeJson(json, fallbackText = "fallback")

        assertEquals("高数A班调课", item.title)
        assertEquals("课程通知", item.scene)
        assertEquals("今天 18:30 / 22:00 截止", item.time)
        assertEquals("B203", item.location)
        assertEquals("待确认", item.status)
        assertEquals(listOf("加入日历", "课前提醒"), item.actions)
        assertEquals(sampleCourse().startEpochMillis, item.startEpochMillis)
        assertEquals("后端 /v1/analyze：识别为课程通知，时间和地点完整", item.rawText)
    }

    @Test
    fun itemFromAnalyzeJson_eventPosterUsesFallbacksForBlankFields() {
        val json = JSONObject()
            .put("scene_type", "event_poster")
            .put("title", "")
            .put("time", JSONObject().put("start_text", "").put("deadline_text", ""))
            .put("location", JSONObject().put("raw", ""))
            .put("suggested_actions", JSONArray())

        val item = itemFromAnalyzeJson(json, fallbackText = "OCR 原文兜底")

        assertEquals("", item.title)
        assertEquals("活动海报", item.scene)
        assertEquals("待确认", item.time)
        assertEquals("待确认", item.location)
        assertEquals(listOf("稍后确认"), item.actions)
        assertEquals(sampleEvent().startEpochMillis, item.startEpochMillis)
        assertEquals("后端 /v1/analyze：OCR 原文兜底", item.rawText)
    }

    @Test
    fun actionsFromJson_ignoresBlankAndMalformedActions() {
        val actions = JSONArray()
            .put(JSONObject().put("label", "打开地图"))
            .put(JSONObject().put("label", ""))
            .put("not-an-object")

        assertEquals(listOf("打开地图"), actionsFromJson(actions))
        assertEquals(listOf("稍后确认"), actionsFromJson(null))
        assertTrue(actionsFromJson(JSONArray().put(JSONObject().put("label", ""))).contains("稍后确认"))
    }

    @Test
    fun normalizeBackendUrl_stripsPathQueryAndFragment() {
        assertEquals("http://192.168.1.10:8000", normalizeBackendUrl("192.168.1.10:8000/v1/analyze"))
        assertEquals("http://192.168.1.10:8000", normalizeBackendUrl("http://192.168.1.10:8000/v1/analyze?x=1#frag"))
        assertEquals("https://example.test:8443", normalizeBackendUrl("https://example.test:8443/api/v1/analyze/"))
    }
}
