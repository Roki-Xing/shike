# Shike Release-Candidate Blocking Report

Strict release mode is blocked by external evidence gaps. No secret values are required in this file.

## Missing Evidence
- `strict_cloud_device_package_passes`: validate_cloud_device_package.py --strict
- `strict_cloud_videos_present`: 9 cloud mp4 files
- `strict_report_has_no_tbd`: cloud-device-test-report.md
- `strict_logcat_not_placeholder`: cloud-device-logcat.txt

## Missing Cloud Videos

- [ ] `materials/evidence/cloud-device/01-cloud-install-open.mp4`
- [ ] `materials/evidence/cloud-device/02-cloud-gallery-bluelm.mp4`
- [ ] `materials/evidence/cloud-device/03-cloud-camera-bluelm.mp4`
- [ ] `materials/evidence/cloud-device/04-cloud-share-text.mp4`
- [ ] `materials/evidence/cloud-device/05-cloud-permission-fallback.mp4`
- [ ] `materials/evidence/cloud-device/06-cloud-backend-failure.mp4`
- [ ] `materials/evidence/cloud-device/07-cloud-restart-restore.mp4`
- [ ] `materials/evidence/cloud-device/08-cloud-ui-polish.mp4`
- [ ] `materials/evidence/cloud-device/09-cloud-final-route.mp4`

## Report Fields Still Placeholder

- `- 机型: TBD`
- `- Android 版本: TBD`
- `- 测试时间: TBD`
- `- 后端地址: TBD`
- `- 后端地址脱敏: TBD`
- `- 结果: TBD`
- `- 安装与打开: TBD`
- `- 相册导入: TBD`
- `- 拍照导入: TBD`
- `- 分享导入: TBD`
- `- 权限降级: TBD`
- `- 后端失败回退: TBD`
- `- 重启恢复: TBD`
- `- UI 体验: TBD`
- `- `01-cloud-install-open.mp4`: TBD`
- `- `02-cloud-gallery-bluelm.mp4`: TBD`
- `- `03-cloud-camera-bluelm.mp4`: TBD`
- `- `04-cloud-share-text.mp4`: TBD`
- `- `05-cloud-permission-fallback.mp4`: TBD`
- `- `06-cloud-backend-failure.mp4`: TBD`
- `- `07-cloud-restart-restore.mp4`: TBD`
- `- `08-cloud-ui-polish.mp4`: TBD`
- `- `09-cloud-final-route.mp4`: TBD`

## Required Next Actions

1. Record every missing MP4 listed above on a cloud device using a HTTPS backend URL.
2. Fill every placeholder line in `cloud-device-test-report.md` with redacted real device evidence.
3. Replace `cloud-device-logcat.txt` placeholder text with redacted session-level diagnostics from the actual cloud-device run.
4. In the report's `Pre-recording Evidence Gate`, confirm the desktop guidance source, requirement matrix file, `REQUIREMENT_MATRIX_METRIC 9/9`, `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7`, all 9 real cloud-device MP4 files, and no placeholder fields remain after capture.
5. Refresh `apk-sha256.txt` and `cloud-device-capture-todo.md` with `python3 shike/scripts/prepare_cloud_device_evidence.py`, then confirm `CLOUD_DEVICE_PREP_METRIC 5/5` and the expected pre-capture state `CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9`.
6. Rerun `python3 shike/validation/validate_cloud_device_package.py` so the non-strict package handoff remains at `CLOUD_DEVICE_PACKAGE_METRIC 27/27` before strict validation.
7. Rerun `python3 shike/validation/validate_release_evidence_index.py` so the release evidence index still matches the refreshed cloud-device package.
8. Rerun `python3 shike/validation/validate_requirement_matrix.py` so the desktop guidance stages A-E still map to refreshed cloud-device blockers.
9. Before recording, confirm `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md` is still the desktop guidance source and `materials/evidence/requirement-matrix.md` still passes `REQUIREMENT_MATRIX_METRIC 9/9`.
10. Keep AppKEY, backend tokens, full OCR text, phone numbers, emails, and student IDs out of videos, logs, and filenames.
11. Rerun `python3 shike/validation/validate_landing_release_candidate.py --strict`.
