package cn.shike.app.ui

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

@Composable
fun AgendaCard(
    iconText: String,
    iconBackground: Color,
    title: String,
    statusText: String,
    statusBackground: Color,
    statusColor: Color,
    detailLines: List<String>,
    footerLabel: String,
    actionLabel: String,
    actionColor: Color,
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        shape = RoundedCornerShape(16.dp),
        border = BorderStroke(1.dp, Color(0xFFE6EDF1)),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
    ) {
        Column(
            modifier = Modifier.padding(14.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            AgendaCardHeader(
                iconText = iconText,
                iconBackground = iconBackground,
                title = title,
                statusText = statusText,
                statusBackground = statusBackground,
                statusColor = statusColor,
                detailLines = detailLines,
                actionColor = actionColor,
            )
            AgendaCardFooter(footerLabel, actionLabel, actionColor)
        }
    }
}
