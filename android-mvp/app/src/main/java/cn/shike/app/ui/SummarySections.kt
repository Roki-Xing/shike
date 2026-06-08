package cn.shike.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun TodaySummaryPanel() {
    SectionCard("今日概要") {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
        ) {
            SummaryStat(value = "3", label = "待办事项", color = Color(0xFF0F766E))
            SummaryStat(value = "1", label = "即将截止", color = Color(0xFFF97316))
            SummaryStat(value = "2", label = "地点需前往", color = Color(0xFF2563EB))
        }
    }
}

@Composable
fun DemoRoutePanel() {
    SectionCard("3分钟演示路线") {
        DemoRouteStep("1", "课程截图", "选择截图 -> 课程样例 -> 确认并安排")
        DemoRouteStep("2", "活动拍照", "拍照导入 -> 活动样例 -> 即将截止")
        DemoRouteStep("3", "后端回退", "后端解析失败时保留 MockModelAdapter")
        DemoRouteStep("4", "重启恢复", "返回今日行动台查看收件箱缓存")
    }
}

@Composable
fun SummaryStat(value: String, label: String, color: Color) {
    Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(4.dp)) {
        Text(value, color = color, fontSize = 22.sp, fontWeight = FontWeight.Bold)
        Text(label, color = Color(0xFF667085), fontSize = 12.sp, textAlign = TextAlign.Center)
    }
}
