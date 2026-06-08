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
| `PrivacySettingsScreen` | 隐私与端云设置页 | 端侧优先、端侧模型三态、云侧增强、版本号 5 连击进入开发者模式 |

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

`source_type` 支持 `screenshot`、`camera`、`share_text`、`manual`，分别对应相册截图、拍照导入、系统文本分享和手动输入；Android 会按当前采集来源映射，不把分享/手动内容伪装成截图。

响应必须符合 `contracts/model-output.schema.json`。

图片导入路径在 Android 端仍保留上述 v1 `source_type` 映射作为文本兜底合同；当当前草稿有图片 URI 或相机预览时，Android 会改走 `/v2/analyze-image`，v2 的 `source_type` 使用 `photo_picker`、`screenshot_share`、`recent_screenshot_assist`、`camera` 或 `manual`，并把 OCR 草稿作为 `ocr_text_hint`。

Android 图片 payload 由 `ImagePayloadPreprocessor` 统一生成：URI 字节先按 JPEG/PNG/WebP 魔数识别 MIME，非图片字节会在解码前拒绝；随后读取 bounds，再按 `ImagePreprocessPolicy.MAX_EDGE = 1600` 计算采样，读取 EXIF orientation 后归一化旋转；截图分享和最近截图助手来源会裁掉顶部/底部 UI chrome，相册普通图片和相机 Bitmap 不裁剪；最后以 JPEG 82 压缩为 `data:image/jpeg;base64,...`，并附带 MIME、尺寸和 SHA-256。用户触发图片解析时，`fromBytesWithThumbnail` / `fromBitmapWithThumbnail` 会同步生成最长边 360px 的私有 JPEG 缩略图，写入 App 私有 `shike-image-thumbnails` cache 目录并按图片 SHA-256 复用；该路径由 `ImageThumbnailCache` 负责。`MainActivity` 只负责读取用户授权的 URI 或相机 Bitmap，不再手写 `BitmapFactory`、`Base64` 或 `MessageDigest` 逻辑；该边界由 `validate_android_image_preprocess.py` 和 `ANDROID_IMAGE_PREPROCESS_METRIC 15/15` 守卫。

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
| 长期收件箱 | SQLite `inbox_items` + 旧快照迁移 | 多条行动卡、状态、来源、OCR 摘要和动作列表进入长期收件箱；`SharedPreferences` 仅保留旧快照/轻配置兜底 |
| 后端文本解析 | `HttpURLConnection` -> `POST /v1/analyze` | 分享文本、手动输入和无图片草稿提交可编辑 OCR 文本，映射 JSON 响应到行动卡 |
| 后端图片解析 | `HttpURLConnection` -> `POST /v2/analyze-image` | 相册截图、系统图片分享、最近截图助手和相机预览上传后端图片 payload，携带 OCR hint、日期、时区、尺寸和 SHA-256；后端会从图片 data URL 尝试服务端 vivo OCR enrichment，合并 OCR 文本和 blocks 后再交给多模态解析 |
| 失败回退 | `runCatching` + 本地样例 | 后端超时、未启动或返回非 2xx 时回退本地 MockModelAdapter |
| OCR 草稿 | `OutlinedTextField` + `ocrDraft` | 相册、相机、样例和分享导入后可编辑 OCR 文本草稿；文本路径提交到 `/v1/analyze`，图片路径作为 hint 提交到 `/v2/analyze-image` |
| 后端地址配置 | `OutlinedTextField` + `SharedPreferences` | 默认 `https://roky.chat`；旧安装保存的 `http://10.0.2.2:8000` 自动迁移，模拟器/局域网调试仍可手动保存自定义地址 |
| 手动修正 | `ParseConfirmPanel` + `onReviewed` | 用户可编辑标题、时间、地点和状态，点“确认并安排”后持久化 |
| 忽略动作 | `status = "已忽略"` | 低置信度或字段不可信时保留记录但不推进执行 |

后端文本合同保持兼容：`/v1/analyze` 的 `source_type` 仍只使用 `screenshot`、`camera`、`share_text`、`manual`。图片合同是新增分层，不改变旧文本合同。

### OCR 分层

导入入口统一先生成 `CaptureInput`，再通过 `OcrEngine` 输出 `OcrResult`，最后汇入 `CaptureDraft`。当前已落地两类可测试实现：

| 引擎 | 入口 | 行为 |
|---|---|---|
| `ManualOcrEngine` | 分享文本、手动输入、OCR 失败兜底 | 保留用户文本；空文本返回低置信度和“手动粘贴”提示，不阻断主链路 |
| `MockOcrEngine` | 相册、相机演示入口 | 产出课程通知和活动海报两组合成 OCR 草稿，供无真 OCR 环境下演示与单测复现 |

`CaptureDraft` 会记录 `sourceType`、`ocrText`、`ocrConfidence`、`ocrEngineName`、`privacyLevel`、`cloudAllowed`、`imageCleared`、`sourceMediaStoreUri`、`thumbnailUri` 和 `imageCleanupStatus`。分享文本默认使用 `ManualOcrEngine` 且 `allowCloudEnhancement = false`，避免把用户从其他应用分享来的原文自动送云；相册/相机当前使用 `MockOcrEngine`，后续可替换为端侧或云侧 OCR，但必须保留手动继续路径。

图片上传边界是用户主动导入后触发：被动截图检测仍只生成候选或通知，不自动上传图片；用户主动选择相册、拍照或确认导入截图后自动请求自有后端 `/v2/analyze-image`，同时保留“解析当前草稿”作为手动重试入口。手动输入会清空上一张图片 URI 和相机预览，避免从图片模式切到文本模式后误带旧图。Android 仍然只调用自有后端，不持有 vivo/DeepSeek/BlueLM 密钥；该边界由 `validate_no_default_image_upload.py` 的 `NO_DEFAULT_IMAGE_UPLOAD_METRIC 12/12` 守卫。

后端 v2 图片链路在收到 `image.data_url` 后会提取 base64 图片并调用服务端 `VivoOcrAdapter`，把后端 OCR 文本合并进 `ocr_text_hint`，把服务端 OCR blocks 合并进 `ocr_blocks`，并再次过滤顶部状态栏和底部导航块，再调用 `VivoCloudMultimodalAdapter`。这条 enrichment 只在后端发生，不把 vivo AppKEY 下发到 Android；OCR 缺凭据、网络失败或空结果不会自动执行动作，只会把请求继续送多模态或进入 `manual_review` 风险说明，用户确认前日历、提醒、地图仍不可执行。

### 端侧 3B 多模态边界

`LocalMultimodalStatus` 仅描述可选端侧模型的运行边界：`未安装`、`可用`、`初始化失败`。当前 APK 不打包端侧 3B 模型，默认显示“端侧模型：未安装”，且明确不会假装可用；只有未来真机运行态证明可用，并且云端关闭或用户选择端侧优先时，才允许进入端侧优先路由。`LocalMultimodalRuntime` 作为可插拔 runtime 合同层，要求真实 SDK 适配器按 `init(multimodal=true) -> callVit -> generate` 执行，本地生成结果必须通过 schema 基础校验后只落成“待确认”草稿；schema 缺字段或 SDK 缺失时进入本地待确认/不可用边界，不注入训练样例，也不会绕过用户确认和系统动作闸门。

权限细节、安装命令和失败排查见 `docs/device-runbook.md`。离线演示继续使用 `MockModelAdapter` 和页面内“课程样例/活动样例”兜底，保证无网络、无图片或相机权限被拒绝时仍能跑通课程通知和活动海报主链路。

收件箱长期化已新增 `InboxItemEntity`、`CaptureDraftEntity`、`ActionDraftEntity`、`ExecutionResultEntity` 和 SQLite `InboxDatabase`。`CaptureDraft` / `CaptureDraftEntity` 会把 `localImageUri` 和 App 私有 `thumbnailUri` 分开保存：前者代表用户授权选择或分享进来的原图，可用于系统删除确认；后者只代表拾刻私有缓存缩略图，不会被当作可删除的相册原图。`CaptureDraft.canDeleteOriginal` 和 `CaptureDraft.deleteState` 只从 `sourceMediaStoreUri` 与 `imageCleanupStatus` 派生：无原图 URI 时显示 `ScreenshotDeleteState.NotAvailable`，系统确认中显示 `RequestingSystemConfirmation`，已删除显示 `Deleted`，用户保留显示 `Denied`，失败显示 `Failed`。这保证“删除原截图”和“清除拾刻缓存”在数据层也保持分离。`saveSnapshot` 继续保留重启恢复快照，同时写入长期收件箱；启动时优先读取 SQLite 历史记录，旧 `SharedPreferences` 快照作为迁移兜底。落地守卫为：

```bash
python3 shike/validation/validate_inbox_workbench_landing.py
```
