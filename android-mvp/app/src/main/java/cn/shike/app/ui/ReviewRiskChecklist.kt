package cn.shike.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import cn.shike.app.domain.ShikeItem

@Composable
fun RiskChecklistPanel(item: ShikeItem) {
    val warnings = actionCardUiModelFrom(item).userWarnings
    if (warnings.isEmpty()) return
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .background(Color(0xFFFFF7ED), RoundedCornerShape(12.dp))
            .padding(12.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        Text("需要确认", color = Color(0xFF9A3412), fontSize = 13.sp, fontWeight = FontWeight.Bold)
        warnings.forEach { warning ->
            RiskItem(warning)
        }
    }
}

@Composable
private fun RiskItem(value: String) {
    Text("- $value", color = Color(0xFF7C2D12), fontSize = 12.sp)
}
