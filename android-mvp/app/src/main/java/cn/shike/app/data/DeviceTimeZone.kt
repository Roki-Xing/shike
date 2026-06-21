package cn.shike.app.data

import java.time.ZoneId

fun deviceZoneId(): ZoneId = ZoneId.systemDefault()

fun deviceTimeZoneId(): String = deviceZoneId().id
