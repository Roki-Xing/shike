package cn.shike.app.ui

import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun OcrDraftEditor(
    ocrDraft: String,
    onOcrDraftChange: (String) -> Unit,
) {
    OutlinedTextField(
        value = ocrDraft,
        onValueChange = onOcrDraftChange,
        label = { Text("OCR 文本草稿") },
        modifier = Modifier
            .fillMaxWidth()
            .height(132.dp),
        minLines = 3,
    )
}
