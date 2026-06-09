# Shike Release Evidence Index

Status: local release-candidate ready; strict external cloud-device evidence remains blocked until real recordings are collected.

## Local Readiness Gates

| Gate | Command | Current Evidence |
|---|---|---|
| Release candidate | `python3 shike/validation/validate_landing_release_candidate.py` | `LANDING_RELEASE_CANDIDATE_METRIC 63/63` |
| Real-world readiness | `python3 shike/validation/validate_real_world_ready.py` | `REAL_WORLD_READY_METRIC 22/22` |
| Cloud-device prep helper | `python3 shike/scripts/prepare_cloud_device_evidence.py` | `CLOUD_DEVICE_PREP_METRIC 5/5` |
| HTTPS backend deployment readiness | `python3 shike/validation/validate_cloud_backend_ready.py` | `CLOUD_BACKEND_READY_METRIC 9/9`; `docs/server-deployment-runbook.md` covers `https://roky.chat`, `https://api.roky.chat`, `/etc/shike/shike-backend.env`, `/opt/shike/backend`, systemd, Nginx, certbot, public smoke checks, `shike_backend.eval.http_server_smoke`, and redacted log boundaries |
| Backend audit log | `python3 shike/validation/validate_backend_audit_log.py` | `BACKEND_AUDIT_LOG_METRIC 8/8`; guards `/v2/analyze-image` metadata-only audit events, `input_id_hash`, PII redaction, and no raw Authorization/AppKEY/base64/full-OCR/input-id logging |
| Cloud-device package skeleton | `python3 shike/validation/validate_cloud_device_package.py` | `CLOUD_DEVICE_PACKAGE_METRIC 30/30` |
| Release handoff runner | `python3 shike/scripts/run_release_handoff_checks.py --strict` | `RELEASE_HANDOFF_CHECKS_METRIC 24/24` with `validate_android16_definition_of_done.py`, `validate_image_semantic_cases.py`, and `validate_live_smoke_evidence.py` explicit in the handoff and strict gates treated as expected blockers before real recordings |
| Live smoke evidence gate | `python3 shike/validation/validate_live_smoke_evidence.py` | `LIVE_SMOKE_EVIDENCE_METRIC 7/7`; mechanically checks the redacted backend log for BlueLM text parsing, vivo OCR image clearing, multimodal fallback from `Volc-DeepSeek-V3.2` to `Doubao-Seed-2.0-mini`, route-v2 schema validity, user-confirmation action gate, ignored-region allowlist, `live_smoke_metric=4/4`, and no AppKEY/token/base64/PII leakage |
| Strict blocker quality | `python3 shike/validation/validate_release_blocking_report.py` | `RELEASE_BLOCKING_REPORT_METRIC 8/8` |
| BlueLM adapter plumbing | `python3 shike/validation/validate_bluelm_adapter.py` | `BLUELM_ADAPTER_METRIC 8/8` |
| vivo OCR adapter plumbing | `python3 shike/validation/validate_vivo_ocr_adapter.py` | `VIVO_OCR_ADAPTER_METRIC 11/11` |
| vivo multimodal image contract | `python3 shike/validation/validate_vivo_multimodal_contract.py` | `VIVO_MULTIMODAL_CONTRACT_METRIC 28/28`; guards `/v2/analyze-image`, image data URL payloads, OCR block enrichment, ignored UI chrome regions, ignored-region metadata allowlist, `VIVO_MULTIMODAL_MODELS` candidate chaining, default vivo VisionChat model selection, signed VisionChat fallback through `/vivogpt/completions`, Shike UI chrome copy filtering, prompt location/action gate rules, `allow_cloud_image=false` no-cloud-image fallback, text-model fallback, final server-side user-confirmation action gate, and route-level smoke support |
| Desktop guidance traceability | `python3 shike/validation/validate_requirement_matrix.py` | `REQUIREMENT_MATRIX_METRIC 9/9` |
| User research evidence boundary | `python3 shike/validation/validate_user_research_evidence.py` | `USER_RESEARCH_EVIDENCE_METRIC 8/8`; real interviews and survey metrics remain `待采集` and must not be fabricated |
| Deliverables traceability | `python3 shike/validation/validate_deliverables.py` | `DELIVERABLES_METRIC 10/10`; `validation/traceability.md` SHIKE-070 includes release evidence metrics |
| Secret hygiene | `python3 shike/validation/validate_secret_hygiene.py` | `PASS secret_hygiene`; includes repository text scanning plus the APK artifact gate |
| APK secret hygiene | `python3 shike/validation/validate_apk_secret_hygiene.py` | `APK_SECRET_HYGIENE_METRIC 8/8`; scans local and desktop APK zip entries for `sk-*` tokens, provider secret env names, vivo direct endpoints, and exact private env values without printing secrets |
| No default image upload | `python3 shike/validation/validate_no_default_image_upload.py` | `NO_DEFAULT_IMAGE_UPLOAD_METRIC 12/12`; import/share/screenshot-assist/manual paths stay local until the user explicitly triggers backend image analysis |
| Android 16 real implementation guide | `python3 shike/validation/validate_android16_real_implementation_guide.py` | `ANDROID16_REAL_IMPLEMENTATION_GUIDE_METRIC 12/12`; aggregates guide tasks SHIKE-P0-001 through SHIKE-P1-012 across fake-device removal, unified `CaptureDraft`, image share import, screenshot cleanup, vivo multimodal/OCR, action execution, home slimming, screenshot assist, and optional local 3B boundaries |
| Android 16 Definition of Done | `python3 shike/validation/validate_android16_definition_of_done.py` | `ANDROID16_DOD_COVERAGE_METRIC 28/28`; maps guide section 19 functional, evidence, and safety DoD to executable gates while keeping missing cloud-device MP4/report/logcat proof explicit as strict external blockers |

Android 16 guide source: `/mnt/c/Users/Xing/Desktop/SHIKE_ANDROID16_REAL_IMPLEMENTATION_GUIDE (1).md`. Cloud-device operators must keep this file readable before recording, then confirm `ANDROID16_REAL_IMPLEMENTATION_GUIDE_METRIC 12/12` still maps SHIKE-P0-001 through SHIKE-P1-012.
| Android 16 screenshot flow | `python3 shike/validation/validate_android16_screenshot_flow.py` | `ANDROID16_SCREENSHOT_FLOW_METRIC 18/18`; guards targetSdk 36, edge-to-edge safeDrawing Insets, image/text share import, visible-only screen capture callback, page-level screenshot prompt, Photo Picker handoff, system MediaStore confirmation, screenshot-assist privacy copy, and Android provider-secret isolation |
| Screenshot assist | `python3 shike/validation/validate_screenshot_assist.py` | `SCREENSHOT_ASSIST_METRIC 15/15`; guards the opt-in recent screenshot helper, restart-persistent switch, clear-cache reset, 30-second MediaStore lookback, notification candidate metadata preservation, notification confirmation, repeated-candidate notification dedupe, no overlay/accessibility main path, display-name digesting, and screenshot detection that requires filename or path screenshot signals instead of screen-size-only matches |
| No fake device chrome | `python3 shike/validation/validate_no_fake_device_chrome.py` | `NO_FAKE_DEVICE_CHROME_METRIC 1/1`; production Android/prototype surfaces do not draw fake status time, battery, fixed date, fake device chrome, or historical phone-frame copy |
| One-screen home | `python3 shike/validation/validate_home_one_screen.py` | `HOME_ONE_SCREEN_METRIC 9/9`; guards fixed bottom navigation, four user tabs, compact home action surface, no debug/backend controls on home, and hidden developer entry |
| Screenshot cleanup | `python3 shike/validation/validate_screenshot_cleanup.py` | `SCREENSHOT_CLEANUP_METRIC 15/15`; guards system-confirmed MediaStore delete flow, no silent delete, user-facing cleanup status copy, App-internal cache-clear confirmation, and current-card cleanup result persistence |
| Android image preprocessing | `python3 shike/validation/validate_android_image_preprocess.py` | `ANDROID_IMAGE_PREPROCESS_METRIC 15/15`; guards `ImagePayloadPreprocessor`, `ImageThumbnailCache`, input MIME magic-byte detection, non-image rejection, EXIF normalization, 1600px long-edge sampling, screenshot UI chrome crop, private thumbnail cache, JPEG data URL generation, dimensions, and SHA-256 image identity |

## Model Evidence

- Regression set: `validation/regression-cases.json` contains 110 synthetic cases.
- Image semantic set: `validation/fixtures/image_cases.json` contains 40 synthetic screenshot/photo semantic cases and is guarded by `IMAGE_SEMANTIC_CASES_METRIC 9/9`; its negative cases explicitly require `unknown` output, empty actions, task/time/location missing fields, and own-UI/navigation/status-region forbidden evidence so Shike pages, bottom tabs, and status-bar text cannot become action-card fields.
- Model eval case gate: `python3 shike/validation/validate_model_eval_cases.py` produces `MODEL_EVAL_CASES_METRIC 9/9` and includes the image semantic case gate.
- Full local model eval: `python3 shike/backend/shike_backend/eval/run_model_eval.py --progress-every 25` produces `MODEL_EVAL_METRIC 110/110`.
- BlueLM adapter gate: `BLUELM_ADAPTER_METRIC 8/8` verifies provider switch, safe fallback without credentials, vivo doc-center model body variants (`thinking.type` for DeepSeek/Doubao, `enable_thinking` for qwen, `BLUELM_THINKING_MODE=provider_default`, and `requestId` / `request_id` configurability), and `current_date` context for relative-time normalization.
- vivo OCR adapter gate: `VIVO_OCR_ADAPTER_METRIC 11/11` verifies server-side `/v1/ocr`, official `/ocr/general_recognition` form parameters (`image`, `pos`, `businessid=aigc + AppID`, `requestId`), missing-credential fallback, Android secret isolation, and the secret-safe `backend/shike_backend/eval/live_smoke.py` runner.
- vivo multimodal contract gate: `VIVO_MULTIMODAL_CONTRACT_METRIC 28/28` verifies `/v2/analyze-image`, image data URL payloads, OCR blocks, ignored-region filtering, ignored-region metadata allowlist, Shike UI chrome copy filtering, prompt location/action gate rules, vivo multimodal request shape, `VIVO_MULTIMODAL_MODELS` candidate chaining, default `vivo-BlueLM-V-2.0` / `BlueLM-Vision-prd` VisionChat candidates, signed VisionChat fallback through `/vivogpt/completions` when OpenAI-compatible image routes reject the request, `allow_cloud_image=false` no-cloud-image fallback with `cloud_image_disabled` evidence, OCR+BlueLM text fallback after image candidates fail, a final server-side user-confirmation action gate that overwrites model-claimed executable actions, and the route-level smoke runner.
- Redacted live BlueLM smoke evidence: `materials/evidence/cloud-device/backend-redacted-access-log.txt` contains `provider=bluelm`, `result_schema_valid=true`, `scene_type=course_notice`, and non-sensitive latency/input-length fields.
- Redacted live vivo OCR smoke evidence: the same log contains `provider=vivo_general_ocr`, `ocr_status=pass`, `image_persisted=false`, `image_cleared=true`, and non-sensitive `ocr_text_length` fields.
- Redacted live smoke evidence gate: `python3 shike/validation/validate_live_smoke_evidence.py` produces `LIVE_SMOKE_EVIDENCE_METRIC 7/7` and turns the combined private-env live smoke into a mechanical handoff check.
- Combined live model smoke with backend private env: `PYTHONPATH=shike/backend python3 -m shike_backend.eval.live_smoke --ocr-image /tmp/shike-live-course-notice.png --multimodal --multimodal-image /tmp/shike-live-course-notice.png --route-v2 --route-v2-image /tmp/shike-live-course-notice.png --timeout-seconds 60` produced `live_smoke_metric=4/4`, with BlueLM text parsing, vivo General OCR, vivo multimodal image parsing, and route-level `/v2/analyze-image` all passing through redacted evidence. `route_v2_actions_disabled=true` confirms all downstream actions remain user-confirmation-gated.
- Live smoke runner: `PYTHONPATH=shike/backend python3 -m shike_backend.eval.live_smoke --ocr-image /path/to/synthetic-course-notice.png --route-v2 --route-v2-image /path/to/synthetic-course-notice.png --timeout-seconds 35` prints redacted `provider`, `result_schema_valid`, `ocr_provider`, `image_persisted=false`, route-v2 schema/action-gate fields, `route_v2_ignored_regions_allowed=true`, and `live_smoke_metric` lines without printing credentials, full OCR text, or base64 image content. Latest secret-safe synthetic smoke produced `live_smoke_metric=3/3`.
- Native image-input evidence remains split: the checked redacted release log still preserves the earlier `live_smoke_metric=4/4` success evidence, while the latest direct probe with the current test key reached the new signed VisionChat fallback but the vision models returned `legacy_http_status:401`. `/v2/analyze-image` still keeps OCR + BlueLM text fallback for image-provider failures and every downstream action remains user-confirmation-gated by the backend before the response leaves the route.
- Route-v2 smoke runner: `PYTHONPATH=shike/backend python3 -m shike_backend.eval.live_smoke --skip-bluelm --skip-ocr --route-v2 --route-v2-image /path/to/synthetic-course-notice.png --timeout-seconds 35` calls FastAPI `POST /v2/analyze-image` through `TestClient` and prints only redacted fields: `route_v2_http_status=200`, `route_v2_status=pass`, `route_v2_schema_valid=true`, `route_v2_actions_disabled=true`, `route_v2_ignored_regions_allowed=true`, `route_v2_ignored_regions=top_status_bar,bottom_navigation_bar`, and `live_smoke_metric=1/1`.
- Android still calls the Shike backend only; BlueLM/OCR AppID/AppKEY stay server-side.
- APK secret hygiene: `python3 shike/validation/validate_apk_secret_hygiene.py` proves the built Android artifacts do not embed AppKEY-like tokens, provider secret variable names, vivo direct endpoints, or backend private env values.

## Cloud-Device Evidence

- Evidence folder: `materials/evidence/cloud-device/`
- Prep helper: `python3 shike/scripts/prepare_cloud_device_evidence.py` currently produces `CLOUD_DEVICE_PREP_METRIC 5/5`, expected `CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9`, and expected `CLOUD_DEVICE_PREP_REPORT_VIDEO_TBD_FIELDS 9/9` before real cloud recordings are collected and report video notes are filled.
- HTTPS backend deployment runbook: `docs/server-deployment-runbook.md`
- Deployment readiness gate: `python3 shike/validation/validate_cloud_backend_ready.py` currently produces `CLOUD_BACKEND_READY_METRIC 9/9`.
- Real HTTP server smoke: `PYTHONPATH=shike/backend python3 -m shike_backend.eval.http_server_smoke --timeout-seconds 35 --disable-cloud-image` starts a temporary uvicorn server, calls `/health`, `/v2/schema`, and `POST /v2/analyze-image`, proves the deterministic no-cloud-image route with `allow_cloud_image=false`, checks `http_smoke_actions_disabled=True` and `http_smoke_ignored_regions_allowed=True`, scans the server log for secret markers, and currently produces `http_server_smoke_metric=1/1`.
- Handoff runner: `python3 shike/scripts/run_release_handoff_checks.py --strict` runs the local release handoff gates and confirms strict gates remain expected blockers; use `--strict-ready` only after the MP4 files, report, and logcat are complete.
- Public backend preflight: `python3 shike/scripts/test_preflight_cloud_backend.py` guards the helper and `python3 shike/scripts/preflight_cloud_backend.py --base-url https://roky.chat` must print `CLOUD_BACKEND_PREFLIGHT_METRIC` with redacted evidence before cloud-device recording.
- ADB collection helper: `python3 shike/scripts/collect_cloud_device_evidence.py --list` lists the 9 required cloud-device recording scenarios; `--record <1-9>` captures real MP4s with `adb screenrecord`, and `--capture-logcat --write-report-draft` exports redacted logcat plus a report draft. The helper is guarded by `python3 shike/scripts/test_collect_cloud_device_evidence.py` and does not fabricate strict evidence.
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
- The SHIKE-070 row links submission materials to `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md`, `RELEASE_EVIDENCE_INDEX_METRIC 10/10`, `REQUIREMENT_MATRIX_METRIC 9/9`, `ANDROID16_REAL_IMPLEMENTATION_GUIDE_METRIC 12/12`, `ANDROID16_DOD_COVERAGE_METRIC 28/28`, `IMAGE_SEMANTIC_CASES_METRIC 9/9`, `LIVE_SMOKE_EVIDENCE_METRIC 7/7`, `CLOUD_DEVICE_PREP_METRIC 5/5`, expected `CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9`, `CLOUD_DEVICE_PACKAGE_METRIC 30/30`, `RELEASE_HANDOFF_CHECKS_METRIC 24/24`, and expected strict `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7`.

## User Research Evidence

- Research plan: `docs/user-research-plan.md`
- Interview summary template: `docs/user-interview-summary.md`
- Scoring evidence map: `materials/evidence/scoring-evidence-map.md`
- User research gate: `USER_RESEARCH_EVIDENCE_METRIC 8/8`
- Traceability row: `validation/traceability.md` SHIKE-075 links the application-value evidence package to `docs/user-research-plan.md`, `docs/user-interview-summary.md`, and `materials/evidence/scoring-evidence-map.md`.
- Boundary: real interviews, survey counts, privacy preferences, and missed-action examples remain `待采集`; do not fabricate interview data or present planned evidence as collected user validation.

## Optimization Handoff Trace

- Current handoff summary: `docs/optimization-log.md`
- The first visible optimization-log entry records the current handoff state, including `CLOUD_DEVICE_PACKAGE_METRIC 30/30`, `RELEASE_HANDOFF_CHECKS_METRIC 24/24`, `BACKEND_AUDIT_LOG_METRIC 8/8`, `LIVE_SMOKE_EVIDENCE_METRIC 7/7`, `IMAGE_SEMANTIC_CASES_METRIC 9/9`, `CLOUD_BACKEND_PREFLIGHT_METRIC`, `ANDROID16_REAL_IMPLEMENTATION_GUIDE_METRIC 12/12`, `ANDROID16_DOD_COVERAGE_METRIC 28/28`, `RELEASE_EVIDENCE_INDEX_METRIC 10/10`, `REQUIREMENT_MATRIX_METRIC 9/9`, default release `LANDING_RELEASE_CANDIDATE_METRIC 63/63`, `VIVO_OCR_ADAPTER_METRIC 11/11`, `VIVO_MULTIMODAL_CONTRACT_METRIC 28/28`, signed VisionChat fallback, Shike UI chrome copy filtering, prompt location/action gate rules, ignored-region metadata allowlist, `allow_cloud_image=false` no-cloud-image fallback, `cloud_image_disabled`, `NO_DEFAULT_IMAGE_UPLOAD_METRIC 12/12`, `ANDROID_IMAGE_PREPROCESS_METRIC 15/15`, route-v2 smoke evidence, and expected strict `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7`.
- Historical optimization-log entries keep their original evidence values because they describe earlier rounds; use this index and the latest log entry for the current release handoff.

## Redaction Rules

- Do not record or commit AppKEY, backend tokens, full OCR text, phone numbers, emails, student IDs, or personal notifications.
- Keep backend logs redacted to method, path, status, provider, schema-valid flag, request_id, and non-sensitive lengths.
- Use only synthetic screenshots, camera content, share text, and manual input during demos.

## Rebuild Evidence Checklist

```bash
python3 shike/scripts/prepare_cloud_device_evidence.py
python3 shike/scripts/test_collect_cloud_device_evidence.py
python3 shike/scripts/test_preflight_cloud_backend.py
python3 shike/validation/validate_cloud_backend_ready.py
python3 shike/validation/validate_backend_audit_log.py
python3 shike/validation/validate_cloud_device_package.py
python3 shike/validation/validate_live_smoke_evidence.py
python3 shike/scripts/run_release_handoff_checks.py --strict
python3 shike/validation/validate_user_research_evidence.py
python3 shike/validation/validate_requirement_matrix.py
python3 shike/validation/validate_deliverables.py
python3 shike/validation/validate_release_evidence_index.py
python3 shike/validation/validate_bluelm_adapter.py
python3 shike/validation/validate_vivo_ocr_adapter.py
python3 shike/validation/validate_vivo_multimodal_contract.py
python3 shike/validation/validate_image_semantic_cases.py
python3 shike/validation/validate_model_eval_cases.py
python3 shike/validation/validate_landing_release_candidate.py
python3 shike/validation/validate_release_blocking_report.py
python3 shike/validation/validate_landing_release_candidate.py --strict
python3 shike/validation/validate_real_world_ready.py
python3 shike/validation/validate_apk_secret_hygiene.py
python3 shike/validation/validate_no_default_image_upload.py
python3 shike/validation/validate_android16_real_implementation_guide.py
python3 shike/validation/validate_android16_definition_of_done.py
python3 shike/validation/validate_android16_screenshot_flow.py
python3 shike/validation/validate_screenshot_assist.py
python3 shike/validation/validate_no_fake_device_chrome.py
python3 shike/validation/validate_home_one_screen.py
python3 shike/validation/validate_screenshot_cleanup.py
python3 shike/validation/validate_android_image_preprocess.py
python3 shike/validation/validate_secret_hygiene.py
```
