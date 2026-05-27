package cn.shike.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import cn.shike.app.domain.ShikeItem

@Composable
fun RiskChecklistPanel(item: ShikeItem) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .background(Color(0xFFFFF7ED), RoundedCornerShape(12.dp))
            .padding(12.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        Text("风险与缺失字段", color = Color(0xFF9A3412), fontSize = 13.sp, fontWeight = FontWeight.Bold)
        RiskItem("模型置信度", if (item.status == "待确认") "低置信度，待人工确认" else "人工确认已完成")
        RiskItem("相对时间", if ("今天" in item.time || "今晚" in item.time) "需按当前日期确认" else "已明确")
        RiskItem("报名链接", if ("活动" in item.scene) "缺失，先创建提醒和地点入口" else "不需要")
        RiskItem("系统写入", "日历、提醒、地图均需用户确认")
    }
}

@Composable
private fun RiskItem(label: String, value: String) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Text(label, color = Color(0xFF9A3412), fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
        Text(value, color = Color(0xFF7C2D12), fontSize = 12.sp, textAlign = TextAlign.End)
    }
}
