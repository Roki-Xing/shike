# 初赛 PPT 大纲：拾刻

对应 issue：`SHIKE-070`

建议页数：15 页。

## 1. 封面

- 标题：拾刻：手机碎片信息行动助手
- 副标题：把“先截个图，回头再看”变成“我已经帮你安排好了”
- 视觉：截图缩略图流入行动卡，再落到今日行动台

## 2. 团队分工

| 角色 | 职责 |
|---|---|
| 产品/PM | 用户洞察、范围控制、评分映射 |
| UI/交互 | 高保真原型、演示动效、提交海报 |
| Android | 导入、确认、动作执行、本地状态 |
| AI/后端 | ModelAdapter、FastAPI、结构化抽取 |
| 测试/材料 | 样例回归、演示脚本、答辩材料 |

## 3. 作品简介

拾刻不是聊天助手，也不是普通收藏夹，而是手机碎片信息行动层。

```text
截图/拍照 -> AI 解析 -> 用户确认 -> 动作编排 -> 收件箱追踪
```

## 4. 用户洞察

- 大学生高频保存截图、群通知、海报和临时任务。
- 痛点不是没有保存入口，而是保存后没有转成行动。
- “明明截了图，还是错过”是本项目要解决的核心问题。

## 5. 设计理念

| 原则 | 解释 |
|---|---|
| 少打扰 | 只处理有时间、地点、任务特征的碎片 |
| 强闭环 | 输出必须落到日历、提醒、地图或收件箱 |
| 手机原生 | 优先利用截图、相机、通知、日历和地图 |
| 可控 AI | AI 建议，用户确认，系统执行 |

## 6. 核心创新点

1. 多入口碎片采集：截图和拍照是用户真实入口。
2. 行动编排：不是识别文字，而是建议行动组合。
3. 主动追踪：收件箱和今日行动台让碎片不再失踪。

## 7. MVP 边界

| 维度 | 首期范围 |
|---|---|
| 入口 | 截图导入、相机拍照 |
| 场景 | 课程通知、活动海报 |
| 动作 | 日历、提醒、地图 |
| 持续层 | 收件箱、今日行动台 |

## 8. 功能架构

```text
采集入口 -> AI 理解引擎 -> 动作编排层 -> 系统执行层 -> 收件箱/今日行动台
```

这页用一张架构图说明模型、规则和系统能力的职责分离。

## 9. 原型总览

展示 7 个页面缩略图：

- 今日行动台
- 截图导入卡
- 相机导办页
- AI 解析确认页
- 行动编排页
- 收件箱页
- 隐私与端云设置页

## 10. 核心页面展示：截图导入卡

讲法：

“用户从分享面板或相册把截图交给拾刻后，拾刻先判断这张图是否值得处理。它不是把所有截图都丢进收藏夹，而是识别到课程通知后给出明确动作建议。”

## 11. 核心页面展示：AI 解析确认

讲法：

“AI 输出结构化字段、置信度和缺失项。用户能编辑，确认后才进入执行。”

## 12. 核心页面展示：行动编排

讲法：

“同一条碎片信息可以同时生成日历、提醒和地图动作。执行层由程序负责，AI 不越权。”

## 13. 大模型应用说明

| 大模型 | 程序规则 |
|---|---|
| 场景判断 | 模板路由 |
| 字段抽取 | 格式校验 |
| 行动建议 | 系统 API 执行 |
| 缺失字段解释 | 用户确认与状态机 |

## 14. 技术实现路线

| 阶段 | 产出 |
|---|---|
| 初赛 | 高保真原型、PPT、海报、演示脚本、Spike |
| 复赛 | Android APK、FastAPI、Room/SQLite、两类样例闭环 |
| 决赛 | 端侧轻分类、隐私脱敏、桌面组件、智能体兼容层 |

## 15. 复赛落地证据包

| 证据页 | 展示内容 | 对应门禁 |
|---|---|---|
| BlueLM 接入证据 | `ModelAdapter`、结构化输出、脱敏后端日志、Android 不持有 AppKEY | `BLUELM_ADAPTER_METRIC 8/8`、`PASS secret_hygiene` |
| 云真机测试 | HTTPS 后端、9 段云真机录屏清单、APK hash、测试报告、Android 16 指导文件聚合门禁、截图语义样例门禁、live-smoke 脱敏证据门禁、release handoff runner、公网后端录制前预检 | `CLOUD_DEVICE_PREP_METRIC 5/5`、`CLOUD_BACKEND_PREFLIGHT_METRIC`、`CLOUD_DEVICE_PACKAGE_METRIC 30/30`、`ANDROID16_REAL_IMPLEMENTATION_GUIDE_METRIC 12/12`、`IMAGE_SEMANTIC_CASES_METRIC 9/9`、`LIVE_SMOKE_EVIDENCE_METRIC 7/7`、`RELEASE_HANDOFF_CHECKS_METRIC 24/24` |
| 真实 App 前端 | 首页行动台、采集页、解析确认页、行动编排页、收件箱、Debug 页分离 | `FRONTEND_POLISH_METRIC 12/12`、`DEMO_ACCEPTANCE_METRIC 18/18` |
| 失败降级 | 后端失败、权限拒绝、地图不可用、提醒权限不可用、用户确认门禁 | `REAL_WORLD_READY_METRIC 22/22`、`ACTION_EXECUTION_METRIC 18/18` |
| 隐私安全 | AppKEY 不进 APK、环境变量、日志脱敏、一键清除本地数据 | `PASS secret_hygiene` |
| 模型评测 | 110 条样例、低质量输入、unknown 兜底、场景扩展契约 | `MODEL_EVAL_METRIC 110/110`、`MODEL_CONTRACT_STRICT_METRIC 10/10` |
| 评分证据 | 创新性、应用价值、完成度、大模型应用能力逐项映射到代码/视频/文档；用户访谈和问卷仍为 `待采集`，不得编造 | `USER_RESEARCH_EVIDENCE_METRIC 8/8`、`REQUIREMENT_MATRIX_METRIC 9/9`、`DELIVERABLES_METRIC 10/10` |

本地发布候选入口是 `materials/evidence/release-evidence-index.md` 和 `python3 shike/validation/validate_landing_release_candidate.py`，当前为 `LANDING_RELEASE_CANDIDATE_METRIC 63/63`，并直接纳入 `BACKEND_AUDIT_LOG_METRIC 8/8` 与 `LIVE_SMOKE_EVIDENCE_METRIC 7/7`。真实 9 段云真机 MP4 和填写后的 `cloud-device-test-report.md` 未收齐前，strict 发布保持 `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7` 阻断；录制前必须完成 `cloud-device-test-report.md` 的 `Pre-recording Evidence Gate`，确认 `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md` 仍是桌面指导源，`materials/evidence/requirement-matrix.md` 仍通过 `REQUIREMENT_MATRIX_METRIC 9/9`，all 9 real cloud-device MP4 files 已进入证据包，且 no placeholder fields remain after capture。阻断报告为 `materials/evidence/blocking-report.md`。`validation/traceability.md` 的 SHIKE-070 行用于串起 PPT、演示脚本、真机验收清单、发布证据索引和云真机证据包。

## 16. 竞争差异

| 对比对象 | 拾刻差异 |
|---|---|
| 普通 OCR | 输出行动卡，而不是文字 |
| 普通收藏 | 进入状态机，而不是分类存放 |
| AI 聊天助手 | 入口在截图/拍照，不要求用户复制提问 |
| 系统识屏/记忆 | 面向青年模板和执行追踪 |

## 17. 总结

拾刻抓住手机 AI 最适合解决的问题：把真实高频的碎片信息直接转化成可确认、可执行、可追踪的行动。

收口句：

**拾刻不是收藏器，而是青年生活的碎片执行代理。**
