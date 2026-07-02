package cn.shike.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.Switch
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
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
import cn.shike.app.system.ScreenshotAssistDiagnostics

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
    screenshotAssistDiagnostics: ScreenshotAssistDiagnostics? = null,
    screenshotAssistEnabled: Boolean = false,
    onScreenshotAssistChange: (Boolean) -> Unit = {},
    cleanupPreference: String = "每次询问（推荐）",
) {
    var clearConfirmationState by remember { mutableStateOf(LocalDataClearConfirmationState()) }
    var diagnosticsExpanded by rememberSaveable { mutableStateOf(false) }
    SectionCard("设置") {
        SettingPlainRow(
            title = "图片识别",
            detail = "只有你主动导入的图片才会用于生成行动卡。",
        )
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = androidx.compose.foundation.layout.Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text("使用图片识别", color = Color(0xFF667085), fontSize = 14.sp)
            Switch(
                checked = localMultimodalStatus.preference == LocalMultimodalPreference.CloudFirst,
                onCheckedChange = { enabled ->
                    onLocalMultimodalPreferenceChange(
                        if (enabled) LocalMultimodalPreference.CloudFirst else LocalMultimodalPreference.LocalPreferred,
                    )
                },
            )
        }
        SettingPlainRow(
            title = "文字解析",
            detail = "整理时间、地点和准备事项。",
        )
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = androidx.compose.foundation.layout.Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text("生成行动卡", color = Color(0xFF667085), fontSize = 14.sp)
            Switch(
                checked = cloudEnhancedEnabled,
                onCheckedChange = onCloudEnhancedChange,
            )
        }
        SettingPlainRow(
            title = "截图提醒",
            detail = "检测到新截图后提醒你处理，不会自动上传图片。",
        )
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = androidx.compose.foundation.layout.Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text("提醒我处理新截图", color = Color(0xFF667085), fontSize = 14.sp)
            Switch(
                checked = screenshotAssistEnabled,
                onCheckedChange = onScreenshotAssistChange,
            )
        }
        OutlinedButton(
            onClick = {
                clearConfirmationState =
                    requestLocalDataClearConfirmation(clearConfirmationState).state
            },
            modifier = Modifier.fillMaxWidth(),
        ) {
            Text("清除本地数据")
        }
        if (clearConfirmationState.isAwaitingConfirmation) {
            Text(
                "将删除 App 私有缓存图、识别文字、行动台记录和待触发提醒；不会删除系统相册原截图。",
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
        TextButton(onClick = { diagnosticsExpanded = !diagnosticsExpanded }) {
            Text(if (diagnosticsExpanded) "收起高级诊断" else "高级诊断")
        }
        if (diagnosticsExpanded) {
            KeyValue("图片处理", localMultimodalStatus.preference.userLabel)
            KeyValue("文字解析", if (cloudEnhancedEnabled) "已开启" else "已关闭")
            KeyValue("导入后处理原截图", cleanupPreference)
            screenshotAssistDiagnostics?.let { diagnostics ->
                ScreenshotAssistDiagnosticsPanel(diagnostics)
            }
            KeyValue("系统协同", "日历、提醒和地图都需要确认后执行")
        }
    }
}

@Composable
private fun SettingPlainRow(title: String, detail: String) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = androidx.compose.foundation.layout.Arrangement.spacedBy(10.dp),
        verticalAlignment = Alignment.Top,
    ) {
        Text(
            title,
            modifier = Modifier.weight(0.9f),
            color = ShikeColors.Ink,
            fontSize = 14.sp,
            fontWeight = FontWeight.SemiBold,
        )
        Text(
            detail,
            modifier = Modifier.weight(1.8f),
            color = Color(0xFF667085),
            fontSize = 12.sp,
            textAlign = TextAlign.End,
        )
    }
}

@Composable
fun ScreenshotAssistDiagnosticsPanel(diagnostics: ScreenshotAssistDiagnostics) {
    SectionCard("截图助手诊断") {
        KeyValue("助手状态", if (diagnostics.enabled) "已开启" else "未开启")
        KeyValue("图片权限", if (diagnostics.mediaPermissionGranted) "已授权" else "未授权")
        KeyValue("通知权限", if (diagnostics.notificationPermissionGranted) "已授权" else "未授权")
        KeyValue("后台服务", if (diagnostics.serviceRunning) "运行中" else "已停止")
        KeyValue("最近检测截图", diagnostics.lastDetectedAtText.removePrefix("最近检测截图："))
        KeyValue("最近通知", diagnostics.lastNotificationStatus.removePrefix("最近通知："))
    }
}
