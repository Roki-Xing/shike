package cn.shike.app

import cn.shike.app.ui.cleanPreparationItem
import cn.shike.app.ui.cleanPreparationItems
import cn.shike.app.ui.userFacingLocationText
import cn.shike.app.ui.userFacingRiskCopy
import org.junit.Assert.assertEquals
import org.junit.Test

class UserFacingCopySanitizerTest {
    @Test
    fun cleanPreparationItem_removesExtraQuotesAndPunctuation() {
        assertEquals("带红领巾", cleanPreparationItem("带红领巾'"))
        assertEquals(listOf("带红领巾"), cleanPreparationItems(listOf(" 带红领巾'，", "")))
    }

    @Test
    fun userFacingRiskCopy_mapsDueTimeWord() {
        assertEquals("可能有截止时间，请确认", userFacingRiskCopy("deadline"))
    }

    @Test
    fun userFacingLocationText_usesGentleMissingLocationCopy() {
        assertEquals("地点还没识别到，可以稍后补充", userFacingLocationText(""))
        assertEquals("地点还没识别到，可以稍后补充", userFacingLocationText("待确认"))
    }
}
