package cn.shike.app

import cn.shike.app.data.sampleCourse
import cn.shike.app.data.sampleEvent
import cn.shike.app.ui.modelExplanation
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class ModelExplanationTest {
    @Test
    fun modelExplanation_usesBackendExplanationWhenPresent() {
        val item = sampleEvent().copy(
            status = "待确认",
            rawText = "后端 /v1/analyze：模型识别为活动海报，地点和报名截止时间完整。\n原始OCR：AI应用分享会",
        )

        assertEquals("模型识别为活动海报，地点和报名截止时间完整。", modelExplanation(item))
    }

    @Test
    fun modelExplanation_explainsBackendFallbackBeforeLocalConfirmation() {
        val item = sampleCourse().copy(
            status = "待确认",
            rawText = "后端不可用，回退本地 MockModelAdapter。高数A班今晚18:30改到B203",
        )

        val explanation = modelExplanation(item)

        assertTrue(explanation.contains("后端不可用"))
        assertTrue(explanation.contains("本地规则保留行动卡"))
        assertTrue(explanation.contains("置信度或字段完整性仍需用户确认"))
    }

    @Test
    fun modelExplanation_marksConfirmedCourseFieldsAsTrusted() {
        val explanation = modelExplanation(sampleCourse())

        assertTrue(explanation.contains("文本包含课程、时间、地点或截止事项"))
        assertTrue(explanation.contains("关键字段已确认"))
    }
}
