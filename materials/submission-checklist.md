# 初赛提交材料清单

对应 issue：`SHIKE-070`

| 材料 | 文件 | 状态 | 备注 |
|---|---|---|---|
| 12 到 15 页 PPT | `materials/preliminary-deck.md` | 已完成文稿 | 可转 PPT |
| 产品海报 | `materials/poster-copy.md` | 已完成文案 | 可交给设计排版 |
| 演示脚本 | `materials/demo-script.md` | 已完成 | 覆盖 3 分钟口播和追问 |
| 录屏/动效分镜 | `prototype/demo-storyboard.md` | 已完成 | 两条链路均不少于 4 步 |
| 真机演示验收清单 | `materials/device-demo-checklist.md` | 已完成 | 覆盖安装、录屏证据、课程链路、活动链路、失败降级和重启恢复 |
| 发布证据索引 | `materials/evidence/release-evidence-index.md` | 已完成 | 汇总本地门禁、BlueLM 脱敏证据、云真机 prep/helper、strict 阻断项、APK hash、优化日志交接摘要、`validation/traceability.md` SHIKE-070 交付追踪和重跑命令 |
| 桌面指导追踪矩阵 | `materials/evidence/requirement-matrix.md` | 已完成 | 将桌面指导文档阶段 A-E 映射到本地证据、验证命令和 strict 云真机阻断项 |
| 高保真原型 | `prototype/index.html` | 已完成 | 可浏览 HTML |
| 技术 Spike | `spike/run_spike.py` | 已完成 | 可复现本地运行 |
| 核心 20 文件核对 | `scripts/verify_core20_package.py` | 已完成 | 可核对文件数、必需文件、APK SHA-256、结构守卫引用、执行层守卫引用和单元测试守卫引用 |

## 现场必看点

- 今日行动台包含“交付物自检中心”，用于说明 APK、真机证据、后端和总体验收状态。
- 发布证据索引集中列出 `LANDING_RELEASE_CANDIDATE_METRIC 52/52`、`REAL_WORLD_READY_METRIC 22/22`、`CLOUD_DEVICE_PREP_METRIC 5/5`、`CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9`、`CLOUD_DEVICE_PACKAGE_METRIC 27/27`、`RELEASE_EVIDENCE_INDEX_METRIC 10/10`、`DELIVERABLES_METRIC 10/10`、BlueLM 脱敏日志、`REQUIREMENT_MATRIX_METRIC 9/9`、`validation/traceability.md` SHIKE-070、`docs/optimization-log.md` 当前交接摘要、strict 云真机阻断项和重跑命令。
- 桌面指导追踪矩阵 `materials/evidence/requirement-matrix.md` 可用于逐项解释阶段 A-E 已落地证据和仍需外部采集的 strict 云真机证明；云真机录制前必须确认 `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md` 仍是桌面指导源，且矩阵仍通过 `REQUIREMENT_MATRIX_METRIC 9/9`。
- 云真机 strict 证据包位于 `materials/evidence/cloud-device/`，当前阻断报告为 `materials/evidence/blocking-report.md`；在真实云真机 MP4 和填写后的报告收齐前，`LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7` 是预期阻断状态，不应当作为已发布完成证明。提交前必须完成 `cloud-device-test-report.md` 的 `Pre-recording Evidence Gate`，确认 all 9 real cloud-device MP4 files 已进入证据包，且 no placeholder fields remain after capture。
- “3分钟演示路线”覆盖课程截图、活动拍照、后端回退和重启恢复四段。
- AI 解析确认页包含“风险与缺失字段”，明确相对时间、报名链接和系统写入权限。
- 复赛扩展场景可展示 `assignment_deadline`、`meeting_notice`、`interview_notice`、`travel_ticket`，但所有系统动作仍保留用户确认。
