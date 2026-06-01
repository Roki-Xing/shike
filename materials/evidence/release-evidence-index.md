# Shike Release Evidence Index

Status: local release-candidate ready; strict external cloud-device evidence remains blocked until real recordings are collected.

## Local Readiness Gates

| Gate | Command | Current Evidence |
|---|---|---|
| Release candidate | `python3 shike/validation/validate_landing_release_candidate.py` | `LANDING_RELEASE_CANDIDATE_METRIC 52/52` |
| Real-world readiness | `python3 shike/validation/validate_real_world_ready.py` | `REAL_WORLD_READY_METRIC 22/22` |
| Cloud-device prep helper | `python3 shike/scripts/prepare_cloud_device_evidence.py` | `CLOUD_DEVICE_PREP_METRIC 5/5` |
| Cloud-device package skeleton | `python3 shike/validation/validate_cloud_device_package.py` | `CLOUD_DEVICE_PACKAGE_METRIC 27/27` |
| Strict blocker quality | `python3 shike/validation/validate_release_blocking_report.py` | `RELEASE_BLOCKING_REPORT_METRIC 8/8` |
| BlueLM adapter plumbing | `python3 shike/validation/validate_bluelm_adapter.py` | `BLUELM_ADAPTER_METRIC 7/7` |
| Desktop guidance traceability | `python3 shike/validation/validate_requirement_matrix.py` | `REQUIREMENT_MATRIX_METRIC 9/9` |
| Deliverables traceability | `python3 shike/validation/validate_deliverables.py` | `DELIVERABLES_METRIC 10/10`; `validation/traceability.md` SHIKE-070 includes release evidence metrics |
| Secret hygiene | `python3 shike/validation/validate_secret_hygiene.py` | `PASS secret_hygiene` |

## Model Evidence

- Regression set: `validation/regression-cases.json` contains 110 synthetic cases.
- Full local model eval: `python3 shike/backend/shike_backend/eval/run_model_eval.py --progress-every 25` produces `MODEL_EVAL_METRIC 110/110`.
- BlueLM adapter gate: `BLUELM_ADAPTER_METRIC 7/7` verifies provider switch, safe fallback without credentials, and vivo doc-center model body variants (`thinking.type` for DeepSeek/Doubao, `enable_thinking` for qwen, `BLUELM_THINKING_MODE=provider_default`, and `requestId` / `request_id` configurability).
- Redacted live BlueLM smoke evidence: `materials/evidence/cloud-device/backend-redacted-access-log.txt` contains `provider=bluelm` and `result_schema_valid=true`.
- Android still calls the Shike backend only; BlueLM AppID/AppKEY stay server-side.

## Cloud-Device Evidence

- Evidence folder: `materials/evidence/cloud-device/`
- Prep helper: `python3 shike/scripts/prepare_cloud_device_evidence.py` currently produces `CLOUD_DEVICE_PREP_METRIC 5/5`, expected `CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9`, and expected `CLOUD_DEVICE_PREP_REPORT_VIDEO_TBD_FIELDS 9/9` before real cloud recordings are collected and report video notes are filled.
- APK hash: `materials/evidence/cloud-device/apk-sha256.txt`
- Capture checklist: `materials/evidence/cloud-device/cloud-device-capture-todo.md`
- Strict blocker report: `materials/evidence/blocking-report.md`
- Strict release command: `python3 shike/validation/validate_landing_release_candidate.py --strict`
- Current strict status: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7`
- Before cloud-device recording, re-confirm `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md` remains the desktop guidance source and `materials/evidence/requirement-matrix.md` still passes `REQUIREMENT_MATRIX_METRIC 9/9`; the local release evidence index must not be treated as release-ready strict proof.

Missing external proof:
- Nine real cloud-device MP4 recordings listed in `materials/evidence/cloud-device/cloud-device-capture-todo.md`
- Completed `materials/evidence/cloud-device/cloud-device-test-report.md` with placeholders removed

## Desktop Guidance Traceability

- Requirement matrix: `materials/evidence/requirement-matrix.md`
- Desktop source availability note: `materials/evidence/desktop-guidance-source-status.md`
- Matrix gate: `REQUIREMENT_MATRIX_METRIC 9/9`
- It maps `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md` stages A-E to local evidence, validation commands, and the remaining strict cloud-device blockers.
- Current closeout note: the expected desktop source file was restored from the Windows recycle bin and is readable at that path, so the matrix is again tied to a current source file. This still does not turn local evidence into strict cloud-device proof.
- Deliverables traceability: `validation/traceability.md`
- Deliverables gate: `DELIVERABLES_METRIC 10/10`
- The SHIKE-070 row links submission materials to `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md`, `RELEASE_EVIDENCE_INDEX_METRIC 10/10`, `REQUIREMENT_MATRIX_METRIC 9/9`, `CLOUD_DEVICE_PREP_METRIC 5/5`, expected `CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9`, `CLOUD_DEVICE_PACKAGE_METRIC 27/27`, and expected strict `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7`.

## Optimization Handoff Trace

- Current handoff summary: `docs/optimization-log.md`
- The first visible optimization-log entry records `CLOUD_DEVICE_PACKAGE_METRIC 27/27`, `RELEASE_EVIDENCE_INDEX_METRIC 10/10`, `REQUIREMENT_MATRIX_METRIC 9/9`, default release `LANDING_RELEASE_CANDIDATE_METRIC 52/52`, and expected strict `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7`.
- Historical optimization-log entries keep their original evidence values because they describe earlier rounds; use this index and the latest log entry for the current release handoff.

## Redaction Rules

- Do not record or commit AppKEY, backend tokens, full OCR text, phone numbers, emails, student IDs, or personal notifications.
- Keep backend logs redacted to method, path, status, provider, schema-valid flag, request_id, and non-sensitive lengths.
- Use only synthetic screenshots, camera content, share text, and manual input during demos.

## Rebuild Evidence Checklist

```bash
python3 shike/scripts/prepare_cloud_device_evidence.py
python3 shike/validation/validate_cloud_device_package.py
python3 shike/validation/validate_requirement_matrix.py
python3 shike/validation/validate_deliverables.py
python3 shike/validation/validate_release_evidence_index.py
python3 shike/validation/validate_bluelm_adapter.py
python3 shike/validation/validate_landing_release_candidate.py
python3 shike/validation/validate_release_blocking_report.py
python3 shike/validation/validate_landing_release_candidate.py --strict
python3 shike/validation/validate_real_world_ready.py
python3 shike/validation/validate_secret_hygiene.py
```
