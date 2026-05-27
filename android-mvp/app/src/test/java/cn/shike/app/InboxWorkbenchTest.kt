package cn.shike.app

import cn.shike.app.data.sampleCourse
import cn.shike.app.ui.ExecutionResult
import cn.shike.app.ui.inboxAllStatusFilter
import cn.shike.app.ui.inboxArchiveActionStateFor
import cn.shike.app.ui.inboxWorkbenchEntryFrom
import cn.shike.app.ui.selectedInboxStatusFor
import cn.shike.app.ui.visibleInboxEntries
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class InboxWorkbenchTest {
    @Test
    fun selectedInboxStatusFor_unsupportedStatusFallsBackToPendingReview() {
        assertEquals("待确认", selectedInboxStatusFor("草稿"))
        assertEquals("即将截止", selectedInboxStatusFor("即将截止"))
        assertEquals(inboxAllStatusFilter, selectedInboxStatusFor(inboxAllStatusFilter))
    }

    @Test
    fun inboxWorkbenchEntryFrom_searchesRawTextExplanationAndExecutionSummary() {
        val item = sampleCourse().copy(rawText = "后端 /v1/analyze：课程教室变更可信\n原文 B203")
        val entry = inboxWorkbenchEntryFrom(
            item = item,
            source = "相册图片 course.png",
            executionResults = listOf(ExecutionResult("地图", "已请求", "打开地图")),
        )

        assertTrue(entry.matches("B203"))
        assertTrue(entry.matches("课程教室变更可信"))
        assertTrue(entry.matches("地图:已请求"))
    }

    @Test
    fun visibleInboxEntries_respectsArchiveStatusAndSearchQuery() {
        val current = inboxWorkbenchEntryFrom(sampleCourse(), "截图", emptyList())
        val other = current.copy(title = "活动报名", status = "即将截止", rawText = "报名截止")

        assertEquals(
            listOf(current),
            visibleInboxEntries(
                entries = listOf(current, other),
                selectedStatus = "已安排",
                query = "截图",
                archivedKeys = emptySet(),
            ),
        )
        assertTrue(
            visibleInboxEntries(
                entries = listOf(current),
                selectedStatus = "已安排",
                query = "",
                archivedKeys = setOf(current.archiveKey),
            ).isEmpty(),
        )
    }

    @Test
    fun visibleInboxEntries_allStatusPrioritizesUrgentReviewAndScheduleOrder() {
        val due = inboxWorkbenchEntryFrom(
            sampleCourse().copy(title = "报名截止", status = "即将截止", startEpochMillis = 30L),
            "分享",
            emptyList(),
        )
        val pending = inboxWorkbenchEntryFrom(
            sampleCourse().copy(title = "待确认课程", status = "待确认", startEpochMillis = 10L),
            "截图",
            emptyList(),
        )
        val scheduledEarly = inboxWorkbenchEntryFrom(
            sampleCourse().copy(title = "早课", status = "已安排", startEpochMillis = 20L),
            "相册",
            emptyList(),
        )
        val scheduledLate = inboxWorkbenchEntryFrom(
            sampleCourse().copy(title = "晚课", status = "已安排", startEpochMillis = 40L),
            "相册",
            emptyList(),
        )

        val visible = visibleInboxEntries(
            entries = listOf(scheduledLate, scheduledEarly, pending, due),
            selectedStatus = inboxAllStatusFilter,
            query = "",
            archivedKeys = emptySet(),
        )

        assertEquals(listOf(due, pending, scheduledEarly, scheduledLate), visible)
    }

    @Test
    fun inboxArchiveActionStateFor_separatesArchiveAndRestoreDecisions() {
        val active = inboxArchiveActionStateFor(isArchived = false)
        val archived = inboxArchiveActionStateFor(isArchived = true)

        assertTrue(active.archiveEnabled)
        assertFalse(active.restoreEnabled)
        assertEquals("收件箱内", active.statusLabel)
        assertTrue(active.detailText.contains("不会删除原始信息"))

        assertFalse(archived.archiveEnabled)
        assertTrue(archived.restoreEnabled)
        assertEquals("已归档", archived.statusLabel)
        assertTrue(archived.detailText.contains("恢复后回到状态筛选结果"))
    }
}
