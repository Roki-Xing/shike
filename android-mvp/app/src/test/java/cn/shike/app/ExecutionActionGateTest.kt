package cn.shike.app

import cn.shike.app.data.sampleCourse
import cn.shike.app.ui.ExecutionResult
import cn.shike.app.ui.executionActionButtonLabelsFor
import cn.shike.app.ui.executionActionGateFor
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class ExecutionActionGateTest {
    @Test
    fun executionActionGateFor_unconfirmedItemBlocksAllSensitiveActions() {
        val gate = executionActionGateFor(sampleCourse(), isConfirmed = false)

        assertFalse(gate.canUseCalendar)
        assertFalse(gate.canUseReminder)
        assertFalse(gate.canUseMap)
        assertFalse(gate.missingTime)
        assertFalse(gate.missingLocation)
    }

    @Test
    fun executionActionGateFor_confirmedItemAllowsCompleteFields() {
        val gate = executionActionGateFor(sampleCourse(), isConfirmed = true)

        assertTrue(gate.canUseCalendar)
        assertTrue(gate.canUseReminder)
        assertTrue(gate.canUseMap)
    }

    @Test
    fun executionActionGateFor_missingFieldsBlockCalendarReminderAndMap() {
        val item = sampleCourse().copy(time = "待确认", location = "")

        val gate = executionActionGateFor(item, isConfirmed = true)

        assertTrue(gate.missingTime)
        assertTrue(gate.missingLocation)
        assertFalse(gate.canUseCalendar)
        assertFalse(gate.canUseReminder)
        assertFalse(gate.canUseMap)
    }

    @Test
    fun executionActionGateFor_timeTextWithoutEpochBlocksCalendarAndReminder() {
        val item = sampleCourse().copy(time = "明天早上九点", location = "E520", startEpochMillis = 0L)

        val gate = executionActionGateFor(item, isConfirmed = true)

        assertTrue(gate.missingTime)
        assertFalse(gate.missingLocation)
        assertFalse(gate.canUseCalendar)
        assertFalse(gate.canUseReminder)
        assertTrue(gate.canUseMap)
    }

    @Test
    fun executionActionButtonLabelsFor_usesGuideActionCopyAfterConfirmation() {
        val labels = executionActionButtonLabelsFor(sampleCourse(), isConfirmed = true)

        assertEquals("打开日历", labels.calendar)
        assertEquals("设置提醒", labels.reminder)
        assertEquals("查看路线", labels.map)
    }

    @Test
    fun executionActionButtonLabelsFor_namesMissingFieldRecovery() {
        val item = sampleCourse().copy(time = "待确认", location = "")

        val labels = executionActionButtonLabelsFor(item, isConfirmed = true)

        assertEquals("补充时间后可用", labels.calendar)
        assertEquals("补充时间后可用", labels.reminder)
        assertEquals("补充地点后可用", labels.map)
    }

    @Test
    fun executionActionButtonLabelsFor_blocksUnconfirmedActionsWithReviewCopy() {
        val labels = executionActionButtonLabelsFor(sampleCourse(), isConfirmed = false)

        assertEquals("先确认字段", labels.calendar)
        assertEquals("先确认字段", labels.reminder)
        assertEquals("先确认字段", labels.map)
    }

    @Test
    fun executionActionButtonLabelsFor_namesNotificationRecoveryAfterPermissionBlocked() {
        val labels = executionActionButtonLabelsFor(
            item = sampleCourse(),
            isConfirmed = true,
            executionResults = listOf(
                ExecutionResult("提醒", "已调度", "通知权限拒绝时进入 permission_blocked 并保留行动卡。")
            ),
        )

        assertEquals("打开日历", labels.calendar)
        assertEquals("去开启通知", labels.reminder)
        assertEquals("查看路线", labels.map)
    }
}
