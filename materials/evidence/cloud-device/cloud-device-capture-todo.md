# Cloud Device Capture TODO

Use this file as the operator checklist before running strict validation.

## Current Missing Evidence
- Missing videos: 9/9
- Report fields still TBD: 14/14
- Report video evidence still TBD: 9/9
- Rerun this helper after adding MP4 files or editing the report; this section is generated from the current evidence package.

### Missing Videos
- `01-cloud-install-open.mp4`
- `02-cloud-gallery-bluelm.mp4`
- `03-cloud-camera-bluelm.mp4`
- `04-cloud-share-text.mp4`
- `05-cloud-permission-fallback.mp4`
- `06-cloud-backend-failure.mp4`
- `07-cloud-restart-restore.mp4`
- `08-cloud-ui-polish.mp4`
- `09-cloud-final-route.mp4`

### Report Fields Still TBD
- 机型
- Android 版本
- 测试时间
- 后端地址
- 后端地址脱敏
- 结果
- 安装与打开
- 相册导入
- 拍照导入
- 分享导入
- 权限降级
- 后端失败回退
- 重启恢复
- UI 体验

### Report Video Evidence Still TBD
- `01-cloud-install-open.mp4`
- `02-cloud-gallery-bluelm.mp4`
- `03-cloud-camera-bluelm.mp4`
- `04-cloud-share-text.mp4`
- `05-cloud-permission-fallback.mp4`
- `06-cloud-backend-failure.mp4`
- `07-cloud-restart-restore.mp4`
- `08-cloud-ui-polish.mp4`
- `09-cloud-final-route.mp4`

## Required Videos
- [ ] `01-cloud-install-open.mp4`
- [ ] `02-cloud-gallery-bluelm.mp4`
- [ ] `03-cloud-camera-bluelm.mp4`
- [ ] `04-cloud-share-text.mp4`
- [ ] `05-cloud-permission-fallback.mp4`
- [ ] `06-cloud-backend-failure.mp4`
- [ ] `07-cloud-restart-restore.mp4`
- [ ] `08-cloud-ui-polish.mp4`
- [ ] `09-cloud-final-route.mp4`

## Report Fields
- [ ] 机型
- [ ] Android 版本
- [ ] 测试时间
- [ ] 后端地址
- [ ] 后端地址脱敏
- [ ] 结果
- [ ] 安装与打开
- [ ] 相册导入
- [ ] 拍照导入
- [ ] 分享导入
- [ ] 权限降级
- [ ] 后端失败回退
- [ ] 重启恢复
- [ ] UI 体验

### Report Evidence Gate Fields
- [ ] Pre-recording Evidence Gate
- [ ] Desktop guidance source checked
- [ ] Requirement matrix checked
- [ ] Requirement matrix gate
- [ ] Strict release gate before filling this report
- [ ] All 9 real cloud-device MP4 files present
- [ ] No placeholder fields remain after capture

## Report Video Evidence Section
- [ ] Add a `## Video Evidence` section to `cloud-device-test-report.md`.
- [ ] List all 9 MP4 filenames in that section after recording.
- [ ] Replace every video evidence `TBD` note with a concise redacted result note.
- [ ] Keep video notes concise and redacted; do not paste backend tokens, raw OCR text, or personal data.

## Pre-capture Checks
- [ ] Run `python3 shike/scripts/prepare_cloud_device_evidence.py` before capture and confirm `CLOUD_DEVICE_PREP_METRIC 5/5`.
- [ ] Confirm `CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9` is the expected pre-capture state until the real cloud-device recordings are present.
- [ ] Use a HTTPS backend URL that the cloud device can reach.
- [ ] Keep AppKEY, backend tokens, full OCR text, phone numbers, emails, and student IDs out of videos, logs, and filenames.
- [ ] Capture one backend success path with `provider=bluelm` and `result_schema_valid=true` in the redacted backend log.
- [ ] Capture one permission fallback path, one backend failure fallback path, and one restart-restore path.

## Release Handoff
- [ ] Confirm `materials/evidence/release-evidence-index.md` references this capture package.
- [ ] Confirm `RELEASE_EVIDENCE_INDEX_METRIC 10/10` still passes, including `docs/optimization-log.md` current handoff summary and README public entrypoint checks.
- [ ] Confirm `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md` remains the desktop guidance source before recording.
- [ ] Confirm `materials/evidence/requirement-matrix.md` still maps stages A-E to local evidence and strict cloud-device blockers, then confirm `REQUIREMENT_MATRIX_METRIC 9/9`.
- [ ] Confirm `materials/evidence/blocking-report.md` still lists any missing strict evidence.
- [ ] Keep the default local gate at `LANDING_RELEASE_CANDIDATE_METRIC 52/52`.
- [ ] Keep strict release blocked at `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7` until real recordings and the filled report are collected.

## Strict Validation

```bash
python3 shike/validation/validate_cloud_device_package.py
python3 shike/validation/validate_release_evidence_index.py
python3 shike/validation/validate_cloud_device_package.py --strict
python3 shike/validation/validate_landing_release_candidate.py --strict
```
