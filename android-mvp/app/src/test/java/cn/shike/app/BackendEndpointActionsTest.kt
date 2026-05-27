package cn.shike.app

import cn.shike.app.data.DEFAULT_BACKEND_BASE_URL
import org.junit.Assert.assertEquals
import org.junit.Test

class BackendEndpointActionsTest {
    @Test
    fun saveBackendEndpointAction_addsHttpSchemeAndTrimsSlash() {
        val saved = mutableListOf<String>()

        val result = saveBackendEndpointAction(" 192.168.1.10:8000/ ", saved::add)

        assertEquals("http://192.168.1.10:8000", result.endpoint)
        assertEquals(listOf("http://192.168.1.10:8000"), saved)
        assertEquals("模型编排：后端地址已保存", result.statusMessage)
    }

    @Test
    fun saveBackendEndpointAction_keepsHttpsEndpoint() {
        val saved = mutableListOf<String>()

        val result = saveBackendEndpointAction("https://example.test:8443/", saved::add)

        assertEquals("https://example.test:8443", result.endpoint)
        assertEquals(listOf("https://example.test:8443"), saved)
    }

    @Test
    fun saveBackendEndpointAction_blankInputFallsBackToDefault() {
        val saved = mutableListOf<String>()

        val result = saveBackendEndpointAction("   ", saved::add)

        assertEquals(DEFAULT_BACKEND_BASE_URL, result.endpoint)
        assertEquals(listOf(DEFAULT_BACKEND_BASE_URL), saved)
    }
}
