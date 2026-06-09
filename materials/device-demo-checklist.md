# 真机演示验收清单

对应目标：让拾刻复赛演示从“可运行”变成“可录屏、可复测、可交接”。

## 验收前准备

| 项目 | 命令或操作 | 通过标准 |
|---|---|---|
| 构建 APK | `bash shike/android-mvp/build_apk.sh` | 产出 `shike/android-mvp/app/build/outputs/apk/debug/app-debug.apk` |
| Android 结构守卫 | `python3 shike/validation/validate_android_structure.py` | 输出 `ANDROID_STRUCTURE_METRIC 31/31` |
| Android 单元测试守卫 | `python3 shike/validation/validate_android_unit_tests.py` | 输出 `ANDROID_UNIT_TEST_METRIC 88/88`；最近一次 `gradle --no-daemon :app:testDebugUnitTest` 已通过 |
| Android 图片预处理守卫 | `python3 shike/validation/validate_android_image_preprocess.py` | 输出 `ANDROID_IMAGE_PREPROCESS_METRIC 15/15`；覆盖 `ImagePayloadPreprocessor` 的输入 MIME 魔数识别、非图片拒绝、EXIF 旋转、1600 长边压缩、截图 UI chrome 裁剪、`ImageThumbnailCache` 私有缩略图缓存、JPEG data URL 和 SHA-256 合同 |
| 执行层守卫 | `python3 shike/validation/validate_action_execution.py` | 输出 `ACTION_EXECUTION_METRIC 18/18` |
| 总体验收 | `python3 shike/validation/validate_real_world_ready.py` | 输出 `REAL_WORLD_READY_METRIC 22/22` |
| 后端 smoke | `python3 shike/backend/verify_backend.py` | 输出 `backend_passed` |
| 启动后端 | `cd shike/backend && python3 -m uvicorn shike_backend.main:app --host 0.0.0.0 --port 8000` | `/health` 返回 `{"status":"ok"}` |
| 安装 APK | `adb install -r shike/android-mvp/app/build/outputs/apk/debug/app-debug.apk` | 设备出现“拾刻” |

所有命令默认从工作区根目录执行，即 `shike/` 的上一级目录。`--host 0.0.0.0` 仅用于同一可信局域网真机演示；不要暴露到公网，不要提交真实截图 OCR，演示结束后关闭后端服务。

## 录屏证据文件

建议统一放到 `shike/materials/evidence/`，文件名按下面规则保存：

| 文件 | 内容 | 必须覆盖 |
|---|---|---|
| `01-install-and-open.mp4` | 安装后首次打开 | 今日行动台、导入入口、收件箱状态 |
| `02-course-gallery-backend.mp4` | 课程通知链路 | 选择截图、识别到的文字、生成行动卡、确认并安排 |
| `03-event-camera-actions.mp4` | 活动海报链路 | 拍照导入、生成行动卡、提醒、地图 |
| `04-fallback-offline.mp4` | 失败降级链路 | 停掉后端、后端不可用、后端失败、回退本地 MockModelAdapter、相机权限拒绝、已忽略 |
| `05-restart-restore.mp4` | 重启恢复链路 | 杀掉应用后重开，行动卡、待触发提醒和后端地址仍保留 |
| `06-delivery-readiness.mp4` | 交付物自检 | 交付物自检中心、3分钟演示路线、风险与缺失字段 |

复赛扩展场景若需要补录，可追加到云真机证据包，不影响上面六段主线录屏：

| 文件 | 内容 | 必须覆盖 |
|---|---|---|
| `07-assignment-meeting-scenes.mp4` | 作业截止和会议通知 | `assignment_deadline`、`meeting_notice`、缺失字段、用户确认 |
| `08-interview-travel-scenes.mp4` | 面试通知和出行票务 | `interview_notice`、`travel_ticket`、提醒、地图 |

## 云真机 strict 证据包

上面的六段主线录屏用于本地/USB 真机演示验收，不等同于云真机 strict 发布证据。云真机证据包统一放在 `materials/evidence/cloud-device/`，入口文件为 `materials/evidence/cloud-device/README.md`，总索引为 `materials/evidence/release-evidence-index.md`，当前索引门禁是 `RELEASE_EVIDENCE_INDEX_METRIC 10/10`，并已覆盖 `docs/optimization-log.md` 当前交接摘要、README 公开入口、`validation/traceability.md` SHIKE-070 交付追踪和 `DELIVERABLES_METRIC 10/10`。云真机录制前先运行 `python3 shike/scripts/prepare_cloud_device_evidence.py`，当前准备门禁是 `CLOUD_DEVICE_PREP_METRIC 5/5`，在未收齐真实录屏前 `CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9` 是预期状态；随后运行 `python3 shike/scripts/test_collect_cloud_device_evidence.py` 守住 adb 采集 helper，运行 `python3 shike/scripts/test_preflight_cloud_backend.py` 和 `python3 shike/scripts/preflight_cloud_backend.py --base-url https://roky.chat` 确认 `CLOUD_BACKEND_PREFLIGHT_METRIC`，再运行 `python3 shike/scripts/collect_cloud_device_evidence.py --preflight-backend --backend-url https://roky.chat` 统一验证 no-cloud-image 与 `--allow-cloud-image` 两条公网后端分支，并用 `python3 shike/scripts/collect_cloud_device_evidence.py --list` 复核 9 段录屏场景。录制时逐条执行 `python3 shike/scripts/collect_cloud_device_evidence.py --record <1-9> --duration-seconds 180`。录制完成后执行 `python3 shike/scripts/collect_cloud_device_evidence.py --capture-logcat --write-report-draft --backend-url https://roky.chat`，再人工复核生成的脱敏 logcat、报告草稿和 `Pre-recording Evidence Gate` 字段。录制前后都要保持 `validate_cloud_device_package.py` 非 strict 门禁为 `CLOUD_DEVICE_PACKAGE_METRIC 30/30`，用 `python3 shike/validation/validate_android16_real_implementation_guide.py` 确认 `ANDROID16_REAL_IMPLEMENTATION_GUIDE_METRIC 12/12`，用 `python3 shike/validation/validate_android16_definition_of_done.py` 确认 `ANDROID16_DOD_COVERAGE_METRIC 28/28`，用 `python3 shike/validation/validate_image_semantic_cases.py` 确认 `IMAGE_SEMANTIC_CASES_METRIC 9/9`，用 `python3 shike/validation/validate_live_smoke_evidence.py` 确认 `LIVE_SMOKE_EVIDENCE_METRIC 7/7`，并用 `python3 shike/scripts/run_release_handoff_checks.py --strict` 确认 `RELEASE_HANDOFF_CHECKS_METRIC 24/24`。桌面指导源必须仍是 `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md`，桌面指导逐项证据见 `materials/evidence/requirement-matrix.md`，录制前确认其仍通过 `REQUIREMENT_MATRIX_METRIC 9/9`；当前外部阻断项见 `materials/evidence/blocking-report.md`。只有在真实 MP4、脱敏 logcat 和已填报告全部齐备后，才允许使用 `python3 shike/scripts/run_release_handoff_checks.py --strict-ready` 做最终核验，并在 `cloud-device-test-report.md` 中确认 all 9 real cloud-device MP4 files 和 no placeholder fields remain after capture。

当前本地发布候选门禁应保持：

```bash
python3 shike/validation/validate_requirement_matrix.py
python3 shike/scripts/prepare_cloud_device_evidence.py
python3 shike/scripts/test_collect_cloud_device_evidence.py
python3 shike/scripts/collect_cloud_device_evidence.py --list
python3 shike/validation/validate_cloud_device_package.py
python3 shike/scripts/run_release_handoff_checks.py --strict
python3 shike/validation/validate_landing_release_candidate.py
# CLOUD_DEVICE_PREP_METRIC 5/5
# CLOUD_DEVICE_PACKAGE_METRIC 30/30
# ANDROID16_REAL_IMPLEMENTATION_GUIDE_METRIC 12/12
# IMAGE_SEMANTIC_CASES_METRIC 9/9
# LIVE_SMOKE_EVIDENCE_METRIC 7/7
# RELEASE_HANDOFF_CHECKS_METRIC 24/24
# LANDING_RELEASE_CANDIDATE_METRIC 63/63
```

在真实云真机录屏和填写后的报告尚未收齐前，strict 发布候选预期保持阻断：

```bash
python3 shike/validation/validate_landing_release_candidate.py --strict
# LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7
```

云真机补录必须使用 HTTPS 后端地址，收齐 `01-cloud-install-open.mp4` 到 `09-cloud-final-route.mp4` 九段真实云真机视频，并填写 `cloud-device-test-report.md`。录屏、日志、文件名和报告不得包含 AppKEY、backend tokens、完整 OCR 原文、手机号、邮箱、学号或个人通知。

这 9 段 strict 视频同时承接 `/mnt/c/Users/Xing/Desktop/SHIKE_ANDROID16_REAL_IMPLEMENTATION_GUIDE (1).md` 第 14 章手工真机验收脚本：`14.1 无假信息` 对应 `01-cloud-install-open.mp4`，`14.2 截图分享导入` 对应 `04-cloud-share-text.mp4` 且必须从系统截图浮层分享合成图片到拾刻，`14.3 确认后打开日历`、`14.5 地图`、`14.6 删除原截图` 对应 `09-cloud-final-route.mp4`，`14.4 通知权限与提醒` 对应 `05-cloud-permission-fallback.mp4`，`14.7 最近截图助手` 对应 `08-cloud-ui-polish.mp4`。

## 课程通知链路

| 步骤 | 操作 | 预期 |
|---|---|---|
| 1 | 点“选择截图” | 首页显示 AI 解析进度，导入页可查看识别到的文字 |
| 2 | 必要时编辑“识别到的文字” | 文本可编辑，云端解析会使用编辑后的内容 |
| 3 | 保持默认云端 AI 配置 | 解析状态显示正在处理 |
| 4 | 点“生成行动卡” | 返回课程通知结构化字段 |
| 5 | 编辑标题、时间、地点或状态并点“确认并安排” | 今日行动台和收件箱同步更新 |
| 6 | 点“打开日历” | 仅在确认并安排后可点；打开系统日历新增页，标题和地点预填 |

录屏时同时扫过“风险与缺失字段”，确认相对时间和系统写入权限不是黑盒执行。

## 活动海报链路

| 步骤 | 操作 | 预期 |
|---|---|---|
| 1 | 点“拍照导入”并授权相机 | 显示拍照预览和活动 OCR 草稿 |
| 2 | 点“生成行动卡” | 返回活动海报结构化字段 |
| 3 | 点“确认并安排” | 当前行动卡持久化，设置提醒和查看路线按钮变为可用 |
| 4 | 点“设置提醒” | Android 13+ 申请通知权限，授权后调度本地定时提醒；拒绝通知权限时保留行动卡并把提醒按钮改成“去开启通知”；exact-alarm 不可用时降级为普通定时 |
| 5 | 点“查看路线” | 打开 `geo:` deeplink |

## 扩展场景抽查

| 场景 | 操作 | 预期 |
|---|---|---|
| 作业截止 | 手动输入“数据库实验报告今晚22:00前通过教学平台提交”后解析 | 场景显示作业截止，动作包含截止提醒，用户确认前不可执行 |
| 会议通知 | 分享或粘贴“项目周会今晚10:00在腾讯会议进行” | 场景显示会议通知，地点为腾讯会议，缺字段时保留人工确认 |
| 面试通知 | 粘贴“HR通知明天14:00线上会议室面试” | 场景显示面试通知，动作包含面试日历和提醒 |
| 出行票务 | 拍照或手动输入“高铁出行今晚10:00在西安北站集合” | 场景显示出行票务，地图动作指向集合地点 |

## 降级与失败验收

| 场景 | 操作 | 预期 |
|---|---|---|
| 云端不可用 | 停掉 FastAPI 后生成行动卡 | 解析状态显示云端暂不可用，并进入本地待确认 |
| 相机权限拒绝 | 拒绝 `CAMERA` | 页面提示改用相册或文本分享入口 |
| 字段不可信 | 点“忽略” | 当前卡片状态变为“已忽略” |
| 应用重启 | 关闭应用后重新打开 | `SharedPreferences` 恢复当前行动卡、采集来源和后端地址；未过期提醒通过 `restoreScheduledReminder` 重新调度 |
| 设备重启 | 重启设备后重新打开拾刻 | `BootReminderReceiver` 接收 `BOOT_COMPLETED` 并恢复未过期待触发提醒 |
| 清除拾刻缓存 | 点“隐私与端云设置”里的“清除拾刻缓存”，再点“确认清除” | App 内二次确认后 `cancelScheduledReminder` 取消系统待触发提醒并清空本地提醒记录；不会删除系统相册原截图 |
| 精确闹钟策略 | 运行执行层守卫 | `setExactAndAllowWhileIdle`、`canScheduleExactAlarms` 和普通定时 fallback 均被 `ACTION_EXECUTION_METRIC 18/18` 覆盖 |

## 最终验收命令

```bash
bash shike/android-mvp/build_apk.sh
python3 shike/validation/validate_android_structure.py
python3 shike/validation/validate_android_unit_tests.py
python3 shike/validation/validate_android_image_preprocess.py
python3 shike/validation/validate_action_execution.py
python3 shike/validation/validate_demo_acceptance.py
python3 shike/validation/validate_real_world_ready.py
python3 shike/scripts/verify_core20_package.py "/path/to/拾刻_核心20文件交付包_20260505"
```

以上命令通过后，可将 APK、录屏证据、`device-runbook.md` 和本清单一起交给评审或队友复测。录屏只使用合成样例，录制前隐藏通知栏、账号、相册真实图片和局域网敏感地址。
