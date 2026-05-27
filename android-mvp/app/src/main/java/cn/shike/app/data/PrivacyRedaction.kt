package cn.shike.app.data

private val phoneRegex = Regex("""1[3-9]\d{9}""")
private val emailRegex = Regex("""[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}""")
private val studentIdRegex = Regex("""(学号[:：\s]*)[A-Za-z0-9-]{6,}""")
private val localAddressRegex = Regex("""\b(?:10|172\.(?:1[6-9]|2\d|3[0-1])|192\.168)(?:\.\d{1,3}){2}(?::\d{2,5})?\b""")

/**
 * Redacts sensitive OCR or backend text before storing fallback logs.
 *
 * Args:
 *     text: Raw OCR text or backend explanation.
 *
 * Returns:
 *     Text with 手机号, 邮箱, 学号 and local network addresses removed.
 */
fun redactSensitiveLogText(text: String): String =
    text
        .replace(phoneRegex, "[手机号已脱敏]")
        .replace(emailRegex, "[邮箱已脱敏]")
        .replace(studentIdRegex) { "${it.groupValues[1]}[学号已脱敏]" }
        .replace(localAddressRegex, "[局域网地址已脱敏]")
