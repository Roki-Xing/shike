package cn.shike.app.ui

import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import cn.shike.app.domain.userVisibleEvidenceText

@Composable
fun OcrDraftEditor(
    ocrDraft: String,
    onOcrDraftChange: (String) -> Unit,
) {
    OutlinedTextField(
        value = userVisibleOcrDraftText(ocrDraft),
        onValueChange = onOcrDraftChange,
        label = { Text("识别到的文字") },
        modifier = Modifier
            .fillMaxWidth()
            .height(132.dp),
        minLines = 3,
    )
}

fun userVisibleOcrDraftText(text: String): String = userVisibleEvidenceText(text)
