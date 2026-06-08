package cn.shike.app.ui

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun BottomNavBar(
    selectedSection: ShikeMainSection,
    onSelected: (ShikeMainSection) -> Unit,
    modifier: Modifier = Modifier,
) {
    Card(
        modifier = modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = ShikeColors.Surface),
        shape = RoundedCornerShape(16.dp),
        border = BorderStroke(1.dp, ShikeColors.Line),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(vertical = 10.dp),
            horizontalArrangement = Arrangement.SpaceEvenly,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            BottomNavItem("首页", "⌂", selectedSection == ShikeMainSection.Home, Modifier.clickable { onSelected(ShikeMainSection.Home) })
            BottomNavItem("导入", "入", selectedSection == ShikeMainSection.Import, Modifier.clickable { onSelected(ShikeMainSection.Import) })
            BottomNavItem("收件箱", "箱", selectedSection == ShikeMainSection.Inbox, Modifier.clickable { onSelected(ShikeMainSection.Inbox) })
            BottomNavItem("设置", "设", selectedSection == ShikeMainSection.Settings, Modifier.clickable { onSelected(ShikeMainSection.Settings) })
        }
    }
}
