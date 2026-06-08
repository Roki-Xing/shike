# Cloud Device Manifest

Status: staging package

## Required videos

- `01-cloud-install-open.mp4`
- `02-cloud-gallery-bluelm.mp4`
- `03-cloud-camera-bluelm.mp4`
- `04-cloud-share-text.mp4`
- `05-cloud-permission-fallback.mp4`
- `06-cloud-backend-failure.mp4`
- `07-cloud-restart-restore.mp4`
- `08-cloud-ui-polish.mp4`
- `09-cloud-final-route.mp4`

## Required text artifacts

- `cloud-device-test-report.md`
- `cloud-device-logcat.txt`
- `backend-redacted-access-log.txt`
- `apk-sha256.txt`
- `cloud-device-capture-todo.md`
- `README.md`

## Related release handoff files

- Prep helper: `python3 shike/scripts/prepare_cloud_device_evidence.py`
- Current prep gate: `CLOUD_DEVICE_PREP_METRIC 5/5`
- Expected pre-recording video gap: `CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9`
- `materials/evidence/release-evidence-index.md`
- Release evidence gate: `RELEASE_EVIDENCE_INDEX_METRIC 10/10`
- Current handoff summary: `docs/optimization-log.md`
- README public entrypoint is part of the release evidence index.
- Desktop guidance source: `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md`
- `materials/evidence/requirement-matrix.md`
- Requirement matrix gate: `REQUIREMENT_MATRIX_METRIC 9/9`
- Before recording, complete the `cloud-device-test-report.md` `Pre-recording Evidence Gate`: confirm the desktop guidance source, `REQUIREMENT_MATRIX_METRIC 9/9`, all 9 real cloud-device MP4 files, and no placeholder fields remain after capture; this manifest is only a staging checklist and must not be treated as release-ready strict evidence.
- `materials/evidence/blocking-report.md`
- Default local release gate: `LANDING_RELEASE_CANDIDATE_METRIC 63/63`
- Expected strict blocker before real recordings/report: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7`

## Capture notes

- Use a HTTPS backend URL on cloud devices.
- Keep backend URLs, AppKEY, OCR text, and personal data redacted.
- Record at least one fallback path and one restart-restore path.
