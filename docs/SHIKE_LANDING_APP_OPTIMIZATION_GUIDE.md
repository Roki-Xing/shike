# 拾刻落地应用差距评估与后续优化指导

> 面向目标：在初赛文档与当前核心 20 文件基础上，把“可演示 MVP”继续推进到“可在云真机稳定跑通、接入蓝心大模型、前端体验接近真实 App、材料可支撑复赛/答辩”的落地应用。
>
> 适用方式：放入仓库 `docs/SHIKE_LANDING_APP_OPTIMIZATION_GUIDE.md`，让 Codex Goal 模式按本文逐项推进。
>
> 重要说明：本文不写入任何 AppKEY。蓝心大模型密钥只允许存在于本地环境变量、云端环境变量或比赛平台密钥管理中，不进入 Android、Git、README、录屏、日志、截图或交付包。

---

## 0. 一句话结论

当前“拾刻”已经具备很强的比赛级 MVP 基础：产品定位清晰，主链路完整，初赛文档叙事统一，Android 端已覆盖相册、相机、分享、确认、日历、提醒、地图、本地恢复和后端解析回退；后端已有 `/health`、`/v1/schema`、`/v1/analyze` 和结构化输出契约。

但它距离“真正落地应用”还有 6 个关键差距：

1. **模型还没有真正接入蓝心大模型**：当前后端仍是规则/Mock 风格的结构化返回，缺少 vivo 鉴权、BlueLM Adapter、在线模型质量评测和错误降级。
2. **云真机链路还没升级为真实评审链路**：当前 runbook 偏本地/局域网；云真机访问不到 `10.0.2.2` 和普通局域网地址，需要 HTTPS 可访问后端、云真机录屏证据和机型矩阵。
3. **前端仍偏“演示控制台”而不是“真实 App”**：Android 端需要从长滚动演示页升级为多页面、有导航、有加载/失败/空状态、有真实交互层级的产品界面。
4. **OCR 与截图入口仍需产品化**：当前靠 OCR 文本草稿/模拟文本支撑演示；落地应用至少要有稳定的图片到文本链路，普通 App 无法随意做系统级截图浮窗，必须明确采用相册导入、分享入口、拍照、可选截图监听等可实现入口。
5. **收件箱需要从“当前行动卡/演示状态”升级到“多条长期工作台”**：需要多条记录、状态流转、搜索、筛选、归档、恢复、执行结果和过期处理都真实数据驱动。
6. **材料需要从“初赛策划”升级到“复赛落地证据”**：PDF/PPT/演示脚本要加入 BlueLM 接入、云真机测试、真实 APK、失败降级、隐私安全和对评分项的证据映射。

---

## 1. 当前核心 20 文件给出的能力盘点

### 1.1 已经很强的部分

| 维度 | 当前已有能力 | 下一步含义 |
|---|---|---|
| 产品主线 | “截图/拍照 -> AI 解析 -> 用户确认 -> 行动编排 -> 收件箱/今日行动台追踪”已经稳定 | 不要推翻主线，所有增强都围绕这条链路 |
| 差异化 | 不做聊天首页、不做普通收藏夹，强调“碎片执行代理” | 评审材料继续突出“行动闭环”，不要变成泛 AI 助手 |
| Android 能力 | 相册、相机、文本分享、通知、日历 Intent、地图 deeplink、本地恢复、后端地址配置 | 已经足够进入云真机测试和 UI 精修阶段 |
| 执行安全 | 用户确认后才执行日历、提醒、地图 | 必须继续作为最高优先级红线 |
| 后端契约 | `/health`、`/v1/schema`、`/v1/analyze`，输出符合 JSON Schema | 适合直接替换为 BlueLM Adapter |
| 演示材料 | 策划书、海报、演示脚本、设备 runbook、验收清单都有 | 后续重点是把“计划”换成“实证” |
| 验收脚本 | 已有 real_world、demo_acceptance、action_execution 等脚本 | 后续新增 BlueLM、云真机、前端精修、密钥安全验收 |

### 1.2 当前核心文件暴露的真实落地差距

| 差距 | 为什么重要 | 当前证据 | 落地要求 |
|---|---|---|---|
| 后端仍像 Mock/规则服务 | 评审会看是否真正使用赛组委模型 | `main.py` 通过关键词和 scene_hint 返回固定课程/活动结构 | 增加 `BlueLMModelAdapter`，Mock 只做兜底 |
| 云真机无法访问本地地址 | 云真机不在你的电脑局域网内 | runbook 主要写 `10.0.2.2` 和局域网 IP | 部署 HTTPS 后端或安全隧道，云真机填远程地址 |
| AppKEY 泄露风险 | 一旦写进 Android/APK/Git，任何人可反编译或盗刷 | 你已在对话里提供了 AppKEY | 尽量重置；至少只放后端环境变量 |
| Android 前端信息密度偏演示 | 长滚动页适合答辩检查，不适合真实用户 | 当前文档和原型已经有多页面设计，但 Android 应落地多页 | 拆成首页、导入、确认、编排、收件箱、设置 |
| OCR 还不是稳定能力 | 没有 OCR，拍照/截图只能模拟文本 | OCR 草稿是好兜底，但不是真实识别 | 接入可替换 OCR；失败时保留手输继续 |
| 截图浮窗是系统级能力 | 普通 Android App 通常无法无权限监听所有截图并弹浮窗 | 产品文档中有“截图动作卡”愿景 | 交付中明确采用“相册/分享/拍照”，截图浮窗作为系统合作方向 |
| 收件箱要长期化 | 真用户不是只处理一张卡 | 当前核心包更像当前卡片恢复/演示状态 | 多条 InboxItem、执行结果、状态机、搜索筛选 |
| 测试证据需升级 | 复赛/答辩需要云真机实证 | 已有 runbook 和清单 | 增加云真机测试矩阵、录屏、logcat、后端请求证据 |

---

## 2. 必须遵守的安全红线

### 2.1 AppKEY 与密钥处理

你已经提供了蓝心大模型的 AppID 和 AppKEY。后续开发必须按下面处理：

| 规则 | 要求 |
|---|---|
| 不进 Android | 不得把 AppKEY 写入 Kotlin、BuildConfig、strings.xml、assets、raw、Manifest、APK |
| 不进 Git | `.env`、`.env.local`、`.env.production` 必须加入 `.gitignore` |
| 不进文档 | README、PPT、PDF、录屏、issue、优化日志里只写 `BLUELM_APP_KEY=***` |
| 不进日志 | 后端日志最多显示 `key_present=true`，不能打印完整值 |
| 不进前端 | Android 只知道你自己的后端地址，不知道蓝心 AppKEY |
| 可轮换 | 如果平台支持，建议在正式提交前重置/重新生成 AppKEY，因为密钥已经出现在对话上下文中 |

推荐环境变量：

```bash
# backend/.env.local，不提交 Git
SHIKE_MODEL_PROVIDER=bluelm
BLUELM_APP_ID=***
BLUELM_APP_KEY=***
BLUELM_TIMEOUT_SECONDS=12
BLUELM_MAX_RETRIES=1
SHIKE_ALLOW_MOCK_FALLBACK=true
```

### 2.2 用户动作红线

任何时候都不能让模型直接执行系统动作。必须坚持：

```text
模型只生成草稿与建议
规则层做校验、权限、状态判断
用户确认后才允许执行日历、提醒、地图
执行失败必须保留行动卡并给出降级路径
```

### 2.3 真实数据红线

| 场景 | 规则 |
|---|---|
| 云真机录屏 | 不使用真实班群、真实手机号、真实姓名、真实学号、真实相册 |
| 后端请求 | 只用合成样例；不要上传真实聊天记录或私密通知 |
| OCR 原文 | 默认只保存脱敏摘要；详情页需明确可清除 |
| 图片 | 默认不上传图片，只上传 OCR 文本；如果未来上传图片，必须有显式开关和用途说明 |
| 一键清除 | 清除 Inbox、OCR 原文、后端地址、已调度提醒、缓存图片 |

---

## 3. 目标技术架构

### 3.1 推荐总架构

```text
Android App
  ├─ CaptureModule
  │   ├─ 相册图片
  │   ├─ 拍照预览
  │   ├─ 文本分享
  │   └─ 手动输入 / OCR 草稿
  │
  ├─ OCR Layer
  │   ├─ LocalOcrEngine，可选
  │   ├─ CloudOcrEngine，可选
  │   └─ ManualTextFallback，必须
  │
  ├─ AnalyzeRepository
  │   └─ POST /v1/analyze 到 Shike Backend
  │
  ├─ Confirm / ActionPlan / Executor
  │   ├─ Calendar Intent
  │   ├─ AlarmManager Reminder
  │   └─ geo: Map deeplink
  │
  └─ InboxStore
      ├─ InboxItem
      ├─ ActionPlan
      ├─ ExecutionResult
      └─ PrivacySettings

Shike Backend FastAPI
  ├─ /health
  ├─ /v1/schema
  ├─ /v1/analyze
  ├─ ModelAdapter interface
  │   ├─ MockModelAdapter
  │   └─ BlueLMModelAdapter
  ├─ OutputValidator
  ├─ PrivacyRedactor
  └─ Request/Response Audit Log（脱敏）

BlueLM / vivo AI Gateway
  └─ 只由后端调用，不由 Android 直接调用
```

### 3.2 为什么不建议 Android 直连蓝心大模型

| 方案 | 优点 | 致命问题 | 结论 |
|---|---|---|---|
| Android 直接调用 BlueLM | 少一层后端 | AppKEY 会进入 APK，容易被反编译；签名逻辑暴露；难做日志和重试 | 不推荐 |
| Android -> 自有后端 -> BlueLM | 密钥安全；方便 fallback；可做 schema 修复；可统一评测 | 需要部署后端 | 推荐 |
| Android 只用 Mock | 稳定可演示 | 不体现赛组委模型 | 只能做兜底 |

---

## 4. BlueLM 接入优化方案

### 4.1 后端文件结构建议

```text
backend/shike_backend/
  main.py
  settings.py
  schemas.py
  privacy.py
  adapters/
    __init__.py
    base.py
    mock_adapter.py
    bluelm_adapter.py
    vivo_auth.py
  prompts/
    analyze_system_prompt.txt
    analyze_user_template.txt
  eval/
    regression_cases.json
    run_model_eval.py
  tests/
    test_secret_hygiene.py
    test_vivo_auth_headers.py
    test_mock_adapter.py
    test_bluelm_adapter_contract.py
    test_output_validation.py
```

### 4.2 `ModelAdapter` 抽象

后端不应在 `/v1/analyze` 里直接拼 Prompt 或调用模型。建议定义：

```python
class ModelAdapter(Protocol):
    def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        ...
```

实现：

| Adapter | 用途 |
|---|---|
| `MockModelAdapter` | 离线演示、后端不可用 fallback、单元测试 |
| `BlueLMModelAdapter` | 正式接入赛组委蓝心大模型 |
| `RecordedBlueLMAdapter` | 可选，用于录制一批稳定响应，避免每次测试都消耗模型额度 |

### 4.3 BlueLM 调用流程

```text
/v1/analyze 收到 Android 请求
  -> 脱敏 OCR 文本用于日志
  -> 构造模型 Prompt
  -> BlueLMModelAdapter 生成签名 Header
  -> 请求 vivo AI Gateway
  -> 解析模型输出
  -> 如果是 JSON：直接 Pydantic 校验
  -> 如果不是 JSON：有限重试一次“修复为 JSON”
  -> 仍失败：返回 needs_manual_review / Mock fallback
  -> 统一返回 AnalyzeResponse
```

### 4.4 Prompt 设计原则

系统提示词必须让模型只做结构化抽取，不要聊天式回答。

建议核心要求：

```text
你是“拾刻”的信息解析模块，不是聊天助手。
你的任务是把 OCR 文本转成可确认、可执行、可追踪的行动卡。
必须只输出 JSON，不要输出 Markdown，不要解释 JSON 之外的内容。
字段必须符合 ShikeModelOutput JSON Schema。
若时间、地点、报名链接、任务不确定，应降低 confidence，并把缺失项写入 missing_fields。
相对时间必须保留 start_text/deadline_text，同时尽量按 user_timezone 生成 normalized_*。
不得声称已经创建日历、提醒或地图动作；你只能建议动作。
```

### 4.5 模型输出质量控制

| 问题 | 处理 |
|---|---|
| 返回 Markdown | 提取 JSON 块；如果失败，发起一次修复请求 |
| 字段缺失 | Pydantic 校验失败，转 needs_manual_review |
| 时间模糊 | 保留原文，`normalized_* = null`，增加 `relative_time` 缺失/风险提示 |
| 地点不明确 | `location.confidence < 0.6`，地图按钮禁用 |
| 低置信度 | 进入待确认，不允许直接执行 |
| 模型超时 | 记录脱敏错误，回退 Mock 或本地待确认卡 |
| 429/额度限制 | 前端提示“云侧增强暂不可用，可手动确认继续” |
| 鉴权失败 | 后端返回安全错误文案，不把 AppKEY 打印出来 |

### 4.6 新增验收脚本

新增：

```bash
python3 shike/validation/validate_secret_hygiene.py
python3 shike/validation/validate_bluelm_adapter.py
python3 shike/validation/validate_model_contract_strict.py
python3 shike/validation/validate_cloud_backend_ready.py
```

`validate_secret_hygiene.py` 要检查：

- Android 目录没有 `BLUELM_APP_KEY`、`sk-`、完整 AppKEY 字样。
- README、docs、materials、prototype 没有完整密钥。
- `.gitignore` 包含 `.env`、`.env.local`、`.env.production`。
- 后端 `settings.py` 从环境变量读取密钥。
- 日志函数会 mask key。

`validate_bluelm_adapter.py` 要检查：

- 存在 `BlueLMModelAdapter`。
- 存在 vivo 鉴权 Header 生成模块。
- `/v1/analyze` 可通过配置切换 `mock` 与 `bluelm`。
- BlueLM 响应经过 JSON Schema/Pydantic 校验。
- 模型失败时仍返回待确认/降级结果。
- 单元测试不依赖真实 AppKEY。

---

## 5. 云真机落地测试方案

### 5.1 当前 runbook 需要升级的地方

当前文档已经写了模拟器 `10.0.2.2:8000` 和真机局域网地址，这对 USB 真机可用，但对云真机通常不可用。云真机在远端网络环境里，无法访问你电脑的 `10.0.2.2`，也大概率无法访问你的家庭/校园局域网 IP。

因此必须增加一个“云真机后端访问方案”。

### 5.2 推荐云真机后端方案

| 方案 | 推荐度 | 说明 |
|---|---:|---|
| 云服务器部署 FastAPI + HTTPS | 高 | 最稳定，适合答辩和复测 |
| Cloudflare Tunnel / ngrok / frp 临时 HTTPS 隧道 | 中 | 快速，但稳定性和安全需要注意 |
| Android 直连 BlueLM | 低 | 不安全，不建议 |
| 云真机访问本机局域网 IP | 低 | 大概率不可达 |

后端部署最低要求：

```text
https://your-domain.example.com/health        -> 200
https://your-domain.example.com/v1/schema     -> 200
https://your-domain.example.com/v1/analyze    -> 200/422/受控错误
```

Android 端要求：

- Debug 允许输入后端地址。
- Release 默认使用 HTTPS 后端。
- 如果输入 `http://`，Debug 可用，Release 应提示不安全或拒绝。
- 后端地址不能包含 path/query/fragment，保存前要归一化。

### 5.3 云真机测试矩阵

| 测试组 | 机型/系统 | 必测内容 |
|---|---|---|
| A | vivo 中端机，Android 12/OriginOS | 相册、拍照、分享、日历、地图 |
| B | vivo 新系统，Android 13+ | 通知权限 `POST_NOTIFICATIONS`、提醒调度 |
| C | 大屏/高分辨率机型 | UI 是否溢出、按钮是否遮挡 |
| D | 低性能/小内存机型 | 启动速度、图片导入、后端超时回退 |
| E | 网络弱/断网 | Mock fallback、手动确认继续 |

### 5.4 云真机必录证据

建议材料放到：

```text
materials/evidence/cloud-device/
```

文件：

| 文件 | 内容 |
|---|---|
| `01-cloud-install-open.mp4` | 云真机安装 APK 并打开首页 |
| `02-cloud-gallery-bluelm.mp4` | 相册导入课程通知，调用 BlueLM 后端，确认并打开日历 |
| `03-cloud-camera-bluelm.mp4` | 拍照导入活动海报，调用 BlueLM 后端，提醒与地图 |
| `04-cloud-share-text.mp4` | 从其他应用分享文本到拾刻并生成待确认卡 |
| `05-cloud-permission-fallback.mp4` | 拒绝通知/相机权限后的降级文案 |
| `06-cloud-backend-failure.mp4` | 后端不可用时回退 Mock/待确认 |
| `07-cloud-restart-restore.mp4` | force-stop 后重开，收件箱和后端地址恢复 |
| `08-cloud-ui-polish.mp4` | 展示多页面前端、收件箱筛选、隐私设置 |
| `09-cloud-final-route.mp4` | 3 分钟完整答辩路线 |

同时保存：

```text
cloud-device-test-report.md
cloud-device-logcat.txt
backend-redacted-access-log.txt
apk-sha256.txt
```

### 5.5 新增云真机验收脚本

新增：

```bash
python3 shike/validation/validate_cloud_device_package.py
```

检查项：

- `materials/evidence/cloud-device/` 存在。
- 9 个录屏文件名齐全。
- `cloud-device-test-report.md` 包含机型、Android 版本、测试时间、后端地址脱敏、结果。
- `backend-redacted-access-log.txt` 不含 AppKEY、不含真实个人信息。
- `device-runbook.md` 已区分 USB 真机、模拟器、云真机三种网络配置。
- `README.md` 已加入云真机验收命令。

---

## 6. 前端体验优化方案

### 6.1 当前前端问题定位

现在 Android 端已经很好地承载了“演示”和“自检”，但真实用户打开后会觉得它像一个纵向 demo 控制台：信息密度高，调试入口多，演示路线、自检中心、后端地址、样例按钮都直接暴露在主界面上。

落地应用应该把这些内容分层：

| 类型 | 应该放哪里 |
|---|---|
| 用户每天要看的内容 | 首页/今日行动台 |
| 导入入口 | 首页主按钮 + 导入页 |
| AI 解析结果 | 解析确认页 |
| 动作选择 | 行动编排页或确认页底部 |
| 历史任务 | 收件箱页 |
| 隐私与后端设置 | 设置页 |
| 演示路线、自检中心、后端地址、样例按钮 | Debug/演示模式，不在普通用户首页常驻 |

### 6.2 页面重构目标

```text
MainActivity
  -> ShikeRootApp
      -> HomeActionScreen
      -> CaptureHubScreen
      -> ParseConfirmScreen
      -> ActionPlanScreen
      -> InboxScreen
      -> PrivacySettingsScreen
      -> DebugDemoScreen，仅 debug 或长按进入
```

### 6.3 首页：今日行动台

首页只回答 3 个问题：

1. 今天最该处理什么？
2. 哪些马上截止？
3. 哪些需要我确认？

首页结构：

```text
顶部：拾刻 / 日期 / 设置入口
主行动区：今日最重要 1-3 张行动卡
快捷导入：截图/相册、拍照、分享说明、手动输入
即将截止：按 deadline 排序
待确认：低置信度或缺字段卡片
底部导航：首页 / 收件箱 / 导入 / 设置
```

不要在首页长期展示：

- 后端地址输入框。
- 所有样例按钮。
- 交付物自检中心。
- 3 分钟演示路线。

这些可以放到 Debug 页面。

### 6.4 导入页：CaptureHub

导入页要让用户明确知道自己能做什么：

| 入口 | 文案 |
|---|---|
| 相册截图 | “从相册选择通知截图” |
| 拍照 | “拍海报/公告” |
| 文本分享 | “从微信/浏览器/短信分享文字到拾刻” |
| 手动输入 | “没有 OCR 时，直接粘贴文字继续” |

导入后进入统一 `CaptureDraft`：

```kotlin
data class CaptureDraft(
    val id: String,
    val sourceType: CaptureSourceType,
    val localImageUri: String?,
    val ocrText: String,
    val createdAt: Instant,
    val privacyLevel: PrivacyLevel,
)
```

### 6.5 解析确认页

必须保留但美化：

- 标题可编辑。
- 场景标签。
- 置信度条。
- 时间、地点、任务、截止事项。
- 风险与缺失字段。
- “为什么这么判断”的模型解释。
- “确认并生成动作”和“先存入待确认”。

新增交互：

| 场景 | UI 行为 |
|---|---|
| 模型请求中 | Skeleton/loading，显示“正在解析 OCR 文本” |
| BlueLM 失败 | 提示“云侧增强暂不可用，可手动确认继续” |
| 低置信度 | 默认按钮为“存入待确认”，不是“立即执行” |
| 缺时间 | 日历按钮禁用，提示原因 |
| 缺地点 | 地图按钮禁用，提示原因 |
| 缺报名链接 | 允许提醒，但标注“报名链接需手动补充” |

### 6.6 行动编排页

行动编排页应从“按钮集合”升级为“可勾选 ActionPlan”：

```text
[✓] 加入日历：今天 18:30，高数A班教室变更，B203
[✓] 本地提醒：课前 30 分钟；截止前 2 小时
[ ] 打开地图：B203

确认执行
```

执行后展示：

```text
日历：已打开系统新增页，需用户在日历中保存
提醒：已调度本地定时提醒，模式 exact/fallback
地图：已打开地图；若失败已复制地点
```

注意：日历 Intent 只能说“已打开系统新增页”，不能声称“已写入日历”，除非你真的拿 Calendar Provider 权限并确认写入成功。

### 6.7 收件箱页

收件箱要成为落地产品的核心，而不是静态统计。

必须有：

| 功能 | 要求 |
|---|---|
| 多条卡片 | 至少支持 50 条历史记录 |
| 筛选 | 全部、待确认、已安排、即将截止、已完成、已忽略 |
| 搜索 | 标题、地点、来源、OCR 摘要 |
| 状态流转 | 待确认 -> 已安排 -> 即将截止 -> 已完成/已忽略 |
| 归档/恢复 | 不删除，只改变状态 |
| 执行结果 | 每个动作有执行状态、时间、失败原因 |
| 过期处理 | deadline 过期后显示“已过期/需复核” |

### 6.8 视觉系统

继续沿用初赛材料中的青绿色主色，但要形成 design tokens：

```kotlin
object ShikeColors {
    val Brand = Color(0xFF0F766E)
    val BrandSoft = Color(0xFFDDF4EE)
    val Warning = Color(0xFFF97316)
    val WarningSoft = Color(0xFFFFF7ED)
    val Info = Color(0xFF2563EB)
    val Ink = Color(0xFF101828)
    val Muted = Color(0xFF667085)
    val Surface = Color(0xFFF7FBFA)
    val Line = Color(0xFFE6EDF1)
}
```

组件：

```text
ShikeActionCard
ShikeStatusPill
ShikePrimaryButton
ShikeRiskPanel
ShikeFieldEditor
ShikeInboxFilterBar
ShikeEmptyState
ShikeErrorState
ShikeLoadingSkeleton
```

### 6.9 新增前端验收脚本

```bash
python3 shike/validation/validate_frontend_polish.py
```

检查：

- 存在 `HomeActionScreen`、`CaptureHubScreen`、`ParseConfirmScreen`、`InboxScreen`、`PrivacySettingsScreen`。
- DebugDemoScreen 不在 release 默认首页。
- 有 loading、empty、error 三类状态。
- 有 design tokens。
- 后端地址输入只在设置/Debug 中出现。
- 首页不出现“validate_”“交付物自检”“3分钟演示路线”等工程词。

---

## 7. OCR 与截图入口落地方案

### 7.1 必须澄清的入口边界

产品材料里提到“截图悬浮动作卡”。作为产品愿景是成立的，但普通 Android App 一般不能无感知监听全局截图后立刻弹系统级浮窗，除非获得特殊权限、使用通知/媒体库观察、辅助功能、系统合作能力或平台提供的能力。

复赛/落地建议这样写：

```text
当前 APK 落地入口：相册导入、拍照导入、文本分享、手动输入。
系统级截图浮窗：作为与 vivo 系统能力结合的增强方向；普通 App 版本不强行承诺无感截图监听。
```

### 7.2 OCR 分层

```text
OcrEngine
  ├─ ManualOcrEngine：用户粘贴/编辑 OCR 文本，必须保留
  ├─ LocalOcrEngine：端侧 OCR，可选
  ├─ CloudOcrEngine：云侧 OCR，可选
  └─ MockOcrEngine：演示和测试样例
```

`CaptureDraft` 里必须记录：

- 来源：gallery/camera/share/manual。
- OCR 原文。
- OCR 置信度。
- 是否经过脱敏。
- 是否允许云侧增强。
- 图片是否已本地清除。

### 7.3 OCR 失败处理

| 失败场景 | UI |
|---|---|
| 没识别出文字 | “未识别到稳定文字，可手动粘贴通知内容继续” |
| 图片太糊 | “图片可能不清晰，建议重新拍照或手动输入” |
| 云侧 OCR 不可用 | “云侧识别暂不可用，已切换手动确认” |
| 文本太短 | “内容不足以判断任务，可先存入待确认” |

---

## 8. 数据与状态机落地

### 8.1 推荐数据模型

```kotlin
data class InboxItem(
    val id: String,
    val title: String,
    val sceneType: SceneType,
    val sourceType: CaptureSourceType,
    val status: InboxStatus,
    val priority: Priority,
    val startAt: Instant?,
    val deadlineAt: Instant?,
    val locationText: String?,
    val taskSummary: String,
    val confidence: Float,
    val missingFields: List<String>,
    val createdAt: Instant,
    val updatedAt: Instant,
)

data class ActionPlan(
    val itemId: String,
    val actions: List<ActionDraft>,
)

data class ExecutionResult(
    val actionId: String,
    val type: ActionType,
    val status: ExecutionStatus,
    val message: String,
    val executedAt: Instant,
)
```

### 8.2 状态机

```text
captured
  -> analyzing
  -> pending_confirmation
  -> ready_to_execute
  -> executing
  -> scheduled
  -> due_soon
  -> completed

异常：
analyzing -> needs_manual_review
ready_to_execute -> permission_blocked -> fallback_ready
executing -> execution_failed -> fallback_ready
any -> ignored
any -> archived
```

### 8.3 排序规则

今日行动台排序：

1. 即将截止且未完成。
2. 今天开始且未安排。
3. 高优先级课程/活动。
4. 待确认但置信度高。
5. 低置信度但缺时间/地点。
6. 已完成、已忽略默认不显示在首页。

---

## 9. 初赛文档如何升级

你的初赛材料已经有很好的叙事：不是收藏器，是碎片执行代理；从截图/拍照到可确认、可执行、可追踪的行动卡。现在要把材料从“产品策划书”升级为“落地应用证明”。

### 9.1 PDF/PPT 新增页面建议

| 新增页 | 标题 | 内容 |
|---|---|---|
| 1 | 复赛落地升级概览 | 从初赛原型到 Android APK + BlueLM + 云真机 |
| 2 | 蓝心大模型接入 | 后端 ModelAdapter、结构化输出、schema 校验 |
| 3 | 云真机测试证据 | 机型、系统、录屏、通过项、失败降级 |
| 4 | 真实 App 前端升级 | 多页面截图：今日、导入、确认、编排、收件箱、设置 |
| 5 | 隐私与安全 | 密钥不进 APK、OCR 脱敏、用户确认、数据清除 |
| 6 | 评测集与质量 | 100 条样例、课程/活动/会议/作业/低质量反例 |
| 7 | 失败降级 | BlueLM 不可用、权限拒绝、地图不可用、OCR 失败 |
| 8 | 与 vivo 场景结合 | 手机生态入口、云真机、OriginOS/蓝心能力增强方向 |

### 9.2 原有页要修改的说法

| 原说法 | 建议改法 |
|---|---|
| “后端解析” | “后端模型编排：Mock 兜底 + BlueLM 在线解析” |
| “截图悬浮动作卡” | “当前落地入口为相册/分享/拍照；截图浮窗是系统能力增强方向” |
| “已写入日历” | “已打开系统日历新增页，由用户保存；或已调度本地提醒” |
| “端侧优先、云侧增强” | “端侧保存与确认；云侧只处理用户确认允许的 OCR 文本” |
| “已完成 Product Beta” | “已完成 MVP/Beta 验收，复赛升级为 BlueLM + 云真机实证” |

### 9.3 答辩口播升级版

```text
初赛时，我们证明了“截图/拍照到行动卡”的产品闭环。
复赛阶段，我们把它从原型推进到真实 Android APK：
第一，接入赛组委提供的蓝心大模型，通过后端 ModelAdapter 输出符合 JSON Schema 的结构化行动卡；
第二，在云真机上验证相册、拍照、分享、日历、提醒、地图和失败降级；
第三，把前端从演示控制台升级成多页面行动应用，首页只展示今天最该处理的事；
第四，坚持用户确认机制，模型只生成草稿，系统动作必须由用户确认后执行。
```

---

## 10. 新的总体验收指标

新增一个总脚本：

```bash
python3 shike/validation/validate_landing_release_candidate.py
```

建议总分 50 项：

| 模块 | 分值 | 检查内容 |
|---|---:|---|
| BlueLM 接入 | 8 | Adapter、鉴权、schema、fallback、错误处理 |
| 密钥安全 | 6 | AppKEY 不进 Android/Git/日志/文档 |
| 云真机 | 8 | 后端 HTTPS、录屏、机型、logcat、报告 |
| 前端精修 | 8 | 多页面、状态、设计系统、Debug 隐藏 |
| OCR 与导入 | 5 | 相册、拍照、分享、手动、OCR 失败 |
| 执行闭环 | 5 | 日历、提醒、地图、权限、结果记录 |
| 收件箱 | 4 | 多条、筛选、搜索、状态机 |
| 隐私 | 3 | 脱敏、一键清除、云侧开关 |
| 材料 | 3 | PDF/PPT/脚本/证据包更新 |

通过标准：

```text
LANDING_RELEASE_CANDIDATE_METRIC 50/50
```

允许在开发中先设宽松标准：

```text
>= 40/50 可录屏
>= 45/50 可提交复赛材料
50/50 可作为最终交付包
```

---

## 11. Codex Goal 模式执行顺序

### Goal 0：密钥安全与仓库防泄漏

```text
/goal 根据 docs/SHIKE_LANDING_APP_OPTIMIZATION_GUIDE.md 的密钥安全要求，建立后端环境变量配置、.gitignore、密钥脱敏日志和 validate_secret_hygiene.py。不得把用户提供的 AppKEY 写入任何源码、文档、测试样例或 Android 资源。完成条件：validate_secret_hygiene.py 通过；Android、docs、materials、prototype 中不存在完整 AppKEY 或 sk- 前缀密钥；README 说明如何用环境变量配置 BlueLM。
```

### Goal 1：BlueLM ModelAdapter

```text
/goal 在不破坏现有 /health、/v1/schema、/v1/analyze 契约的前提下，把后端改造成 ModelAdapter 架构，新增 MockModelAdapter 和 BlueLMModelAdapter。BlueLM 鉴权信息从环境变量读取，调用失败时回退 Mock 或 needs_manual_review，输出必须通过 Pydantic/JSON Schema 校验。完成条件：validate_bluelm_adapter.py 和 verify_backend.py 通过；没有密钥泄漏；Android 无需修改即可继续调用 /v1/analyze。
```

### Goal 2：BlueLM 结构化 Prompt 与模型评测

```text
/goal 为拾刻建立 BlueLM 结构化抽取 prompt、100 条回归样例评测和模型输出质量报告。模型只能输出符合 ShikeModelOutput 的 JSON；失败时进入人工确认。完成条件：validate_model_contract_strict.py 通过；课程、活动、会议、作业、低质量反例均覆盖；生成 docs/model-eval-report.md。
```

### Goal 3：云真机后端访问与测试包

```text
/goal 升级 device-runbook.md 和 device-demo-checklist.md，明确模拟器、USB 真机、云真机三种网络配置；新增 validate_cloud_device_package.py；新增 cloud-device-test-report.md 模板。完成条件：文档不再把 10.0.2.2 当作云真机方案；录屏证据目录和 9 段文件名被脚本检查；README 有云真机验收命令。
```

### Goal 4：前端从演示控制台升级为真实 App 多页面

```text
/goal 按 docs/SHIKE_LANDING_APP_OPTIMIZATION_GUIDE.md 将 Android 前端重构为 HomeActionScreen、CaptureHubScreen、ParseConfirmScreen、ActionPlanScreen、InboxScreen、PrivacySettingsScreen 和 DebugDemoScreen。首页不得常驻后端地址、样例按钮、交付物自检和演示路线；这些内容移入 DebugDemoScreen。完成条件：validate_frontend_polish.py 通过；截图/拍照/分享/后端解析/确认/日历/提醒/地图主链路不回退。
```

### Goal 5：OCR 与导入产品化

```text
/goal 建立 CaptureDraft 与 OcrEngine 分层，统一相册、相机、分享文本、手动输入入口。保留 ManualTextFallback，OCR 失败时可手动继续；不默认上传图片。完成条件：相册/相机/分享/手动四类输入都能进入同一解析流程；OCR 失败不会中断主链路；新增 validate_capture_ocr_pipeline.py。
```

### Goal 6：收件箱长期工作台

```text
/goal 将收件箱升级为多条 InboxItem 工作台，支持状态筛选、搜索、归档/恢复、执行结果和过期处理。不要只保存当前行动卡。完成条件：至少 50 条合成记录可持久化；待确认、已安排、即将截止、已完成、已忽略五状态可筛选；validate_inbox_workbench_landing.py 通过。
```

### Goal 7：材料升级为复赛落地证据

```text
/goal 在初赛材料基础上更新 PDF/PPT 大纲、演示脚本、device-demo-checklist 和 README，加入 BlueLM 接入、云真机证据、真实 App 前端、隐私安全、失败降级和评分映射。完成条件：materials/final-demo-script.md、materials/landing-deck-outline.md、docs/scoring-evidence-map.md 存在；validate_landing_materials.py 通过。
```

### Goal 8：最终 Release Candidate

```text
/goal 建立 validate_landing_release_candidate.py，将 BlueLM、密钥安全、云真机、前端、OCR、执行闭环、收件箱、隐私和材料整合成 50 项验收。逐项补齐直到达到 LANDING_RELEASE_CANDIDATE_METRIC 50/50。不得删除现有 validate_real_world_ready.py、validate_demo_acceptance.py、validate_action_execution.py。遇到 BlueLM 凭据、云真机平台或外部网络阻塞时生成 blocking-report.md。
```

---

## 12. 推荐开发节奏

### 第一阶段：安全接入 BlueLM

目标：后端能安全调用赛组委模型。

交付：

- `settings.py`
- `vivo_auth.py`
- `bluelm_adapter.py`
- `validate_secret_hygiene.py`
- `validate_bluelm_adapter.py`
- `docs/bluelm-integration-runbook.md`

验收：

```bash
python3 shike/backend/verify_backend.py
python3 shike/validation/validate_secret_hygiene.py
python3 shike/validation/validate_bluelm_adapter.py
```

### 第二阶段：云真机可跑通

目标：云真机能访问 HTTPS 后端并跑完整主链路。

交付：

- 云端后端地址。
- 云真机 runbook。
- 云真机录屏证据目录。
- 后端脱敏访问日志。

验收：

```bash
python3 shike/validation/validate_cloud_device_package.py
```

### 第三阶段：前端像真实 App

目标：首页不再像 demo 控制台，而像可用产品。

交付：

- 多页面 Compose。
- DebugDemoScreen。
- 设计系统组件。
- loading/empty/error 状态。

验收：

```bash
python3 shike/validation/validate_frontend_polish.py
```

### 第四阶段：OCR 与收件箱长期化

目标：用户可以持续使用，而不是只演示一张卡。

交付：

- CaptureDraft。
- OcrEngine。
- InboxItem 多条持久化。
- 状态筛选和搜索。

验收：

```bash
python3 shike/validation/validate_capture_ocr_pipeline.py
python3 shike/validation/validate_inbox_workbench_landing.py
```

### 第五阶段：材料和最终包

目标：文档、PPT、PDF、录屏证据都能证明“已落地”。

交付：

- `materials/landing-deck-outline.md`
- `materials/final-demo-script.md`
- `docs/scoring-evidence-map.md`
- `materials/evidence/cloud-device/*.mp4`
- `apk-sha256.txt`

验收：

```bash
python3 shike/validation/validate_landing_materials.py
python3 shike/validation/validate_landing_release_candidate.py
```

---

## 13. 最终交付包建议

```text
拾刻_复赛落地交付包/
  app-debug.apk
  apk-sha256.txt
  README.md
  docs/
    product-spec.md
    bluelm-integration-runbook.md
    cloud-device-test-report.md
    device-runbook.md
    scoring-evidence-map.md
    privacy-and-security.md
  backend/
    main.py
    adapters/
    requirements.txt
    env.example
  contracts/
    model-output.schema.json
    sample-course-request.json
    sample-course-response.json
  materials/
    final-demo-script.md
    landing-deck-outline.md
    evidence/
      cloud-device/
        01-cloud-install-open.mp4
        02-cloud-gallery-bluelm.mp4
        03-cloud-camera-bluelm.mp4
        04-cloud-share-text.mp4
        05-cloud-permission-fallback.mp4
        06-cloud-backend-failure.mp4
        07-cloud-restart-restore.mp4
        08-cloud-ui-polish.mp4
        09-cloud-final-route.mp4
  validation/
    validate_secret_hygiene.py
    validate_bluelm_adapter.py
    validate_cloud_device_package.py
    validate_frontend_polish.py
    validate_landing_release_candidate.py
```

注意：正式交付包里不能出现 `.env.local`，不能出现完整 AppKEY。

---

## 14. 复赛评审时最该展示的 5 个证据

1. **BlueLM 在线解析证据**：后端脱敏日志 + App 页面显示“蓝心解析成功” + 结构化字段。
2. **云真机跑通证据**：云真机录屏，包含相册/拍照/分享至少两条链路。
3. **用户确认后执行证据**：未确认时按钮禁用，确认后日历/提醒/地图可用。
4. **失败降级证据**：BlueLM/后端失败、权限拒绝、地图不可用时仍保留行动卡。
5. **前端产品化证据**：多页面 App，而不是只在一个长滚动页里堆控件。

---

## 15. 最终标准

当你可以稳定回答下面 8 个问题时，拾刻就从“比赛 MVP”进入“落地应用候选”：

1. 评委问“你们真的用了蓝心大模型吗？”——能展示 BlueLM Adapter、脱敏日志和在线解析录屏。
2. 评委问“云真机能跑吗？”——能展示云真机安装、解析、确认、执行、降级录屏。
3. 评委问“密钥安全吗？”——能说明 AppKEY 不在 APK，后端环境变量管理，日志脱敏。
4. 评委问“模型错了怎么办？”——能展示置信度、缺失字段、人工确认和 fallback。
5. 评委问“这不是收藏夹吗？”——能展示日历、提醒、地图、收件箱状态机。
6. 评委问“截图浮窗能实现吗？”——能诚实说明当前落地入口与系统级增强边界。
7. 评委问“前端只是原型吗？”——能展示多页面真实 App 与云真机交互。
8. 评委问“能持续使用吗？”——能展示多条收件箱、搜索筛选、过期处理和一键清除。

```
# 拾刻 AI Agent 项目知识建设指导文件

适用目标：让后续 Codex / AI Agent 在修改、重构、排障、测试、扩展“拾刻”项目时，能优先理解项目事实、复用已有模块、遵守架构边界、避免重复造轮子和破坏主链路。

本文件不是普通项目介绍，而是用于指导 AI 生成或完善：

- `AGENTS.md`
- `.agents/skills/`
- 必要的轻量验证脚本
- 必要的项目知识索引文档

## 0. 当前项目事实基线

### 0.1 项目是什么

拾刻是一款面向 vivo AIGC 创新赛应用赛道的 Android 应用，定位是“手机碎片信息行动助手”。

项目核心闭环：

```text
截图/拍照/文本分享
  -> OCR 草稿 / 文本输入
  -> 后端或本地模型解析
  -> AI 解析确认
  -> 用户确认修正
  -> 日历 / 提醒 / 地图动作
  -> 收件箱 / 今日行动台持续追踪
```

首期锁定：

```
入口：截图导入、相机拍照、文本分享
场景：课程通知、活动海报
动作：日历、提醒、地图
持续层：收件箱与今日行动台
```

后续 AI 修改项目时必须围绕这个闭环，不允许把产品改成聊天机器人首页、普通收藏夹、泛化文件管理器或大型知识库。

### 0.2 当前已有能力

当前项目已经具备以下能力，后续 AI 不应重复造轮子：

#### Android 端

- Kotlin + Jetpack Compose。
- `MainActivity` 作为 Activity 入口与组合层。
- `ShikeApp` 作为主 UI 组合入口。
- 系统相册截图选择。
- 相机拍照预览。
- 文本分享入口：`ACTION_SEND` + `text/plain`。
- 后端地址配置与本地保存。
- OCR 文本草稿编辑。
- 后端解析课程 / 活动。
- 后端失败时回退本地 MockModelAdapter。
- AI 解析确认页。
- 用户可编辑标题、时间、地点、状态。
- 用户确认后才启用日历、提醒、地图。
- 系统日历插入 Intent。
- 本地定时提醒。
- 通知权限申请。
- 地图 deeplink。
- 地图不可用时复制地点并保留行动卡。
- `SharedPreferences` 本地恢复。
- 一键清除本地数据。
- 应用启动恢复待触发提醒。
- 设备重启后通过 `BootReminderReceiver` 恢复提醒。

#### 后端

- Python FastAPI。
- `GET /health`。
- `GET /v1/schema`。
- `POST /v1/analyze`。
- Pydantic 请求 / 响应模型。
- 当前可根据课程通知、活动海报或未知内容返回结构化行动卡。
- 输出必须匹配 `contracts/model-output.schema.json`。
- 当前适合继续演示和兜底，但接入蓝心大模型后需要保留 Mock / fallback 能力。

#### 模型契约

结构化输出字段包括：

```
scene_type
confidence
title
time
location
task
suggested_actions
missing_fields
explanation
```

动作类型当前只允许：

```
calendar
reminder
map
```

核心场景当前只允许：

```
course_notice
event_poster
unknown
```

后续扩展会议、作业、面试、出行等场景时，必须先更新 schema、样例、Android 映射、验证脚本和文档，不允许只在 Prompt 中口头增加。

#### 验收体系

当前项目已经存在多类机械验收，后续修改必须优先保持这些验收不退化：

```
python3 shike/validation/validate_android_structure.py
python3 shike/validation/validate_android_unit_tests.py
python3 shike/validation/validate_real_world_ready.py
python3 shike/validation/validate_demo_acceptance.py
python3 shike/validation/validate_deliverables.py
python3 shike/validation/validate_landable.py
python3 shike/validation/validate_action_execution.py
python3 shike/validation/validate_today_ranking.py
python3 shike/validation/validate_advanced_product_beta.py
python3 shike/validation/validate_model_eval_cases.py
python3 shike/spike/run_spike.py --all
python3 shike/scripts/verify_core20_package.py "/path/to/拾刻_核心20文件交付包_20260505"
```

文档型修改至少应运行轻量 Markdown / 路径 / 关键文件存在检查，以及 `git diff` 人工审查。

## 1. 不可破坏的核心约束

### 1.1 用户确认优先

任何后续 AI 修改都必须遵守：

```
未经过用户确认修正，不得执行日历、提醒、地图等敏感动作。
```

允许 AI 做：

```
识别
抽取
建议
置信度解释
缺失字段提示
生成行动草稿
```

不允许 AI 自动做：

```
直接写日历
直接调通知
直接打开地图
直接替用户决定忽略或完成
直接上传真实个人数据
```

### 1.2 模型只负责理解，规则层负责执行

项目架构边界：

```
大模型：场景判断、字段抽取、时间/地点/任务理解、置信度、缺失项、建议动作
规则层：schema 校验、权限判断、状态机、系统动作、失败降级、日志脱敏
用户：最终确认权
```

后续 AI 不得让模型直接决定系统写入结果，也不得把系统动作逻辑藏进模型自然语言输出。

### 1.3 BlueLM / 蓝心大模型接入安全

用户已提供 AppID 和 AppKEY，但这些是敏感凭据。

后续 AI 必须遵守：

```
不得把完整 AppKEY 写入源码。
不得把完整 AppKEY 写入 AGENTS.md。
不得把完整 AppKEY 写入 .agents/skills。
不得把完整 AppKEY 写入 README、docs、materials、prototype。
不得把完整 AppKEY 写入 Android 资源。
不得把完整 AppKEY 打进日志。
不得把完整 AppKEY 打进测试快照。
不得把完整 AppKEY 打包进 APK。
```

推荐环境变量命名：

```
BLUELM_APP_ID=...
BLUELM_APP_KEY=...
BLUELM_BASE_URL=...
BLUELM_MODEL=...
BLUELM_TIMEOUT_SECONDS=20
```

仓库只允许出现占位符：

```
BLUELM_APP_ID=your-app-id
BLUELM_APP_KEY=your-app-key
```

因为 AppKEY 已经出现在对话中，正式交付前建议在平台侧重置或换新密钥。后续 Codex 只需要实现环境变量读取和脱敏，不要复述完整密钥。

### 1.4 Android 不直接持有模型密钥

正确链路：

```
Android App
  -> 你的 FastAPI 后端 /v1/analyze
  -> BlueLMModelAdapter
  -> 蓝心大模型
```

禁止链路：

```
Android App
  -> 直接携带 AppKEY 请求蓝心大模型
```

理由：

- APK 可被反编译。
- 日志和崩溃信息可能泄漏密钥。
- 用户端网络失败、鉴权失败和模型输出异常不好统一降级。
- 后端才能统一 schema 校验、脱敏、fallback 和评测记录。

### 1.5 云真机测试约束

本地模拟器可以使用：

```
http://10.0.2.2:8000
```

局域网真机可以使用：

```
http://192.168.x.x:8000
```

云真机通常不能访问本机局域网，也不能使用模拟器专用 `10.0.2.2`。因此云真机测试需要：

```
HTTPS 后端地址
或可信临时 HTTPS 隧道
或赛事平台允许访问的公开测试服务
```

云真机录屏时必须隐藏：

```
AppKEY
本机公网隧道 token
真实手机号
学号
群聊成员
真实通知
真实相册内容
局域网敏感地址
```

### 1.6 不得删除已有验收入口

后续 AI 修改时不得删除或弱化：

```
validation/
backend/verify_backend.py
contracts/model-output.schema.json
sample-course-request.json
sample-course-response.json
docs/device-runbook.md
materials/device-demo-checklist.md
README.md 中的机械验收说明
```

如果必须调整命令或路径，必须同步更新 README、runbook、checklist、验证脚本和 AGENTS.md。

## 2. 本次目标：建设 AGENTS.md 与 .agents/skills

本次不是直接加业务功能，而是让后续 AI 更聪明地维护项目。

目标产物：

```
AGENTS.md
.agents/skills/
  shike-project-navigation/SKILL.md
  shike-android-development/SKILL.md
  shike-backend-model-adapter/SKILL.md
  shike-bluelm-integration/SKILL.md
  shike-validation-and-regression/SKILL.md
  shike-device-cloud-testing/SKILL.md
  shike-ui-product-polish/SKILL.md
  shike-security-privacy/SKILL.md
  shike-materials-submission/SKILL.md
```

如果仓库已有 `.agents/skills` 或 `AGENTS.md`，必须增量更新，不得覆盖有效内容。

如果某个 skill 只是在讲通用工程经验，且没有项目特异性，不要创建。

## 3. 建议写入 AGENTS.md 的结构

`AGENTS.md` 应该简洁、项目专属、可执行。建议结构如下：

```
# AGENTS.md

## Project

拾刻是 vivo AIGC 创新赛应用赛道 Android 应用，核心链路是：

截图/拍照/文本分享 -> AI 解析 -> 用户确认 -> 行动编排 -> 收件箱/今日行动台追踪。

不要把项目改成聊天助手首页、普通收藏夹或泛化知识库。

## Key directories

- `android-mvp/`: Android Kotlin + Jetpack Compose App。
- `backend/`: FastAPI 模型编排服务。
- `contracts/`: 模型输出 schema、样例请求与响应。
- `docs/`: 产品规格、设备联调、落地路线、优化日志。
- `materials/`: 演示脚本、提交清单、真机录屏验收。
- `prototype/`: HTML 高保真原型与 Demo 控制台。
- `validation/`: 机械验收脚本和回归样例。
- `spike/`: 技术可行性验证。

## First files to read before changing code

通用任务先读：

- `README.md`
- `docs/product-spec.md`
- `docs/android-mvp-implementation.md`
- `docs/device-runbook.md`
- `contracts/model-output.schema.json`

Android 任务再读：

- `android-mvp/app/src/main/AndroidManifest.xml`
- `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt`
- `android-mvp/app/src/main/java/cn/shike/app/domain/`
- `android-mvp/app/src/main/java/cn/shike/app/data/`
- `android-mvp/app/src/main/java/cn/shike/app/system/`
- `android-mvp/app/src/main/java/cn/shike/app/ui/`

后端任务再读：

- `backend/shike_backend/main.py`
- `backend/verify_backend.py`
- `contracts/model-output.schema.json`
- `contracts/sample-course-request.json`
- `contracts/sample-course-response.json`

验证任务再读：

- `validation/`
- `materials/device-demo-checklist.md`
- `docs/device-runbook.md`

材料任务再读：

- `materials/demo-script.md`
- `materials/submission-checklist.md`
- `prototype/index.html`
- `shike.pdf`

## Non-negotiable invariants

- 用户确认前不得执行日历、提醒、地图动作。
- Android 不得保存或携带 BlueLM AppKEY。
- BlueLM AppID/AppKEY 只能由后端从环境变量读取。
- 不允许把完整密钥写入源码、文档、日志、测试或 APK。
- `/health`、`/v1/schema`、`/v1/analyze` 契约必须保持兼容，除非同步更新 Android、schema、样例、测试和文档。
- 模型输出必须符合 `contracts/model-output.schema.json`。
- 后端失败必须回退 MockModelAdapter 或进入 `needs_manual_review`，不能静默失败。
- 所有演示数据必须是合成样例，不得提交真实群聊、手机号、学号、个人通知或真实 OCR。
- 不要删除已有 validation 脚本。
- 不要把已拆分的 Android 职责重新压回单个大文件。

## Common commands

```bash
# Backend
cd shike/backend
python3 -m uvicorn shike_backend.main:app --host 0.0.0.0 --port 8000

# Backend smoke
python3 shike/backend/verify_backend.py

# Android build
bash shike/android-mvp/build_apk.sh

# Core validation
python3 shike/validation/validate_android_structure.py
python3 shike/validation/validate_android_unit_tests.py
python3 shike/validation/validate_action_execution.py
python3 shike/validation/validate_demo_acceptance.py
python3 shike/validation/validate_real_world_ready.py

# Spike
python3 shike/spike/run_spike.py --all

# Core 20 package check
python3 shike/scripts/verify_core20_package.py "/path/to/拾刻_核心20文件交付包_20260505"
```

## Development rules

- Prefer small, verifiable changes.
- Update validation or docs when behavior changes.
- Preserve existing fallback behavior.
- Prefer synthetic test cases.
- Run the narrowest validation first, then broader validations.
- For documentation-only changes, at minimum check paths, headings, and `git diff`.
- For Android system actions, verify permission denial and unavailable-app fallback.
- For backend model changes, verify schema compatibility and Android mapping.
- For BlueLM integration, add secret hygiene checks before adding network calls.

## Skill routing

Use project skills:

- Android UI / system action task -> `shike-android-development`
- Backend `/v1/analyze` or model adapter task -> `shike-backend-model-adapter`
- BlueLM integration task -> `shike-bluelm-integration`
- Validation failure or test update -> `shike-validation-and-regression`
- Cloud device / real device testing -> `shike-device-cloud-testing`
- Frontend visual polish -> `shike-ui-product-polish`
- Privacy, credential, log redaction -> `shike-security-privacy`
- PPT, PDF, demo script, submission package -> `shike-materials-submission`

## Done checklist

Before finishing:

- Mention changed files.
- Mention validation commands run and results.
- Mention any unverified assumptions.
- Confirm no complete AppKEY appears in diff.
- Confirm user-confirmation-before-execution invariant still holds.

```
## 4. 建议创建的 skills

### 4.1 `.agents/skills/shike-project-navigation/SKILL.md`

```md
# Shike Project Navigation Skill

## When to use

Use this skill whenever an AI agent enters the project, needs to understand file ownership, or is about to modify more than one module.

## Must read first

- `README.md`
- `docs/product-spec.md`
- `docs/android-mvp-implementation.md`
- `contracts/model-output.schema.json`
- `docs/device-runbook.md`
- `materials/device-demo-checklist.md`

## Project map

- `android-mvp/`: Android app.
- `backend/`: FastAPI model orchestration.
- `contracts/`: schema and sample payloads.
- `docs/`: product and engineering guidance.
- `materials/`: demo and submission assets.
- `prototype/`: visual prototype.
- `validation/`: validation scripts.
- `spike/`: local feasibility spike.

## Core flow

```text
capture -> analyze -> confirm -> plan actions -> execute/fallback -> inbox/today tracking
```

## Do not miss

- User confirmation gates all system actions.
- `/v1/analyze` output must match schema.
- Backend failure must fallback.
- Real demo data must be synthetic.
- Existing validation scripts are part of product quality, not optional extras.

## Validation

For navigation-only or documentation changes:

```
git diff -- AGENTS.md .agents/skills docs README.md
```

For behavior-related changes, route to the specific skill.

```
### 4.2 `.agents/skills/shike-android-development/SKILL.md`

```md
# Shike Android Development Skill

## When to use

Use for Android Kotlin, Jetpack Compose UI, permissions, reminders, calendar intents, map deeplinks, local persistence, or share/camera/gallery entry changes.

## Must read first

- `android-mvp/app/src/main/AndroidManifest.xml`
- `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt`
- `android-mvp/app/src/main/java/cn/shike/app/domain/`
- `android-mvp/app/src/main/java/cn/shike/app/data/`
- `android-mvp/app/src/main/java/cn/shike/app/system/`
- `android-mvp/app/src/main/java/cn/shike/app/ui/`
- `docs/device-runbook.md`
- `validation/validate_action_execution.py`

## Existing Android capabilities

- Gallery import.
- Camera preview import.
- Text share import.
- OCR draft editing.
- Backend URL persistence.
- Backend analyze trigger.
- Local fallback.
- Manual confirmation.
- Calendar insert Intent.
- Scheduled reminder.
- Notification permission flow.
- Map deeplink.
- Fallback for unavailable system apps.
- Boot reminder restore.
- Local data clear.

## Recommended flow

1. Identify whether change is UI, domain, data, system, or test.
2. Avoid putting new domain/system logic directly into `MainActivity`.
3. Preserve `ShikeApp` public callbacks unless intentionally refactoring.
4. Check confirmation gates before any external action.
5. Add or update unit tests / validation when behavior changes.
6. Run narrow Android validation first.

## High-risk mistakes

- Enabling calendar/reminder/map before confirmation.
- Moving system action code into Compose components.
- Logging raw OCR or sensitive data.
- Removing fallback when permission is denied.
- Breaking text share intent.
- Breaking boot reminder restore.
- Treating “opened calendar insert page” as “event definitely saved”.

## Common commands

```bash
bash shike/android-mvp/build_apk.sh
python3 shike/validation/validate_android_structure.py
python3 shike/validation/validate_android_unit_tests.py
python3 shike/validation/validate_action_execution.py
python3 shike/validation/validate_real_world_ready.py
```

## Validation focus

- Confirmation gate.
- Permission denied behavior.
- System app unavailable behavior.
- App restart restore.
- Device reboot reminder restore.
- Local data clear cancels pending reminders.

```
### 4.3 `.agents/skills/shike-backend-model-adapter/SKILL.md`

```md
# Shike Backend Model Adapter Skill

## When to use

Use for FastAPI backend, `/v1/analyze`, schema validation, model adapter abstraction, mock fallback, prompt construction, or model response parsing.

## Must read first

- `backend/shike_backend/main.py`
- `backend/verify_backend.py`
- `contracts/model-output.schema.json`
- `contracts/sample-course-request.json`
- `contracts/sample-course-response.json`
- `validation/validate_model_eval_cases.py`
- `validation/regression-cases.json`

## Existing backend contract

Endpoints:

```text
GET /health
GET /v1/schema
POST /v1/analyze
```

`/v1/analyze` request includes:

```
input_id
source_type
ocr_text
locale
scene_hint
user_timezone
```

Response must match `contracts/model-output.schema.json`.

## Recommended architecture

Prefer:

```
main.py
  routes
  request/response models
  adapter selection

model_adapters/
  base.py
  mock_adapter.py
  bluelm_adapter.py

schemas/
  contract loading and validation

prompts/
  shike_structured_prompt.py
```

Keep `/v1/analyze` stable for Android.

## Adapter rules

- MockModelAdapter must remain available.
- BlueLMModelAdapter must be optional.
- Empty OCR text should return validation error, not hallucinated data.
- Low-confidence / unknown content should produce `unknown` and missing fields.
- Model output must be parsed and schema-validated before returning to Android.
- If model returns malformed JSON, fallback to manual review or Mock, not raw text.

## High-risk mistakes

- Returning natural language instead of schema JSON.
- Adding fields not allowed by schema.
- Removing `missing_fields`.
- Removing `explanation`.
- Changing action type names without updating Android.
- Making BlueLM required for offline demo.
- Exposing AppKEY in logs or docs.

## Common commands

```
python3 shike/backend/verify_backend.py

cd shike/backend
python3 -m uvicorn shike_backend.main:app --host 0.0.0.0 --port 8000
```

Manual smoke:

```
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/v1/schema
curl -X POST http://127.0.0.1:8000/v1/analyze \
  -H 'Content-Type: application/json' \
  -d '{"input_id":"demo","source_type":"screenshot","ocr_text":"高数A班今晚18:30改到B203，作业第5章今晚22:00前提交。","scene_hint":"course_notice"}'
```

## Validation

Run:

```
python3 shike/backend/verify_backend.py
python3 shike/validation/validate_model_eval_cases.py
python3 shike/validation/validate_real_world_ready.py
### 4.4 `.agents/skills/shike-bluelm-integration/SKILL.md`

```md
# Shike BlueLM Integration Skill

## When to use

Use when integrating or modifying vivo 蓝心大模型 / BlueLM access, model authentication, request signing, prompt templates, adapter fallback, or cloud-enhanced analysis.

## Must read first

- Official vivo AIGC / BlueLM documentation provided by the user.
- `backend/shike_backend/main.py`
- `contracts/model-output.schema.json`
- `contracts/sample-course-request.json`
- `contracts/sample-course-response.json`
- `docs/device-runbook.md`
- `README.md`
- `.gitignore`
- `.env.example` if present.

## Credential rules

Never write complete secrets into:

- Android source.
- Backend source.
- AGENTS.md.
- `.agents/skills`.
- README.
- docs.
- materials.
- prototype.
- tests.
- logs.
- generated APK.

Use environment variables only:

```bash
BLUELM_APP_ID=your-app-id
BLUELM_APP_KEY=your-app-key
BLUELM_BASE_URL=...
BLUELM_MODEL=...
```

## Required safety checks

Before implementing network calls, add or update:

```
.env.example
.gitignore
validate_secret_hygiene.py
```

The secret hygiene validation should scan at least:

```
android-mvp/
backend/
contracts/
docs/
materials/
prototype/
validation/
AGENTS.md
.agents/
README.md
```

It should fail if it finds:

```
sk-
AppKEY=
BLUELM_APP_KEY=real-looking-secret
X-AI-GATEWAY-SIGNATURE value with secret material
```

Allow placeholders only.

## Adapter behavior

BlueLM must be implemented behind a backend adapter:

```
Android -> FastAPI /v1/analyze -> BlueLMModelAdapter -> BlueLM
```

Do not call BlueLM directly from Android.

If BlueLM call fails:

- fallback to MockModelAdapter, or
- return structured `unknown` / `needs_manual_review` equivalent,
- never return raw provider errors to Android,
- redact AppID/AppKEY/signatures in logs.

## Prompt requirements

The model prompt must ask for strict JSON compatible with `contracts/model-output.schema.json`.

Prompt must emphasize:

- no extra fields,
- Chinese user-facing explanation,
- confidence 0-1,
- missing fields,
- suggested actions only from `calendar`, `reminder`, `map`,
- unknown if insufficient evidence,
- never claim a system action was executed.

## High-risk mistakes

- Committing AppKEY.
- Putting BlueLM key into Android.
- Trusting model JSON without schema validation.
- Removing Mock fallback.
- Letting malformed model output break `/v1/analyze`.
- Using real personal OCR in tests or examples.
- Treating official API details as stable without re-reading docs.

## Validation

Suggested commands:

```
python3 shike/validation/validate_secret_hygiene.py
python3 shike/backend/verify_backend.py
python3 shike/validation/validate_model_eval_cases.py
python3 shike/validation/validate_real_world_ready.py
### 4.5 `.agents/skills/shike-validation-and-regression/SKILL.md`

```md
# Shike Validation and Regression Skill

## When to use

Use when a validation script fails, when changing business behavior, when adding features, or when preparing a submission package.

## Must read first

- `README.md`
- `validation/`
- `backend/verify_backend.py`
- `materials/device-demo-checklist.md`
- `docs/device-runbook.md`
- `scripts/verify_core20_package.py`

## Existing validation categories

- Android structure.
- Android unit tests.
- Action execution safety.
- Product beta readiness.
- Model eval cases.
- Demo acceptance.
- Real-world readiness.
- Deliverables.
- Landability.
- Spike.
- Core 20 package.

## Recommended workflow

1. Reproduce the failure.
2. Read the failing validation script.
3. Identify whether the script checks code, docs, generated files, or command outputs.
4. Fix the root cause, not just the string check.
5. If the intended behavior legitimately changed, update code, docs, tests, and script together.
6. Re-run the narrow script.
7. Re-run broader readiness if behavior changed.

## Common commands

```bash
python3 shike/validation/validate_android_structure.py
python3 shike/validation/validate_android_unit_tests.py
python3 shike/validation/validate_action_execution.py
python3 shike/validation/validate_advanced_product_beta.py
python3 shike/validation/validate_model_eval_cases.py
python3 shike/validation/validate_demo_acceptance.py
python3 shike/validation/validate_real_world_ready.py
python3 shike/spike/run_spike.py --all
```

## High-risk mistakes

- Editing validation scripts to pass without preserving product behavior.
- Removing checks for user confirmation.
- Weakening secret hygiene.
- Ignoring demo checklist when changing user flows.
- Changing commands in README but not checklist.
- Changing schema but not sample response.

## Done criteria

- Failing script passes.
- Related broader script passes.
- `git diff` shows behavior and docs are consistent.
- No secret is introduced.

```
### 4.6 `.agents/skills/shike-device-cloud-testing/SKILL.md`

```md
# Shike Device and Cloud Testing Skill

## When to use

Use for local emulator, USB real device, vivo cloud device, APK install, backend connectivity, recording evidence, logcat, or demo rehearsal.

## Must read first

- `docs/device-runbook.md`
- `materials/device-demo-checklist.md`
- `README.md`
- `AndroidManifest.xml`
- `backend/verify_backend.py`

## Current local testing modes

Emulator backend:

```text
http://10.0.2.2:8000
```

USB / LAN device backend:

```
http://192.168.x.x:8000
```

Start backend:

```
cd shike/backend
python3 -m uvicorn shike_backend.main:app --host 0.0.0.0 --port 8000
```

Install APK:

```
adb install -r shike/android-mvp/app/build/outputs/apk/debug/app-debug.apk
```

## Cloud device requirement

Cloud devices usually cannot access `10.0.2.2` or local LAN IP. Use:

- deployed HTTPS backend,
- or safe temporary HTTPS tunnel,
- or competition-provided reachable endpoint.

Never expose AppKEY in query params, logs, or screenshots.

## Required recording evidence

Use these filenames under:

```
shike/materials/evidence/
```

Files:

```
01-install-and-open.mp4
02-course-gallery-backend.mp4
03-event-camera-actions.mp4
04-fallback-offline.mp4
05-restart-restore.mp4
06-delivery-readiness.mp4
```

## Flows to verify

- Install and open.
- Course gallery import.
- OCR draft edit.
- Backend course analysis.
- Manual confirm.
- Calendar insert.
- Event camera import.
- Backend event analysis.
- Reminder permission.
- Map deeplink.
- Backend failure fallback.
- Restart restore.
- Local data clear.
- Device reboot reminder restore if available.

## High-risk mistakes

- Recording real personal notifications.
- Showing AppKEY or tunnel tokens.
- Assuming cloud device can access local backend.
- Using `10.0.2.2` on cloud real device.
- Forgetting backend fallback recording.
- Claiming calendar event was saved when only insert page was opened.

## Validation

```
bash shike/android-mvp/build_apk.sh
python3 shike/backend/verify_backend.py
python3 shike/validation/validate_demo_acceptance.py
python3 shike/validation/validate_real_world_ready.py
### 4.7 `.agents/skills/shike-ui-product-polish/SKILL.md`

```md
# Shike UI and Product Polish Skill

## When to use

Use for Android frontend polish, Compose screen split, visual consistency, state-driven UI, prototype alignment, or competition demo refinement.

## Must read first

- `docs/product-spec.md`
- `prototype/index.html`
- `materials/demo-script.md`
- `shike.pdf`
- Android Compose UI files under `android-mvp/app/src/main/java/cn/shike/app/ui/`
- `README.md`

## Product UI principles

- The app is action-centered, not chat-centered.
- The homepage is 今日行动台, not a blank conversation box.
- Use card-based, calm, trustworthy visual style.
- Green means confirmed / arranged / trustworthy.
- Orange means due soon / missing / risk.
- Blue means pending / informational.
- Explicitly show risks and missing fields.
- Keep “用户确认后执行” visible in critical flows.

## Required screens / areas

- 今日行动台
- 采集入口
- OCR 文本草稿
- AI 解析确认
- 风险与缺失字段
- 行动编排
- 收件箱状态
- 隐私与端云设置
- 交付物自检 / demo route may remain debug-only

## Recommended frontend direction

Move from long demo page toward real app structure:

```text
HomeActionScreen
ImportScreen / ImportPanel
ParseConfirmScreen
ActionComposeScreen
InboxScreen
PrivacySettingsScreen
DebugDeliveryScreen
```

Demo-only controls should move toward Debug / Delivery area, not dominate normal user flow.

## High-risk mistakes

- Removing risk panel.
- Making UI look like generic chatbot.
- Hiding confirmation requirement.
- Making all cards static instead of data-driven.
- Removing offline demo samples.
- Removing delivery self-check before competition.
- Introducing visual polish that breaks validation text tokens.

## Validation

```
python3 shike/validation/validate_demo_acceptance.py
python3 shike/validation/validate_real_world_ready.py
```

When UI text changes, inspect validation scripts first because some checks may rely on exact Chinese text.

```
### 4.8 `.agents/skills/shike-security-privacy/SKILL.md`

```md
# Shike Security and Privacy Skill

## When to use

Use for secrets, environment variables, log redaction, personal data, local data clearing, cloud enhancement settings, permissions, or privacy copy.

## Must read first

- `docs/product-spec.md`
- `docs/device-runbook.md`
- `README.md`
- Android data/system files.
- Backend config/model adapter files.
- `.gitignore`
- `.env.example`
- `validation/`

## Core privacy rules

- Use synthetic demo data only.
- Do not store real OCR unless user explicitly chooses.
- Do not upload real screenshots by default.
- Do not log raw OCR, phone numbers, names, student IDs, group messages, AppKEY, signatures, or backend tokens.
- Android must not contain BlueLM AppKEY.
- Backend must read secrets from environment variables.
- Local data clear must clear inbox snapshot, backend URL if intended, and scheduled reminder.

## Redaction rules

Logs should show:

```text
AppID: 2026****887
AppKEY: sk-****redacted****
OCR: [redacted length=...]
```

Never show full secret or full real OCR.

## Permissions

- `POST_NOTIFICATIONS`: request when user confirms and taps reminder.
- `CAMERA`: request when user taps camera import.
- Calendar: current flow uses insert Intent, do not claim direct calendar provider write.
- Map: deeplink, with fallback.

## High-risk mistakes

- Putting keys in Android.
- Saving raw OCR in debug logs.
- Uploading real personal screenshots during tests.
- Weakening one-click local data clear.
- Forgetting boot reminder cleanup.
- Writing privacy claims not backed by implementation.

## Validation

```
python3 shike/validation/validate_action_execution.py
python3 shike/validation/validate_real_world_ready.py
python3 shike/validation/validate_secret_hygiene.py
```

If `validate_secret_hygiene.py` does not exist yet, create it before implementing BlueLM.

```
### 4.9 `.agents/skills/shike-materials-submission/SKILL.md`

```md
# Shike Materials and Submission Skill

## When to use

Use for competition submission materials, demo script, PDF/PPT copy, poster copy, evidence checklist, core 20 package, or final review.

## Must read first

- `materials/demo-script.md`
- `materials/submission-checklist.md`
- `materials/device-demo-checklist.md`
- `prototype/index.html`
- `README.md`
- `docs/product-spec.md`
- `shike.pdf`
- `scripts/verify_core20_package.py`

## Product narrative

Use these stable phrases:

- “从截图到行动闭环”
- “不是收藏器，是执行代理”
- “端侧优先、云侧增强、用户可控”
- “用户确认后执行”
- “把手机碎片推进到日历、提醒、地图和收件箱状态”

## Demo must show

- 今日行动台。
- 课程通知截图。
- AI 解析确认。
- 风险与缺失字段。
- 用户确认。
- 日历 / 提醒 / 地图。
- 活动海报拍照。
- 收件箱追踪。
- 后端失败 fallback。
- 重启恢复。
- 隐私与端云设置。

## High-risk mistakes

- Claiming fully autonomous execution.
- Claiming BlueLM integrated before code and evidence exist.
- Showing full AppKEY.
- Showing real user data.
- Removing fallback story.
- Making materials inconsistent with Android behavior.
- Overpromising unsupported vivo official APIs.

## Validation

```bash
python3 shike/validation/validate_demo_acceptance.py
python3 shike/validation/validate_deliverables.py
python3 shike/scripts/verify_core20_package.py "/path/to/拾刻_核心20文件交付包_20260505"
## 5. Subagent 并行分析建议

主 agent 应在第一阶段快速盘点后，立即并行派发以下 subagent。每个 subagent 只分析自己的范围，避免重复工作。

### Subagent A：项目结构与 AGENTS.md

范围：

```text
README.md
AGENTS.md 如果存在
.agents/skills 如果存在
docs/
validation/
scripts/
```

产出：

- 项目目录职责。
- 首读文件清单。
- 常用命令。
- 高风险区域。
- `AGENTS.md` 增量更新建议。

### Subagent B：Android 架构与系统动作

范围：

```
android-mvp/
AndroidManifest.xml
MainActivity.kt
domain/
data/
system/
ui/
Android unit tests
```

产出：

- Android 分层事实。
- 系统动作确认门禁。
- 可复用 helper。
- 不应重复实现的模块。
- Android skill 内容。

### Subagent C：后端与模型契约

范围：

```
backend/
contracts/
sample request/response
backend smoke test
model eval validation
```

产出：

- API 契约。
- schema 字段约束。
- Mock / fallback 现状。
- BlueLM Adapter 接入点。
- 后端 skill 内容。

### Subagent D：验证与质量体系

范围：

```
validation/
spike/
backend/verify_backend.py
README mechanical acceptance
materials/device-demo-checklist.md
```

产出：

- 验收命令地图。
- 每个脚本负责什么。
- 常见失败原因。
- 修改代码后的验证顺序。
- validation skill 内容。

### Subagent E：前端视觉与产品材料

范围：

```
prototype/
materials/
shike.pdf
docs/product-spec.md
Android Compose UI
```

产出：

- UI 风格。
- 产品话术。
- 演示叙事。
- 普通用户页面与 debug 页面边界。
- UI polish 和 submission skills 内容。

### Subagent F：安全、隐私与外部集成

范围：

```
BlueLM docs
backend config
Android manifest permissions
logs
.gitignore
.env.example
privacy settings
device runbook
```

产出：

- 密钥管理约束。
- 环境变量方案。
- 日志脱敏规则。
- 云真机测试安全约束。
- security / BlueLM / cloud-device skills 内容。

## 6. 写入规则

### 6.1 AGENTS.md

必须：

- 简洁。
- 可执行。
- 项目专属。
- 不堆长篇背景。
- 不写未经代码验证的能力。
- 不写完整 AppKEY。
- 不覆盖已有有效内容。

### 6.2 Skills

每个 skill 必须包含：

```
When to use
Must read first
Existing project facts
Recommended workflow
Reusable modules / commands
High-risk mistakes
Validation
```

每个 skill 只服务一个明确开发场景，不要做万能大 skill。

### 6.3 不要创建的 skill

不要创建以下泛泛 skill：

```
general-python-best-practices
general-android-best-practices
general-security-best-practices
general-markdown-writing
```

除非内容强绑定拾刻项目事实，否则不应创建。

## 7. 最终验证

完成后至少检查：

```
find .agents/skills -maxdepth 2 -type f -name "SKILL.md" -print
test -f AGENTS.md
git diff -- AGENTS.md .agents/skills
```

还要人工确认：

```
AGENTS.md 不含完整 AppKEY
skills 不含完整 AppKEY
所有引用路径真实存在
所有命令来自 README、runbook、validation 或实际项目文件
没有把旧的有效内容覆盖掉
没有把通用工程建议伪装成项目事实
```

如果只做文档与 skills 变更，通常不需要完整 Android 构建；但如果改了代码、命令、路径、schema 或 validation，必须运行对应验证命令。

## 8. 完成后输出格式

最终回复应包含：

```
新增 / 更新了哪些文件
每个 skill 的触发场景
AGENTS.md 新增了哪些项目约束
运行了哪些验证
哪些信息仍未确认
是否发现密钥泄漏风险
后续建议的第一条业务开发 Goal
```
