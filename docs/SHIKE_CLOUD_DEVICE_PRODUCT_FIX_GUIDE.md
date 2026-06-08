# 拾刻云真机产品问题深度复盘与下一轮优化指导

> 适用目标：基于当前云真机实测视频、仓库现状、复赛要求和真实用户体验，指导 Codex Goal 模式持续优化“拾刻”。本文件重点处理 4 个真实落地问题：截图后能否主动提示、解析不准确、首页过长且工程信息外露、导入后能否清理原截图。
>
> 建议仓库路径：`docs/SHIKE_CLOUD_DEVICE_PRODUCT_FIX_GUIDE.md`
>
> 安全原则：本文不写入完整 BlueLM AppKEY，不写入私钥内容，不写入真实 OCR、手机号、学号、群聊记录或云真机账号信息。

---

## 0. 本轮结论

当前云真机表现说明：拾刻已经能作为 APK 在 vivo 云真机上运行，主链路也能走到导入、解析、确认、行动编排和收件箱。但从真实用户和复赛评委角度看，仍存在明显“产品化不足”：

1. **截图入口还不够自然**：用户截图后仍要主动打开拾刻或从相册选择，和“截图后弹出交给拾刻”的初赛叙事还有距离。
2. **解析存在样例化/幻觉化倾向**：用户输入或截图里关键是“高数”，但 App 可能输出“相册导入的课程通知”“18:30/B203/作业第5章”等样例字段。核心问题是：系统没有严格区分“用户真实 OCR 内容”和“演示样例 fallback”。
3. **首页仍显得过长**：虽然已经拆出首页、导入、收件箱、设置、调试等 section，但每个页面内部仍是长卡片堆叠，且底部导航不是标准固定 Scaffold 体验。
4. **工程/调试信息仍对用户可见**：后端地址、Mock、模型状态、交付物自检、调试入口等信息应进入 Debug 或高级设置，不应出现在普通用户默认路径。
5. **截图清理没有形成闭环**：拾刻的核心痛点是“别让截图睡在相册里”，如果导入成功后原截图仍留在相册，就没有彻底解决相册堆积问题。

下一轮优化目标应从“能跑”变成“像真实软件、解决真实痛点、可被评委理解”。优先级如下：

```text
P0  截图导入与清理闭环：检测/提醒/导入/移入回收站
P0  解析准确性：严格基于 OCR，不得用样例字段污染真实输入
P0  首页产品化：一屏内看懂价值，调试信息隐藏
P1  云真机体验修复：状态栏安全区、底部导航固定、按钮可达
P1  BlueLM 在线证据：云真机 + HTTPS 后端 + 脱敏日志
P2  长期收件箱：多条记录与截图清理状态联动
```

---

## 1. 云真机实测观察

### 1.1 设备环境

当前云真机信息：

```text
平台：vivo 云真机
机型：V2502A
Android 版本：16
系统版本：OS 6
分辨率：1260 x 2800
ABI：arm64-v8a
```

这台机器适合做复赛证据，因为它覆盖了高分辨率、大屏、Android 16 新权限环境和 vivo 真实设备生态。

### 1.2 视频中看到的问题

从你上传的云真机视频抽帧看，当前 App 已经能完成这些操作：

- 在手机中安装并打开“拾刻”。
- 从相册导入图片。
- 进入“导入”页并显示 OCR 文本草稿。
- 进入“AI 解析确认”。
- 点击确认修正后进入行动编排。
- 查看收件箱状态。

但问题也很明显：

| 问题 | 表现 | 对用户/评委的影响 |
|---|---|---|
| 截图后没有主动入口 | 用户截图后没有自然弹出“是否交给拾刻” | 初赛主张“截图动作卡”的惊喜感不足 |
| 真实输入被样例污染 | 用户文字关键是“高数”，但结果像固定样例 | 评委会怀疑是硬编码，不是真 AI 理解 |
| 首页信息过多 | 首页含今日行动、快捷导入、概要、待确认、确认横幅等 | 像 Demo 页，不像现代 App 首页 |
| 底部导航占位但不是标准应用骨架 | 页面仍在整体滚动容器内 | 体验不稳，长内容时用户迷路 |
| 调试入口对普通用户可见 | 底部有“调试”，设置里有后端连接 | 普通用户不应看到工程入口 |
| 原截图未处理 | 导入后相册中仍保留截图 | 没有解决“相册截图越来越多”的痛点 |

---

## 2. 复赛与产品视角的判断标准

复赛不是只看“能不能演示”，而是看：

```text
作品是否可运行
功能是否清晰
交互是否自然
大模型是否真正用于核心功能
是否体现用户真实需求
材料是否能快速让评委理解
```

复赛交流会要求作品介绍 PPT、演示视频和海报、作品文件、开发代码打包都要提交，作品文件必须可运行，代码打包要重点标注 API 调用大模型的部分。评审标准里，作品创新性、应用价值、作品完成度、大模型应用能力共同决定成绩。

对拾刻来说，最能打动评委的不是“我们有很多验证脚本”，而是下面这条真实体验：

```text
用户刚截图完，拾刻识别到这可能是一条课程/活动/截止信息；
用户点一次“交给拾刻”；
AI 只基于截图内容生成可确认行动卡；
用户确认后进入日历、提醒、地图和收件箱；
最后用户可选择把原截图移入系统回收站，避免相册继续堆积。
```

这条链路比“打开 App -> 选择截图 -> 编辑 OCR 草稿 -> 点后端解析”更像真实产品，也更符合“别让截图睡在相册里”的 slogan。

---

## 3. 问题一：截图后能否弹出“检测到截图，是否启动拾刻”

### 3.1 结论

可以做，但不能按“普通 App 无权限全局弹窗”来承诺。正确分级是：

| 方案 | 可行性 | 推荐度 | 说明 |
|---|---:|---:|---|
| App 内截图检测 | 高 | 低 | Android API 34+ 可以监听“本 Activity 被截图”，但只能检测用户截了拾刻自己的界面，不是检测其他 App 的截图 |
| MediaStore 截图观察 + 通知提醒 | 中 | 高 | 监听系统相册中新截图，发通知“检测到截图，是否交给拾刻”，用户点通知进入 App |
| 悬浮窗 Overlay 弹窗 | 中 | 低 | 需要悬浮窗权限，用户信任成本高，复赛不建议主打 |
| AccessibilityService 辅助功能 | 中 | 低 | 权限重、隐私风险高，容易被评委认为过度授权 |
| vivo 系统级入口合作 | 高价值但非普通 APK | 作为未来增强 | 可以作为与 vivo 生态结合的方向，不作为当前 APK 必交能力 |

推荐当前复赛落地：

```text
不做全局悬浮窗。
做“截图助手模式”：用户主动开启后，App 通过 MediaStore 观察新截图；检测到疑似截图后发高优先级通知或 App 内弹窗；用户点通知后进入拾刻。
```

### 3.2 为什么不推荐直接全局弹窗

普通 Android App 在后台直接弹出 Activity 或覆盖在其他 App 上，会遇到系统限制和用户信任问题。即使技术上通过悬浮窗权限实现，也会让用户看到“允许显示在其他应用上层”这类敏感授权，不符合拾刻“克制、可信”的产品气质。

因此主路径应是：

```text
检测到截图 -> 发系统通知 / heads-up 通知 -> 用户主动点击 -> 打开拾刻导入确认页
```

文案建议：

```text
拾刻检测到一张新截图
可能包含课程、活动或截止事项，是否交给拾刻生成行动卡？
[交给拾刻] [忽略]
```

### 3.3 Android 16 云真机实现建议

新增模块：

```text
android-mvp/app/src/main/java/cn/shike/app/system/ScreenshotObserver.kt
android-mvp/app/src/main/java/cn/shike/app/system/ScreenshotNotification.kt
android-mvp/app/src/main/java/cn/shike/app/data/ScreenshotCandidateStore.kt
android-mvp/app/src/main/java/cn/shike/app/ui/ScreenshotDetectedSheet.kt
validation/validate_screenshot_assist.py
```

实现策略：

1. 用户在设置中开启“截图助手模式”。
2. 请求必要权限：
   - Android 13+：`READ_MEDIA_IMAGES` 或系统照片访问能力。
   - Android 13+：`POST_NOTIFICATIONS`，用于后台提示。
3. 注册 `MediaStore.Images.Media.EXTERNAL_CONTENT_URI` 的 `ContentObserver`。
4. 新增图片时查询最近 5 秒内新增图片。
5. 判断是否为截图：
   - `RELATIVE_PATH` 包含 `Screenshots` / `截屏`。
   - `DISPLAY_NAME` 包含 `Screenshot` / `截屏` / `屏幕截图`。
   - 宽高接近屏幕尺寸，例如云真机 1260x2800。
6. 只保存 `content://` Uri、时间、宽高、文件名脱敏摘要，不保存图片本体。
7. 发通知或如果 App 当前前台则显示底部弹窗。
8. 用户点“交给拾刻”后进入 `CaptureDraft`。

注意：

```text
不能默认监听用户相册。
必须有显式开关和权限说明。
必须允许关闭。
不能上传图片，只上传 OCR 文本或用户确认后的文本。
```

### 3.4 复赛演示话术

```text
当前 APK 支持相册导入、拍照导入、文本分享和手动输入。
同时我们增加了“截图助手模式”：在用户授权后，拾刻可以观察新截图并发出通知式动作卡。
我们没有使用高风险全局悬浮窗，而是通过系统通知让用户主动选择是否交给拾刻，符合 Android 权限边界和隐私预期。
未来如果与 vivo 系统能力结合，可进一步升级为系统级截图动作卡。
```

---

## 4. 问题二：解析不准确，关键是“高数”但结果像样例

### 4.1 当前问题本质

当前视频里用户内容类似：

```text
今天晚上需要上高数 A
```

用户真正想要的是：

```text
标题：上高数 A
场景：课程 / 待确认课程事项
时间：今天晚上（相对时间，不精确）
地点：缺失
动作：提醒 / 待确认
缺失字段：exact_start_time, location
```

但当前 App 可能输出：

```text
标题：相册导入的课程通知
时间：今天 18:30 / 22:00 截止
地点：B203
任务：提交第5章作业
```

这说明真实输入被样例 fallback 污染了。对评委来说，这是高风险问题：他们会认为不是大模型理解，而是固定样例硬编码。

### 4.2 必须建立“禁止样例污染”的解析原则

新增原则：

```text
真实 OCR 优先级 > 用户手动输入 > BlueLM 解析 > Mock fallback。
Mock fallback 只能在用户明确点击“课程样例/活动样例”或后端不可用时作为兜底。
只要用户提供了真实 OCR/手动文本，就不得填入样例中的 B203、18:30、22:00、第5章作业等字段，除非这些字段确实出现在输入文本里。
```

### 4.3 对“今天晚上需要上高数A”的正确输出示例

```json
{
  "scene_type": "course_notice",
  "confidence": 0.72,
  "title": "上高数 A",
  "time": {
    "start_text": "今天晚上",
    "deadline_text": null,
    "normalized_start": null,
    "normalized_deadline": null
  },
  "location": null,
  "task": {
    "summary": "今天晚上需要上高数 A",
    "priority": "medium",
    "topic": "course"
  },
  "suggested_actions": [
    {"type": "reminder", "label": "上课前提醒", "requires_permission": true}
  ],
  "missing_fields": ["exact_start_time", "location"],
  "explanation": "文本包含课程关键词“高数A”和相对时间“今天晚上”，但没有具体上课时间和地点，因此需要用户确认后再安排。"
}
```

### 4.4 代码层改造建议

新增或修改：

```text
backend/shike_backend/adapters/mock_adapter.py
backend/shike_backend/prompts/analyze_system_prompt.txt
backend/shike_backend/prompts/analyze_user_template.txt
backend/shike_backend/eval/run_model_eval.py
validation/regression-cases.json
validation/validate_no_sample_contamination.py
android-mvp/app/src/main/java/cn/shike/app/data/BackendAnalysisRunner.kt
android-mvp/app/src/main/java/cn/shike/app/data/ModelApiClient.kt
```

必须新增回归样例：

```json
{
  "id": "course-short-need-math-001",
  "scene": "course_notice",
  "input": "今天晚上需要上高数A",
  "expected_fields": ["title", "time"],
  "expected_actions": ["reminder"],
  "expected_missing_fields": ["exact_start_time", "location"],
  "forbidden_output_tokens": ["B203", "18:30", "22:00", "第5章", "相册导入的课程通知"]
}
```

### 4.5 UI 层展示建议

不要把低信息文本包装得太确定。应该展示：

```text
AI 解析确认
标题：上高数 A
时间：今天晚上（需确认具体时间）
地点：待补充
置信度：72%
风险：缺少具体上课时间和地点
建议：先设置提醒草稿，补齐时间后再加入日历
```

按钮：

```text
[补充时间地点] [先存入待确认]
```

不要默认显示：

```text
已安排
加入日历
打开地图
B203
```

除非用户确认补齐字段。

---

## 5. 问题三：首页太长，不像现代软件

### 5.1 当前状态

当前仓库已经有 `HomeActionScreen`、`CaptureHubScreen`、`ParseConfirmScreen`、`ActionPlanScreen`、`InboxScreen`、`PrivacySettingsScreen`、`DebugDemoScreen` 这类页面壳，方向是对的。但从云真机视频看，页面仍然偏“卡片堆叠 + 长滚动”，不够像真实 App。

现代手机 App 首页应该先回答一个问题：

```text
我现在要处理什么？
```

而不是把所有功能、状态、入口、调试信息都展示出来。

### 5.2 首页新信息架构

首页一屏内只保留：

```text
顶部：拾刻 + 今日 + 设置/通知入口
主卡：今天最重要 1 张行动卡
次卡：即将截止 1-2 条
快捷入口：导入截图 / 拍照 / 手动输入
底部：固定导航 首页 / 导入 / 收件箱 / 设置
```

首页不展示：

```text
后端地址
MockModelAdapter
模型状态全文
交付物自检中心
3分钟演示路线
validate_* 文案
调试 Tab
完整 OCR 原文
```

这些内容移动到：

```text
DebugDemoScreen，仅 debug 构建显示；
或设置页中“连续点击版本号 7 次”后显示。
```

### 5.3 技术实现建议

当前 `ShikeMainScreen` 外层仍使用 `Column + verticalScroll` 并把底部导航放在内容末尾。建议改成标准 `Scaffold`：

```kotlin
Scaffold(
    bottomBar = {
        BottomNavBar(
            selectedSection = selectedSection,
            onSelected = { selectedSection = it },
        )
    }
) { padding ->
    when (selectedSection) {
        Home -> HomeActionScreen(modifier = Modifier.padding(padding))
        Import -> CaptureHubScreen(...)
        Inbox -> InboxScreen(...)
        Settings -> PrivacySettingsScreen(...)
        Debug -> DebugDemoScreen(...)
    }
}
```

要求：

- BottomNav 固定，不跟随页面内容一起滚动。
- 每个页面自己决定是否滚动。
- 首页尽量不滚动或只轻微滚动。
- 使用 `WindowInsets.safeDrawing` 或 `systemBarsPadding()` 处理 Android 16 状态栏遮挡。
- 云真机 1260x2800 上，首页首屏必须完整显示主卡和快捷导入。

### 5.4 底部导航建议

普通用户看到：

```text
首页 / 导入 / 收件箱 / 我的
```

或：

```text
今日 / 导入 / 收件箱 / 设置
```

不建议直接显示：

```text
调试
```

Debug 入口建议：

```text
设置 -> 关于拾刻 -> 连点版本号 7 次 -> 显示开发者模式
```

---

## 6. 问题四：后端、Mock、调试信息不能给用户展示

### 6.1 当前问题

用户不应该看到：

```text
后端地址
/v1/analyze
MockModelAdapter
validate_*
交付物自检中心
CLOUD_DEVICE_PACKAGE_METRIC
```

这些是工程和评审证据，不是用户功能。

### 6.2 产品化分层

| 信息 | 普通用户位置 | Debug/评审位置 |
|---|---|---|
| 云侧增强开关 | 设置页，简单说明 | Debug 中显示 provider/backend/status |
| 后端地址 | 默认隐藏 | Debug 页可编辑 |
| Mock fallback | 用户看到“云侧暂不可用，已切换本地确认” | Debug 显示 MockModelAdapter |
| 交付物自检 | 不展示 | DebugDemoScreen |
| 3分钟演示路线 | 不展示 | DebugDemoScreen |
| BlueLM provider | 用户看到“云侧解析成功” | Debug 显示 `provider=bluelm` |

### 6.3 用户文案替换

工程文案：

```text
模型编排：本地 mock 待命
后端 /v1/analyze
MockModelAdapter
```

产品文案：

```text
本地解析已就绪
云侧解析成功
云侧暂不可用，已切换为本地确认
```

---

## 7. 问题五：导入后能否删除截图

### 7.1 结论

可以做，但必须用户明确同意；普通 App 不能偷偷删除用户相册里的图片。

推荐做法不是“直接删除”，而是：

```text
导入成功 -> 生成行动卡 -> 用户确认 -> 提示“是否把原截图移入系统回收站” -> 系统确认弹窗 -> 移入回收站
```

这样既解决痛点，又不会让用户害怕 App 私自删图。

### 7.2 推荐交互

在 AI 解析成功后显示：

```text
已生成行动卡
这张截图已经被拾刻处理。是否把原截图移入系统回收站？
[移入回收站] [保留原图] [以后都询问]
```

在设置页提供：

```text
导入后处理原截图
- 每次询问（推荐）
- 默认保留
- 默认移入回收站（仍会弹系统确认）
```

### 7.3 技术实现建议

新增：

```text
android-mvp/app/src/main/java/cn/shike/app/system/MediaCleanupActions.kt
android-mvp/app/src/main/java/cn/shike/app/data/CaptureDraft.kt
android-mvp/app/src/main/java/cn/shike/app/ui/ScreenshotCleanupPrompt.kt
validation/validate_screenshot_cleanup.py
```

`CaptureDraft` 增加：

```kotlin
data class CaptureDraft(
    val id: String,
    val sourceType: CaptureSourceType,
    val sourceUri: String?,
    val sourceMediaStoreUri: String?,
    val ocrText: String,
    val ocrConfidence: Float,
    val imageCleanupStatus: ImageCleanupStatus,
    val createdAt: Long,
)

enum class ImageCleanupStatus {
    NOT_REQUESTED,
    NOT_SUPPORTED,
    USER_KEPT,
    TRASH_REQUESTED,
    TRASHED,
    FAILED
}
```

Android 11+ 可使用 `MediaStore.createTrashRequest(...)` 把图片移入系统回收站。对于用户明确要求永久删除的情况，可使用 `MediaStore.createDeleteRequest(...)`，但不建议作为默认。优先级：

```text
移入回收站 > 永久删除
```

### 7.4 限制说明

不是所有导入 Uri 都能删除：

| 来源 | 是否能清理 | 说明 |
|---|---|---|
| MediaStore 截图 Uri | 可尝试移入回收站 | 最适合截图监听路径 |
| Photo Picker 返回 Uri | 不一定可直接删除 | 可能只有读取授权 |
| ACTION_OPEN_DOCUMENT 返回 Uri | 不一定可删除 | 依赖 DocumentProvider |
| 相机临时 Bitmap | 无需删除 | 本来不是系统相册文件 |
| 文本分享 | 无需删除 | 没有图片 |

UI 必须在不支持清理时说明：

```text
当前来源不支持直接清理原图，你可以稍后在相册中删除。
```

---

## 8. 竞品学习与差异化表达

### 8.1 可以学习什么

| 产品类型 | 可以学习 | 不应照搬 |
|---|---|---|
| Google Keep / 笔记工具 | 轻量记录、图片文字提取、提醒 | 不要停留在“保存一条笔记” |
| Todoist / 待办工具 | 今日视图、优先级、自然语言任务 | 不要要求用户手动录入所有字段 |
| 扫描/OCR 工具 | 图片选取、裁剪、识别反馈 | 不要把目标变成文档扫描 |
| 系统识屏/一键问屏 | 手机原生入口、即时理解 | 不要只回答问题，要生成行动卡 |
| 小V记忆/收藏类能力 | 记忆、归档、搜索 | 拾刻重点是“处理到哪一步” |

### 8.2 拾刻为什么更好

拾刻不能比拼“功能最多”，要比拼“动作闭环最短”：

```text
截图/拍照/分享
  -> 识别任务型碎片
  -> 生成可确认行动卡
  -> 用户确认
  -> 日历/提醒/地图
  -> 收件箱持续追踪
  -> 原截图可清理
```

竞品通常停在：

```text
识别文字 / 保存笔记 / 创建待办 / 搜索收藏
```

拾刻的核心差异是：

```text
不是保存更多，而是漏掉更少；
不是回答问题，而是推动下一步；
不是替用户决定，而是让用户确认后执行。
```

---

## 9. 服务器与云真机上线补充

### 9.1 当前服务器信息

```text
服务器 IP：118.89.119.107 / 118.25.15.72
域名：roky.chat
SSH 私钥本地路径：C:\Users\Xing\Downloads\Roky.pem
```

注意：

```text
Roky.pem 文件内容绝不能进仓库。
AppKEY 绝不能写入服务器部署文档明文。
```

### 9.2 推荐部署结构

```text
https://roky.chat
  -> 作品介绍页 / 健康检查入口 / 下载 APK 链接

https://api.roky.chat
  -> FastAPI 后端
  -> /health
  -> /v1/schema
  -> /v1/analyze
```

如果短期只有一个域名，也可以：

```text
https://roky.chat/health
https://roky.chat/v1/schema
https://roky.chat/v1/analyze
```

### 9.3 后端环境变量

```bash
SHIKE_MODEL_PROVIDER=bluelm
BLUELM_APP_ID=***
BLUELM_APP_KEY=***
BLUELM_BASE_URL=https://api-ai.vivo.com.cn
BLUELM_URI=/v1/chat/completions
BLUELM_MODEL=Volc-DeepSeek-V3.2
BLUELM_TIMEOUT_SECONDS=12
BLUELM_MAX_RETRIES=1
SHIKE_ALLOW_MOCK_FALLBACK=true
```

### 9.4 云真机 App 配置

云真机里 App 后端地址应填写：

```text
https://roky.chat
```

或：

```text
https://api.roky.chat
```

不要使用：

```text
http://10.0.2.2:8000
http://192.168.x.x:8000
```

---

## 10. 新增验收脚本建议

新增以下验证脚本，锁定本轮真实问题：

```bash
python3 shike/validation/validate_screenshot_assist.py
python3 shike/validation/validate_screenshot_cleanup.py
python3 shike/validation/validate_no_sample_contamination.py
python3 shike/validation/validate_user_facing_copy.py
python3 shike/validation/validate_home_one_screen.py
```

### 10.1 `validate_screenshot_assist.py`

检查：

- 存在 `ScreenshotObserver.kt` 或等价实现。
- 存在“截图助手模式”设置开关。
- Manifest 中有必要的媒体/通知权限说明。
- 不使用默认全局悬浮窗作为主方案。
- 检测到截图后通过通知或 App 内 sheet 提示。

### 10.2 `validate_screenshot_cleanup.py`

检查：

- 存在 `MediaCleanupActions.kt`。
- 使用 `MediaStore.createTrashRequest` 或等价系统确认流程。
- 不直接静默删除用户图片。
- `CaptureDraft` 有 `imageCleanupStatus`。
- 设置页有“导入后处理原截图”。

### 10.3 `validate_no_sample_contamination.py`

检查：

- 真实 OCR 输入不应输出样例专有字段。
- `今天晚上需要上高数A` 不得输出 `B203`、`18:30`、`22:00`、`第5章`。
- 缺具体时间地点时必须进入待确认。
- `missing_fields` 必须包含 `exact_start_time` 或 `location`。

### 10.4 `validate_user_facing_copy.py`

检查：

- 普通用户页面不出现 `MockModelAdapter`。
- 普通用户页面不出现 `/v1/analyze`。
- 普通用户页面不出现 `validate_`。
- 普通用户页面不出现 `后端地址`。
- Debug 页面可以出现工程信息。

### 10.5 `validate_home_one_screen.py`

检查：

- 首页默认不展示 DebugDemoScreen。
- 首页不展示后端连接。
- 首页不展示交付物自检。
- 首页首屏必须包含主行动卡、快捷导入、即将截止摘要。
- BottomNav 使用固定 bottom bar，不随内容滚动到页面末尾。

---

## 11. Codex Goal 执行顺序

### Goal A：截图助手模式

```text
/goal 按 docs/SHIKE_CLOUD_DEVICE_PRODUCT_FIX_GUIDE.md 实现“截图助手模式”的最小可用版本。不要做全局悬浮窗主方案。新增 ScreenshotObserver、ScreenshotNotification、ScreenshotCandidateStore 和设置开关；检测 MediaStore 中新截图后，通过通知提示“检测到截图，是否交给拾刻”。点击通知进入导入确认页。不得上传图片，不得读取非用户授权内容。完成条件：validate_screenshot_assist.py、validate_secret_hygiene.py、validate_android_structure.py、validate_android_unit_tests.py 通过；Android 16 云真机上能录屏证明截图后出现通知式动作卡。
```

### Goal B：导入后清理原截图

```text
/goal 实现“导入后处理原截图”闭环。用户确认生成行动卡后，显示“是否把原截图移入系统回收站”。使用 MediaStore.createTrashRequest 或系统确认流程，不允许静默删除。CaptureDraft 记录 sourceMediaStoreUri 和 imageCleanupStatus。来源不支持删除时给出解释。完成条件：validate_screenshot_cleanup.py、validate_action_execution.py、validate_real_world_ready.py 通过；云真机录屏展示导入成功后可移入回收站。
```

### Goal C：修复解析样例污染

```text
/goal 修复真实 OCR 被样例字段污染的问题。以“今天晚上需要上高数A”为第一条回归样例，不扩展公开 schema。后端和 Android 都必须严格基于 ocr_text 输出；不得在真实输入里填入 B203、18:30、22:00、第5章等样例字段。缺具体时间地点时进入待确认并标注 missing_fields。完成条件：validate_no_sample_contamination.py、validate_model_contract_strict.py、run_model_eval.py、verify_backend.py 通过。
```

### Goal D：首页简化与工程信息隐藏

```text
/goal 把首页改成真实用户一屏行动台。使用 Scaffold 固定底部导航；首页只展示今日主行动卡、即将截止摘要、快捷导入和待确认摘要。后端地址、MockModelAdapter、交付物自检、3分钟演示路线、调试入口移动到 DebugDemoScreen，Debug 入口仅 debug 构建或设置页隐藏入口可见。完成条件：validate_home_one_screen.py、validate_user_facing_copy.py、validate_frontend_polish.py、validate_demo_acceptance.py 通过。
```

### Goal E：云真机复测包

```text
/goal 基于 Android 16、1260x2800、arm64-v8a 的 vivo 云真机更新测试包。新增/更新 cloud-device-test-report.md，补充截图助手模式、导入后清理原截图、解析准确性、首页一屏化、Debug 隐藏的录屏检查项。完成条件：validate_cloud_device_package.py、validate_release_evidence_index.py、validate_landing_release_candidate.py 通过；strict 外部证据未齐时更新 blocking-report.md。
```

---

## 12. 下一版云真机录屏脚本

建议新增 5 段专项录屏：

```text
10-cloud-screenshot-assist.mp4
11-cloud-screenshot-cleanup.mp4
12-cloud-accurate-math-parse.mp4
13-cloud-home-one-screen.mp4
14-cloud-debug-hidden.mp4
```

### 12.1 截图助手录屏

1. 打开便签/消息，输入课程文本。
2. 系统截图。
3. 顶部出现“检测到截图，是否交给拾刻”的通知。
4. 点击通知进入拾刻。
5. 出现截图导入确认。

### 12.2 截图清理录屏

1. 导入截图并解析成功。
2. 用户确认行动卡。
3. App 提示是否移入系统回收站。
4. 用户同意。
5. 系统确认完成。
6. App 显示“原截图已移入回收站”。

### 12.3 高数准确性录屏

输入：

```text
今天晚上需要上高数A
```

预期：

```text
标题：上高数 A
时间：今天晚上，需确认具体时间
地点：待补充
建议：提醒 / 待确认
不得出现：B203、18:30、22:00、第5章作业
```

### 12.4 首页一屏化录屏

1. 打开拾刻。
2. 首页首屏看到今日主行动卡。
3. 看到快捷导入。
4. 不出现后端地址、Mock、交付物自检、调试指标。

### 12.5 Debug 隐藏录屏

1. 普通首页无“调试”Tab。
2. 设置页连续点击版本号进入开发者模式。
3. DebugDemoScreen 出现后端地址、样例、验证指标。

---

## 13. 复赛材料更新重点

PPT/视频/海报应新增这 4 个“真实产品亮点”：

1. **截图助手模式**：截图后通知式动作卡，不是强行悬浮窗。
2. **准确性修复**：高数短文本能正确生成待确认课程行动卡，不再样例污染。
3. **导入后清理截图**：用户确认后可把原截图移入系统回收站，真正解决相册堆积。
4. **真实 App 首页**：首页只回答“今天该处理什么”，工程入口隐藏。

复赛材料表述建议：

```text
拾刻不仅把截图变成行动卡，还把截图从相册中“处理完毕”：
用户确认导入后，可以选择把原截图移入系统回收站，避免相册继续沉积。
这让拾刻从“识别截图”升级为“完成截图的后续处理”。
```

---

## 14. 最终验收标准

当下面 8 条都能跑通时，本轮优化完成：

1. 云真机截图后能出现通知式“是否交给拾刻”。
2. 用户点击后能进入截图导入确认页。
3. “今天晚上需要上高数A”不会被样例字段污染。
4. 缺具体时间地点时不会默认可执行，而是待确认。
5. 首页首屏简洁，不出现后端、Mock、验证指标。
6. Debug 信息隐藏到 DebugDemoScreen 或开发者模式。
7. 行动卡确认后可提示移入系统回收站。
8. 移入回收站必须走系统确认，不静默删除。

最终推荐验收命令：

```bash
python3 shike/validation/validate_screenshot_assist.py
python3 shike/validation/validate_screenshot_cleanup.py
python3 shike/validation/validate_no_sample_contamination.py
python3 shike/validation/validate_user_facing_copy.py
python3 shike/validation/validate_home_one_screen.py
python3 shike/validation/validate_frontend_polish.py
python3 shike/validation/validate_action_execution.py
python3 shike/validation/validate_real_world_ready.py
python3 shike/validation/validate_cloud_device_package.py
python3 shike/validation/validate_landing_release_candidate.py
```
