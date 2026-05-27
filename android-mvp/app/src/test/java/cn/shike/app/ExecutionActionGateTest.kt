package cn.shike.app

import cn.shike.app.data.sampleCourse
import cn.shike.app.ui.executionActionGateFor
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
    fun executionActionGateFor_missingFieldsBlockCalendarAndMapOnly() {
        val item = sampleCourse().copy(time = "待确认", location = "")

        val gate = executionActionGateFor(item, isConfirmed = true)

        assertTrue(gate.missingTime)
        assertTrue(gate.missingLocation)
        assertFalse(gate.canUseCalendar)
        assertTrue(gate.canUseReminder)
        assertFalse(gate.canUseMap)
    }
}
