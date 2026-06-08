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
python3 shike/validation/validate_cloud_backend_ready.py
python3 shike/validation/validate_backend_audit_log.py
python3 shike/validation/validate_apk_secret_hygiene.py
python3 shike/validation/validate_android_image_preprocess.py
python3 shike/validation/validate_android16_definition_of_done.py
python3 shike/validation/validate_cloud_device_package.py
python3 shike/validation/validate_release_blocking_report.py
python3 shike/validation/validate_release_evidence_index.py
python3 shike/validation/validate_user_research_evidence.py
python3 shike/validation/validate_requirement_matrix.py
python3 shike/validation/validate_vivo_ocr_adapter.py
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

Android 源码结构守卫使用 `validate_android_structure.py`，通过标准是 `ANDROID_STRUCTURE_METRIC 31/31`，会检查 Android 源码边界、文件大小、回调名和 helper ownership，防止后续迭代把已拆分的职责重新压回单个大文件。Android 本地单元测试基线使用 `validate_android_unit_tests.py`，通过标准是 `ANDROID_UNIT_TEST_METRIC 86/86`，会检查 JUnit 依赖、`PrivacyRedactionTest`、`CaptureImportMapperTest`、`ShareImportMapperTest`、`OcrEngineTest`、`InitialSelectionMapperTest`、`ExecutionResultActionsTest`、`ExecutionResultStateTest`、`ReminderPermissionFallbackTest`、`ReviewStatusMapperTest`、`ReviewActionsTest`、`CaptureResultActionsTest`、`ModelExplanationTest`、`ModelApiClientTest`（后端 URL 归一化和 `share_text`/`manual` 请求来源）、`TodayActionItemMapperTest`、`ExecutionActionGateTest`、`InboxWorkbenchTest` 归档/恢复决策状态和全部筛选优先排序、`ReminderPayloadTest`、`BackendAnalysisRunnerTest` 当前草稿来源映射和后端失败回退脱敏文案、`BackendEndpointActionsTest`、`BackendTriggerActionsTest`、`BackendOutcomeActionsTest` 后端 outcome source/status 脱敏兜底、`SampleActionsTest`、`InboxEntitiesTest`、`LocalInboxStoreTest` 本地动作列表持久化 codec、采集来源脱敏与 raw OCR 脱敏、`LocalPersistenceBoundaryTest`、`LocalDataClearActionsTest` 清除拾刻缓存 App 内二次确认、`CloudEnhancementActionsTest`、`DeveloperModeUnlockTest` 设置页版本号 5 连击解锁 Debug、`LocalMultimodalStatusTest` 端侧 3B 未安装/可用/初始化失败边界、`LocalMultimodalRuntimeTest` 端侧 3B `init -> callVit -> generate -> schema_valid -> 待确认` runtime 合同、`ImagePreprocessPolicyTest` 图片长边限制/EXIF 尺寸/输入 MIME 魔数识别、输出 MIME、SHA-256 与截图 UI chrome 裁剪合同、`ImageThumbnailCacheTest` 私有缩略图缓存合同、`ScreenshotCandidateStoreTest` 最近截图助手开关持久化/清除缓存复位合同、`DateStripTest` 首页系统日期只作排序提示的文案合同、`SystemActionsTest` 系统日历新增页文案合同、`ScreenCapturePromptTest` 页内截图提示边界文案合同、最近一次 `gradle --no-daemon :app:testDebugUnitTest` XML 结果和文档入口。Android 图片预处理守卫使用 `validate_android_image_preprocess.py`，通过标准是 `ANDROID_IMAGE_PREPROCESS_METRIC 15/15`，会检查 `ImagePayloadPreprocessor` 对图片先按 JPEG/PNG/WebP 魔数识别 MIME 并拒绝非图片字节、读取 bounds、按 1600 长边采样、EXIF 旋转归一化、截图分享/最近截图助手 source-aware UI chrome 裁剪、JPEG 82 压缩、`ImageThumbnailCache` 私有缩略图缓存、Base64 NO_WRAP data URL、SHA-256 计算，以及 `MainActivity` 只委托预处理器而不再手写 `BitmapFactory`/`Base64`/`MessageDigest`。前端产品化守卫使用 `validate_frontend_polish.py`，通过标准是 `FRONTEND_POLISH_METRIC 12/12`。收件箱长期化守卫使用 `validate_inbox_workbench_landing.py`，通过标准是 `INBOX_WORKBENCH_LANDING_METRIC 12/12`，会检查 SQLite 历史收件箱、50 条合成种子、状态筛选、搜索、归档/恢复入口和状态文档同步。后端来源契约守卫使用 `validate_backend_source_type_contract.py`，通过标准是 `BACKEND_SOURCE_TYPE_CONTRACT_METRIC 9/9`。vivo OCR 导入 API 守卫使用 `validate_vivo_ocr_adapter.py`，通过标准是 `VIVO_OCR_ADAPTER_METRIC 11/11`，会检查 `/v1/ocr`、`/ocr/general_recognition`、`businessid=aigc + AppID`、Bearer AppKey、表单 body、缺凭据降级和 Android 不持有 OCR/BlueLM 密钥。HTTPS 后端部署守卫使用 `validate_cloud_backend_ready.py`，通过标准是 `CLOUD_BACKEND_READY_METRIC 9/9`，会检查 `docs/server-deployment-runbook.md` 对 `https://roky.chat`、`https://api.roky.chat`、`/etc/shike/shike-backend.env`、`/opt/shike/backend`、systemd、Nginx、certbot、公网 smoke 和脱敏日志边界的覆盖。后端审计日志守卫使用 `validate_backend_audit_log.py`，通过标准是 `BACKEND_AUDIT_LOG_METRIC 8/8`，会检查 `/v2/analyze-image` 只记录 provider、source type、SHA-256 前缀、OCR block 数量、key-present、耗时、状态和 `input_id_hash` 等元数据，不记录用户可控 raw input_id、Authorization、AppKEY、base64 图片、完整 OCR、手机号、学号或邮箱。APK 密钥卫生守卫使用 `validate_apk_secret_hygiene.py`，通过标准是 `APK_SECRET_HYGIENE_METRIC 8/8`，会检查本地和桌面 APK 解包条目中没有 `sk-*`、provider secret env 名称、vivo 直连 endpoint 或后端私有 env 值。默认图片上传边界守卫使用 `validate_no_default_image_upload.py`，通过标准是 `NO_DEFAULT_IMAGE_UPLOAD_METRIC 12/12`，会检查分享文本本地化、系统图片分享/最近截图助手只生成候选、手动输入清除旧图片引用、图片 payload 只在用户点“解析当前草稿”后懒构造。执行层守卫使用 `validate_action_execution.py`，通过标准是 `ACTION_EXECUTION_METRIC 18/18`。可落地总体验收使用 `validate_real_world_ready.py`。发布候选总门禁使用 `validate_landing_release_candidate.py`，默认通过标准是 `LANDING_RELEASE_CANDIDATE_METRIC 63/63`，会整合 BlueLM、vivo OCR、vivo 多模态图片契约、后端审计日志、live-smoke 脱敏证据、密钥安全、默认图片上传边界、Android 图片预处理、云真机包、strict blocking report、release evidence index、前端、OCR、执行闭环、收件箱、隐私和材料证据；`--strict` 仅在真实 BlueLM/OCR 在线日志和云真机录屏齐备后使用，缺外部证据时生成 blocking report。真机演示验收使用 `validate_demo_acceptance.py`，通过标准是 `DEMO_ACCEPTANCE_METRIC 18/18`。云真机证据包建议放在 `materials/evidence/cloud-device/`，默认结构检查使用 `validate_cloud_device_package.py`，收齐实际录屏后再用 `--strict` 补做最终核验。`validate_release_blocking_report.py` 会检查 strict 阻断报告是否列出缺失视频、待填报告字段、复跑命令和脱敏警告；`validate_release_evidence_index.py` 通过标准是 `RELEASE_EVIDENCE_INDEX_METRIC 10/10`，会检查发布证据索引是否覆盖本地门禁、模型证据、BlueLM/OCR 脱敏证据、后端审计日志、live-smoke 脱敏证据、strict 阻断项、APK hash、默认图片上传边界、Android 图片预处理、依赖安全重跑命令、`docs/optimization-log.md` 当前交接摘要、README 公开入口、`validation/traceability.md` SHIKE-070 交付追踪和脱敏规则。用户研究证据边界使用 `validate_user_research_evidence.py`，通过标准是 `USER_RESEARCH_EVIDENCE_METRIC 8/8`，会检查 `docs/user-research-plan.md`、`docs/user-interview-summary.md`、`materials/evidence/scoring-evidence-map.md` 和 `validation/traceability.md` SHIKE-075，并明确真实访谈、问卷、应用价值定量结果仍为 `待采集`，不得编造。`validate_deliverables.py` 检查 10 个 SHIKE issue 的交付物覆盖情况；`run_spike.py --all` 验证解析、动作编排、状态存储和降级逻辑。

云真机证据包当前非 strict 通过标准是 `CLOUD_DEVICE_PACKAGE_METRIC 30/30`，会核对 `materials/evidence/cloud-device/` 目录、录屏文件名清单、报告字段、APK hash、脱敏日志、`docs/device-runbook.md` release handoff 步骤、`materials/evidence/release-evidence-index.md`、`materials/evidence/blocking-report.md`、生成脚本不回退 release handoff、`scripts/run_release_handoff_checks.py` 复验入口、默认发布门禁 `LANDING_RELEASE_CANDIDATE_METRIC 63/63`、后端审计日志 `BACKEND_AUDIT_LOG_METRIC 8/8`、live-smoke 脱敏证据 `LIVE_SMOKE_EVIDENCE_METRIC 7/7` 和 strict 外部证据阻断状态 `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7`。录制云真机前先运行 `prepare_cloud_device_evidence.py`，当前准备门禁为 `CLOUD_DEVICE_PREP_METRIC 5/5`，未收齐真实录屏前 `CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9` 是预期状态；随后运行 `test_preflight_cloud_backend.py` 与 `preflight_cloud_backend.py --base-url https://roky.chat`，确认 `CLOUD_BACKEND_PREFLIGHT_METRIC` 通过且输出已脱敏；同时在 `cloud-device-test-report.md` 的 `Pre-recording Evidence Gate` 中确认 `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md` 仍是桌面指导源，`materials/evidence/requirement-matrix.md` 仍通过 `REQUIREMENT_MATRIX_METRIC 9/9`，Android 16 DoD 仍通过 `ANDROID16_DOD_COVERAGE_METRIC 28/28`，all 9 real cloud-device MP4 files 均已采集，且 no placeholder fields remain after capture。收齐真实云真机录屏和已填报告后，先执行 `python3 shike/scripts/run_release_handoff_checks.py --strict-ready`，再执行 `validate_cloud_device_package.py --strict` 与 `validate_landing_release_candidate.py --strict` 做最终核验。

桌面指导文档逐项追踪使用 `validate_requirement_matrix.py`，通过标准是 `REQUIREMENT_MATRIX_METRIC 9/9`，会检查 `materials/evidence/requirement-matrix.md` 是否把阶段 A-E 映射到本地证据、验证命令、strict 云真机阻断项，并确认公开状态页锚定桌面 `1. 当前仓库总体判断.md`。应用价值证据新增 `materials/evidence/scoring-evidence-map.md`、`docs/user-research-plan.md` 和 `docs/user-interview-summary.md`，通过 `USER_RESEARCH_EVIDENCE_METRIC 8/8` 证明研究计划、访谈模板和“不编造真实访谈”的边界已落地。

Today Action 排序基线使用 `validate_today_ranking.py`，通过标准是 `TODAY_RANKING_METRIC 7/7`，覆盖 10 条合成样例和截止时间、开始时间、待确认、低置信度、缺失地点、已完成、已忽略等排序规则。

Product Beta 基线使用 `validate_advanced_product_beta.py`，默认输出当前 30 项产品级 readiness 分数和每个未通过项的下一步建议；需要作为严格发布门禁时可加 `--strict`，满分时返回零状态。当前基线是 `PRODUCT_BETA_METRIC 30/30`，说明项目已经有确认页可编辑、低置信度人工确认提示、缺时间禁用日历和提醒、缺地点禁用地图、用户确认后的真实定时提醒调度、通知权限拒绝时保留行动卡并把提醒按钮改成“去开启通知”、地图不可用时复制地点并保留行动卡、关闭云侧增强时不请求后端、日志脱敏、清除拾刻缓存 App 内二次确认、110-case 模型评测集、模型解释详情、ExecutionResult 执行结果、日历已打开系统新增页口径、收件箱归档/恢复、相册/相机/分享文本统一 CaptureDraft、手动输入继续解析、OCR 失败手动继续、今日排序验证、首页当前行动卡数据驱动、今日空状态、今日错误状态、收件箱五状态筛选、收件箱搜索、OCR 原文详情、相对时间提示、后端 schema 路径和持续优化日志。

模型评测样例使用 `validate_model_eval_cases.py`，通过标准是 `MODEL_EVAL_CASES_METRIC 9/9`，会检查 `validation/regression-cases.json` 至少 110 条、ID 唯一、课程/活动/会议/作业/面试/出行票务/低质量/反例覆盖、核心场景分布、字段结构和动作集合，并串联 `validate_image_semantic_cases.py`。截图语义样例使用 `validation/fixtures/image_cases.json`，通过标准是 `IMAGE_SEMANTIC_CASES_METRIC 9/9`，覆盖 40 条合成截图/拍照语义用例、图片来源、OCR hint、关键字段、动作集合、低置信度人工确认和反例边界；负例会强制纯拾刻界面、底部导航和状态栏区域保持 `unknown`、空动作、缺 task/time/location，并禁止把拾刻自身 UI 文案或导航 tab 当作标题/地点证据。后端场景契约守卫使用 `validate_backend_scene_contract.py`，通过标准是 `BACKEND_SCENE_CONTRACT_METRIC 11/11`，会确保公开输出契约保持保守：`scene_type` 仅允许 `course_notice`、`event_poster`、`unknown`，`task.topic` 仅允许 `course`、`event`、`unknown`；会议/作业/面试/出行等扩展回归样例可作为输入 `scene_hint` 与评测分组存在，但在不扩展 schema 的前提下输出应映射到 `unknown`。

核心 20 文件提交包可用 `scripts/verify_core20_package.py` 核对，脚本会检查文件数、必需文件、APK SHA-256、结构守卫引用、执行层守卫引用和单元测试守卫引用，避免多交计划文件、漏交核心文件或丢掉关键验收入口。

## 真机落地

可直接打开 `prototype/demo.html` 作为一页式 Demo 控制台，里面包含手机首页预览、3 分钟演示路线、验收指标和核心包核对命令；完整多页面原型仍保留在 `prototype/index.html`。

Android MVP 已包含系统相册截图选择、相机拍照预览、`SharedPreferences` 收件箱缓存、日历插入 Intent、`AlarmManager` 本地定时提醒、本地通知、地图 deeplink 和系统文本分享入口。提醒调度会优先使用 `setExactAndAllowWhileIdle`，Android 12+ 无 exact-alarm 能力或精确调度被拒绝时降级为普通 `AlarmManager.set`，并在结果文案里标明调度模式。已调度提醒会持久化到应用私有偏好，应用启动时通过 `restoreScheduledReminder` 恢复未过期待触发提醒，设备重启后由 `BootReminderReceiver` 重新恢复，提醒触发后清理对应记录；用户在 App 内二次确认“清除拾刻缓存”后会调用 `cancelScheduledReminder` 取消系统待触发提醒并清除本地记录，且不会删除系统相册原截图。设备联调步骤见 `docs/device-runbook.md`，可覆盖应用重启后的当前行动卡恢复。

模型编排联调已接入 Android 侧导入后自动云侧解析和“解析当前草稿/活动样例解析”按钮：真机默认请求 `https://roky.chat`，旧安装若保存过模拟器默认 `http://10.0.2.2:8000` 会自动迁移到公网 HTTPS 后端；模拟器本地调试仍可在“后端地址”输入 `http://10.0.2.2:8000` 并点“保存后端地址”。文本/手动草稿会把可编辑的“OCR 文本草稿”作为 `ocr_text` 提交到 `/v1/analyze`，并按当前入口发送 `screenshot`、`camera`、`share_text` 或 `manual`；被动截图检测仍只生成候选或通知，不自动上传图片；用户主动选择相册、拍照或确认导入截图后，Android 会懒构造后端图片 payload 并自动请求 `/v2/analyze-image`，也保留“解析当前草稿”作为手动重试入口。相册截图、系统图片分享、最近截图助手和相机预览在该用户动作触发后才会携带 `data:image/jpeg;base64,...`、尺寸、SHA-256、OCR hint、日期、时区和 locale 调用 `/v2/analyze-image`。手动输入入口会清空上一张图片 URI 和相机预览，避免文本模式误带旧图；该边界由 `NO_DEFAULT_IMAGE_UPLOAD_METRIC 12/12` 守卫。服务不可用或图片读取失败时进入本地待确认回退，不注入训练样例。演示数据均为合成样例；上传前应删除姓名、手机号、学号、群聊内容等个人信息。离线演示不依赖在线模型：`MockModelAdapter` 对课程通知与活动海报输出稳定结构；对会议/作业/面试/出行等扩展语义在不扩展公开 schema 的前提下输出 `scene_type=unknown`，但仍会给出可执行动作建议（提醒/日历/地图的合理子集）与缺失字段标注。后端 FastAPI 提供 `/health`、`/v1/schema`、`/v1/ocr`、`/v1/analyze`、`/v2/schema` 和 `/v2/analyze-image`；`/v1/ocr` 由服务端调用 vivo 通用 OCR 导入 API，`/v1/analyze` 调用 Mock/BlueLM 模型编排，`/v2/analyze-image` 会先从图片 data URL 尝试服务端 vivo OCR enrichment，把后端 OCR 文本和坐标块与 Android OCR hint/blocks 合并，过滤状态栏和底部导航块后再按 `VIVO_MULTIMODAL_MODELS` 顺序调用 vivo 多模态候选；OpenAI-compatible 图片路由不支持或鉴权异常时会尝试签名 VisionChat `/vivogpt/completions`，若图片模型仍不可用则用 OCR 文本走 BlueLM 兜底生成待确认行动卡，所有动作仍保持“用户确认前不可执行”；route-level smoke 用 `--route-v2` 只输出 `route_v2_schema_valid=true`、`route_v2_actions_disabled=true`、`route_v2_ignored_regions=top_status_bar,bottom_navigation_bar` 等脱敏证据；后端私有环境既支持 `BLUELM_*`/`VIVO_AIGC_*`/`VIVO_MULTIMODAL_*`，也支持 Android16 指导里的 `VIVO_APP_ID=***`、`VIVO_APP_KEY=***`、`VIVO_CHAT_BASE_URL=https://api-ai.vivo.com.cn/v1`、`VIVO_CHAT_MODEL=...` 作为别名；Android 只调用自有后端且不持有任何 vivo AppKEY。

确认页支持手动修正标题、时间、地点和状态；用户点“确认并安排”后才会启用日历、提醒和地图动作。缺时间时日历和提醒显示“补充时间后可用”，缺地点时路线显示“补充地点后可用”，通知权限拒绝后提醒入口会改成“去开启通知”；不可信内容可标为“已忽略”。

复赛录屏和复测交接见 `materials/device-demo-checklist.md`，其中定义了安装打开、课程截图、活动拍照、后端失败回退、重启恢复、交付物自检六段证据文件；需要展示扩展场景时可追加作业/会议、面试/出行两段补录。
