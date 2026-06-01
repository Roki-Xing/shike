# 拾刻：手机碎片信息行动助手

本目录承接 `plan/2026-04-24_11-37-49-aigc-shike.md` 与
`issues/2026-04-24_11-41-14-aigc-shike.csv` 的全部落地交付物。

## 项目边界

拾刻面向 vivo AIGC 创新赛应用赛道，主形态定义为安卓 APP。首期只做一个明确闭环：

```text
截图/拍照 -> AI 解析 -> 用户确认 -> 行动编排 -> 收件箱/今日行动台追踪
```

MVP 锁定为：

- 入口：截图导入、相机拍照
- 场景：课程通知、活动海报
- 动作：日历、提醒、地图
- 持续层：收件箱与今日行动台

## 目录结构

| 路径 | 用途 |
|---|---|
| `docs/` | 产品规格、交付边界、MVP 范围、降级路线 |
| `prototype/` | 初赛高保真原型说明、页面脚本、可视化 HTML 原型 |
| `contracts/` | 模型适配器接口、JSON Schema、样例请求响应 |
| `spike/` | 技术可行性 Spike、可复现命令、样例输入、日志 |
| `materials/` | 初赛 PPT 大纲、海报文案、演示脚本、录屏分镜 |
| `validation/` | 回归样例集、验收脚本、需求追踪矩阵 |

## 机械验收

```bash
python3 shike/validation/validate_android_structure.py
python3 shike/validation/validate_android_unit_tests.py
python3 shike/validation/validate_frontend_polish.py
python3 shike/validation/validate_inbox_workbench_landing.py
python3 shike/validation/validate_real_world_ready.py
python3 shike/validation/validate_demo_acceptance.py
python3 shike/validation/validate_cloud_device_package.py
python3 shike/validation/validate_release_blocking_report.py
python3 shike/validation/validate_release_evidence_index.py
python3 shike/validation/validate_requirement_matrix.py
python3 shike/validation/validate_landing_release_candidate.py
python3 shike/validation/validate_deliverables.py
python3 shike/validation/validate_landable.py
python3 shike/validation/validate_action_execution.py
python3 shike/validation/validate_today_ranking.py
python3 shike/validation/validate_advanced_product_beta.py
python3 shike/validation/validate_model_eval_cases.py
python3 shike/spike/run_spike.py --all
python3 shike/scripts/verify_core20_package.py "/path/to/拾刻_核心20文件交付包_20260505"
```

Android 源码结构守卫使用 `validate_android_structure.py`，通过标准是 `ANDROID_STRUCTURE_METRIC 31/31`，会检查 Android 源码边界、文件大小、回调名和 helper ownership，防止后续迭代把已拆分的职责重新压回单个大文件。Android 本地单元测试基线使用 `validate_android_unit_tests.py`，通过标准是 `ANDROID_UNIT_TEST_METRIC 64/64`，会检查 JUnit 依赖、`PrivacyRedactionTest`、`CaptureImportMapperTest`、`ShareImportMapperTest`、`OcrEngineTest`、`InitialSelectionMapperTest`、`ExecutionResultActionsTest`、`ExecutionResultStateTest`、`ReminderPermissionFallbackTest`、`ReviewStatusMapperTest`、`ReviewActionsTest`、`CaptureResultActionsTest`、`ModelExplanationTest`、`ModelApiClientTest`（后端 URL 归一化和 `share_text`/`manual` 请求来源）、`TodayActionItemMapperTest`、`ExecutionActionGateTest`、`InboxWorkbenchTest` 归档/恢复决策状态和全部筛选优先排序、`ReminderPayloadTest`、`BackendAnalysisRunnerTest` 当前草稿来源映射和后端失败回退脱敏文案、`BackendEndpointActionsTest`、`BackendTriggerActionsTest`、`BackendOutcomeActionsTest` 后端 outcome source/status 脱敏兜底、`SampleActionsTest`、`InboxEntitiesTest`、`LocalInboxStoreTest` 本地动作列表持久化 codec、采集来源脱敏与 raw OCR 脱敏、`LocalPersistenceBoundaryTest`、`LocalDataClearActionsTest`、`CloudEnhancementActionsTest`、最近一次 `gradle --no-daemon :app:testDebugUnitTest` XML 结果和文档入口。前端产品化守卫使用 `validate_frontend_polish.py`，通过标准是 `FRONTEND_POLISH_METRIC 12/12`，会检查首页不常驻后端地址、样例按钮、交付物自检和演示路线，Debug 页集中承接工程入口，并要求 design tokens 与 loading/empty/error 状态组件存在。收件箱长期化守卫使用 `validate_inbox_workbench_landing.py`，通过标准是 `INBOX_WORKBENCH_LANDING_METRIC 12/12`，会检查 SQLite 收件箱实体、50 条合成记录能力、旧快照迁移、多状态筛选、搜索、归档/恢复入口和状态文档同步。后端来源契约守卫使用 `validate_backend_source_type_contract.py`，通过标准是 `BACKEND_SOURCE_TYPE_CONTRACT_METRIC 9/9`，会检查 `/v1/analyze` 支持 `screenshot`、`camera`、`share_text`、`manual`，并锁定 Android、样例请求和文档的一致性。执行层守卫使用 `validate_action_execution.py`，通过标准是 `ACTION_EXECUTION_METRIC 17/17`，会检查确认后执行、日历口径、定时提醒、Android 12+ exact-alarm 能力检查与普通定时降级、提醒记录持久化、`restoreScheduledReminder` 应用启动恢复、设备重启恢复、触发后清理、一键清除本地数据时取消待触发提醒、地图降级和权限拒绝保留行动卡。可落地总体验收使用 `validate_real_world_ready.py`，会串联 Android 真机入口、OCR 输入、模型桥接、本地恢复、手动确认、执行层守卫、Android 本地单元测试、后端 smoke、交付物覆盖和 Spike。发布候选总门禁使用 `validate_landing_release_candidate.py`，默认通过标准是 `LANDING_RELEASE_CANDIDATE_METRIC 52/52`，会整合 BlueLM、密钥安全、云真机包、strict blocking report、release evidence index、前端、OCR、执行闭环、收件箱、隐私和材料证据；`--strict` 仅在真实 BlueLM 在线日志和云真机录屏齐备后使用，缺外部证据时生成 blocking report。真机演示验收使用 `validate_demo_acceptance.py`，通过标准是 `DEMO_ACCEPTANCE_METRIC 18/18`，对应 `materials/device-demo-checklist.md` 的录屏证据、复测清单和云真机 strict 证据包交接。云真机证据包建议放在 `materials/evidence/cloud-device/`，默认结构检查使用 `validate_cloud_device_package.py`，收齐实际录屏后再用 `--strict` 补做最终核验。`validate_release_blocking_report.py` 会检查 strict 阻断报告是否列出缺失视频、待填报告字段、复跑命令和脱敏警告；`validate_release_evidence_index.py` 通过标准是 `RELEASE_EVIDENCE_INDEX_METRIC 10/10`，会检查发布证据索引是否覆盖本地门禁、模型证据、BlueLM 脱敏证据、strict 阻断项、APK hash、依赖安全重跑命令、`docs/optimization-log.md` 当前交接摘要、README 公开入口、`validation/traceability.md` SHIKE-070 交付追踪和脱敏规则。`validate_deliverables.py` 检查 10 个 SHIKE issue 的交付物覆盖情况；`run_spike.py --all` 验证解析、动作编排、状态存储和降级逻辑。

云真机证据包当前非 strict 通过标准是 `CLOUD_DEVICE_PACKAGE_METRIC 27/27`，会核对 `materials/evidence/cloud-device/` 目录、录屏文件名清单、报告字段、APK hash、脱敏日志、`docs/device-runbook.md` release handoff 步骤、`materials/evidence/release-evidence-index.md`、`materials/evidence/blocking-report.md`、生成脚本不回退 release handoff、默认发布门禁 `LANDING_RELEASE_CANDIDATE_METRIC 52/52` 和 strict 外部证据阻断状态 `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7`。录制云真机前先运行 `prepare_cloud_device_evidence.py`，当前准备门禁为 `CLOUD_DEVICE_PREP_METRIC 5/5`，未收齐真实录屏前 `CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9` 是预期状态；同时在 `cloud-device-test-report.md` 的 `Pre-recording Evidence Gate` 中确认 `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md` 仍是桌面指导源，`materials/evidence/requirement-matrix.md` 仍通过 `REQUIREMENT_MATRIX_METRIC 9/9`，all 9 real cloud-device MP4 files 均已采集，且 no placeholder fields remain after capture。收齐真实云真机录屏和已填报告后，再执行 `validate_cloud_device_package.py --strict` 与 `validate_landing_release_candidate.py --strict` 做最终核验。

桌面指导文档逐项追踪使用 `validate_requirement_matrix.py`，通过标准是 `REQUIREMENT_MATRIX_METRIC 9/9`，会检查 `materials/evidence/requirement-matrix.md` 是否把阶段 A-E 映射到本地证据、验证命令、strict 云真机阻断项，并确认公开状态页锚定桌面 `1. 当前仓库总体判断.md`。

Today Action 排序基线使用 `validate_today_ranking.py`，通过标准是 `TODAY_RANKING_METRIC 7/7`，覆盖 10 条合成样例和截止时间、开始时间、待确认、低置信度、缺失地点、已完成、已忽略等排序规则。

Product Beta 基线使用 `validate_advanced_product_beta.py`，默认输出当前 30 项产品级 readiness 分数和每个未通过项的下一步建议；需要作为严格发布门禁时可加 `--strict`，满分时返回零状态。当前基线是 `PRODUCT_BETA_METRIC 30/30`，说明项目已经有确认页可编辑、低置信度人工确认提示、缺时间禁用日历、缺地点禁用地图、用户确认后的真实定时提醒调度、通知权限拒绝时保留行动卡、地图不可用时复制地点并保留行动卡、关闭云侧增强时不请求后端、日志脱敏、一键清除本地数据、110-case 模型评测集、模型解释详情、ExecutionResult 执行结果、日历已打开系统新增页口径、收件箱归档/恢复、相册/相机/分享文本统一 CaptureDraft、手动输入继续解析、OCR 失败手动继续、今日排序验证、首页当前行动卡数据驱动、今日空状态、今日错误状态、收件箱五状态筛选、收件箱搜索、OCR 原文详情、相对时间提示、后端 schema 路径和持续优化日志。

模型评测样例使用 `validate_model_eval_cases.py`，通过标准是 `MODEL_EVAL_CASES_METRIC 8/8`，会检查 `validation/regression-cases.json` 至少 110 条、ID 唯一、课程/活动/会议/作业/面试/出行票务/低质量/反例覆盖、核心场景分布、字段结构和动作集合。后端场景契约守卫使用 `validate_backend_scene_contract.py`，通过标准是 `BACKEND_SCENE_CONTRACT_METRIC 11/11`，会确保公开输出契约保持保守：`scene_type` 仅允许 `course_notice`、`event_poster`、`unknown`，`task.topic` 仅允许 `course`、`event`、`unknown`；会议/作业/面试/出行等扩展回归样例可作为输入 `scene_hint` 与评测分组存在，但在不扩展 schema 的前提下输出应映射到 `unknown`。

核心 20 文件提交包可用 `scripts/verify_core20_package.py` 核对，脚本会检查文件数、必需文件、APK SHA-256、结构守卫引用、执行层守卫引用和单元测试守卫引用，避免多交计划文件、漏交核心文件或丢掉关键验收入口。

## 真机落地

可直接打开 `prototype/demo.html` 作为一页式 Demo 控制台，里面包含手机首页预览、3 分钟演示路线、验收指标和核心包核对命令；完整多页面原型仍保留在 `prototype/index.html`。

Android MVP 已包含系统相册截图选择、相机拍照预览、`SharedPreferences` 收件箱缓存、日历插入 Intent、`AlarmManager` 本地定时提醒、本地通知、地图 deeplink 和系统文本分享入口。提醒调度会优先使用 `setExactAndAllowWhileIdle`，Android 12+ 无 exact-alarm 能力或精确调度被拒绝时降级为普通 `AlarmManager.set`，并在结果文案里标明调度模式。已调度提醒会持久化到应用私有偏好，应用启动时通过 `restoreScheduledReminder` 恢复未过期待触发提醒，设备重启后由 `BootReminderReceiver` 重新恢复，提醒触发后清理对应记录；用户执行一键清除本地数据时会调用 `cancelScheduledReminder` 取消系统待触发提醒并清除本地记录。设备联调步骤见 `docs/device-runbook.md`，可覆盖应用重启后的当前行动卡恢复。

模型编排联调已接入 Android 侧“解析当前草稿/活动样例解析”按钮：模拟器默认请求 `http://10.0.2.2:8000/v1/analyze`，真机可在“后端地址”输入局域网地址并点“保存后端地址”；请求会把可编辑的“OCR 文本草稿”作为 `ocr_text` 提交，并按当前入口发送 `screenshot`、`camera`、`share_text` 或 `manual`。服务不可用时回退本地 MockModelAdapter。演示数据均为合成样例；上传前应删除姓名、手机号、学号、群聊内容等个人信息。离线演示不依赖在线模型：`MockModelAdapter` 对课程通知与活动海报输出稳定结构；对会议/作业/面试/出行等扩展语义在不扩展公开 schema 的前提下输出 `scene_type=unknown`，但仍会给出可执行动作建议（提醒/日历/地图的合理子集）与缺失字段标注。后端 FastAPI 提供 `/health`、`/v1/schema` 和 `/v1/analyze` 便于后续替换 BlueLM 或 OpenAI compatible 模型。

确认页支持手动修正标题、时间、地点和状态；用户点“确认修正”后才会启用日历、提醒和地图动作，不可信内容可标为“已忽略”。

复赛录屏和复测交接见 `materials/device-demo-checklist.md`，其中定义了安装打开、课程截图、活动拍照、后端失败回退、重启恢复、交付物自检六段证据文件；需要展示扩展场景时可追加作业/会议、面试/出行两段补录。
