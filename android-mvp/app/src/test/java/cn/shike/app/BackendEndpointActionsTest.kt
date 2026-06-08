package cn.shike.app

import cn.shike.app.data.DEFAULT_BACKEND_BASE_URL
import cn.shike.app.data.migrateLegacyBackendBaseUrl
import org.junit.Assert.assertEquals
import org.junit.Test

class BackendEndpointActionsTest {
    @Test
    fun saveBackendEndpointAction_addsHttpSchemeAndTrimsSlash() {
        val saved = mutableListOf<String>()

        val result = saveBackendEndpointAction(" 192.168.1.10:8000/ ", saved::add)

        assertEquals("http://192.168.1.10:8000", result.endpoint)
        assertEquals(listOf("http://192.168.1.10:8000"), saved)
        assertEquals("云侧连接已保存", result.statusMessage)
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

    @Test
    fun migrateLegacyBackendBaseUrl_replacesOldEmulatorDefaultOnly() {
        assertEquals(DEFAULT_BACKEND_BASE_URL, migrateLegacyBackendBaseUrl(null))
        assertEquals(DEFAULT_BACKEND_BASE_URL, migrateLegacyBackendBaseUrl(""))
        assertEquals(DEFAULT_BACKEND_BASE_URL, migrateLegacyBackendBaseUrl("http://10.0.2.2:8000"))
        assertEquals("http://192.168.1.10:8000", migrateLegacyBackendBaseUrl("http://192.168.1.10:8000"))
    }
}
