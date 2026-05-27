package cn.shike.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun BottomNavItem(label: String, iconText: String, selected: Boolean) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(4.dp),
    ) {
        Box(
            modifier = Modifier
                .size(28.dp)
                .background(if (selected) Color(0xFFDDF4EE) else Color(0xFFF2F4F7), CircleShape),
            contentAlignment = Alignment.Center,
        ) {
            Text(
                iconText,
                color = if (selected) Color(0xFF0F766E) else Color(0xFF667085),
                fontSize = 14.sp,
                fontWeight = FontWeight.Bold,
            )
        }
        Text(
            label,
            color = if (selected) Color(0xFF0F766E) else Color(0xFF667085),
            fontSize = 11.sp,
            fontWeight = if (selected) FontWeight.SemiBold else FontWeight.Normal,
        )
    }
}
