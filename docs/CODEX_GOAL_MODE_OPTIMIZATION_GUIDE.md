# 拾刻后续优化指导：Codex Goal 模式长期任务文档

版本：2026-05-23
适用项目：拾刻 / Shike Android MVP + FastAPI Model Orchestration
目标：把当前“可演示 MVP”推进为“可维护、可测试、可真机复测、可逐步扩展”的功能型软件。

---

## 1. 一句话方向

拾刻不是收藏器，也不是聊天机器人首页，而是把手机里的截图、拍照、分享文本转化为可确认行动卡，并持续追踪的青年场景碎片执行代理。

后续所有优化都必须围绕这条闭环展开：

```text
截图/拍照/分享文本
  -> OCR 或文本草稿
  -> AI/规则解析
  -> 用户确认修正
  -> 行动编排
  -> 日历 / 提醒 / 地图 / 本地降级
  -> 收件箱 / 今日行动台持续追踪
```

不要为了“功能很多”而破坏主链路。每新增一个功能，都必须回答：它是否让“从碎片到行动闭环”更真实、更稳定、更可信？

---

## 2. 当前项目判断

当前项目已经具备演示价值，但还不是功能完善的软件。

已具备的能力包括：

- Android Kotlin + Jetpack Compose 的 MVP 页面。
- 相册截图入口、拍照预览入口、文本分享入口。
- OCR 文本草稿编辑框。
- FastAPI `/health`、`/v1/schema`、`/v1/analyze` 后端服务草案。
- JSON Schema 模型输出契约。
- 课程通知、活动海报两类合成样例。
- 用户确认修正后才启用日历、提醒、地图动作。
- SharedPreferences 的当前行动卡恢复。
- 后端失败时回退本地 MockModelAdapter。
- 演示验收清单、Runbook、验证脚本和录屏路线。

主要短板包括：

- Android 代码集中在 `MainActivity.kt`，UI、状态、网络、持久化、样例数据和系统动作混在一起，长期维护困难。
- 本地存储仍是 SharedPreferences 快照，不足以支撑完整收件箱、状态机、历史记录和执行结果。
- 当前“提醒”更接近即时通知，还不是稳定的定时提醒体系。
- 当前 OCR 仍是草稿/样例驱动，缺少真实 OCR 管线、图片预处理和失败反馈。
- 后端模型逻辑仍是规则 mock，缺少真实模型适配器、结构化校验、置信度策略和回归集。
- 缺少 Android 单元测试、UI 测试、端到端测试、CI 和失败日志体系。
- 页面是演示型长页面，还没有形成真实 App 的导航、列表、详情、编辑、设置等结构。
- 隐私与端云策略已展示，但还没有落成数据脱敏、日志保护、网络安全配置和权限审计。

---

## 3. Codex Goal 模式使用原则

Goal 模式适合“有明确目标、验证循环、停止条件”的长期任务，不适合一句话要求“永远优化”。因此不要把目标写成“把项目做完整”，而要写成“在不破坏主链路的前提下，一轮一轮提高工程成熟度，直到指定验收条件通过”。

### 3.1 推荐启动方式

先把本文件放入仓库，例如：

```text
docs/CODEX_GOAL_MODE_OPTIMIZATION_GUIDE.md
```

然后在 Codex 中先让它规划，再开启目标：

```text
/plan 阅读 docs/CODEX_GOAL_MODE_OPTIMIZATION_GUIDE.md，结合当前仓库，给出第一轮最小可验证优化计划。不要修改代码，先列出风险、验证命令和预期 diff。
```

确认规划合理后，再执行：

```text
/goal 按 docs/CODEX_GOAL_MODE_OPTIMIZATION_GUIDE.md 持续优化拾刻项目：每轮选择一个最高优先级目标，小步修改、运行验证、更新测试和文档；不得破坏“截图/拍照/分享文本 -> 解析 -> 用户确认 -> 行动编排 -> 收件箱/今日行动台追踪”主链路；敏感动作必须用户确认；不引入真实个人数据；连续三轮验证无进展或遇到外部凭据/设备阻塞时暂停并生成 blocking-report.md。
```

### 3.2 每轮工作循环

Codex 每一轮都必须按下面顺序工作：

1. 读取本文件、`README.md`、`docs/product-spec.md`、`docs/android-mvp-implementation.md`、`docs/device-runbook.md`、`materials/device-demo-checklist.md`。
2. 找出当前最高优先级的一个小目标，不要同时大改多个系统。
3. 写出本轮计划：改哪些文件、为什么改、如何验证。
4. 进行小步修改。
5. 运行可用验证命令。
6. 修复失败；如果失败无法修复，保留最小可回滚 diff 并写清阻塞原因。
7. 更新或新增对应测试、验证脚本、文档。
8. 输出本轮总结：完成项、未完成项、验证结果、下一轮建议。

### 3.3 停止条件

Codex 需要在以下情况暂停，而不是无限循环：

- 所有 P0 和 P1 验收通过，且 P2 有清晰 backlog。
- 连续三轮运行同一类验证仍失败，且没有新的改进证据。
- 需要真实设备、外部账号、模型 API key、比赛官方 SDK 或人工产品决策。
- 发现当前目标会破坏主链路、隐私约束或用户确认原则。

暂停时生成：

```text
docs/blocking-report.md
```

内容包括：阻塞点、已尝试方案、失败日志、建议人工动作、恢复命令。

---

## 4. 不可破坏的产品原则

这些原则是 Codex 优化时的硬约束。

### 4.1 用户确认优先

日历、提醒、地图、分享、任何系统写入动作，都必须在用户确认字段之后执行。未确认字段时只能进入待确认状态，不得自动写入系统。

### 4.2 AI 只建议，规则层负责执行

模型负责场景判断、字段抽取、置信度、缺失项和行动建议；规则层负责时间校验、权限判断、状态机和系统动作执行。

### 4.3 保留降级路径

后端不可用、模型低置信度、权限拒绝、地图不可用、日历不可用、OCR 失败，都必须能降级为本地行动卡或人工确认，而不是静默失败。

### 4.4 不碰真实隐私数据

演示、测试、样例、日志均使用合成数据。不得提交姓名、手机号、学号、群聊真实内容、真实相册图片、真实局域网敏感地址。

### 4.5 不假装拥有未验证能力

不要把未接入的 vivo 官方 API、系统级截图监听、通知监听、桌面组件、真实云模型能力写成已实现。可以写为 Roadmap 或 Feature Flag。

---

## 5. 优先级路线图

### P0：先稳住工程地基

目标：让项目可构建、可测试、可回归，不因后续优化变成不可控大杂烩。

#### P0.1 建立仓库基线与验证入口

Codex 任务：

- 扫描真实仓库结构。
- 确认 Android、backend、contracts、validation、docs 的实际路径。
- 新增或更新 `docs/optimization-log.md`，记录每轮变更。
- 确认所有现有验证命令能运行；不能运行的命令写入 `docs/current-validation-status.md`。

验收：

```bash
python3 shike/validation/validate_real_world_ready.py || true
python3 shike/validation/validate_demo_acceptance.py || true
python3 shike/backend/verify_backend.py || true
python3 shike/spike/run_spike.py --all || true
```

输出：

- `docs/current-validation-status.md`
- `docs/optimization-log.md`

#### P0.2 拆分 Android 单文件结构

当前 `MainActivity.kt` 承担了 UI、状态、网络、持久化、系统动作和样例数据。先不要重写 UI，先进行低风险抽离。

建议结构：

```text
android-mvp/app/src/main/java/cn/shike/app/
  MainActivity.kt
  core/
    ResultState.kt
    TimeProvider.kt
  domain/
    ShikeItem.kt
    ShikeStatus.kt
    ActionType.kt
    ActionPlan.kt
  data/
    LocalInboxStore.kt
    BackendConfigStore.kt
    MockModelAdapter.kt
    ModelApiClient.kt
  system/
    CalendarExecutor.kt
    ReminderExecutor.kt
    MapExecutor.kt
  ui/
    ShikeApp.kt
    components/
    screens/
```

Codex 任务：

- 先抽离 data class、常量、样例数据。
- 再抽离后端请求和 JSON 映射。
- 再抽离 SharedPreferences 存储。
- 最后抽离系统动作执行器。
- 每次抽离后保持 UI 行为不变。

验收：

- App 仍可打开今日行动台。
- 选择截图、拍照导入、后端解析课程/活动、确认修正、日历、提醒、地图按钮仍存在。
- 不改变用户确认前不可执行动作的逻辑。

#### P0.3 引入基础测试

Codex 任务：

- 为 `normalizeBackendUrl`、JSON 映射、actions 映射、sceneHint、状态转换写单元测试。
- 后端保留 `/health`、`/v1/schema`、`/v1/analyze` smoke test。
- 为模型输出契约增加 schema 校验测试。

验收：

```bash
python3 shike/backend/verify_backend.py
python3 shike/validation/validate_real_world_ready.py
```

如 Android Gradle 环境可用，再补充：

```bash
./gradlew test
```

---

### P1：把“演示壳”变成“真实收件箱应用”

目标：让数据、状态、列表和用户操作能长期存在，而不是只有当前卡片快照。

#### P1.1 Room/SQLite 收件箱

Codex 任务：

- 设计 `InboxItemEntity`、`ActionEntity`、`ExecutionResultEntity`。
- 字段至少包括：id、title、scene、time_text、normalized_start、deadline、location、status、confidence、missing_fields、raw_text、source_type、created_at、updated_at、confirmed_at、executed_at。
- SharedPreferences 只保留后端地址、端云设置等轻配置；行动卡迁移到 Room。
- 保留从旧 SharedPreferences 快照恢复一次的迁移逻辑。

验收：

- 重启后不是只恢复当前卡片，而是恢复收件箱列表。
- 待确认、已安排、即将截止、已完成、已忽略状态可筛选。
- 至少保留 10 条本地样例/历史记录。

#### P1.2 明确状态机

状态定义：

```text
captured
analyzing
pending_confirmation
needs_manual_review
ready_to_execute
permission_blocked
fallback_ready
executing
scheduled
due_soon
completed
ignored
execution_failed
```

Codex 任务：

- 建立 `StateTransition` 或 `InboxStateMachine`。
- 禁止非法状态跳转，例如 `captured -> scheduled`。
- 所有 UI 按状态显示按钮，而不是散落判断。

验收：

- 未确认卡片不能执行系统动作。
- 忽略卡片不会继续触发提醒/地图/日历。
- 后端失败进入 fallback_ready 或 pending_confirmation，不静默丢失。

#### P1.3 收件箱真实列表与详情页

Codex 任务：

- 从单页长页面拆成：今日行动台、导入页、解析确认页、行动编排页、收件箱页、设置页。
- 收件箱支持筛选：待确认、已安排、即将截止、已完成、已忽略。
- 卡片详情支持再次编辑、再次执行、归档、忽略。

验收：

- 演示路线仍能 3 分钟跑通。
- 新增真实列表后，旧的交付物自检中心可以移到设置或调试页，不影响主流程。

---

### P2：真实采集与解析能力

目标：把“样例 OCR 草稿”推进为可用的真实图片文字识别与模型解析管线。

#### P2.1 OCR 管线

Codex 任务：

- 接入可运行的 OCR 方案。优先考虑端侧 OCR；如果仓库没有依赖条件，则先做接口抽象：`OcrEngine`。
- 对相册 URI 和相机 Bitmap 做统一输入：`CaptureDraft`。
- OCR 失败时显示原因：图片过暗、无文字、权限失败、引擎不可用。
- OCR 原文进入确认页，不自动执行。

验收：

- 相册图片不再只填固定 mock 文本。
- OCR 失败仍可手动输入文本继续解析。
- 验证脚本覆盖空 OCR、过短 OCR、含时间地点文本。

#### P2.2 模型适配器升级

Codex 任务：

- 后端从规则 mock 改成 `ModelAdapter` 接口。
- 保留 `MockModelAdapter` 作为离线兜底。
- 新增 `OpenAICompatibleAdapter` 或 `BlueLMAdapter` 时必须通过环境变量读取 key，不得写死密钥。
- 所有模型输出必须按 `model-output.schema.json` 校验，不合格进入人工确认。
- 为 course_notice、event_poster、unknown 至少各准备 5 条回归样例。

验收：

```bash
python3 shike/backend/verify_backend.py
python3 shike/validation/validate_model_bridge.py
```

#### P2.3 时间地点规范化

Codex 任务：

- 增加 `TimeNormalizer`：处理“今天”“今晚”“明天”“本周五”“4月24日”“报名截止今晚22:00”。
- 增加时区参数，默认 `Asia/Shanghai`，但不写死在业务逻辑里。
- 地点增加 `map_query`、building_hint、confidence。
- 相对时间必须在确认页提示。

验收：

- 相对时间不会被静默转换。
- 缺失年份、缺失地点、多个时间冲突时进入 `needs_manual_review`。

---

### P3：行动执行从“按钮能打开”变成“可靠安排”

目标：动作执行可追踪、可失败、可回退。

#### P3.1 日历动作

Codex 任务：

- 保留 `Intent.ACTION_INSERT` 的用户确认方式。
- 记录用户是否成功返回、是否取消、是否失败。
- 如果后续使用 Calendar Provider，必须重新请求权限并让用户选择日历。

验收：

- 日历应用不可用时，卡片进入 fallback_ready，并保留手动复制内容。

#### P3.2 定时提醒

当前本地通知偏即时提醒。后续应实现真正的提醒计划。

Codex 任务：

- 设计 `ReminderScheduler`。
- 先用 WorkManager 或 AlarmManager 做定时提醒，根据 Android 版本处理限制。
- Android 13+ 申请通知权限；拒绝时保留本地行动卡。
- 提醒触发后记录执行结果。

验收：

- 可以创建“课前 30 分钟提醒”“截止前 2 小时提醒”。
- 权限拒绝不崩溃，不丢卡片。

#### P3.3 地图动作

Codex 任务：

- 保留 `geo:` deeplink。
- 增加“复制地点”和“稍后打开”降级。
- map_query 与 raw location 分离。

验收：

- 无地图 App 时不会崩溃。
- 地点缺失时不能打开地图，只能进入人工确认。

---

### P4：用户体验与真实产品感

目标：减少“评审演示页”痕迹，增强日常使用体验。

Codex 任务：

- 首页只保留今日待办、即将截止、最近待确认。
- 导入流程变成明确的步骤：采集 -> OCR -> 解析 -> 确认 -> 编排。
- 增加空状态、错误状态、加载状态。
- 增加低置信度视觉提示。
- 增加卡片详情页。
- 把“交付物自检中心”“3 分钟演示路线”移动到 debug 或 about 页面。

验收：

- 非评审用户打开也能理解怎么使用。
- 课程通知和活动海报两条路线仍可录屏复测。

---

### P5：隐私、安全、端云设置

目标：让“端侧优先、云侧增强、用户可控”从文案变成工程行为。

Codex 任务：

- 增加隐私设置页：是否允许云侧解析、是否保存 OCR 原文、是否保存图片、是否允许匿名错误日志。
- 默认不上传真实图片；只上传用户确认的 OCR 文本或脱敏文本。
- 日志中自动隐藏手机号、学号、邮箱、URL token。
- 后端地址只允许用户手动配置，不在日志中泄漏局域网敏感信息。
- 网络请求增加超时、错误码、重试限制。

验收：

- 关闭云侧增强后，后端解析按钮不可用或提示原因。
- 导出日志不包含真实敏感字段。

---

### P6：工程质量与发布准备

目标：让团队可以长期维护、复测、发布。

Codex 任务：

- 增加 CI：后端测试、schema 校验、Android 单元测试、lint。
- 增加 changelog。
- 增加 crash/error 日志，但不得泄漏隐私。
- 增加 release/debug 构建区分。
- 增加签名、版本号、APK SHA-256 记录。
- 增加测试数据生成器。

验收：

```bash
python3 shike/validation/validate_real_world_ready.py
python3 shike/validation/validate_demo_acceptance.py
python3 shike/backend/verify_backend.py
python3 shike/spike/run_spike.py --all
./gradlew test
```

如果没有 Android Gradle 环境，Codex 必须写明缺失原因，并保留后端与文档验证。

---

## 6. Codex 分阶段 Goal 模板

不要一次让 Codex 做完整项目。可以按下面顺序逐个 Goal 运行。

### Goal A：工程基线与验证盘点

```text
/goal 先只做工程基线盘点：阅读 docs/CODEX_GOAL_MODE_OPTIMIZATION_GUIDE.md 和现有 README/docs/validation，运行可用验证命令，生成 docs/current-validation-status.md 与 docs/optimization-log.md。不要重构代码。完成条件：列出当前能跑/不能跑的命令、失败原因、下一步最高优先级，并保证没有功能代码 diff。
```

### Goal B：MainActivity 低风险拆分

```text
/goal 在不改变 UI 行为和演示链路的前提下，把 MainActivity.kt 中的数据模型、样例数据、后端请求、SharedPreferences 存储、系统动作执行逐步抽离到 domain/data/system 包。每次只做一个抽离点，保持可构建，更新测试或验证说明。完成条件：MainActivity 只负责 Activity 启动和组合顶层 UI，截图/拍照/后端解析/确认/日历/提醒/地图行为不回退。
```

### Goal C：收件箱持久化升级

```text
/goal 把当前 SharedPreferences 当前卡片快照升级为 Room/SQLite 收件箱。保留后端地址等轻配置在 SharedPreferences。实现 InboxItem、Action、ExecutionResult 的本地持久化、状态筛选和重启恢复。完成条件：至少 10 条历史行动卡可持久化，待确认/已安排/即将截止/已完成/已忽略可筛选，用户确认前不可执行系统动作。
```

### Goal D：模型契约与后端适配器

```text
/goal 强化 backend 模型编排：保留 MockModelAdapter，新增 ModelAdapter 抽象，所有 /v1/analyze 输出必须通过 model-output.schema.json 校验；新增 course_notice/event_poster/unknown 回归样例和 verify_backend 测试。完成条件：后端 smoke、schema 校验、模型桥接验证全部通过；无 API key 写死；服务不可用时 Android 仍能回退本地 mock。
```

### Goal E：真实提醒与动作执行结果

```text
/goal 将行动执行从“按钮触发”升级为可追踪执行结果：实现 ReminderScheduler 的定时提醒计划，Calendar/Map/Reminder 都记录 ExecutionResult；权限拒绝、App 不存在、字段缺失都进入 fallback_ready。完成条件：课前提醒和截止提醒可创建或降级，收件箱能显示执行结果，未确认卡片不能执行。
```

### Goal F：真实 OCR 管线

```text
/goal 为相册和拍照输入实现可替换 OCR 管线：定义 OcrEngine、CaptureDraft、OcrResult；如果无法接入真实端侧 OCR，则先完成接口、mock、失败状态和手动输入兜底。完成条件：相册/相机不再只依赖固定文案，OCR 失败可手动继续，验证覆盖空文本、短文本、课程通知、活动海报。
```

### Goal G：隐私与端云设置落地

```text
/goal 将“端侧优先、云侧增强、用户可控”落成工程行为：新增设置状态、云侧解析开关、日志脱敏、敏感字段保护、后端地址安全显示。完成条件：关闭云侧增强后不会请求后端；日志不包含手机号/学号/邮箱/真实局域网敏感地址；用户确认原则不回退。
```

---

## 7. 每轮 Codex 必须维护的文件

建议 Codex 每轮至少维护以下文件之一：

```text
docs/optimization-log.md
docs/current-validation-status.md
docs/blocking-report.md
backend/verify_backend.py
validation/*.py
android-mvp/app/src/test/**
android-mvp/app/src/androidTest/**
```

`docs/optimization-log.md` 推荐格式：

```markdown
# Optimization Log

## 2026-05-23 / Round 001

Goal: MainActivity data model extraction
Files changed:
- ...
Validation:
- PASS python3 shike/backend/verify_backend.py
- FAIL ./gradlew test: Gradle wrapper missing
Behavior preserved:
- gallery import
- camera import
- backend fallback
- confirm before execute
Next:
- extract ModelApiClient
```

---

## 8. 验证矩阵

| 方向 | 最低验收 | 强化验收 |
|---|---|---|
| Android 构建 | `bash shike/android-mvp/build_apk.sh` | `./gradlew test`, `./gradlew connectedCheck` |
| 后端 | `python3 shike/backend/verify_backend.py` | schema 校验 + 多样例回归 |
| 主链路 | 课程截图、活动拍照、后端回退、重启恢复 | 真机录屏六段证据 |
| 模型 | course/event/unknown 三类输出 | 低置信度、缺失字段、冲突时间回归 |
| 存储 | 重启恢复当前卡片 | Room 收件箱历史、状态筛选、执行结果 |
| 权限 | 相机、通知、地图、日历失败不崩溃 | 权限拒绝自动进入 fallback_ready |
| 隐私 | 不提交真实样例 | 日志脱敏、云侧开关、数据清除 |
| UX | 演示路线可跑通 | 非评审用户也能自然使用 |

---

## 9. 禁止 Codex 做的事

- 不要一次性重写整个项目。
- 不要删除现有演示链路。
- 不要跳过用户确认直接执行日历、提醒、地图。
- 不要把 mock 数据伪装成真实模型结果。
- 不要写死 API key、手机号、学号、真实群聊内容。
- 不要引入无法解释来源的重型依赖。
- 不要把所有错误都吞掉；失败必须有用户提示和日志。
- 不要为了让验证脚本通过而删除真实检查项。
- 不要声明未验证的 vivo 官方 API 已经接入。

---

## 10. 最终完成标准

当项目达到下面标准时，才可以认为从“演示 MVP”接近“功能完善软件”的第一阶段：

1. 用户可以从相册、相机、分享文本创建行动卡。
2. OCR 或文本草稿可以进入模型解析。
3. 模型输出有 schema 校验、置信度、缺失字段和解释。
4. 用户可以编辑标题、时间、地点、状态。
5. 未确认卡片不能执行系统动作。
6. 确认后可以创建日历、定时提醒、地图入口，失败可降级。
7. 收件箱可以持久化多条卡片并按状态筛选。
8. 今日行动台能按时间、截止、地点展示优先级。
9. 后端不可用时仍能离线演示核心链路。
10. 真机重启后数据恢复。
11. 单元测试、后端 smoke、验证脚本能跑。
12. 隐私设置和日志脱敏可用。
13. 所有演示数据均为合成数据。
14. 文档、Runbook、验收清单和优化日志保持同步。
15. 新功能都有回归验证，不靠口头说明。

---

## 11. 推荐第一轮任务

我建议第一轮不要直接加新功能，而是让 Codex 做“工程基线盘点 + 优化日志”。原因是：当前项目已经有 APK、后端、验证脚本和演示文档，但真实仓库环境、Gradle 可用性、验证命令通过情况需要先确认。

第一轮推荐使用：

```text
/goal 先只做工程基线盘点：阅读 docs/CODEX_GOAL_MODE_OPTIMIZATION_GUIDE.md 和现有 README/docs/validation，运行可用验证命令，生成 docs/current-validation-status.md 与 docs/optimization-log.md。不要重构代码。完成条件：列出当前能跑/不能跑的命令、失败原因、下一步最高优先级，并保证没有功能代码 diff。
```

第二轮再使用：

```text
/goal 在不改变 UI 行为和演示链路的前提下，把 MainActivity.kt 中的数据模型、样例数据、后端请求、SharedPreferences 存储、系统动作执行逐步抽离到 domain/data/system 包。每次只做一个抽离点，保持可构建，更新测试或验证说明。完成条件：MainActivity 只负责 Activity 启动和组合顶层 UI，截图/拍照/后端解析/确认/日历/提醒/地图行为不回退。
```

这样做最稳：先知道项目真实状态，再开始结构化优化。
