package cn.shike.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

@Composable
fun ShikeActionCard(title: String, modifier: Modifier = Modifier, content: @Composable () -> Unit) {
    SectionCard(title = title, modifier = modifier, content = content)
}

@Composable
fun ShikeStatusPill(
    label: String,
    background: Color = ShikeColors.BrandSoft,
    contentColor: Color = ShikeColors.Brand,
) {
    Pill(label, background, contentColor)
}

@Composable
fun ShikePrimaryButton(text: String, onClick: () -> Unit, modifier: Modifier = Modifier) {
    Button(
        onClick = onClick,
        modifier = modifier,
        colors = ButtonDefaults.buttonColors(containerColor = ShikeColors.Brand),
    ) {
        Text(text)
    }
}

@Composable
fun ShikeRiskPanel(
    title: String,
    detail: String,
    tone: Color = ShikeColors.Warning,
) {
    ShikeActionCard(title) {
        Text(detail, style = ShikeTypography.Body.copy(color = tone))
    }
}

@Composable
fun ShikeFieldEditor(
    label: String,
    value: String,
    onValueChange: (String) -> Unit,
    modifier: Modifier = Modifier,
    singleLine: Boolean = true,
) {
    OutlinedTextField(
        value = value,
        onValueChange = onValueChange,
        label = { Text(label) },
        modifier = modifier.fillMaxWidth(),
        singleLine = singleLine,
    )
}

@Composable
fun ShikeInboxFilterBar(
    filters: List<String>,
    selected: String,
    onSelected: (String) -> Unit,
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        filters.forEach { filter ->
            val active = filter == selected
            OutlinedButton(onClick = { onSelected(filter) }) {
                Text(if (active) "✓ $filter" else filter)
            }
        }
    }
}

@Composable
fun ShikeEmptyState(
    title: String,
    detail: String,
    actionLabel: String? = null,
    onAction: (() -> Unit)? = null,
) {
    ShikeActionCard(title) {
        Text(detail, style = ShikeTypography.Body)
        if (actionLabel != null && onAction != null) {
            ShikePrimaryButton(actionLabel, onAction)
        }
    }
}

@Composable
fun ShikeErrorState(title: String, detail: String, actionLabel: String? = null, onAction: (() -> Unit)? = null) {
    ShikeActionCard(title) {
        Text(detail, style = ShikeTypography.Body.copy(color = ShikeColors.Warning))
        if (actionLabel != null && onAction != null) {
            ShikePrimaryButton(actionLabel, onAction)
        }
    }
}

@Composable
fun ShikeLoadingSkeleton(title: String, detail: String = "正在加载") {
    ShikeActionCard(title) {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
                CircularProgressIndicator(modifier = Modifier.size(16.dp), strokeWidth = 2.dp, color = ShikeColors.Brand)
                Text(detail, color = ShikeColors.Muted)
            }
            repeat(3) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(10.dp)
                        .background(ShikeColors.BrandSoft, RoundedCornerShape(999.dp)),
                )
            }
        }
    }
}
