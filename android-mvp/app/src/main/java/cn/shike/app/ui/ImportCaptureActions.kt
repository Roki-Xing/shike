package cn.shike.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

@Composable
fun ImportCaptureActions(
    onGallery: () -> Unit,
    onCamera: () -> Unit,
    onManualInput: () -> Unit,
) {
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
        OutlinedButton(onClick = onGallery, modifier = Modifier.weight(1f)) { Text("选择截图") }
        Button(
            onClick = onCamera,
            modifier = Modifier.weight(1f),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF0F766E)),
        ) { Text("拍照导入") }
    }
    OutlinedButton(onClick = onManualInput, modifier = Modifier.fillMaxWidth()) {
        Text("手动输入并继续解析")
    }
}
