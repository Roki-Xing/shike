package cn.shike.app.ui

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun ActionReadinessBar(
    model: ActionReadinessUiModel,
    modifier: Modifier = Modifier,
    compact: Boolean = false,
) {
    val progress = if (model.total <= 0) 0f else model.completed.toFloat() / model.total.toFloat()
    val animatedProgress = animateFloatAsState(targetValue = progress).value
    Column(modifier = modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(if (compact) 6.dp else 8.dp)) {
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text(model.title, color = ShikeColors.Ink, fontSize = if (compact) 12.sp else 14.sp, fontWeight = FontWeight.Bold)
            Text(model.subtitle, color = ShikeColors.Muted, fontSize = if (compact) 11.sp else 12.sp)
        }
        LinearProgressIndicator(
            progress = { animatedProgress },
            modifier = Modifier.fillMaxWidth(),
            color = ShikeColors.Brand,
        )
        Row(horizontalArrangement = Arrangement.spacedBy(6.dp), modifier = Modifier.fillMaxWidth()) {
            model.steps.forEach { step ->
                ReadinessStepChip(
                    step = step,
                    modifier = Modifier.weight(1f),
                )
            }
        }
    }
}

@Composable
private fun ReadinessStepChip(step: ActionReadinessStepUi, modifier: Modifier = Modifier) {
    Pill(
        label = if (step.completed) "✓ ${step.label}" else step.label,
        background = if (step.completed) ShikeColors.BrandSoft else ShikeColors.WarningSoft,
        contentColor = if (step.completed) ShikeColors.Brand else ShikeColors.Warning,
        modifier = modifier,
    )
}
