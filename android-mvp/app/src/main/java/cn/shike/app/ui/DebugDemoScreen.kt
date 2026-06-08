package cn.shike.app.ui

import androidx.compose.runtime.Composable

@Composable
fun DebugDemoScreen(
    backendUrl: String,
    onBackendUrlChange: (String) -> Unit,
    onSaveBackendUrl: () -> Unit,
    onCourse: () -> Unit,
    onEvent: () -> Unit,
    localMultimodalStatus: LocalMultimodalStatus,
) {
    SectionCard("调试入口") {
        BackendEndpointControls(
            backendUrl = backendUrl,
            onBackendUrlChange = onBackendUrlChange,
            onSaveBackendUrl = onSaveBackendUrl,
        )
        OfflineSampleActions(
            onCourse = onCourse,
            onEvent = onEvent,
        )
    }
    LocalMultimodalDebugPanel(localMultimodalStatus)
    DeliveryReadinessPanel()
    DemoRoutePanel()
}

@Composable
private fun LocalMultimodalDebugPanel(status: LocalMultimodalStatus) {
    val uiState = localMultimodalUiState(status)
    SectionCard("端侧 3B 多模态诊断") {
        KeyValue("安装状态", uiState.statusLabel)
        KeyValue("路由状态", uiState.routeLabel)
        KeyValue(
            "偏好",
            if (status.preference == LocalMultimodalPreference.LocalPreferred) "端侧优先" else "云端优先",
        )
        KeyValue("云端增强", if (status.cloudEnhancedEnabled) "开启" else "关闭")
        KeyValue("输出约束", "init -> callVit -> generate 后仍需 JSON Schema 和用户确认")
        if (status.lastErrorCode != null) {
            KeyValue("错误码", status.lastErrorCode.toString())
        }
    }
}
