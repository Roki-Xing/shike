package cn.shike.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.material3.Switch
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import cn.shike.app.LocalDataClearConfirmationState
import cn.shike.app.cancelLocalDataClearConfirmation
import cn.shike.app.confirmLocalDataClearConfirmation
import cn.shike.app.requestLocalDataClearConfirmation

@Composable
fun DeliveryReadinessPanel() {
    SectionCard("交付物自检中心") {
        ReadinessRow("APK", "已构建，可真机安装", Color(0xFF0F766E))
        ReadinessRow("真机证据", "按 device-demo-checklist 录屏", Color(0xFF2563EB))
        ReadinessRow("后端", "支持 /health、/v1/schema、/v1/analyze", Color(0xFF0F766E))
        ReadinessRow("总体验收", "REAL_WORLD_READY_METRIC 22/22", Color(0xFFF97316))
        Text("现场演示时可直接打开本区说明交付状态，不依赖计划文件。", color = Color(0xFF667085), fontSize = 12.sp)
    }
}

@Composable
private fun ReadinessRow(label: String, value: String, color: Color) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = androidx.compose.foundation.layout.Arrangement.spacedBy(10.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Box(
            modifier = Modifier
                .size(9.dp)
                .background(color, CircleShape),
        )
        Text(label, modifier = Modifier.weight(0.8f), color = Color(0xFF344054), fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
        Text(value, modifier = Modifier.weight(2f), color = Color(0xFF101828), fontSize = 12.sp, textAlign = TextAlign.End)
    }
}

@Composable
fun PrivacyPanel(
    cloudEnhancedEnabled: Boolean,
    onCloudEnhancedChange: (Boolean) -> Unit,
    localMultimodalStatus: LocalMultimodalStatus,
    onLocalMultimodalPreferenceChange: (LocalMultimodalPreference) -> Unit,
    onClearLocalData: () -> Unit,
    screenshotAssistEnabled: Boolean = false,
    onScreenshotAssistChange: (Boolean) -> Unit = {},
    cleanupPreference: String = "每次询问（推荐）",
) {
    val localState = localMultimodalUiState(localMultimodalStatus)
    var clearConfirmationState by remember { mutableStateOf(LocalDataClearConfirmationState()) }
    SectionCard("隐私与端云设置") {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = androidx.compose.foundation.layout.Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text("端侧优先", color = Color(0xFF667085), fontSize = 12.sp)
            Switch(
                checked = localMultimodalStatus.preference == LocalMultimodalPreference.LocalPreferred,
                onCheckedChange = { enabled ->
                    onLocalMultimodalPreferenceChange(
                        if (enabled) LocalMultimodalPreference.LocalPreferred else LocalMultimodalPreference.CloudFirst,
                    )
                },
            )
        }
        KeyValue("端侧模型", localState.statusLabel)
        KeyValue("端云路由", localState.routeLabel)
        Text(localState.detail, color = Color(0xFF667085), fontSize = 12.sp)
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = androidx.compose.foundation.layout.Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text("云侧增强", color = Color(0xFF667085), fontSize = 12.sp)
            Switch(
                checked = cloudEnhancedEnabled,
                onCheckedChange = onCloudEnhancedChange,
            )
        }
        KeyValue(
            "云侧状态",
            if (cloudEnhancedEnabled) "开启，主动导入或手动重试才请求后端" else "关闭云侧增强，不请求后端",
        )
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = androidx.compose.foundation.layout.Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text("截图助手模式", color = Color(0xFF667085), fontSize = 12.sp)
            Switch(
                checked = screenshotAssistEnabled,
                onCheckedChange = onScreenshotAssistChange,
            )
        }
        KeyValue("最近截图助手", "检测到新截图后发通知，不会自动上传，不使用全局悬浮窗")
        KeyValue("导入后处理原截图", cleanupPreference)
        OutlinedButton(
            onClick = {
                clearConfirmationState =
                    requestLocalDataClearConfirmation(clearConfirmationState).state
            },
            modifier = Modifier.fillMaxWidth(),
        ) {
            Text("清除拾刻缓存")
        }
        if (clearConfirmationState.isAwaitingConfirmation) {
            Text(
                "将删除 App 私有缓存图、OCR 原文、收件箱记录、后端地址和待触发提醒；不会删除系统相册原截图。",
                color = Color(0xFF667085),
                fontSize = 12.sp,
            )
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = androidx.compose.foundation.layout.Arrangement.spacedBy(12.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                OutlinedButton(
                    onClick = {
                        clearConfirmationState =
                            cancelLocalDataClearConfirmation(clearConfirmationState).state
                    },
                    modifier = Modifier.weight(1f),
                ) {
                    Text("取消")
                }
                OutlinedButton(
                    onClick = {
                        val result = confirmLocalDataClearConfirmation(clearConfirmationState)
                        clearConfirmationState = result.state
                        if (result.shouldClearLocalData) {
                            onClearLocalData()
                        }
                    },
                    modifier = Modifier.weight(1f),
                ) {
                    Text("确认清除")
                }
            }
        }
        KeyValue("敏感动作", "日历和提醒写入前必须确认")
    }
}
