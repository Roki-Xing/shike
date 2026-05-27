# AGENTS.md (Shike / 拾刻)

本文件面向后续 Codex / AI Agent 协作与维护，目标是让任何改动都能：

- 先理解项目事实（SSOT），再动手改；
- 复用既有模块与验证体系，避免重复造轮子；
- 严守红线（确认后执行、密钥安全、契约稳定）；
- 可复现、可验收、可交付。

## 1. 项目定位（What / Why）

拾刻（Shike）是面向 vivo AIGC 创新赛应用赛道的 Android 应用，定位是“手机碎片信息行动助手”。

核心闭环（不得破坏）：

```text
截图/拍照/文本分享
  -> OCR 文本草稿 / 文本输入
  -> 后端或本地解析
  -> AI 解析确认
  -> 用户确认修正
  -> 日历 / 提醒 / 地图动作
  -> 收件箱 / 今日行动台持续追踪
```

范围收敛（MVP 基线）：

- 入口：截图导入、相机拍照、文本分享
- 场景：课程通知、活动海报（含 unknown 兜底）
- 动作：日历、提醒、地图

SSOT：当文档与代码不一致时，以代码与验证脚本运行结果为准，并更新文档/脚本使其反映真实行为。

## 2. 目录职责（Repo Map）

以 `README.md` 的目录表为主，并以当前仓库文件为准：

- `android-mvp/`：Android App（Kotlin + Jetpack Compose）。入口为 `MainActivity`，Compose 主协调为 `ShikeApp`，UI 组件集中在 `cn.shike.app.ui`。
- `backend/`：FastAPI 后端示例。提供 `/health`、`/v1/schema`、`/v1/analyze`；当前实现偏规则/Mock 风格，后续用于接入 BlueLM（必须保持 Mock 兜底）。
- `contracts/`：跨端契约（JSON Schema + 样例请求/响应 + adapter 说明）。核心契约为 `contracts/model-output.schema.json`。
- `validation/`：质量门禁与回归脚本（结构、单测、桥接、执行安全、真机验收、落地 readiness 等）。不得删除或弱化。
- `spike/`：可行性 Spike（workflow + 样例 + 结果落盘到 `spike/logs/`）。
- `prototype/`：高保真原型与 Demo 控制台（HTML/PDF）。
- `materials/`：比赛材料（演示脚本、录屏清单、提交清单、海报/Deck 文稿等）。
- `scripts/`：交付包核对脚本（核心 20 文件交付包）。
- `docs/`：产品规格、MVP 边界、设备 runbook、交付边界、持续优化日志、当前验证状态、落地优化指南等。

说明：当前工作区不是 git 仓库（`git status` 不可用；见 `docs/current-validation-status.md`）。默认以“验证脚本 + 构建产物 + 可复现命令输出”作为变更证据。

## 3. 首读文件（Must Read First）

通用任务先读：

1. `README.md`
2. `docs/SHIKE_LANDING_APP_OPTIMIZATION_GUIDE.md`
3. `docs/product-spec.md`
4. `docs/mvp-scope.md`
5. `docs/device-runbook.md`
6. `contracts/model-output.schema.json`

Android 任务再读：

1. `android-mvp/app/src/main/AndroidManifest.xml`
2. `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt`
3. `android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt`
4. `android-mvp/app/src/main/java/cn/shike/app/domain/`
5. `android-mvp/app/src/main/java/cn/shike/app/data/`
6. `android-mvp/app/src/main/java/cn/shike/app/system/`
7. `android-mvp/app/src/main/java/cn/shike/app/ui/`
8. `docs/android-mvp-implementation.md`

后端 / 契约任务再读：

1. `backend/shike_backend/main.py`
2. `backend/verify_backend.py`
3. `contracts/model-adapter.md`
4. `contracts/sample-course-request.json`
5. `contracts/sample-course-response.json`

验证 / 演示任务再读：

1. `validation/`（聚合器：`validation/validate_real_world_ready.py`）
2. `materials/device-demo-checklist.md`
3. `materials/submission-checklist.md`
4. `prototype/index.html`

## 4. 关键入口（Entry Points）

Android：

- `android-mvp/app/src/main/AndroidManifest.xml`：LAUNCHER + 文本分享 `ACTION_SEND text/plain`；Receiver（提醒触发、开机恢复）等声明。
- `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt`：Android shell（权限、系统 Intent 调度、启动恢复、分享文本注入）。
- `android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt`：Compose 状态协调与回调编排。
- `android-mvp/app/src/main/java/cn/shike/app/ui/`：UI 组件与边界拆分（结构守卫会约束文件规模与职责）。

Backend：

- `backend/shike_backend/main.py`：FastAPI app 与路由实现。
- `backend/verify_backend.py`：后端 smoke（不需要启动 server）。

Contracts：

- `contracts/model-output.schema.json`：结构化输出契约（跨端 SSOT）。

## 5. 不可触碰红线（Hard Red Lines）

1. **用户确认前不得执行系统动作**：日历、提醒、地图等敏感动作必须在“用户确认修正”后才可执行。
2. **Android 不得持有 BlueLM AppKEY**：不得把 AppKEY、签名串、token 等写入 Kotlin/BuildConfig/resources/assets/raw/Manifest/APK。
3. **BlueLM AppID/AppKEY 只能由后端从环境变量读取**：不得写入源码、AGENTS.md、`.agents/skills`、README、docs、materials、prototype、tests、logs、APK。
4. **不得删除或弱化 validation 脚本**：这些脚本是交付质量的一部分，不是可选项。
5. **不得破坏后端契约与路径**：必须保持 `/health`、`/v1/schema`、`/v1/analyze` 路由存在，并保持 `contracts/model-output.schema.json` 契约可用（改动需同步全链路）。
6. **模型输出必须符合 schema**：输出必须匹配 `contracts/model-output.schema.json`（`additionalProperties=false` 等约束不得随意放开）。
7. **后端失败必须可解释且可降级**：模型/网络失败时必须回退 Mock 或进入 `needs_manual_review`（不得静默失败）。
8. **演示与测试数据必须合成**：不得提交真实群聊、手机号、学号、个人通知或真实 OCR 内容。
9. **不得把 Android 已拆分职责压回单文件**：保持结构守卫与单测守卫可通过（避免“一个巨型屏幕文件”回潮）。

## 6. 环境变量（Backend Secrets）

后端密钥（示例，仅占位，禁止在仓库中写入真实值）：

```bash
SHIKE_MODEL_PROVIDER=bluelm
BLUELM_APP_ID=***              # 占位
BLUELM_APP_KEY=***             # 占位
BLUELM_TIMEOUT_SECONDS=12
BLUELM_MAX_RETRIES=1
SHIKE_ALLOW_MOCK_FALLBACK=true
# 可选：录制模式（用于将一批在线响应固化为本地回放，避免每次回归都调用云端）
SHIKE_MODEL_PROVIDER=recorded_bluelm
SHIKE_RECORDED_DIR=...         # 默认写入 backend/shike_backend/eval/recordings
```

现状说明：后端已具备 `ModelAdapter` 架构与 `BlueLMModelAdapter` / `RecordedBlueLMAdapter` 骨架；默认仍使用 Mock，BlueLM 需通过环境变量启用（以 `backend/shike_backend/main.py` 现状为准）。密钥卫生门禁已存在：`validation/validate_secret_hygiene.py`，开始任何 BlueLM 接入前必须保持其通过。

## 7. 常用命令（Commands）

从工作区根目录运行（`README.md` 有更完整清单；此处列出最常用与安全门禁）：

```bash
# Secret hygiene (must stay green)
python3 shike/validation/validate_secret_hygiene.py

# Core validation (narrow -> broad)
python3 shike/validation/validate_android_structure.py
python3 shike/validation/validate_android_unit_tests.py
python3 shike/validation/validate_action_execution.py
python3 shike/validation/validate_model_bridge.py
python3 shike/validation/validate_demo_acceptance.py
python3 shike/validation/validate_real_world_ready.py
python3 shike/validation/validate_deliverables.py
python3 shike/validation/validate_landable.py

# Extra quality gates
python3 shike/validation/validate_today_ranking.py
python3 shike/validation/validate_advanced_product_beta.py
python3 shike/validation/validate_model_eval_cases.py

# Backend smoke (no server required)
python3 shike/backend/verify_backend.py

# BlueLM adapter + contract strictness (no real credentials required)
python3 shike/validation/validate_bluelm_adapter.py
python3 shike/validation/validate_model_contract_strict.py
python3 shike/validation/validate_cloud_backend_ready.py

# Model eval (writes docs/model-eval-report.md)
python3 shike/backend/shike_backend/eval/run_model_eval.py

# Record a subset of regression cases (requires BLUELM_APP_ID/BLUELM_APP_KEY)
python3 shike/backend/shike_backend/eval/record_cases.py

# Spike
python3 shike/spike/run_spike.py --all

# Core-20 submission package check
python3 shike/scripts/verify_core20_package.py \"/path/to/core20-package\"
```

真机联调（仅可信局域网，详见 `docs/device-runbook.md`）：

```bash
cd shike/backend
python3 -m uvicorn shike_backend.main:app --host 0.0.0.0 --port 8000
```

## 8. Done 清单（DoD / Evidence）

每次改动后，至少提供以下证据之一（命令输出 / 日志）：

- `python3 shike/validation/validate_real_world_ready.py` 满分（`REAL_WORLD_READY_METRIC 22/22`）
- 或对应子域脚本全绿（例如结构/单测/执行/桥接）
- 若涉及后端：`python3 shike/backend/verify_backend.py` 输出 `backend_passed`
- 若涉及交付包：`python3 shike/scripts/verify_core20_package.py "<package_dir>"` 输出 `CORE20_FILE_COUNT 20/20`

完成前必检（对应 guide 的输出要求）：

1. 列出本次变更文件清单
2. 列出运行过的验证命令与结果
3. 标注未确认项（例如 BlueLM 官方鉴权细节、云真机网络可达性）
4. 确认 `python3 shike/validation/validate_secret_hygiene.py` 为 PASS
5. 确认“用户确认前不执行日历/提醒/地图”仍成立

密钥风险：任何变更中出现完整 `AppKEY` 或疑似真实 `sk-...` 密钥，必须立即回滚并用脱敏占位替换。

## 9. 开发规则（Development rules）

- 小步提交、每步可验：先跑最窄的 validator，再跑 `validate_real_world_ready.py`。
- 行为变更必须同步：Android/后端/contracts/docs/validation 不一致时，以代码 + validator 为准并同步修正文档/脚本。
- 文档/skills 变更也要做安全检查：至少跑 `validate_secret_hygiene.py`，并检查所有引用路径真实存在。
- Android 系统动作必须验证：权限拒绝、无可用 App、Android 12+ exact-alarm 不可用时的降级与“保留行动卡”。
- 后端模型变更必须验证：输出仍符合 `contracts/model-output.schema.json`，且 `/health`、`/v1/schema`、`/v1/analyze` 路径不破坏。

## 10. Skills 路由（Use Project Skills）

本仓库建议使用项目专属 skills（位于 `.agents/skills/`）：

- 进入项目/找文件/职责边界：`shike-project-navigation`
- Android/UI/系统动作：`shike-android-development`
- 后端/API/schema/adapter：`shike-backend-model-adapter`
- BlueLM 接入：`shike-bluelm-integration`
- 验证/回归/质量体系：`shike-validation-and-regression`
- 云真机/真机联调：`shike-device-cloud-testing`
- UI 产品化与原型对齐：`shike-ui-product-polish`
- 安全与隐私：`shike-security-privacy`
- 材料与提交包：`shike-materials-submission`
