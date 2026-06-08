package cn.shike.app

import cn.shike.app.data.saveBackendUrlFromInput

data class BackendEndpointResult(
    val endpoint: String,
    val statusMessage: String,
)

fun saveBackendEndpointAction(
    backendUrl: String,
    onSaveBackendUrl: (String) -> Unit,
): BackendEndpointResult =
    BackendEndpointResult(
        endpoint = saveBackendUrlFromInput(backendUrl, onSaveBackendUrl),
        statusMessage = "云侧连接已保存",
    )
