package cn.shike.app.data

import org.junit.Assert.assertEquals
import org.junit.Test

class PrivacyRedactionTest {
    @Test
    fun redactSensitiveLogText_removesPersonalAndLocalNetworkData() {
        val raw = "联系人 13812345678，邮箱 test@example.com，学号: 2026123456，后端 http://192.168.1.10:8000 可用。"

        val redacted = redactSensitiveLogText(raw)

        assertEquals(
            "联系人 [手机号已脱敏]，邮箱 [邮箱已脱敏]，学号: [学号已脱敏]，后端 http://[局域网地址已脱敏] 可用。",
            redacted,
        )
    }

    @Test
    fun redactSensitiveLogText_keepsNonSensitiveActionTextReadable() {
        val raw = "课程提醒：今晚 18:30 到 B203，作业第5章 22:00 前提交。"

        val redacted = redactSensitiveLogText(raw)

        assertEquals(raw, redacted)
    }
}
