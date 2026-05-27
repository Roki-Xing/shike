package cn.shike.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun AgendaCardFooter(footerLabel: String, actionLabel: String, actionColor: Color) {
    HorizontalDivider(color = Color(0xFFEAEFF3), thickness = 1.dp)
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Text(footerLabel, color = Color(0xFF667085), fontSize = 12.sp)
        TextButton(onClick = { }) {
            Text(actionLabel, color = actionColor, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
        }
    }
}
