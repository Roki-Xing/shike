package cn.shike.app

import cn.shike.app.data.actionsFromJson
import cn.shike.app.data.buildAnalyzeRequestPayload
import cn.shike.app.data.itemFromAnalyzeImageJson
import cn.shike.app.data.itemFromAnalyzeJson
import cn.shike.app.data.normalizeBackendUrl
import cn.shike.app.data.sampleCourse
import cn.shike.app.data.sampleEvent
import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import java.time.Instant
import java.time.ZoneId

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
    fun buildAnalyzeRequestPayload_acceptsShareTextAndManualSourceTypes() {
        val sharePayload = buildAnalyzeRequestPayload(
            inputId = "android-share-test",
            sourceType = "share_text",
            ocrText = "活动报名今晚截止",
            scene = "活动海报",
        )
        val manualPayload = buildAnalyzeRequestPayload(
            inputId = "android-manual-test",
            sourceType = "manual",
            ocrText = "高数A班今晚18:30改到B203",
            scene = "课程通知",
        )

        assertEquals("share_text", sharePayload.getString("source_type"))
        assertEquals("event_poster", sharePayload.getString("scene_hint"))
        assertEquals("manual", manualPayload.getString("source_type"))
        assertEquals("course_notice", manualPayload.getString("scene_hint"))
    }

    @Test
    fun buildAnalyzeRequestPayload_mapsExtendedSceneHints() {
        val assignmentPayload = buildAnalyzeRequestPayload(
            inputId = "android-assignment-test",
            sourceType = "manual",
            ocrText = "数据库实验报告今晚22:00前提交",
            scene = "作业截止",
        )
        val meetingPayload = buildAnalyzeRequestPayload(
            inputId = "android-meeting-test",
            sourceType = "share_text",
            ocrText = "项目周会今晚10:00在腾讯会议进行",
            scene = "会议通知",
        )
        val interviewPayload = buildAnalyzeRequestPayload(
            inputId = "android-interview-test",
            sourceType = "screenshot",
            ocrText = "HR通知明天14:00线上面试",
            scene = "面试通知",
        )
        val travelPayload = buildAnalyzeRequestPayload(
            inputId = "android-travel-test",
            sourceType = "camera",
            ocrText = "高铁出行今晚10:00在西安北站集合",
            scene = "出行票务",
        )

        assertEquals("assignment_deadline", assignmentPayload.getString("scene_hint"))
        assertEquals("meeting_notice", meetingPayload.getString("scene_hint"))
        assertEquals("interview_notice", interviewPayload.getString("scene_hint"))
        assertEquals("travel_ticket", travelPayload.getString("scene_hint"))
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
        assertTrue(item.startEpochMillis > 0L)
        assertNotEquals(sampleCourse().startEpochMillis, item.startEpochMillis)
        assertEquals("云端 AI 解析：识别为课程通知，时间和地点完整", item.rawText)
    }

    @Test
    fun itemFromAnalyzeJson_usesNormalizedStartInsteadOfSampleEpoch() {
        val item = itemFromAnalyzeJson(
            JSONObject()
                .put("scene_type", "course_notice")
                .put("title", "英语口语课")
                .put(
                    "time",
                    JSONObject()
                        .put("start_text", "明天早上九点")
                        .put("normalized_start", "2026-06-10T09:00:00+08:00")
                        .put("deadline_text", JSONObject.NULL),
                )
                .put("location", JSONObject().put("raw", "E520"))
                .put("suggested_actions", JSONArray().put(JSONObject().put("label", "加入日历"))),
            fallbackText = "明天早上九点上英语口语教室 E520",
        )

        assertEquals("明天早上九点", item.time)
        assertFalseContainsNull(item.time)
        assertEquals(Instant.parse("2026-06-10T01:00:00Z").toEpochMilli(), item.startEpochMillis)
        assertNotEquals(sampleCourse().startEpochMillis, item.startEpochMillis)
    }

    @Test
    fun itemFromAnalyzeImageJson_normalizesChineseRelativeStartTextWhenNormalizedStartMissing() {
        val item = itemFromAnalyzeImageJson(
            JSONObject()
                .put("scene_type", "course_notice")
                .put("title", "英语口语课")
                .put("time", JSONObject().put("start_text", "明天早上九点").put("deadline_text", JSONObject.NULL))
                .put("location", JSONObject().put("raw", "E520"))
                .put("suggested_actions", JSONArray().put(JSONObject().put("label", "加入日历")))
                .put("explanation", "识别到课程、时间和地点"),
            fallbackText = "明天早上九点上英语口语教室 E520",
            referenceNowMillis = Instant.parse("2026-06-09T04:00:00Z").toEpochMilli(),
            zoneId = ZoneId.of("Asia/Shanghai"),
        )

        assertEquals("明天早上九点", item.time)
        assertEquals(Instant.parse("2026-06-10T01:00:00Z").toEpochMilli(), item.startEpochMillis)
        assertNotEquals(sampleCourse().startEpochMillis, item.startEpochMillis)
    }

    @Test
    fun itemFromAnalyzeJson_eventPosterUsesPendingEpochForBlankFields() {
        val json = JSONObject()
            .put("scene_type", "event_poster")
            .put("title", "")
            .put("time", JSONObject().put("start_text", "").put("deadline_text", ""))
            .put("location", JSONObject().put("raw", ""))
            .put("suggested_actions", JSONArray())

        val item = itemFromAnalyzeJson(json, fallbackText = "OCR 原文兜底")

        assertEquals("待确认碎片", item.title)
        assertEquals("活动海报", item.scene)
        assertEquals("待确认", item.time)
        assertEquals("待确认", item.location)
        assertEquals(listOf("稍后确认"), item.actions)
        assertEquals(0L, item.startEpochMillis)
        assertEquals("云端 AI 解析：OCR 原文兜底", item.rawText)
    }

    @Test
    fun itemFromAnalyzeJson_unknownSceneFallsBackToPendingLabel() {
        val item = itemFromAnalyzeJson(
            JSONObject()
                .put("scene_type", "unknown")
                .put("title", "会议通知")
                .put("time", JSONObject().put("start_text", "今晚10:00").put("deadline_text", ""))
                .put("location", JSONObject().put("raw", "腾讯会议"))
                .put("suggested_actions", JSONArray().put(JSONObject().put("label", "加入会议日历")))
                .put("explanation", "识别到会议语义，但按 unknown 输出"),
            fallbackText = "fallback",
        )

        assertEquals("待确认", item.scene)
        assertEquals("今晚10:00", item.time)
        assertEquals(listOf("加入会议日历"), item.actions)
        assertTrue(item.startEpochMillis > 0L)
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

    private fun assertFalseContainsNull(value: String) {
        assertTrue(!value.contains("null", ignoreCase = true))
    }
}
