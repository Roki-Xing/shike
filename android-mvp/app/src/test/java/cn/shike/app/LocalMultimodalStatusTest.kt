package cn.shike.app

import cn.shike.app.ui.LocalMultimodalInstallState
import cn.shike.app.ui.LocalMultimodalPreference
import cn.shike.app.ui.LocalMultimodalStatus
import cn.shike.app.ui.allowCloudImageForPreference
import cn.shike.app.ui.localMultimodalUiState
import cn.shike.app.ui.userLabel
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class LocalMultimodalStatusTest {
    @Test
    fun localMultimodalUiState_reportsNotInstalledWithoutClaimingAvailability() {
        val status = LocalMultimodalStatus(
            installState = LocalMultimodalInstallState.NotInstalled,
            preference = LocalMultimodalPreference.CloudFirst,
            cloudEnhancedEnabled = true,
        )

        val uiState = localMultimodalUiState(status)

        assertEquals("端侧模型：未安装", uiState.statusLabel)
        assertEquals("云端图片理解", uiState.routeLabel)
        assertTrue(uiState.detail.contains("不打包端侧模型"))
        assertTrue(uiState.detail.contains("所选图片会发送至拾刻服务"))
    }

    @Test
    fun localMultimodalUiState_usesAvailableLocalOnlyWhenRequestedOrCloudDisabled() {
        val cloudFirst = localMultimodalUiState(
            LocalMultimodalStatus(
                installState = LocalMultimodalInstallState.Available,
                preference = LocalMultimodalPreference.CloudFirst,
                cloudEnhancedEnabled = true,
            ),
        )
        val localPreferred = localMultimodalUiState(
            LocalMultimodalStatus(
                installState = LocalMultimodalInstallState.Available,
                preference = LocalMultimodalPreference.LocalPreferred,
                cloudEnhancedEnabled = true,
            ),
        )
        val cloudDisabled = localMultimodalUiState(
            LocalMultimodalStatus(
                installState = LocalMultimodalInstallState.Available,
                preference = LocalMultimodalPreference.CloudFirst,
                cloudEnhancedEnabled = false,
            ),
        )

        assertEquals("端侧模型：可用", cloudFirst.statusLabel)
        assertEquals("云端优先", cloudFirst.routeLabel)
        assertTrue(cloudFirst.detail.contains("云端不可用时再启用"))
        assertEquals("端侧优先", localPreferred.routeLabel)
        assertTrue(localPreferred.detail.contains("用户选择端侧模式"))
        assertEquals("云端关闭，端侧接管", cloudDisabled.routeLabel)
        assertTrue(cloudDisabled.detail.contains("云端关闭"))
    }

    @Test
    fun localMultimodalUiState_reportsInitializationFailureAsManualReviewBoundary() {
        val status = LocalMultimodalStatus(
            installState = LocalMultimodalInstallState.InitFailed,
            preference = LocalMultimodalPreference.LocalPreferred,
            cloudEnhancedEnabled = false,
            lastErrorCode = -17,
        )

        val uiState = localMultimodalUiState(status)

        assertEquals("端侧模型：初始化失败", uiState.statusLabel)
        assertEquals("不可用，转人工确认", uiState.routeLabel)
        assertTrue(uiState.detail.contains("错误码 -17"))
        assertTrue(uiState.detail.contains("同一 JSON Schema"))
    }

    @Test
    fun allowCloudImageForPreference_disablesImageUploadWhenLocalPreferred() {
        assertEquals(true, allowCloudImageForPreference(LocalMultimodalPreference.CloudFirst))
        assertEquals(false, allowCloudImageForPreference(LocalMultimodalPreference.LocalPreferred))
    }

    @Test
    fun localMultimodalPreferenceLabels_areHonestUserModes() {
        assertEquals("云端图片理解", LocalMultimodalPreference.CloudFirst.userLabel)
        assertEquals("仅保存待确认草稿", LocalMultimodalPreference.LocalPreferred.userLabel)
    }
}
