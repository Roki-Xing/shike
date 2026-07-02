package cn.shike.app.ui

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun BottomNavBar(
    selectedSection: ShikeMainSection,
    onSelected: (ShikeMainSection) -> Unit,
    onImportClick: () -> Unit,
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
            CenterImportButton(onImportClick)
            BottomNavItem("行动台", "卡", selectedSection == ShikeMainSection.Inbox, Modifier.clickable { onSelected(ShikeMainSection.Inbox) })
            BottomNavItem("设置", "设", selectedSection == ShikeMainSection.Settings, Modifier.clickable { onSelected(ShikeMainSection.Settings) })
        }
    }
}

@Composable
private fun CenterImportButton(onImportClick: () -> Unit) {
    Button(
        onClick = onImportClick,
        modifier = Modifier.widthIn(min = 84.dp),
        colors = ButtonDefaults.buttonColors(containerColor = ShikeColors.Brand),
        shape = RoundedCornerShape(999.dp),
    ) {
        Text("+ 导入")
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ImportActionSheet(
    onGallery: () -> Unit,
    onCamera: () -> Unit,
    onManualInput: () -> Unit,
    onDismiss: () -> Unit,
) {
    ModalBottomSheet(onDismissRequest = onDismiss) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 18.dp, vertical = 12.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Text("新建行动卡", style = ShikeTypography.Title)
            Button(
                onClick = onGallery,
                modifier = Modifier.fillMaxWidth(),
                colors = ButtonDefaults.buttonColors(containerColor = ShikeColors.Brand),
            ) { Text("从截图导入") }
            OutlinedButton(onClick = onCamera, modifier = Modifier.fillMaxWidth()) {
                Text("拍照")
            }
            OutlinedButton(onClick = onManualInput, modifier = Modifier.fillMaxWidth()) {
                Text("手动输入")
            }
        }
    }
}
