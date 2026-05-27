package cn.shike.app.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class LocalInboxStoreTest {
    @Test
    fun encodeInboxActions_filtersBlankLabelsAndEscapesSeparators() {
        val encoded = encodeInboxActions(listOf(" 加入日历 ", "", "提醒|地图", "  "))

        assertEquals("加入日历|提醒 地图", encoded)
        assertFalse(encoded.contains("||"))
    }

    @Test
    fun decodeInboxActions_trimsLabelsAndFallsBackToCourseActions() {
        assertEquals(listOf("加入日历", "课前提醒", "打开地图"), decodeInboxActions(null))
        assertEquals(listOf("加入日历", "课前提醒", "打开地图"), decodeInboxActions("  | "))
        assertEquals(listOf("加入日历", "课前提醒"), decodeInboxActions(" 加入日历 | 课前提醒 "))
    }

    @Test
    fun sanitizeInboxCaptureSource_redactsSensitiveSourceAndFallsBackToDefault() {
        val sanitized = sanitizeInboxCaptureSource(
            " 相册图片 13812345678 demo@example.com 192.168.0.2:8000 ",
        )

        assertEquals("尚未采集图片，已加载离线样例。", sanitizeInboxCaptureSource("  "))
        assertTrue(sanitized.contains("[手机号已脱敏]"))
        assertTrue(sanitized.contains("[邮箱已脱敏]"))
        assertTrue(sanitized.contains("[局域网地址已脱敏]"))
        assertFalse(sanitized.contains("13812345678"))
        assertFalse(sanitized.contains("demo@example.com"))
        assertFalse(sanitized.contains("192.168.0.2"))
    }

    @Test
    fun sanitizeInboxRawText_redactsSensitiveRawTextAndFallsBackToDefault() {
        val sanitized = sanitizeInboxRawText(
            " 高数通知 13812345678 demo@example.com 学号：2026123456 10.0.2.2:8000 ",
        )

        assertEquals("已从本地缓存恢复。", sanitizeInboxRawText(null))
        assertTrue(sanitized.contains("高数通知"))
        assertTrue(sanitized.contains("[手机号已脱敏]"))
        assertTrue(sanitized.contains("[邮箱已脱敏]"))
        assertTrue(sanitized.contains("学号：[学号已脱敏]"))
        assertTrue(sanitized.contains("[局域网地址已脱敏]"))
        assertFalse(sanitized.contains("13812345678"))
        assertFalse(sanitized.contains("demo@example.com"))
        assertFalse(sanitized.contains("2026123456"))
        assertFalse(sanitized.contains("10.0.2.2"))
    }
}
