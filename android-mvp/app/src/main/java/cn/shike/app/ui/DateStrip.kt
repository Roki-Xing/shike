package cn.shike.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import java.time.LocalDate
import java.time.format.DateTimeFormatter
import java.util.Locale

@Composable
fun DateStrip() {
    val todayText = remember { formatTodayForHome(LocalDate.now()) }
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.SpaceBetween,
    ) {
        Row(
            modifier = Modifier.weight(1f),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Box(
                modifier = Modifier
                    .size(28.dp)
                    .background(Color(0xFFE0F5EE), CircleShape),
                contentAlignment = Alignment.Center,
            ) {
                Text("日", color = Color(0xFF0F766E), fontSize = 13.sp, fontWeight = FontWeight.Bold)
            }
            Column(verticalArrangement = Arrangement.spacedBy(2.dp)) {
                Text("今天  $todayText", color = Color(0xFF344054), fontSize = 13.sp)
                Text(dateStripSubtitle(), color = Color(0xFF98A2B3), fontSize = 11.sp)
            }
        }
        Pill("全部日程", Color.White, Color(0xFF667085), Color(0xFFE3E8EF))
    }
}

fun formatTodayForHome(date: LocalDate): String =
    date.format(DateTimeFormatter.ofPattern("M月d日 EEEE", Locale.CHINA))

fun dateStripSubtitle(): String =
    "系统日期仅用于排序提示，不作为任务时间"
