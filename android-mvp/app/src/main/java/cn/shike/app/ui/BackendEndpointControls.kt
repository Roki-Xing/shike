package cn.shike.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun BackendEndpointControls(
    backendUrl: String,
    onBackendUrlChange: (String) -> Unit,
    onSaveBackendUrl: () -> Unit,
) {
    OutlinedTextField(
        value = backendUrl,
        onValueChange = onBackendUrlChange,
        label = { Text("后端地址") },
        modifier = Modifier.fillMaxWidth(),
        singleLine = true,
    )
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
        OutlinedButton(onClick = onSaveBackendUrl, modifier = Modifier.weight(1f)) {
            Text("保存后端地址")
        }
    }
}
