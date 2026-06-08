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
fun ActionPlannerExecutionControls(
    item: ShikeItem,
    isConfirmed: Boolean,
    executionResults: List<ExecutionResult>,
    onAddCalendar: (ShikeItem) -> Unit,
    onReminder: (ShikeItem) -> Unit,
    onOpenMap: (ShikeItem) -> Unit,
) {
    val gate = executionActionGateFor(item, isConfirmed)
    val labels = executionActionButtonLabelsFor(item, isConfirmed, executionResults)
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
        Button(
            onClick = { onAddCalendar(item) },
            enabled = gate.canUseCalendar,
            modifier = Modifier.weight(1f),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF0F766E)),
        ) { Text(labels.calendar) }
        OutlinedButton(onClick = { onReminder(item) }, enabled = gate.canUseReminder, modifier = Modifier.weight(1f)) {
            Text(labels.reminder)
        }
        OutlinedButton(onClick = { onOpenMap(item) }, enabled = gate.canUseMap, modifier = Modifier.weight(1f)) {
            Text(labels.map)
        }
    }
}
