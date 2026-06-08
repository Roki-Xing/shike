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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import cn.shike.app.domain.ShikeItem

@Composable
fun ConfirmBannerActions(
    selected: ShikeItem,
    isConfirmed: Boolean,
    executionResults: List<ExecutionResult>,
    onAddCalendar: (ShikeItem) -> Unit,
    onReminder: (ShikeItem) -> Unit,
    onOpenMap: (ShikeItem) -> Unit,
) {
    val gate = executionActionGateFor(selected, isConfirmed)
    val labels = executionActionButtonLabelsFor(selected, isConfirmed, executionResults)
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
        Button(
            onClick = { onAddCalendar(selected) },
            enabled = gate.canUseCalendar,
            modifier = Modifier.weight(1f),
            colors = ButtonDefaults.buttonColors(containerColor = Color.White),
        ) {
            Text(
                labels.calendar,
                color = Color(0xFF0F766E),
                fontWeight = FontWeight.Bold,
            )
        }
    }
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
        OutlinedButton(
            onClick = { onReminder(selected) },
            enabled = gate.canUseReminder,
            modifier = Modifier.weight(1f),
        ) {
            Text(labels.reminder)
        }
        OutlinedButton(
            onClick = { onOpenMap(selected) },
            enabled = gate.canUseMap,
            modifier = Modifier.weight(1f),
        ) {
            Text(labels.map)
        }
    }
}
