# Shike Desktop Guidance Requirement Matrix

Status: local evidence is traceable; strict cloud-device release evidence is still blocked by real external capture requirements.

Source guidance: `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md`

Source file availability: see `materials/evidence/desktop-guidance-source-status.md`. As of the 2026-05-31 closeout audit, the expected desktop file has been restored from the Windows recycle bin and is readable at that path, so this matrix proves repository-local Stage A-E traceability against a current source file while strict cloud-device proof remains externally blocked.

## Summary

| Phase | Guidance Goal | Local Status | Strict Status | Primary Gate |
|---|---|---|---|---|
| Stage A | BlueLM credible evidence | PASS | PASS for redacted backend log; no secrets stored | `BLUELM_ADAPTER_METRIC 8/8` |
| Stage B | Cloud-device and HTTPS backend evidence | PASS for prep helper, public backend preflight, package skeleton, Android 16 aggregate guide gate, Android 16 DoD coverage gate, adb collection helper, explicit image-semantic cases, live-smoke evidence, and handoff runner | BLOCKED until real cloud-device MP4 files and filled report exist | `CLOUD_DEVICE_PREP_METRIC 5/5`; `CLOUD_BACKEND_PREFLIGHT_METRIC`; `CLOUD_DEVICE_PACKAGE_METRIC 30/30`; `ANDROID16_REAL_IMPLEMENTATION_GUIDE_METRIC 12/12`; `ANDROID16_DOD_COVERAGE_METRIC 28/28`; `IMAGE_SEMANTIC_CASES_METRIC 9/9`; `LIVE_SMOKE_EVIDENCE_METRIC 7/7`; `RELEASE_HANDOFF_CHECKS_METRIC 24/24` |
| Stage C | Frontend productization | PASS | Uses local Android/UI validators | `FRONTEND_POLISH_METRIC 12/12` |
| Stage D | Long-lived inbox workbench | PASS | Uses local Android/persistence validators | `INBOX_WORKBENCH_LANDING_METRIC 12/12` |
| Stage E | Materials upgraded to release evidence package | PASS for local handoff | BLOCKED only where Stage B external evidence is missing | `RELEASE_EVIDENCE_INDEX_METRIC 10/10` |

## Stage A - BlueLM Credible Evidence

Guidance asks the project to prove that Shike can use the contest model without putting credentials into Android, source files, docs, logs, or APKs.

Implemented evidence:

- `backend/requirements.txt` includes `requests` for the BlueLM adapter path.
- `backend/shike_backend/adapters/bluelm_adapter.py` builds `/v1/chat/completions` requests with a backend-only bearer token from `BLUELM_APP_KEY`.
- `backend/shike_backend/adapters/vivo_auth.py` is documented as AI Gateway fallback/reference, not the active chat-completions auth path.
- `docs/bluelm-integration-runbook.md` records the vivo doc-center distinction between `thinking.type`, `enable_thinking`, `requestId`, and `request_id`.
- `materials/evidence/cloud-device/backend-redacted-access-log.txt` contains only redacted backend evidence: `provider=bluelm`, `result_schema_valid=true`, `request_id`, and OCR length.
- Android calls the Shike FastAPI backend only; it does not hold BlueLM AppID/AppKEY.

Mechanical proof:

```bash
python3 shike/validation/validate_secret_hygiene.py
python3 shike/validation/validate_bluelm_adapter.py
python3 shike/validation/validate_model_contract_strict.py
python3 shike/backend/verify_backend.py
python3 shike/backend/shike_backend/eval/run_model_eval.py --progress-every 25
```

Current evidence tokens:

- `PASS secret_hygiene`
- `BLUELM_ADAPTER_METRIC 8/8`
- `MODEL_CONTRACT_STRICT_METRIC 10/10`
- `backend_passed`
- `MODEL_EVAL_METRIC 110/110`
- `provider=bluelm`
- `result_schema_valid=true`

## Stage B - Cloud-Device And HTTPS Backend

Guidance asks the project to move beyond local `10.0.2.2` / LAN-only testing and produce cloud-device evidence against a HTTPS backend.

Implemented evidence:

- `docs/device-runbook.md` separates emulator, USB device, and cloud-device network modes.
- `validation/validate_cloud_backend_ready.py` verifies runtime backend configuration support for cloud-hosted HTTPS deployment.
- `docs/server-deployment-runbook.md` documents the `https://roky.chat` / `https://api.roky.chat` HTTPS deployment shape, `/opt/shike/backend`, `/etc/shike/shike-backend.env`, `systemd`, Nginx, certbot, public smoke checks, and redacted log boundaries without storing AppKEY values.
- `backend/shike_backend/eval/http_server_smoke.py` starts a temporary uvicorn server and exercises `/health`, `/v2/schema`, and `POST /v2/analyze-image` over real HTTP while scanning the server log for secret markers.
- `validation/validate_live_smoke_evidence.py` mechanically validates the redacted private-env live smoke log without storing AppKEY, full OCR text, image payloads, or PII.
- `materials/evidence/cloud-device/` contains the evidence package skeleton, manifest, capture TODO, APK hash, redacted access log, placeholder test report, and README.
- `scripts/prepare_cloud_device_evidence.py` refreshes `apk-sha256.txt` and `cloud-device-capture-todo.md` before operators collect real cloud-device recordings.
- `materials/evidence/blocking-report.md` lists the exact strict blockers and next actions.

Mechanical proof:

```bash
python3 shike/scripts/prepare_cloud_device_evidence.py
python3 shike/scripts/test_collect_cloud_device_evidence.py
python3 shike/scripts/test_preflight_cloud_backend.py
python3 shike/validation/validate_live_smoke_evidence.py
python3 shike/scripts/run_release_handoff_checks.py --strict
python3 shike/validation/validate_android16_real_implementation_guide.py
python3 shike/validation/validate_android16_definition_of_done.py
python3 shike/validation/validate_cloud_backend_ready.py
python3 shike/validation/validate_cloud_device_package.py
python3 shike/validation/validate_release_blocking_report.py
python3 shike/validation/validate_landing_release_candidate.py --strict
```

Current evidence tokens:

- `CLOUD_DEVICE_PREP_METRIC 5/5`
- `CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9`
- `CLOUD_BACKEND_PREFLIGHT_METRIC`
- `CLOUD_BACKEND_READY_METRIC 9/9`
- `http_server_smoke_metric=1/1`
- `docs/server-deployment-runbook.md`
- `CLOUD_DEVICE_PACKAGE_METRIC 30/30`
- `ANDROID16_REAL_IMPLEMENTATION_GUIDE_METRIC 12/12`
- `ANDROID16_DOD_COVERAGE_METRIC 28/28`
- `IMAGE_SEMANTIC_CASES_METRIC 9/9`
- `LIVE_SMOKE_EVIDENCE_METRIC 7/7`
- `RELEASE_HANDOFF_CHECKS_METRIC 24/24`
- `RELEASE_BLOCKING_REPORT_METRIC 8/8`
- `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7`

Strict blockers that must remain explicit:

- Missing 9 real cloud-device MP4 recordings:
  - `01-cloud-install-open.mp4`
  - `02-cloud-gallery-bluelm.mp4`
  - `03-cloud-camera-bluelm.mp4`
  - `04-cloud-share-text.mp4`
  - `05-cloud-permission-fallback.mp4`
  - `06-cloud-backend-failure.mp4`
  - `07-cloud-restart-restore.mp4`
  - `08-cloud-ui-polish.mp4`
  - `09-cloud-final-route.mp4`
- `materials/evidence/cloud-device/cloud-device-test-report.md` still contains `TBD` placeholders.

## Stage C - Frontend Productization

Guidance asks the app to look like a real product instead of a long debugging console.

Implemented evidence:

- `android-mvp/app/src/main/java/cn/shike/app/ui/MainFlowScreens.kt` owns product-facing screens:
  - `HomeActionScreen`
  - `CaptureHubScreen`
  - `ParseConfirmScreen`
  - `ActionPlanScreen`
  - `InboxScreen`
  - `PrivacySettingsScreen`
- `android-mvp/app/src/main/java/cn/shike/app/ui/DebugDemoScreen.kt` owns debugging and delivery self-check surfaces.
- `android-mvp/app/src/main/java/cn/shike/app/ui/ShikeDesignTokens.kt` centralizes design tokens.
- `android-mvp/app/src/main/java/cn/shike/app/ui/FrontendStateComponents.kt` covers loading, empty, error, permission, and backend-failed states.

Mechanical proof:

```bash
python3 shike/validation/validate_frontend_polish.py
python3 shike/validation/validate_android_structure.py
python3 shike/validation/validate_android_unit_tests.py
python3 shike/validation/validate_demo_acceptance.py
```

Current evidence tokens:

- `FRONTEND_POLISH_METRIC 12/12`
- `ANDROID_STRUCTURE_METRIC 31/31`
- `ANDROID_UNIT_TEST_METRIC 88/88`
- `ANDROID_IMAGE_PREPROCESS_METRIC 15/15`
- `LocalMultimodalStatus` covers the optional端侧 3B boundary without claiming the APK bundles a usable model.
- `LocalMultimodalRuntime` covers the optional runtime contract: `init(multimodal=true) -> callVit -> generate -> schema_valid -> 待确认`, without bundling credentials or claiming the SDK is installed.
- `DEMO_ACCEPTANCE_METRIC 18/18`

## Stage D - Long-Lived Inbox Workbench

Guidance asks the inbox to become a durable workbench rather than one transient action card.

Implemented evidence:

- `android-mvp/app/src/main/java/cn/shike/app/data/InboxDatabase.kt` provides the local SQLite-backed inbox store.
- `android-mvp/app/src/main/java/cn/shike/app/data/InboxEntities.kt` defines:
  - `InboxItemEntity`
  - `CaptureDraftEntity`
  - `ActionDraftEntity`
  - `ExecutionResultEntity`
- `android-mvp/app/src/main/java/cn/shike/app/data/InboxSeedFactory.kt` covers 50 synthetic seed records.
- `android-mvp/app/src/main/java/cn/shike/app/data/LegacyInboxSnapshot.kt` covers old snapshot migration.
- UI supports status filters, search, archive, restore, OCR/model/execution details, and all-status priority ordering.

Mechanical proof:

```bash
python3 shike/validation/validate_inbox_workbench_landing.py
python3 shike/validation/validate_android_unit_tests.py
python3 shike/validation/validate_real_world_ready.py
```

Current evidence tokens:

- `INBOX_WORKBENCH_LANDING_METRIC 12/12`
- `ANDROID_UNIT_TEST_METRIC 88/88`
- `REAL_WORLD_READY_METRIC 22/22`

## Stage E - Materials Upgraded To Release Evidence

Guidance asks the submission package to show real engineering evidence: BlueLM, cloud-device status, frontend, failure fallback, privacy, model evaluation, and scoring mapping.

Implemented evidence:

- `materials/evidence/release-evidence-index.md` is the local release evidence index.
- `materials/evidence/desktop-guidance-source-status.md` records whether the original desktop guidance file is currently readable.
- `materials/evidence/blocking-report.md` is the strict external-evidence blocker report.
- `materials/submission-checklist.md` references the release evidence package and strict blocker boundary.
- `materials/device-demo-checklist.md` links demo capture expectations and release-candidate commands.
- `docs/delivery-boundary-and-scoring.md` maps scoring categories to code, docs, validators, and evidence files.
- `docs/current-validation-status.md` lists the baseline commands and current pass/block status, and its Guide header is anchored to `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md`.
- `validation/validate_landing_release_candidate.py` aggregates 53 local release-candidate checks while keeping strict external proof separate.

Mechanical proof:

```bash
python3 shike/validation/validate_deliverables.py
python3 shike/validation/validate_release_evidence_index.py
python3 shike/validation/validate_landing_release_candidate.py
python3 shike/validation/validate_landing_release_candidate.py --strict
```

Current evidence tokens:

- `DELIVERABLES_METRIC 10/10`
- `RELEASE_EVIDENCE_INDEX_METRIC 10/10`
- `REQUIREMENT_MATRIX_METRIC 9/9`
- `LANDING_RELEASE_CANDIDATE_METRIC 63/63`
- `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7`

## Final Blocking Boundary

Do not mark strict release complete until these external facts exist:

1. A real HTTPS backend URL reachable by the cloud device has been used during recording.
2. `cloud-device-test-report.md` includes a completed `Pre-recording Evidence Gate`.
3. All 9 real cloud-device MP4 files exist and are non-empty.
4. `cloud-device-test-report.md` has no `TBD`, `TODO`, `待补录`, or `待采集` placeholders, so no placeholder fields remain after capture.
5. Logs and videos remain redacted: no AppKEY, backend token, full OCR text, phone number, email, student ID, or personal notification content.
6. The original desktop guidance source remains readable at `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md` before claiming the desktop-guidance objective itself is fully re-verified.
