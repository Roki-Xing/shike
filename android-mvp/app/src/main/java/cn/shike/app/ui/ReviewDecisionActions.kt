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
import cn.shike.app.domain.ShikeItem

@Composable
fun ReviewDecisionActions(
    item: ShikeItem,
    draftTitle: String,
    draftTime: String,
    draftLocation: String,
    draftStatus: String,
    onReviewed: (ShikeItem) -> Unit,
) {
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
        Button(
            onClick = {
                onReviewed(
                    item.copy(
                        title = draftTitle.ifBlank { item.title },
                        time = draftTime.ifBlank { "待确认" },
                        location = draftLocation.ifBlank { "待确认" },
                        status = draftStatus.ifBlank { "待确认" },
                    )
                )
            },
            modifier = Modifier.weight(1f),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF0F766E)),
        ) {
            Text("确认修正")
        }
        OutlinedButton(
            onClick = {
                onReviewed(
                    item.copy(
                        title = draftTitle.ifBlank { item.title },
                        time = draftTime.ifBlank { item.time },
                        location = draftLocation.ifBlank { item.location },
                        status = "已忽略",
                    )
                )
            },
            modifier = Modifier.weight(1f),
        ) {
            Text("忽略")
        }
    }
}
