package cn.shike.app.ui

import androidx.compose.runtime.Composable

@Composable
fun DebugDemoScreen(
    backendUrl: String,
    onBackendUrlChange: (String) -> Unit,
    onSaveBackendUrl: () -> Unit,
    onCourse: () -> Unit,
    onEvent: () -> Unit,
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
    DeliveryReadinessPanel()
    DemoRoutePanel()
}
