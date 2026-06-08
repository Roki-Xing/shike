package cn.shike.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import cn.shike.app.system.VisibleScreenCapturePrompt

@Composable
fun VisibleScreenCapturePromptCard(
    prompt: VisibleScreenCapturePrompt,
    onImport: () -> Unit,
    onDismiss: () -> Unit,
) {
    SectionCard(prompt.title) {
        Text(prompt.body, style = ShikeTypography.Body)
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            OutlinedButton(onClick = onImport, modifier = Modifier.weight(1f)) {
                Text(prompt.primaryActionLabel)
            }
            OutlinedButton(onClick = onDismiss, modifier = Modifier.weight(1f)) {
                Text(prompt.secondaryActionLabel)
            }
        }
    }
}
