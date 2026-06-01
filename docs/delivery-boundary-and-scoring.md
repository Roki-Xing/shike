# 交付边界与评分映射

对应 issue：`SHIKE-000`

## 交付边界

| 档位 | 必交内容 | 验收形态 | 不进入本档的内容 |
|---|---|---|---|
| 初赛 | 高保真原型、策划 PPT、产品海报、演示脚本、主链路录屏或动效、技术可行性 Spike 记录 | 评委可在 3 到 5 分钟内看懂“截图/拍照到行动闭环” | 可运行 APK、通知监听、桌面组件、通话导入、复杂跨应用自动执行 |
| 复赛 | Android Kotlin + Jetpack Compose 可运行 APK、FastAPI 模型编排服务、本地状态存储、至少两个系统动作真实可用 | 课程通知、活动海报、作业截止、会议通知、面试通知、出行票务可从导入跑到收件箱追踪 | 端侧模型微调、校园模板市场、智能体平台完整接入 |
| 决赛增强 | 端侧轻分类、隐私脱敏、锁屏/桌面组件、智能体兼容层、校园模板市场、更多青年模板 | 展示更接近系统级 AI 体验的可控增强 | 不做无授权的全自动跨应用代操作 |

## 优先级边界

| 优先级 | 范围 | 说明 |
|---|---|---|
| P0 | 初赛必须可讲、复赛主链路必须依赖 | 交付边界、MVP 收敛、产品规格、核心原型、关键 Spike、模型契约、初赛材料 |
| P1 | 复赛可运行 MVP 与回归样例 | Android MVP、样例回归基线 |
| P2 | 决赛增强与降级路线 | 故障矩阵、端侧增强、系统级插件化路线 |

## 评分映射

| 评分项 | 可展示交付物 | 叙事要点 | 验收方式 |
|---|---|---|---|
| 创新性 | 截图悬浮动作卡、行动编排页、今日行动台、竞品差异页 | 拾刻不是信息收藏器，而是青年场景的碎片执行代理 | 原型中必须出现 AI 判断、动作建议、执行结果和后续追踪 |
| 应用价值 | 用户画像、课程通知链路、活动海报链路、回归样例集 | 高频场景来自课程、社团、竞赛和校园活动，不是泛泛的聊天助手 | 两条任务链路均能在演示脚本中闭环 |
| 完成度 | PPT、海报、演示脚本、技术 Spike、复赛路线图 | 初赛材料完整，复赛路径不依赖未知重权限能力 | 每个材料项可追踪到本目录文件 |
| 大模型应用能力 | `ModelAdapter` 契约、JSON Schema、样例响应、置信度与缺失字段机制 | 模型承担理解和建议，规则层承担校验、状态机和系统 API 执行 | 契约字段完整，支持 mock、OpenAI compatible、BlueLM 三类适配方式 |

## 评分证据包映射

| 评分项 | 代码证据 | 视频/演示证据 | 文档与门禁证据 |
|---|---|---|---|
| 创新性 | `prototype/index.html`、`android-mvp/app/src/main/java/cn/shike/app/ui/MainFlowScreens.kt`、`android-mvp/app/src/main/java/cn/shike/app/ui/ActionPlannerPanel.kt` | `materials/device-demo-checklist.md` 的 `01-install-and-open.mp4`、`02-course-gallery-backend.mp4`、`03-event-camera-actions.mp4` | `materials/evidence/release-evidence-index.md`、`validation/traceability.md` SHIKE-070、`DEMO_ACCEPTANCE_METRIC 18/18` |
| 应用价值 | `validation/regression-cases.json`、`backend/shike_backend/eval/run_model_eval.py`、`android-mvp/app/src/main/java/cn/shike/app/data/InboxEntities.kt` | 作业/会议、面试/出行扩展补录可按 `materials/device-demo-checklist.md` 追加 | `materials/evidence/requirement-matrix.md`、`REQUIREMENT_MATRIX_METRIC 9/9`、`MODEL_EVAL_METRIC 110/110` |
| 完成度 | Android APK、FastAPI 后端、SQLite 收件箱、执行层守卫、云真机 prep helper | 本地/USB 真机六段主线录屏；云真机 strict 录屏收齐前不宣称发布完成 | `LANDING_RELEASE_CANDIDATE_METRIC 52/52`、`DELIVERABLES_METRIC 10/10`、`CLOUD_DEVICE_PREP_METRIC 5/5`、`CLOUD_DEVICE_PACKAGE_METRIC 27/27`、expected `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7` |
| 大模型应用能力 | `contracts/model-adapter.md`、`contracts/model-output.schema.json`、`backend/shike_backend/adapters/bluelm_adapter.py` | BlueLM 在线 smoke 仅展示脱敏日志，不展示 AppKEY、签名或完整 OCR 原文 | `BLUELM_ADAPTER_METRIC 7/7`、`MODEL_CONTRACT_STRICT_METRIC 10/10`、`materials/evidence/cloud-device/backend-redacted-access-log.txt`、`PASS secret_hygiene` |

`materials/evidence/release-evidence-index.md` 是提交前的总证据入口；`validation/traceability.md` 的 SHIKE-070 行负责把提交材料、演示验收、云真机证据包、strict 阻断报告和 `DELIVERABLES_METRIC 10/10` 串到同一条可复核链路。真实云真机 9 段 MP4 与填写后的测试报告未收齐前，`LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7` 必须保持为外部证据阻断状态。云真机录制前还必须完成 `cloud-device-test-report.md` 的 `Pre-recording Evidence Gate`：确认 `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md` 仍是桌面指导源，`materials/evidence/requirement-matrix.md` 仍通过 `REQUIREMENT_MATRIX_METRIC 9/9`，all 9 real cloud-device MP4 files 已进入证据包，且 no placeholder fields remain after capture。

## 显性非目标范围

- 初赛不承诺真实系统截图钩子，仅以可讲清的悬浮动作卡原型表达系统入口。
- 初赛不承诺真实 APK，复赛才进入可运行 Android MVP。
- MVP 不做通知监听、无障碍代操作、桌面组件和通话导入。
- AI 不允许绕过用户确认直接写日历、设提醒或跳转地图。
- 官方开放 API、端侧模型接入门槛和云测细则以赛方最新文档为准，当前材料只保留适配器边界。

## 公开依据与待确认

| 类型 | 结论 | 来源 |
|---|---|---|
| Fact | 第三届 AIGC 创新赛官方网站为 `https://aigc.vivo.com.cn/`，公开检索结果显示赛事由南开大学与 vivo 联合承办，面向高校学生。 | [vivo AIGC 创新赛官网, 2026, https://aigc.vivo.com.cn/] |
| Fact | 媒体公开报道显示应用赛道报名及初赛作品提交截止为 2026 年 5 月 11 日。 | [中国日报中文网, 2026-03-18, https://cn.chinadaily.com.cn/a/202603/18/WS69ba42a3a310942cc49a3c18.html] |
| Unknown | 完整评分细则、云测平台规则、端侧模型 API 和 vivo 系统权限边界仍需报名后以官方文档和群通知核验。 | 当前未获取完整官方细则 |

置信度：Medium。官方网站可作为一级入口，但网页内容抓取受前端渲染限制；具体赛程细节目前以公开媒体报道和源材料交叉核验，后续应以赛方报名后台为准。
