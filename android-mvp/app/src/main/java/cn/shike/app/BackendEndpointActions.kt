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
        statusMessage = "模型编排：后端地址已保存",
    )
