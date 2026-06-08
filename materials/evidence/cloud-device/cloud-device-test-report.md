# Cloud Device Test Report

- 机型: TBD
- Android 版本: TBD
- 测试时间: TBD
- 后端地址: TBD
- 后端地址脱敏: TBD
- 结果: TBD

## Pre-recording Evidence Gate

- Desktop guidance source checked: `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md`
- Android 16 real implementation guide checked: `/mnt/c/Users/Xing/Desktop/SHIKE_ANDROID16_REAL_IMPLEMENTATION_GUIDE (1).md`
- Android 16 Definition of Done checked: `validation/validate_android16_definition_of_done.py`
- Requirement matrix checked: `materials/evidence/requirement-matrix.md`
- Requirement matrix gate: `REQUIREMENT_MATRIX_METRIC 9/9`
- Android 16 guide gate: `ANDROID16_REAL_IMPLEMENTATION_GUIDE_METRIC 12/12`
- Android 16 DoD gate: `ANDROID16_DOD_COVERAGE_METRIC 28/28`
- Strict release gate before filling this report: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7`
- Do not mark strict release evidence as passed until all 9 real cloud-device MP4 files are present and this report has no placeholder fields.

## Summary

- 安装与打开: TBD
- 相册导入: TBD
- 拍照导入: TBD
- 分享导入: TBD
- 权限降级: TBD
- 后端失败回退: TBD
- 重启恢复: TBD
- UI 体验: TBD

## Android 16 Guide Acceptance Coverage

- 14.1 无假信息: `01-cloud-install-open.mp4` - 只显示系统状态栏；页面内无 10:28 / 100% / 固定 5月24日。
- 14.2 截图分享导入: `04-cloud-share-text.mp4` - 从系统截图浮层分享图片到拾刻，显示缩略图，用户点击开始识别后才请求后端。
- 14.3 确认后打开日历: `09-cloud-final-route.mp4` - 用户确认后打开系统日历新增页，标题/时间/地点带入。
- 14.4 通知权限与提醒: `05-cloud-permission-fallback.mp4` - 通知权限允许/拒绝都有可恢复状态，提醒不在确认前执行。
- 14.5 地图: `09-cloud-final-route.mp4` - 确认后打开地图或复制地点 fallback。
- 14.6 删除原截图: `09-cloud-final-route.mp4` - MediaStore 系统删除确认后行动卡仍保留并显示删除状态。
- 14.7 最近截图助手: `08-cloud-ui-polish.mp4` - 最近截图助手默认关闭，开启后只提示导入，关闭后不再提示。

## Video Evidence

- `01-cloud-install-open.mp4`: TBD
- `02-cloud-gallery-bluelm.mp4`: TBD
- `03-cloud-camera-bluelm.mp4`: TBD
- `04-cloud-share-text.mp4`: TBD
- `05-cloud-permission-fallback.mp4`: TBD
- `06-cloud-backend-failure.mp4`: TBD
- `07-cloud-restart-restore.mp4`: TBD
- `08-cloud-ui-polish.mp4`: TBD
- `09-cloud-final-route.mp4`: TBD
