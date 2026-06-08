# Cloud Device Evidence Package

This folder stages the cloud-device evidence bundle for Shike.

Populate it with the recorded videos and redacted text artifacts listed in
`cloud-device-manifest.md`, including `cloud-device-test-report.md`.

Use this folder together with the release handoff files:

- `materials/evidence/release-evidence-index.md` is the top-level evidence index.
- `RELEASE_EVIDENCE_INDEX_METRIC 10/10` is the current release evidence index gate, including `docs/optimization-log.md` current handoff summary and README public entrypoint checks.
- `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md` is the desktop guidance source for the current landing-readiness audit.
- `materials/evidence/requirement-matrix.md` maps the desktop guidance stages A-E to local evidence and strict cloud-device blockers, guarded by `REQUIREMENT_MATRIX_METRIC 9/9`.
- `materials/evidence/blocking-report.md` lists the current strict evidence blockers.
- `python3 shike/validation/validate_landing_release_candidate.py` must stay at `LANDING_RELEASE_CANDIDATE_METRIC 63/63`.
- `python3 shike/validation/validate_landing_release_candidate.py --strict` is expected to stay blocked at `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7` until the real cloud-device recordings and filled report are collected.

Before recording, refresh the APK hash and generate the operator checklist:

```bash
python3 shike/scripts/prepare_cloud_device_evidence.py
python3 shike/scripts/test_preflight_cloud_backend.py
python3 shike/scripts/preflight_cloud_backend.py --base-url https://roky.chat
python3 shike/scripts/collect_cloud_device_evidence.py --preflight-backend --backend-url https://roky.chat
python3 shike/scripts/collect_cloud_device_evidence.py --list
```

The prep helper must pass at `CLOUD_DEVICE_PREP_METRIC 5/5`. Until the real cloud-device recordings are collected, `CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9` is the expected state and must not be treated as release-ready strict evidence.
The public backend preflight must print `CLOUD_BACKEND_PREFLIGHT_METRIC=1/1` before recording. It uses a synthetic image request with `allow_cloud_image=false` by default, checks `/health`, `/v2/schema`, and `/v2/analyze-image`, and redacts the public host in its evidence output.
`collect_cloud_device_evidence.py --preflight-backend` runs both backend branches in order: the default no-cloud-image preflight and the live image preflight with `--allow-cloud-image`. The redacted access log must keep `allow_cloud_image=true`, `actions_disabled=true`, and `CLOUD_BACKEND_PREFLIGHT_METRIC=1/1` without AppKEY, Authorization headers, base64 image payloads, or full OCR text.
Before recording, also complete the `cloud-device-test-report.md` `Pre-recording Evidence Gate`: confirm the current handoff still points back to `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md`, `REQUIREMENT_MATRIX_METRIC 9/9` still passes, `ANDROID16_DOD_COVERAGE_METRIC 28/28` still passes, all 9 real cloud-device MP4 files are present, and no placeholder fields remain after capture.
The report and generated TODO must also keep an `Android 16 Guide Acceptance Coverage` section that maps the desktop guide's section 14 manual acceptance scripts to the strict videos. In particular, `14.2 截图分享导入` is captured by `04-cloud-share-text.mp4`: the operator must use the system screenshot floating share surface to share a synthetic image into Shike, confirm a thumbnail is shown, and only then tap start analysis. `09-cloud-final-route.mp4` covers confirmed calendar, map, and original-screenshot deletion flows.

For a connected cloud device or USB device with adb access, use the collection
helper to record each real scenario and then export redacted logcat plus a
report draft:

```bash
python3 shike/scripts/collect_cloud_device_evidence.py --record 1 --duration-seconds 180
python3 shike/scripts/collect_cloud_device_evidence.py --capture-logcat --write-report-draft --backend-url https://roky.chat
```

The helper only automates capture mechanics. It does not fabricate videos,
report results, or logcat content; review the generated report before running
strict-ready gates.

Then run:

```bash
python3 shike/scripts/test_collect_cloud_device_evidence.py
python3 shike/scripts/test_preflight_cloud_backend.py
python3 shike/validation/validate_cloud_device_package.py
python3 shike/validation/validate_live_smoke_evidence.py
python3 shike/scripts/run_release_handoff_checks.py --strict
python3 shike/validation/validate_cloud_device_package.py --strict
```

The non-strict check must pass at `CLOUD_DEVICE_PACKAGE_METRIC 30/30`; it validates package structure, device-runbook release handoff steps, release handoff links, the generated capture TODO handoff template, the release evidence `10/10` gate, the desktop guidance matrix pointer, the Android 16 DoD pre-capture gate, the public backend preflight, the `run_release_handoff_checks.py` runner, the expected strict blocker state, and redaction surfaces.
The live-smoke evidence check must pass at `LIVE_SMOKE_EVIDENCE_METRIC 7/7`; it mechanically verifies the redacted backend private-env smoke log without storing AppKEY, full OCR text, or image payloads.
The handoff runner must pass at `RELEASE_HANDOFF_CHECKS_METRIC 24/24` with `--strict` while strict evidence is still expected to block. This includes the explicit `IMAGE_SEMANTIC_CASES_METRIC 9/9` screenshot/photo semantic fixture gate from the Android 16 guide and `LIVE_SMOKE_EVIDENCE_METRIC 7/7` from the backend live-smoke gate. Use `--strict-ready` only after the final cloud-device recording set, report, and logcat are complete.

Do not put AppKEY, backend tokens, full OCR text, phone numbers, emails,
student IDs, or personal notifications in videos, logs, filenames, or reports.
