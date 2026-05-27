# 复赛 Android MVP 主链路实现方案

对应 issue：`SHIKE-060`

## 技术栈

| 层 | 方案 | 说明 |
|---|---|---|
| Android UI | Kotlin + Jetpack Compose | 原生权限、日历、通知和相机链路更稳 |
| 本地数据 | Room/SQLite | 存储行动卡、状态、来源、执行结果 |
| 模型编排 | Python FastAPI | 初期封装 mock/OpenAI compatible，复赛替换 BlueLM |
| 模型契约 | `ModelAdapter` + JSON Schema | 上层流程不绑定供应商 |
| 系统动作 | Calendar Intent/Provider、本地通知、地图 deeplink | 所有敏感动作必须用户确认 |

## 主链路模块

| 模块 | 输入 | 输出 | 验收 |
|---|---|---|---|
| ImportModule | 截图/相册 URI、相机 Bitmap | 本地 `CaptureDraft` | 支持截图导入和拍照导入 |
| AnalyzeModule | `CaptureDraft` + OCR 文本 | `ShikeModelOutput` | 两类场景返回结构化字段 |
| ConfirmModule | 模型输出 | 用户确认后的 `ActionDraft` | 字段可编辑，置信度可见 |
| ActionPlanner | `ActionDraft` + 权限状态 | `ActionPlan` | 日历/提醒/地图至少两个真实可用 |
| Executor | `ActionPlan` | `ExecutionResult` | 失败时写入降级模式 |
| InboxStore | `ExecutionResult` | `InboxItem` | 待确认、已安排、即将截止、已完成、已忽略等收件箱状态完整 |

动作编排由 `ActionPlanner` 统一生成，避免 Android 页面、模型服务和本地执行层各自拼接动作。

## 状态机

```text
captured
  -> analyzing
  -> pending_confirmation
  -> ready_to_execute
  -> executing
  -> scheduled
  -> due_soon
  -> completed
```

异常分支：

```text
analyzing -> needs_manual_review
ready_to_execute -> permission_blocked -> fallback_ready
executing -> execution_failed -> fallback_ready
```

## Android 页面映射

| Compose Screen | 对应原型页 | 关键状态 |
|---|---|---|
| `HomeActionScreen` | 今日行动台 | 今日三件事、即将截止 |
| `ScreenshotActionSheet` | 截图悬浮动作卡 | 场景判断、快捷动作 |
| `CameraGuideScreen` | 相机导办页 | 识别框、拍照、底部建议 |
| `ParseConfirmScreen` | AI 解析确认页 | 字段编辑、置信度、缺失字段 |
| `ActionComposeScreen` | 行动编排页 | 动作勾选、权限提示 |
| `InboxScreen` | 收件箱页 | 状态过滤、归档、执行 |
| `PrivacySettingsScreen` | 隐私与端云设置页 | 端侧优先、云侧增强 |

## 复赛验收链路

| 链路 | 必须跑通 | 降级要求 |
|---|---|---|
| 课程通知截图 | 导入 -> 解析 -> 确认 -> 日历/提醒 -> 今日行动台 | 日历权限拒绝时创建本地行动卡 |
| 活动海报拍照 | 拍照 -> 解析 -> 确认 -> 提醒/地图 -> 收件箱 | 地图不可用时复制地点并保留提醒 |

## FastAPI 服务草案

```http
POST /v1/analyze
Content-Type: application/json

{
  "input_id": "sample-course-001",
  "source_type": "screenshot",
  "ocr_text": "...",
  "scene_hint": "course_notice"
}
```

响应必须符合 `contracts/model-output.schema.json`。

## 验证命令

初期可在本地先使用 Spike 作为服务逻辑基线：

```bash
python3 shike/spike/run_spike.py --all
```

Android 工程创建后，最低回归命令应补充为：

```bash
./gradlew test
./gradlew connectedCheck
```

## 当前落地状态

本目录已经补充最小 Android MVP 工程和 FastAPI smoke service：

| 交付 | 路径 | 状态 |
|---|---|---|
| Android Compose 工程 | `android-mvp/` | 已创建 |
| Debug APK | `android-mvp/app/build/outputs/apk/debug/app-debug.apk` | 已构建 |
| 构建报告 | `android-mvp/build-report.md` | 已生成 |
| FastAPI 服务 | `backend/shike_backend/main.py` | 已创建 |
| 后端 smoke test | `backend/verify_backend.py` | 已通过 |

构建命令：

```bash
bash shike/android-mvp/build_apk.sh
python3 shike/backend/verify_backend.py
```

说明：当前 APK 是复赛主链路的最小可运行壳，包含导入入口模拟、解析确认、行动编排、收件箱状态和隐私端云设置；真实系统日历/提醒/地图 API 写入仍需在 Android 设备联调阶段接入。

## 落地增强状态

当前 Android MVP 已补入以下设备动作：

| 动作 | 实现方式 | 说明 |
|---|---|---|
| 相册截图 | `ActivityResultContracts.GetContent` + `image/*` | 从系统相册选择截图，页面回显采集来源 |
| 拍照导入 | `ActivityResultContracts.TakePicturePreview` + `CAMERA` | 运行时申请相机权限，回显拍照预览 |
| 日历 | `Intent.ACTION_INSERT` + `CalendarContract.Events.CONTENT_URI` | 打开系统日历新增页，由用户确认保存 |
| 提醒 | `NotificationCompat` + `POST_NOTIFICATIONS` | Android 13+ 运行时申请通知权限 |
| 地图 | `geo:` deeplink + `Uri.encode` | 使用当前行动卡地点打开地图 |
| 分享导入 | `ACTION_SEND` + `Intent.EXTRA_TEXT` | 从其他应用分享文本到拾刻生成行动卡 |
| 本地恢复 | `SharedPreferences` 收件箱缓存 | 保存当前行动卡、动作、时间、地点和采集来源，应用重启后恢复 |
| 后端解析 | `HttpURLConnection` -> `POST /v1/analyze` | 模拟器默认访问 `http://10.0.2.2:8000`，映射 JSON 响应到行动卡 |
| 失败回退 | `runCatching` + 本地样例 | 后端超时、未启动或返回非 2xx 时回退本地 MockModelAdapter |
| OCR 草稿 | `OutlinedTextField` + `ocrDraft` | 相册、相机、样例和分享导入后可编辑 OCR 文本草稿，再提交到 `/v1/analyze` |
| 后端地址配置 | `OutlinedTextField` + `SharedPreferences` | 默认 `http://10.0.2.2:8000`，真机可保存局域网后端地址 |
| 手动修正 | `ParseConfirmPanel` + `onReviewed` | 用户可编辑标题、时间、地点和状态，点“确认修正”后持久化 |
| 忽略动作 | `status = "已忽略"` | 低置信度或字段不可信时保留记录但不推进执行 |

权限细节、安装命令和失败排查见 `docs/device-runbook.md`。离线演示继续使用 `MockModelAdapter` 和页面内“课程样例/活动样例”兜底，保证无网络、无图片或相机权限被拒绝时仍能跑通课程通知和活动海报主链路。
