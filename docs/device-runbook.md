# 设备联调 Runbook

对应目标：让拾刻 MVP 从“可构建”推进到“可真机验证”。

## 前置条件

- 已构建 APK：`shike/android-mvp/app/build/outputs/apk/debug/app-debug.apk`
- Android 8.0 及以上设备开启开发者选项和 USB 调试；不要求 vivo 专属权限。
- 本机已安装 Android platform-tools，构建脚本会安装到 `~/.local/share/shike-android-tools/android-sdk/platform-tools`。
- Android 结构守卫已通过：`python3 shike/validation/validate_android_structure.py` 输出 `ANDROID_STRUCTURE_METRIC 31/31`。
- Android 本地单元测试守卫已通过：`python3 shike/validation/validate_android_unit_tests.py` 输出 `ANDROID_UNIT_TEST_METRIC 86/86`；最近一次 `gradle --no-daemon :app:testDebugUnitTest` 通过。
- Android 图片预处理守卫已通过：`python3 shike/validation/validate_android_image_preprocess.py` 输出 `ANDROID_IMAGE_PREPROCESS_METRIC 15/15`，覆盖输入 MIME 魔数识别、非图片拒绝、EXIF 旋转、截图 UI chrome 裁剪、`ImageThumbnailCache` 私有缩略图缓存、JPEG data URL 和 SHA-256 合同。
- 后端 smoke test 已通过：`python3 shike/backend/verify_backend.py`

## 安装 APK

```bash
export PATH="$HOME/.local/share/shike-android-tools/android-sdk/platform-tools:$PATH"
adb devices
adb install -r shike/android-mvp/app/build/outputs/apk/debug/app-debug.apk
```

## 真机验证路径

| 验证项 | 操作 | 预期 |
|---|---|---|
| 首页主链路 | 打开拾刻 | 显示今日行动台、导入入口、AI 解析确认、行动编排、收件箱状态 |
| 相册截图 | 点“选择截图”，从系统相册选择图片 | 页面显示采集来源并自动进入云侧图片解析，成功后当前卡片更新为待确认行动卡 |
| 拍照导入 | 点“拍照导入”，授权 `CAMERA` 后拍照 | 页面显示拍照预览和采集来源并自动进入云侧图片解析，成功后当前卡片更新为待确认行动卡 |
| 识别文字 | 在“主链路采集”后编辑“识别到的文字” | 文本/手动路径会把编辑后的文本作为 `/v1/analyze` 的 `ocr_text`；图片路径会把它作为 `/v2/analyze-image` 的 `ocr_text_hint` |
| 离线兜底 | 点“课程样例”或“活动样例” | 无图片、无网络时仍可演示两类核心样例 |
| 后端地址 | 真机默认使用 `https://roky.chat`；模拟器本地调试可手动填 `http://10.0.2.2:8000`；USB 真机可填电脑局域网地址后点“保存后端地址” | 地址保存到本地配置，旧安装里的 `http://10.0.2.2:8000` 会自动迁移到公网 HTTPS 后端 |
| 后端解析 | 确认公网 `https://roky.chat/health` 可用后导入图片，或点后端解析入口手动重试 | 文本/手动草稿请求 `${后端地址}/v1/analyze`；相册截图、系统图片分享、最近截图助手和相机预览请求 `${后端地址}/v2/analyze-image`，并用响应更新行动卡 |
| source_type 合同 | 文本路径保留 `screenshot`、`camera`、`share_text`、`manual`；图片路径使用 `photo_picker`、`screenshot_share`、`recent_screenshot_assist`、`camera`、`manual` | v2 图片合同不破坏 v1 文本合同，旧回归样例和 schema 继续可验证 |
| 后端回退 | 不启动 FastAPI 时点后端解析按钮 | 页面显示后端失败，并回退本地 MockModelAdapter 行动卡 |
| 手动修正 | 在“AI 解析确认”里编辑任务标题、时间、地点或状态后点“确认并安排” | 当前行动卡更新并保存到收件箱缓存 |
| 忽略低置信度 | 点“忽略” | 当前行动卡状态变为“已忽略”，避免直接进入执行 |
| 重启恢复 | 选择截图、拍照或样例后杀掉应用再打开 | 当前行动卡和采集来源从 `SharedPreferences` 收件箱缓存恢复；未过期待触发提醒通过 `restoreScheduledReminder` 重新调度 |
| 设备重启恢复 | 安排提醒后重启设备并打开拾刻 | `BootReminderReceiver` 接收 `BOOT_COMPLETED`，恢复未过期待触发提醒 |
| 日历动作 | 点“确认并安排”后点“打开日历” | 打开系统日历新增事件页，标题和地点已预填 |
| 提醒动作 | 点“确认并安排”后点“设置提醒” | Android 13+ 会请求 `POST_NOTIFICATIONS`，授权后调度本地提醒；拒绝通知权限时保留行动卡并把提醒按钮改成“去开启通知”；exact-alarm 可用时走精确定时，不可用时降级为普通定时 |
| 地图动作 | 点“确认并安排”后点“查看路线” | 打开 `geo:` deeplink，地点为当前卡片地点 |
| 分享入口 | 从其他应用分享一段文本到拾刻 | 拾刻作为文本分享目标出现，并生成“分享导入”的待确认行动卡；未点“确认并安排”前不落盘 |

## 权限说明

| 权限 | Manifest 名称 | 触发时机 | 降级 |
|---|---|---|---|
| 通知 | `POST_NOTIFICATIONS` | 用户确认字段后点击“提醒”时申请 | 权限拒绝时保留收件箱卡片 |
| 日历 | 无日历读写权限 | 当前使用系统日历插入 Intent，不直接写 Calendar Provider | 系统日历不可用时保留行动卡 |
| 相机 | `CAMERA` | 用户点击“拍照导入”时申请 | 权限拒绝时改用相册、文本分享或离线样例 |

## 后端联调

启动服务：

```bash
cd shike/backend
python3 -m uvicorn shike_backend.main:app --host 0.0.0.0 --port 8000
```

`--host 0.0.0.0` 仅用于可信局域网真机联调。不要暴露到公网，不要粘贴真实聊天、教务通知或邮件 OCR；演示结束后停止服务。

## 云真机联调

云真机通常不能访问 `10.0.2.2` 或电脑局域网地址，必须改用公网可达的 HTTPS 后端。

| 设备类型 | 后端地址示例 | 说明 |
|---|---|---|
| 真机默认 | `https://roky.chat` | 公网 HTTPS 后端，推荐演示使用 |
| 模拟器 | `http://10.0.2.2:8000` | 仅宿主机调试可用 |
| USB 真机 | `http://192.168.1.10:8000` | 同一局域网内可用 |
| 云真机 | `https://your-domain.example.com` | 需要 HTTPS，可公开访问 |

云真机证据包建议放在 `materials/evidence/cloud-device/`，结构校验命令：

```bash
python3 shike/scripts/prepare_cloud_device_evidence.py
python3 shike/validation/validate_cloud_device_package.py
python3 shike/validation/validate_live_smoke_evidence.py
python3 shike/scripts/run_release_handoff_checks.py --strict
python3 shike/validation/validate_release_evidence_index.py
python3 shike/validation/validate_cloud_device_package.py --strict
```

当前 prep helper 门禁为 `CLOUD_DEVICE_PREP_METRIC 5/5`，在未收齐真实云真机录屏前 `CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9` 是预期状态；录制前还要运行 `test_preflight_cloud_backend.py` 和 `preflight_cloud_backend.py --base-url https://roky.chat`，确认 `CLOUD_BACKEND_PREFLIGHT_METRIC` 且输出不包含密钥。当前非 strict 交接门禁为 `CLOUD_DEVICE_PACKAGE_METRIC 30/30`，发布证据索引门禁为 `RELEASE_EVIDENCE_INDEX_METRIC 10/10`，截图语义样例门禁为 `IMAGE_SEMANTIC_CASES_METRIC 9/9`，live-smoke 脱敏证据门禁为 `LIVE_SMOKE_EVIDENCE_METRIC 7/7`，集中 strict 复验入口为 `RELEASE_HANDOFF_CHECKS_METRIC 24/24`。云真机录制前还必须确认 `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md` 仍是桌面指导源，且 `materials/evidence/requirement-matrix.md` 的 `REQUIREMENT_MATRIX_METRIC 9/9` 仍通过。`docs/optimization-log.md` 的当前交接摘要是 release handoff 的可追溯入口；历史条目保留当时数值，不应用来替代当前 release evidence index。strict 发布仍必须阻断，直到 `materials/evidence/cloud-device/` 内 9 个真实云真机 MP4 和填写后的 `cloud-device-test-report.md` 都存在。

本地接口：

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/v1/schema
curl -X POST http://127.0.0.1:8000/v1/analyze \
  -H 'Content-Type: application/json' \
  -d '{"input_id":"demo","source_type":"screenshot","ocr_text":"高数A班今晚18:30改到B203，作业第5章今晚22:00前提交。","scene_hint":"course_notice"}'
curl -X POST http://127.0.0.1:8000/v1/analyze \
  -H 'Content-Type: application/json' \
  -d '{"input_id":"demo-share","source_type":"share_text","ocr_text":"AI应用分享会 4月24日19:30 图书馆报告厅 报名截止今晚22:00","scene_hint":"event_poster"}'
curl -X POST http://127.0.0.1:8000/v1/analyze \
  -H 'Content-Type: application/json' \
  -d '{"input_id":"demo-manual","source_type":"manual","ocr_text":"高数A班今晚18:30改到B203，作业第5章今晚22:00前提交。","scene_hint":"course_notice"}'
```

Android 真机默认访问 `https://roky.chat`。模拟器访问宿主机服务使用 `10.0.2.2:8000`；真机局域网联调时在应用内“后端地址”输入同一局域网内电脑 IP，例如 `http://192.168.1.10:8000`，点“保存后端地址”，并确保电脑防火墙允许 8000 端口。

## 离线 MockModelAdapter

当前 Android MVP 不依赖在线模型即可演示主链路。离线验证通过 `MockModelAdapter` 和 Spike 完成：

```bash
python3 shike/spike/run_spike.py --all
```

离线模式覆盖：

- 课程通知结构化输出。
- 活动海报结构化输出。
- 权限拒绝时从日历/地图动作降级到本地行动卡和复制地点。
- 低置信度内容进入待确认，不自动执行。

## 失败排查

| 问题 | 检查 |
|---|---|
| APK 安装失败 | 重新运行 `bash shike/android-mvp/build_apk.sh`，检查 `build-report.md` |
| 分享入口不出现 | 确认分享内容 MIME type 为 `text/plain` |
| 选择截图无结果 | 确认系统相册有图片；也可用“课程样例”继续离线演示 |
| 拍照导入无预览 | 检查 `CAMERA` 授权；权限拒绝时用“活动样例”继续演示 |
| 云端结果仍像样例 | 检查“生成行动卡”前是否已编辑识别到的文字；空草稿会回退当前行动卡文本 |
| 后端解析失败 | 先确认 `https://roky.chat/health` 返回 `{"status":"ok"}`；本地调试时再确认 `python3 -m uvicorn shike_backend.main:app --host 0.0.0.0 --port 8000` 已启动；模拟器使用 `10.0.2.2:8000`，真机局域网调试使用电脑局域网 IP 并点“保存后端地址”；失败时应回退本地 MockModelAdapter |
| 字段不可信 | 在“AI 解析确认”中手动修正后点“确认并安排”；不想执行时点“忽略” |
| 重启后未恢复 | 先完成一次截图、拍照、样例或分享导入；确认页面出现“本地恢复：已保存到收件箱缓存” |
| 通知不出现 | Android 13+ 需要授权 `POST_NOTIFICATIONS` |
| 重启后提醒未恢复 | 先确认已经点“设置提醒”并通过 `validate_action_execution.py` 的 `ACTION_EXECUTION_METRIC 18/18`；过期提醒会在恢复时清理 |
| 清除后仍收到提醒 | 重新运行 `validate_action_execution.py`，通过标准为 `ACTION_EXECUTION_METRIC 18/18`；二次确认“清除拾刻缓存”会调用 `cancelScheduledReminder`，不会删除系统相册原截图 |
| 精确闹钟不可用 | Android 12+ 可关闭 exact-alarm 能力 | `ReminderScheduler` 会从 `setExactAndAllowWhileIdle` 降级到普通 `AlarmManager.set`，不会静默丢失提醒 |
| 地图打不开 | 设备无地图应用时保留收件箱卡片，采集来源记录“地图应用不可用” |
| 系统日历不可用 | 保留行动卡，采集来源记录“系统日历不可用”，用户可手动添加日程 |
| 后端返回 422 | 检查 `ocr_text` 是否为空或过短 |
