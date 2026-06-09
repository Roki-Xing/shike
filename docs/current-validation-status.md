# Current Validation Status

Date: 2026-06-09
Guide: `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md`  
Deep review guide applied this round: `/mnt/c/Users/Xing/Desktop/SHIKE_PRODUCT_MANAGER_DEEP_REVIEW_GUIDE.md`
Guide source availability: the expected desktop source file was restored from the Windows recycle bin and is currently readable in this closeout audit; see `materials/evidence/desktop-guidance-source-status.md`. The local matrix remains useful for repository evidence traceability, while strict external cloud-device evidence remains blocked.
Scope: Desktop guidance stages A-E: BlueLM credible evidence, cloud-device and HTTPS backend evidence, frontend productization, long-lived inbox workbench, and materials upgraded to a release evidence package. Historical S2/S3 hardening remains part of the evidence base, but the current public status is anchored to `materials/evidence/requirement-matrix.md` and `REQUIREMENT_MATRIX_METRIC 9/9`.

## 2026-06-09 Closeout Evidence

This closeout pass focused on the real screenshot-to-action product loop: no real gallery/screenshot path may fall back to fixed `MockOcrEngine` / `sampleCourse` values, the home import path now stays on the home screen with staged AI parsing progress, the Android UI displays structured action-card fields without `"null"` copy, screenshot assist uses opt-in MediaStore observation plus a high-priority notification, and ordinary user screens hide backend endpoint, Mock, validation, self-check, and demo tooling copy.

Fresh local evidence from this pass:

| Command | Status | Evidence |
|---|---|---|
| `python3 validation/validate_real_world_ready.py` | PASS | `REAL_WORLD_READY_METRIC 22/22` |
| `python3 validation/validate_landing_release_candidate.py` | PASS | `LANDING_RELEASE_CANDIDATE_METRIC 63/63` |
| `python3 validation/validate_landable.py` | PASS | `LANDABLE_METRIC 16/16` |
| `python3 validation/validate_demo_acceptance.py` | PASS | `DEMO_ACCEPTANCE_METRIC 18/18` |
| `python3 validation/validate_deliverables.py` | PASS | `METRIC 10/10` |
| `python3 validation/validate_no_sample_contamination.py` | PASS | `NO_SAMPLE_CONTAMINATION_METRIC 14/14` |
| `python3 validation/validate_real_ocr_routing.py` | PASS | `REAL_OCR_ROUTING_METRIC 3/3` |
| `python3 validation/validate_no_default_image_upload.py` | PASS | `NO_DEFAULT_IMAGE_UPLOAD_METRIC 12/12` |
| `python3 validation/validate_analyze_progress_ui.py` | PASS | `ANALYZE_PROGRESS_UI_METRIC 7/7` |
| `python3 validation/validate_structured_action_card_ui.py` | PASS | `STRUCTURED_ACTION_CARD_UI_METRIC 8/8` |
| `python3 validation/validate_screenshot_assist.py` | PASS | `SCREENSHOT_ASSIST_METRIC 17/17` |
| `python3 validation/validate_user_facing_copy.py` | PASS | `USER_FACING_COPY_METRIC 13/13` |
| `python3 validation/validate_home_one_screen.py` | PASS | `HOME_ONE_SCREEN_METRIC 10/10` |
| `python3 validation/validate_frontend_polish.py` | PASS | `FRONTEND_POLISH_METRIC 13/13` |
| `python3 validation/validate_screenshot_cleanup.py` | PASS | `SCREENSHOT_CLEANUP_METRIC 15/15` |
| `python3 validation/validate_android_unit_tests.py` | PASS | `ANDROID_UNIT_TEST_METRIC 88/88` |
| `python3 validation/validate_action_execution.py` | PASS | `ACTION_EXECUTION_METRIC 18/18` |
| `python3 validation/validate_advanced_product_beta.py --strict` | PASS | `PRODUCT_BETA_METRIC 30/30` |
| `python3 validation/validate_secret_hygiene.py` | PASS | `PASS secret_hygiene` |
| `python3 validation/validate_apk_secret_hygiene.py` | PASS | `APK_SECRET_HYGIENE_METRIC 8/8` |
| `gradle --no-daemon :app:testDebugUnitTest` from `shike/android-mvp/` | PASS | `BUILD SUCCESSFUL`; local unit suites report 149 tests, 0 failures, 0 errors |
| `bash android-mvp/build_apk.sh` | PASS | APK copied to `/mnt/c/Users/Xing/Desktop/Shike-app-debug.apk`; local and Desktop SHA-256 both `733fd972ac7a1d2a0454acb9a37dd48449b48d2475a49e93156e51288dbcca93` |

Strict external cloud-device evidence remains a separate manual recording gate: the local repository and APK gates pass, but final release proof still requires real cloud-device MP4s, filled report fields, and redacted logcat evidence before strict release status can be claimed.

## Repository Structure Baseline

The current Shike workspace is rooted at `shike/` under `/home/xing-12_26/projects/codex-workspace`.

| Area | Current path | Status |
|---|---|---|
| Android MVP | `shike/android-mvp/` | Present; debug APK exists |
| Android entry code | `shike/android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` | Present; reduced to Android shell responsibilities after model, samples, initial selection, review status mapping, permission decisions, share import mapping, capture import mapping, camera/gallery result application helpers, camera permission launch helper, gallery launch helper, backend trigger helpers, notification permission result helper, notification permission request helper, system action fallback helper, backend client, backend analysis input mapping, backend outcome application, offline sample application helpers, backend endpoint save helper, backend analysis runner, backend URL save helper, local storage, system actions, main screen layout, readiness UI, bottom navigation, home overview UI, summary UI, demo route UI, import UI, confirmation banner UI, parse-confirm UI, action planner UI, inbox UI, shared UI primitives, and the `ShikeApp` composable have been extracted |
| Android app coordinator | `shike/android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt` | Present; owns app-level Compose state, backend orchestration callbacks, OCR draft state, and handoff into `ShikeMainScreen` |
| Android capture launchers | `shike/android-mvp/app/src/main/java/cn/shike/app/CaptureLaunchers.kt` | Present; owns camera/gallery Activity Result launcher wiring, camera permission launch, and user-result callback routing |
| Android capture result actions | `shike/android-mvp/app/src/main/java/cn/shike/app/CaptureResultActions.kt` | Present; owns successful camera/gallery capture selection application and source handoff |
| Android backend actions | `shike/android-mvp/app/src/main/java/cn/shike/app/BackendAnalysisActions.kt` | Present; owns UI-facing backend analysis request kickoff, main-thread result handoff, and request status return |
| Android backend outcome actions | `shike/android-mvp/app/src/main/java/cn/shike/app/BackendOutcomeActions.kt` | Present; owns backend analysis outcome persistence and model-status return |
| Android backend endpoint actions | `shike/android-mvp/app/src/main/java/cn/shike/app/BackendEndpointActions.kt` | Present; owns backend URL save action result and status message return |
| Android backend trigger actions | `shike/android-mvp/app/src/main/java/cn/shike/app/BackendTriggerActions.kt` | Present; owns course/event backend input trigger dispatch |
| Android cloud enhancement actions | `shike/android-mvp/app/src/main/java/cn/shike/app/CloudEnhancementActions.kt` | Present; owns cloud-off local fallback status so disabling cloud enhancement does not call backend parsing |
| Android sample actions | `shike/android-mvp/app/src/main/java/cn/shike/app/SampleActions.kt` | Present; owns offline course/event sample selection application and source labels |
| Android review actions | `shike/android-mvp/app/src/main/java/cn/shike/app/ReviewActions.kt` | Present; owns manually reviewed item persistence mapping and model-status return |
| Android execution result actions | `shike/android-mvp/app/src/main/java/cn/shike/app/ExecutionResultActions.kt` | Present; records calendar, reminder, and map request outcomes after user-confirmed actions |
| Android reminder permission fallback | `shike/android-mvp/app/src/main/java/cn/shike/app/ReminderPermissionFallback.kt` + `shike/android-mvp/app/src/main/java/cn/shike/app/ui/ExecutionActionGate.kt` | Present; owns shared `permission_blocked` persistence source, execution-result copy, and the “去开启通知” reminder recovery label for notification permission denial |
| Android domain model | `shike/android-mvp/app/src/main/java/cn/shike/app/domain/ShikeItem.kt` | Present |
| Android sample data | `shike/android-mvp/app/src/main/java/cn/shike/app/data/SampleItems.kt` | Present |
| Android initial selection mapper | `shike/android-mvp/app/src/main/java/cn/shike/app/data/InitialSelectionMapper.kt` | Present |
| Android review status mapper | `shike/android-mvp/app/src/main/java/cn/shike/app/data/ReviewStatusMapper.kt` | Present |
| Android capture import mapper | `shike/android-mvp/app/src/main/java/cn/shike/app/data/CaptureImportMapper.kt` | Present; owns `CaptureDraft` plus camera/gallery sample item and source selection mapping |
| Android model API client | `shike/android-mvp/app/src/main/java/cn/shike/app/data/ModelApiClient.kt` | Present |
| Android share import mapper | `shike/android-mvp/app/src/main/java/cn/shike/app/data/ShareImportMapper.kt` | Present; maps share-sheet text through `CaptureDraft` before creating the review card |
| Android local inbox store | `shike/android-mvp/app/src/main/java/cn/shike/app/data/LocalInboxStore.kt` | Present; owns snapshot persistence, action-list encode/decode, capture-source sanitization, raw-text sanitization, and one-tap local data clearing for app-scoped preferences |
| Android local data clear actions | `shike/android-mvp/app/src/main/java/cn/shike/app/LocalDataClearActions.kt` | Present; resets the current workbench to an empty local-data-cleared state after the user taps the privacy control, while `MainActivity` cancels any pending scheduled reminder before clearing persistence |
| Android backend config store | `shike/android-mvp/app/src/main/java/cn/shike/app/data/BackendConfigStore.kt` | Present; owns backend URL persistence and UI save normalization helper |
| Android backend analysis runner | `shike/android-mvp/app/src/main/java/cn/shike/app/data/BackendAnalysisRunner.kt` | Present; owns backend input mapping, backend result orchestration, and shared backend-failure fallback copy with redacted OCR evidence |
| Android privacy redaction | `shike/android-mvp/app/src/main/java/cn/shike/app/data/PrivacyRedaction.kt` | Present; redacts 手机号、邮箱、学号 and local network addresses before storing fallback logs |
| Android system actions | `shike/android-mvp/app/src/main/java/cn/shike/app/system/SystemActions.kt` | Present |
| Android reminder scheduler | `shike/android-mvp/app/src/main/java/cn/shike/app/system/ReminderScheduler.kt` | Present; schedules confirmed action cards through `AlarmManager`, prefers `setExactAndAllowWhileIdle` when exact alarms are available, falls back to ordinary `AlarmManager.set` when exact scheduling is unavailable or rejected, persists pending reminder payloads, restores non-expired reminders with `restoreScheduledReminder`, cancels pending alarms with `cancelScheduledReminder`, and clears delivered/expired records |
| Android reminder receiver | `shike/android-mvp/app/src/main/java/cn/shike/app/system/ReminderReceiver.kt` | Present; receives scheduled reminder alarms, maps intent extras through `reminderDeliveryPayloadFrom`, posts the local notification payload, and clears delivered reminder persistence |
| Android boot reminder receiver | `shike/android-mvp/app/src/main/java/cn/shike/app/system/BootReminderReceiver.kt` | Present; receives `BOOT_COMPLETED` and restores non-expired scheduled reminders |
| Android permission decisions | `shike/android-mvp/app/src/main/java/cn/shike/app/system/PermissionDecisions.kt` | Present |
| Android readiness UI sections | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/ReadinessSections.kt` | Present |
| Android bottom navigation UI | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/BottomNavigation.kt` | Present |
| Android bottom nav item UI | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/BottomNavItem.kt` | Present; extracted from bottom navigation UI and covered by Android structure validator |
| Android home overview UI | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/HomeOverview.kt` | Present |
| Android dashboard notification badge UI | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/DashboardNotificationBadge.kt` | Present; extracted from dashboard header UI and covered by Android structure validator |
| Android agenda card UI | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/AgendaCard.kt` | Present; extracted from home overview and covered by Android structure validator |
| Android agenda card footer UI | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/AgendaCardFooter.kt` | Present; extracted from agenda card UI and covered by Android structure validator |
| Android agenda card header UI | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/AgendaCardHeader.kt` | Present; extracted from agenda card UI and covered by Android structure validator |
| Android summary/demo route UI | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/SummarySections.kt` | Present |
| Android demo route step UI | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/DemoRouteStep.kt` | Present; extracted from summary/demo route UI and covered by Android structure validator |
| Android import UI | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/ImportPanel.kt` | Present; shows OCR failure/manual continuation guidance before backend parsing |
| Android import capture actions UI | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/ImportCaptureActions.kt` | Present; extracted from import UI and covered by Android structure validator; includes manual input continue action |
| Android backend analysis controls UI | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/BackendAnalysisControls.kt` | Present; extracted from import UI and covered by Android structure validator |
| Android backend endpoint controls UI | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/BackendEndpointControls.kt` | Present; extracted from import UI and covered by Android structure validator |
| Android offline sample actions UI | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/OfflineSampleActions.kt` | Present; extracted from import UI and covered by Android structure validator |
| Android confirmation banner UI | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/ConfirmBanner.kt` | Present |
| Android confirm banner actions UI | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/ConfirmBannerActions.kt` | Present; extracted from confirmation banner UI and covered by Android structure validator; disables calendar without time and map without location |
| Android parse-confirm UI | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/ParseConfirmPanel.kt` | Present |
| Android parse confirm header UI | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/ParseConfirmHeader.kt` | Present; extracted from parse-confirm UI and covered by Android structure validator |
| Android review risk checklist UI | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/ReviewRiskChecklist.kt` | Present; extracted from parse-confirm UI and covered by Android structure validator; shows low-confidence/manual-review state |
| Android review decision actions UI | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/ReviewDecisionActions.kt` | Present; extracted from parse-confirm UI and covered by Android structure validator |
| Android action planner UI | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/ActionPlannerPanel.kt` | Present; action controls disable calendar without time and map without location |
| Android inbox UI | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/InboxPanel.kt` | Present; includes status filters, search, OCR/model/execution detail, and current-card archive/restore controls backed by `inboxArchiveActionStateFor(...)` |
| Android execution result UI | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/ExecutionResult.kt` | Present; renders pending and requested execution outcomes in planner and inbox detail |
| Android shared UI primitives | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/UiPrimitives.kt` | Present |
| Android main screen layout | `shike/android-mvp/app/src/main/java/cn/shike/app/ui/ShikeMainScreen.kt` | Present |
| Backend | `shike/backend/shike_backend/main.py` | Present; FastAPI smoke passes |
| Backend audit log | `shike/backend/shike_backend/audit_log.py` | Present; owns metadata-only `/v2/analyze-image` audit evidence, records user-controlled `input_id` only as `input_id_hash`, and keeps raw input IDs, AppKEY, Authorization headers, image data URLs, base64 payloads, full OCR text, phone numbers, student IDs, emails, and names out of backend logs |
| Backend verifier | `shike/backend/verify_backend.py` | Present; passes |
| Contracts | `shike/contracts/model-output.schema.json` | Present |
| Prototype | `shike/prototype/index.html`, `shike/prototype/demo.html` | Present; PDF exports also present |
| Validation scripts | `shike/validation/*.py` | Present; baseline commands pass |
| Android structure validator | `shike/validation/validate_android_structure.py` | Present; checks extracted Android source boundaries, file-size caps, callback names, and helper ownership; listed in README mechanical acceptance, device demo checklist, and Demo console |
| Android unit-test validator | `shike/validation/validate_android_unit_tests.py` | Present; checks JUnit wiring, `PrivacyRedactionTest`, `CaptureImportMapperTest`, `ShareImportMapperTest`, `OcrEngineTest`, `InitialSelectionMapperTest`, `ExecutionResultActionsTest`, `ExecutionResultStateTest`, `ReminderPermissionFallbackTest`, `ReviewStatusMapperTest`, `ReviewActionsTest`, `CaptureResultActionsTest`, `ModelExplanationTest`, `ModelApiClientTest` including backend request payload contract fields and `share_text`/`manual` source types, `TodayActionItemMapperTest`, `ExecutionActionGateTest`, `InboxWorkbenchTest` including archive/restore action state and all-status priority ordering, `ReminderPayloadTest` including receiver delivery payload defaults, `BackendAnalysisRunnerTest` including backend-failure fallback copy and current-draft source-type mapping, `BackendEndpointActionsTest`, `BackendTriggerActionsTest`, `BackendOutcomeActionsTest`, `SampleActionsTest`, `InboxEntitiesTest`, `LocalInboxStoreTest` including action-list encode/decode, capture-source sanitization, and raw-text sanitization, `LocalPersistenceBoundaryTest`, `LocalDataClearActionsTest` including App-internal cache-clear confirmation, `CloudEnhancementActionsTest`, `DeveloperModeUnlockTest` for settings version-tap Debug unlock, `LocalMultimodalStatusTest` for optional端侧 3B install/route/failure boundaries, `LocalMultimodalRuntimeTest` for optional端侧 3B `init -> callVit -> generate -> schema_valid -> 待确认` runtime contract, `DateStripTest` for home date sorting-hint copy, `SystemActionsTest` for system calendar insert-page wording, `ScreenCapturePromptTest` for visible screenshot callback boundary copy, latest `testDebugUnitTest` XML results, and documentation references |
| Action execution validator | `shike/validation/validate_action_execution.py` | Present; checks confirmation gating, calendar result wording, timed reminder scheduling, exact-alarm fallback, reminder persistence, app-start restore, device reboot restore, delivery cleanup, local-data-clear reminder cancellation, map fallback, permission fallback, and UI/system boundary separation |
| Today Action ranking validator | `shike/validation/validate_today_ranking.py` | Present; checks 10 synthetic TodayActionItem samples and deterministic S2 ranking rules |
| Model evaluation case validator | `shike/validation/validate_model_eval_cases.py` | Present; checks 110 synthetic model evaluation cases, unique IDs, required scene coverage, low-quality and negative examples |
| Backend scene contract validator | `shike/validation/validate_backend_scene_contract.py` | Present; keeps public response contract conservative (`scene_type` only `course_notice`/`event_poster`/`unknown`, `task.topic` only `course`/`event`/`unknown`) while still allowing assignment/meeting/interview/travel regression groups as input hints that must map to `unknown` output |
| Product Beta validator | `shike/validation/validate_advanced_product_beta.py` | Present; scans the advanced guide's 30 Product Beta readiness checks and prints missing next steps without weakening existing guards |
| Android image preprocessing validator | `shike/validation/validate_android_image_preprocess.py` | Present; checks `ImagePayloadPreprocessor`, `ImageThumbnailCache`, input MIME magic-byte detection, non-image rejection, EXIF rotation, 1600px long-edge sampling, screenshot UI chrome crop, private thumbnail cache, JPEG data URL, dimensions, SHA-256, and `MainActivity` delegation |
| Landing release-candidate validator | `shike/validation/validate_landing_release_candidate.py` | Present; aggregates 61 local checks across BlueLM, vivo OCR, secret hygiene, no-default-image-upload boundary, Android image preprocessing, cloud-device package skeleton, strict blocking-report quality, release evidence index quality, frontend, OCR, execution loop, inbox, privacy, materials, backend, and legacy guards; strict mode adds real BlueLM online evidence and real cloud-device recordings and writes `materials/evidence/blocking-report.md` when external evidence is missing |
| Scoring evidence map | `shike/docs/delivery-boundary-and-scoring.md` | Present; maps innovation, application value, completion, and model-ability scoring claims to code evidence, video/demo evidence, release evidence, `validation/traceability.md` SHIKE-070, `DELIVERABLES_METRIC 10/10`, and expected strict `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7` blocker state |
| User research evidence package | `shike/docs/user-research-plan.md`, `shike/docs/user-interview-summary.md`, `shike/materials/evidence/scoring-evidence-map.md` | Present; `USER_RESEARCH_EVIDENCE_METRIC 8/8` keeps application-value evidence honest by marking real interviews, survey counts, privacy preferences, and missed-action examples as `待采集`; `validation/traceability.md` SHIKE-075 links the package to the public release evidence chain |
| Deck landing evidence package | `shike/materials/preliminary-deck.md` | Present; includes the复赛落地证据包 section for BlueLM evidence, cloud-device testing, real app frontend, failure fallback, privacy, model evaluation, scoring evidence, release evidence index, local `LANDING_RELEASE_CANDIDATE_METRIC 63/63`, and expected strict `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7` |
| Core 20 package verifier | `shike/scripts/verify_core20_package.py` | Present; checks exact 20-file package contents, APK SHA-256, plus structure, action-execution, and unit-test guard references in packaged README, device checklist, and demo acceptance script |
| Spike | `shike/spike/run_spike.py` | Present; all spike checks pass |
| Runbook | `shike/docs/device-runbook.md` | Present; prerequisites include Android structure guard |
| Demo checklist | `shike/materials/device-demo-checklist.md` | Present |

## Baseline Commands

All commands below were run from `/home/xing-12_26/projects/codex-workspace`.

| Command | Result | Evidence |
|---|---|---|
| `python3 shike/validation/validate_real_world_ready.py` | PASS | `REAL_WORLD_READY_METRIC 22/22` |
| `python3 shike/validation/validate_demo_acceptance.py` | PASS | `DEMO_ACCEPTANCE_METRIC 18/18` |
| `python3 shike/backend/verify_backend.py` | PASS | `backend_passed` |
| `python3 shike/spike/run_spike.py --all` | PASS | `spike_passed` |
| `python3 shike/validation/validate_android_structure.py` | PASS | `ANDROID_STRUCTURE_METRIC 31/31` |
| `python3 shike/validation/validate_android_unit_tests.py` | PASS | `ANDROID_UNIT_TEST_METRIC 88/88` |
| `python3 shike/validation/validate_android_image_preprocess.py` | PASS | `ANDROID_IMAGE_PREPROCESS_METRIC 15/15` |
| `python3 shike/validation/validate_landable.py` | PASS | `LANDABLE_METRIC 16/16` |
| `python3 shike/validation/validate_action_execution.py` | PASS | `ACTION_EXECUTION_METRIC 18/18` |
| `python3 shike/validation/validate_today_ranking.py` | PASS | `TODAY_RANKING_METRIC 7/7` |
| `python3 shike/validation/validate_image_semantic_cases.py` | PASS | `IMAGE_SEMANTIC_CASES_METRIC 9/9` |
| `python3 shike/validation/validate_model_eval_cases.py` | PASS | `MODEL_EVAL_CASES_METRIC 9/9` |
| `python3 shike/validation/validate_backend_scene_contract.py` | PASS | `BACKEND_SCENE_CONTRACT_METRIC 11/11` |
| `python3 shike/validation/validate_bluelm_adapter.py` | PASS | `BLUELM_ADAPTER_METRIC 8/8`; covers Bearer AppKey boundary, missing-credential fallback, vivo doc-center model body variants (`thinking.type` vs `enable_thinking`, `requestId` vs `request_id`), and `current_date` context for relative-time normalization without requiring real credentials |
| `python3 shike/validation/validate_vivo_ocr_adapter.py` | PASS | `VIVO_OCR_ADAPTER_METRIC 11/11`; covers server-side `/v1/ocr`, vivo `/ocr/general_recognition`, `businessid=aigc + AppID`, Bearer AppKey, form body, missing-credential fallback, and Android secret isolation |
| `python3 shike/validation/validate_vivo_multimodal_contract.py` | PASS | `VIVO_MULTIMODAL_CONTRACT_METRIC 28/28`; covers `/v2/analyze-image`, image data URL payloads, OCR blocks, ignored-region filtering, ignored-region metadata allowlist, Shike UI chrome copy filtering, prompt location/action gate rules, vivo multimodal request shape, server-side OCR text/block enrichment before multimodal analysis, `VIVO_MULTIMODAL_MODELS` candidate chaining, default vivo VisionChat model selection, signed VisionChat fallback through `/vivogpt/completions`, `allow_cloud_image=false` no-cloud-image fallback, OCR+BlueLM text fallback after image candidates fail, and final server-side user-confirmation action gate coverage for successful image-model results |
| `PYTHONPATH=shike/backend python3 -m shike_backend.eval.live_smoke --ocr-image /tmp/shike-live-course-notice.png --multimodal --multimodal-image /tmp/shike-live-course-notice.png --route-v2 --route-v2-image /tmp/shike-live-course-notice.png --timeout-seconds 60` | PASS | Secret-safe live smoke with backend private env produced `bluelm_status=pass`, `result_schema_valid=true`, `ocr_status=pass`, `multimodal_status=pass`, `route_v2_status=pass`, `route_v2_actions_disabled=true`, `route_v2_ignored_regions_allowed=true`, and `live_smoke_metric=4/4`; `Volc-DeepSeek-V3.2` was recorded as `provider_model_does_not_support_image` for image input, then `Doubao-Seed-2.0-mini` returned a schema-valid course notice; no AppKEY, Authorization header, base64 image payload, or full OCR text was written to repo evidence |
| `python3 shike/validation/validate_live_smoke_evidence.py` | PASS | `LIVE_SMOKE_EVIDENCE_METRIC 7/7`; mechanically checks the redacted backend private-env live smoke log for BlueLM text schema validity, vivo OCR image clearing, multimodal fallback then pass, route-v2 schema validity, `route_v2_actions_disabled=true`, ignored-region allowlist, `live_smoke_metric=4/4`, and no AppKEY/token/base64/PII leakage |
| `PYTHONPATH=shike/backend python3 -m shike_backend.eval.live_smoke --ocr-image /tmp/shike-live-ocr-course.png --route-v2 --route-v2-image /tmp/shike-live-ocr-course.png --timeout-seconds 35` | PASS | Secret-safe synthetic live smoke produced `bluelm_status=pass`, `result_schema_valid=true`, `ocr_status=pass`, `route_v2_status=pass`, `route_v2_actions_disabled=true`, `route_v2_ignored_regions_allowed=true`, and `live_smoke_metric=3/3`; no AppKEY, Authorization header, base64 image payload, or full OCR text was written to repo evidence |
| `PYTHONPATH=shike/backend python3 -m shike_backend.eval.live_smoke --skip-bluelm --skip-ocr --route-v2 --route-v2-image /tmp/shike-live-ocr-course.png --timeout-seconds 35` | PASS | Route-level FastAPI smoke produced `route_v2_http_status=200`, `route_v2_status=pass`, `route_v2_schema_valid=true`, `route_v2_actions_disabled=true`, `route_v2_ignored_regions_allowed=true`, `route_v2_ignored_regions=top_status_bar,bottom_navigation_bar`, and `live_smoke_metric=1/1`; output remains redacted and does not include credentials, full OCR text, or image payloads |
| `PYTHONPATH=backend python3 -m unittest backend.tests.test_settings_env_file` | PASS | Proves backend private env files load via `SHIKE_BACKEND_ENV_FILE` / `~/.config/shike/bluelm.env`, while process environment variables keep higher priority |
| `PYTHONPATH=shike/backend python3 -m shike_backend.eval.live_smoke --skip-bluelm --skip-ocr --multimodal --multimodal-image /tmp/shike-live-smoke-synthetic.png --timeout-seconds 25` | PASS | Secret-safe default-candidate smoke produced `multimodal_status=pass`, `multimodal_scene_type=meeting_notice`, `multimodal_schema_valid=True`, and `live_smoke_metric=1/1`; the default chain first records `Volc-DeepSeek-V3.2` as `provider_model_does_not_support_image`, then selects `Doubao-Seed-2.0-mini` without printing AppKEY, Authorization, base64 image payloads, or full OCR text |
| `python3 shike/validation/validate_cloud_backend_ready.py` | PASS | `CLOUD_BACKEND_READY_METRIC 9/9`; validates backend smoke, provider config, and `docs/server-deployment-runbook.md` coverage for `roky.chat` / `api.roky.chat`, `/etc/shike/shike-backend.env`, `/opt/shike/backend`, systemd, Nginx, certbot, public smoke checks, `VIVO_AIGC_*` / `VIVO_OCR_*` / `VIVO_MULTIMODAL_*` server-side placeholders, and redacted log boundaries |
| `PYTHONPATH=shike/backend python3 -m shike_backend.eval.http_server_smoke --timeout-seconds 35 --disable-cloud-image` | PASS | Temporary uvicorn HTTP smoke proves the deterministic no-cloud-image route, produced `http_smoke_health_status=ok`, `http_smoke_route_status=pass`, `http_smoke_actions_disabled=True`, `http_smoke_ignored_regions_allowed=True`, `http_smoke_log_secret_scan=pass`, and `http_server_smoke_metric=1/1` |
| `python3 shike/validation/validate_backend_audit_log.py` | PASS | `BACKEND_AUDIT_LOG_METRIC 8/8`; validates `/v2/analyze-image` metadata-only audit events, route integration, user-controlled `input_id_hash` logging, PII redaction helper, unit coverage, and no raw Authorization/AppKEY/base64/full-OCR/input-id logging |
| `python3 shike/validation/validate_apk_secret_hygiene.py` | PASS | `APK_SECRET_HYGIENE_METRIC 8/8`; scans local and desktop APK zip entries for `sk-*` tokens, provider secret env names, vivo direct endpoints, and exact private env values without printing secrets |
| `python3 shike/backend/shike_backend/eval/run_model_eval.py --progress-every 25` | PASS | `MODEL_EVAL_METRIC 110/110` |
| `python3 shike/validation/validate_model_contract_strict.py` | PASS | `MODEL_CONTRACT_STRICT_METRIC 10/10` |
| `python3 shike/validation/validate_advanced_product_beta.py` | PASS | `PRODUCT_BETA_METRIC 30/30` |
| `python3 shike/validation/validate_advanced_product_beta.py --strict` | PASS | Full Product Beta readiness gate passes at `30/30` |
| `python3 shike/scripts/prepare_cloud_device_evidence.py` | PASS | `CLOUD_DEVICE_PREP_METRIC 5/5`; expected `CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9` until real cloud-device videos are collected |
| `python3 shike/validation/validate_cloud_device_package.py` | PASS | `CLOUD_DEVICE_PACKAGE_METRIC 30/30`; package skeleton, runbook release handoff, release evidence handoff, blocking report handoff, generated capture TODO handoff, Android 16 DoD pre-capture gate, public backend preflight, release handoff runner, redaction surfaces, and current strict external-evidence blocker state are documented |
| `python3 shike/scripts/test_preflight_cloud_backend.py` | PASS | public backend preflight helper unit tests pass; live preflight must print `CLOUD_BACKEND_PREFLIGHT_METRIC` with redacted evidence before cloud-device recording |
| `python3 shike/validation/validate_android16_real_implementation_guide.py` | PASS | `ANDROID16_REAL_IMPLEMENTATION_GUIDE_METRIC 12/12`; aggregates SHIKE-P0-001 through SHIKE-P1-012 from the Android 16 guide, including fake-device removal, unified `CaptureDraft`, no-default image upload, vivo multimodal/OCR, system-confirmed screenshot cleanup, confirmed calendar/reminder/map actions, home slimming, recent screenshot assist, and optional local 3B boundaries |
| `python3 shike/validation/validate_android16_definition_of_done.py` | PASS | `ANDROID16_DOD_COVERAGE_METRIC 28/28`; maps Android 16 guide section 19 functional, evidence, and safety DoD to executable gates while preserving missing MP4/report/logcat proof as strict external blockers |
| `python3 shike/scripts/run_release_handoff_checks.py --strict` | PASS | `RELEASE_HANDOFF_CHECKS_METRIC 24/24`; local handoff gates now explicitly include `ANDROID16_DOD_COVERAGE_METRIC 28/28`, `IMAGE_SEMANTIC_CASES_METRIC 9/9`, and `LIVE_SMOKE_EVIDENCE_METRIC 7/7`, and strict gates are treated as expected blockers until real cloud-device recordings, report, and logcat are complete |
| `python3 shike/validation/validate_release_blocking_report.py` | PASS | `RELEASE_BLOCKING_REPORT_METRIC 8/8`; `materials/evidence/blocking-report.md` Required Next Actions list strict blockers, missing cloud videos, placeholder report fields, required rerun commands, redaction rules, and the report `Pre-recording Evidence Gate` check before cloud-device recording that `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md` remains the desktop guidance source while `materials/evidence/requirement-matrix.md` still passes `REQUIREMENT_MATRIX_METRIC 9/9`, all 9 real cloud-device MP4 files are present, and no placeholder fields remain after capture |
| `python3 shike/validation/validate_release_evidence_index.py` | PASS | `RELEASE_EVIDENCE_INDEX_METRIC 10/10`; release index covers local gates, BlueLM evidence, desktop guidance matrix, scoring evidence map, preliminary deck landing evidence package, `validate_deliverables.py`, `validation/traceability.md` SHIKE-070, strict blockers, APK hash, APK secret hygiene, dependency-safe rebuild commands, optimization-log handoff summary, README public entrypoint, and redaction rules |
| `python3 shike/validation/validate_requirement_matrix.py` | PASS | `REQUIREMENT_MATRIX_METRIC 9/9`; maps desktop guidance stages A-E to local evidence, validation commands, strict cloud-device blockers, the public status page's desktop guidance anchor, and `materials/evidence/desktop-guidance-source-status.md` source-availability note |
| `python3 shike/validation/validate_user_research_evidence.py` | PASS | `USER_RESEARCH_EVIDENCE_METRIC 8/8`; validates user research plan, interview summary template, scoring evidence map, `validation/traceability.md` SHIKE-075, and the `待采集` / no-fabrication boundary for application-value evidence |
| `python3 shike/validation/validate_landing_release_candidate.py` | PASS | `LANDING_RELEASE_CANDIDATE_METRIC 63/63`; default local release-candidate now runs both `validate_backend_audit_log.py` and `validate_live_smoke_evidence.py` directly, so metadata-only backend logging and the redacted private-env live smoke are covered by the main gate as well as the release handoff runner |
| `python3 shike/validation/validate_landing_release_candidate.py --strict` | BLOCKED | `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7`; still missing real cloud-device videos, filled report, and redacted logcat |
| `python3 shike/scripts/verify_core20_package.py "$tmp_core20_package"` | PASS | `CORE20_FILE_COUNT 20/20`; structure/action/unit-test guard references pass |
| `bash shike/android-mvp/build_apk.sh` | PASS | APK rebuilt with the project-local Gradle/JDK/SDK toolchain; local APK and `/mnt/c/Users/Xing/Desktop/Shike-app-debug.apk` SHA-256 both `733fd972ac7a1d2a0454acb9a37dd48449b48d2475a49e93156e51288dbcca93` |
| `gradle --no-daemon :app:testDebugUnitTest` from `shike/android-mvp/` | PASS | `BUILD SUCCESSFUL`; local unit suites report 149 tests, 0 failures, 0 errors |

## Current Strengths

- The Android demo APK is present at `shike/android-mvp/app/build/outputs/apk/debug/app-debug.apk`.
- The backend smoke path is available and passes.
- The Spike path covers parser, action planning, persistence, and fallback behavior.
- Demo acceptance and real-world readiness validators both pass.
- Android source structure now has a dedicated validator covering file boundaries, coordinator size, action helper size, callback names, helper ownership, the extracted AgendaCard boundary, the extracted agenda card footer boundary, the extracted agenda card header boundary, the extracted review risk checklist boundary, the extracted review decision actions boundary, the extracted backend analysis controls boundary, the extracted backend endpoint controls boundary, the extracted import capture actions boundary, the extracted offline sample actions boundary, the extracted OCR draft editor boundary, the extracted captured image preview boundary, the extracted dashboard header boundary, the extracted dashboard notification badge boundary, the extracted system status row boundary, the extracted date strip boundary, the extracted home agenda list boundary, the extracted demo route step boundary, the extracted bottom nav item boundary, the extracted confirm banner actions boundary, the extracted parse confirm header boundary, and the extracted action planner execution controls boundary; it is listed in README, the device demo checklist, and the Demo console.
- The core 20 package verifier now also checks that packaged acceptance surfaces keep Android structure, action-execution, and unit-test guard references.
- The real-world readiness validator now keeps the README mechanical acceptance entry tied to `validate_android_structure.py`, `validate_android_unit_tests.py`, `ANDROID_STRUCTURE_METRIC 31/31`, and `ANDROID_UNIT_TEST_METRIC 88/88`.
- The landable validator now checks that `docs/device-runbook.md` names the Android structure guard prerequisite before device testing.
- The Product Beta validator establishes the S2 readiness baseline from the advanced guide and keeps future work tied to real product capabilities instead of display-only component splits.
- The action execution validator now keeps confirmation-before-action, timed reminder scheduling, exact-alarm fallback, scheduled reminder persistence, app-start recovery, device reboot recovery, local-data-clear alarm cancellation, map copy fallback, calendar wording, and permission denial persistence covered by a dedicated S3 guard.
- The Android local unit-test baseline now runs through `:app:testDebugUnitTest` and is guarded by `validate_android_unit_tests.py`, covering privacy redaction, camera/gallery/share import mapping, `source_type` mapping for `screenshot`/`camera`/`share_text`/`manual`, OCR engine layering, initial selection, action execution result recording, execution result state derivation, notification permission fallback copy, backend failure fallback copy, model explanation wording, model API JSON mapping, model API request payload contract fields, Today action item mapping, execution action gates, inbox workbench filtering/search/archive logic, all-status priority ordering, archive/restore action state, reminder payload scheduling/restore logic, reminder receiver payload defaults, backend analysis input/failure mapping, review-status mapping, review action persistence,导入源图清理状态在后端解析和用户确认后保留, capture result action persistence, backend endpoint saving, backend trigger dispatch, backend outcome persistence, offline sample actions, local inbox entity mapping, local inbox action-list persistence codec, local inbox capture-source sanitization, local inbox raw-text sanitization, local persistence namespace boundaries, local data clear state and App-internal cache-clear confirmation, cloud-off fallback state, settings version-tap Debug unlock state, optional端侧 3B install/route/failure status boundaries, recent screenshot helper opt-in preference persistence, clear-cache reset, 30-second MediaStore lookback, notification-tap candidate metadata preservation, home date sorting-hint wording that avoids treating system date as task time, system calendar insert-page wording that avoids claiming saved/written before the user saves in Calendar, and visible screenshot callback prompt wording that states the app does not directly receive the image.
- Backend settings now auto-load a private `~/.config/shike/bluelm.env` or `SHIKE_BACKEND_ENV_FILE` file for local/server runs, while `verify_backend.py` explicitly isolates itself to mock mode so local smoke remains deterministic even when real credentials exist on the machine.
- Backend `/v2/analyze-image` now emits only metadata audit evidence through `build_analyze_image_audit_event`; `BACKEND_AUDIT_LOG_METRIC 8/8` guards that logs do not copy provider secrets, image payloads, full OCR text, user-controlled raw input IDs, or common PII.
- Backend `/v2/analyze-image` now tries `VIVO_MULTIMODAL_MODELS` image-capable candidates before OCR+BlueLM text fallback; when `VIVO_MULTIMODAL_MODELS` is omitted, settings default the image path to `vivo-BlueLM-V-2.0`, then keep `BlueLM-Vision-prd`, `Volc-DeepSeek-V3.2`, `Doubao-Seed-2.0-mini`, `Doubao-Seed-2.0-lite`, `Doubao-Seed-2.0-pro`, and `qwen3.5-plus` as candidates. `VIVO_MULTIMODAL_CONTRACT_METRIC 28/28` and `backend/verify_backend.py` guard that the route keeps schema-valid output, filters Shike UI chrome copy before prompt construction, sanitizes `ignored_regions` to backend-approved metadata labels, applies prompt location/action gate rules, supports signed VisionChat fallback through `/vivogpt/completions`, respects `allow_cloud_image=false` by skipping server OCR and image-model calls with `cloud_image_disabled` risk evidence, avoids fixed training samples, and disables every downstream action until user confirmation. The final route return now applies `_require_user_confirmation_for_card(card)` so even a successful image model that claims an action is executable is overwritten to `disabled_reason=用户确认前不可执行` before leaving the backend. Latest direct probe with the current test key reached the signed VisionChat fallback but the vision models returned `legacy_http_status:401`; route-v2 still returned schema-valid fallback output.
- APK artifact hygiene now has an explicit gate: `APK_SECRET_HYGIENE_METRIC 8/8` scans both `android-mvp/app/build/outputs/apk/debug/app-debug.apk` and `/mnt/c/Users/Xing/Desktop/Shike-app-debug.apk` for AppKEY-like tokens, provider secret variable names, vivo direct endpoints, and backend private env values without printing secrets.
- The backend scene contract is intentionally conservative: `assignment_deadline`/`meeting_notice`/`interview_notice`/`travel_ticket` remain as regression groups and request `scene_hint` values, but current public output contract still maps them to `scene_type=unknown` and `task.topic=unknown`.
- The landing release-candidate validator now gives the project one 59-item local release gate while keeping strict external evidence separate: default mode proves repository readiness including vivo OCR, no-default-image-upload boundary, strict blocking-report and release evidence index quality; `--strict` requires real BlueLM online evidence and nine cloud-device recordings.
- The cloud-device prep helper now has a 5-item local gate: `prepare_cloud_device_evidence.py` refreshes `apk-sha256.txt` and `cloud-device-capture-todo.md`, reports `CLOUD_DEVICE_PREP_METRIC 5/5`, and intentionally keeps `CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9` explicit until real cloud-device MP4 files are collected.
- The cloud-device package now has a 30-item non-strict handoff gate: `validate_cloud_device_package.py` checks the skeleton, capture TODO, device-runbook release handoff steps, generated capture TODO handoff, Android 16 DoD pre-capture gate, public backend preflight, release evidence index pointer, backend audit log pointer, live-smoke evidence pointer, blocking report pointer, dependency-safe handoff order, `run_release_handoff_checks.py` including the Android 16 guide aggregate gate, `LANDING_RELEASE_CANDIDATE_METRIC 63/63`, expected strict `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7`, and redaction surfaces before any real cloud-device recording is collected.
- Existing autoresearch artifacts are present:
  - `shike/research-results.tsv`
  - `shike/autoresearch-state.json`
  - `shike/autoresearch-hook-context.json`
  - `shike/autoresearch-lessons.md`

## Current Risks And Gaps

- `MainActivity.kt` is now reduced to 120 lines and mainly owns Android Activity shell concerns: share intent intake, reminder permission result handling, notification permission fallback persistence, map copy fallback dispatch, notification channel setup, persistence callbacks, and system action dispatch.
- `ShikeApp.kt` now owns app-level screen state and callback wiring; `CaptureLaunchers.kt` owns camera/gallery Activity Result launcher wiring, `CaptureResultActions.kt` owns successful capture result application, `BackendAnalysisActions.kt` owns backend request kickoff plus main-thread delivery, `BackendOutcomeActions.kt` owns backend outcome application, `BackendEndpointActions.kt` owns backend URL save action output, `BackendTriggerActions.kt` owns course/event backend trigger dispatch, `SampleActions.kt` owns offline sample selection application, and `ReviewActions.kt` owns review-result application.
- Pure domain/sample data, initial selection, review status mapping, review result application, permission decisions, share import mapping, capture result mapping, capture result application helpers, camera/gallery launcher wiring, camera permission launch helper, gallery launch helper, backend trigger helpers, backend request kickoff, backend outcome application helper, backend endpoint action helper, notification permission result helper, notification permission request helper, system action fallback helper, backend request/JSON mapping, backend analysis input mapping, backend outcome application, offline sample action helpers, backend endpoint save helper, backend analysis runner, backend URL save normalization, SharedPreferences inbox snapshot, backend URL storage, system action helpers, main screen layout, shared UI primitives, import UI, confirmation banner UI, parse-confirm UI, action planner UI, inbox UI, and several display-only Compose sections have been extracted.
- Local persistence now includes `InboxDatabase` SQLite history, `InboxItemEntity` mapping, 50-record synthetic seed coverage, and legacy `SharedPreferences` snapshot migration; remaining persistence work is device/emulator durability verification rather than the old Room/SQLite baseline gap.
- Timed reminders now use `AlarmManager` scheduling with exact-alarm capability checks, ordinary-alarm fallback, persisted pending payloads, app-start recovery through `restoreScheduledReminder`, and device reboot recovery through `BootReminderReceiver`; device-level exact-alarm settings still need manual or emulator verification.
- Native vivo image-input live smoke now has a working default candidate path with the current test key: `Volc-DeepSeek-V3.2` still reports `provider_model_does_not_support_image`, but the default chain reaches `Doubao-Seed-2.0-mini` and returns a schema-valid `meeting_notice` card. The practical `/v2/analyze-image` path still keeps OCR+BlueLM text fallback for future model/permission failures and disables downstream actions until user confirmation through the final backend response gate.
- Product Beta readiness now passes at `30/30`; S2 Product Beta is mechanically complete, with future work shifting to deeper S3 stability and S4 model quality.
- Android local unit-test coverage is established as a baseline gate; UI and connected-device tests still need a future device/emulator track.
- This directory is a git repository; prefer using git commits/diffs/status for rollback evidence, and use validation logs/package verification as the runnable acceptance proof.

## Commands Not Run In This Baseline

| Command | Status | Reason |
|---|---|---|
| `bash shike/android-mvp/build_apk.sh` | PASS | Completed on 2026-06-07 with the project-local Gradle/JDK/SDK toolchain; SDK XML version warnings were non-blocking |
| `./gradlew test` | Not run | This workspace uses the project-local Gradle binary directly; the validated local-test baseline is `gradle --no-daemon :app:testDebugUnitTest` |
| `./gradlew connectedCheck` | Not run | Requires a connected Android device/emulator and is outside this baseline pass |

## Next Highest Priority

Continue S3 quality hardening from the advanced guide:

1. Move into S3 quality hardening while keeping timed reminder scheduling, the 110-case model evaluation set, clear-local-data controls, log redaction, cloud-off backend guard, map copy fallback, reminder permission fallback, the today empty/error state path, model explanation detail, execution result visibility, missing-field guards, archive/restore controls, CaptureDraft, manual input continuation, low-confidence review, and inbox workbench data-driven.
2. Keep `validate_today_ranking.py` as the narrow regression test for ranking behavior.
3. Keep existing permission, fallback, and confirmation-before-action behavior covered by validators.
4. Keep `validate_advanced_product_beta.py --strict` in the release-candidate gate because Product Beta now passes at `PRODUCT_BETA_METRIC 30/30`.
5. Keep UI behavior unchanged except where an explicit S3 stability or S4 model-quality target is paired with a validator.
6. Re-run:
   - `gradle --no-daemon :app:assembleDebug`
   - `python3 shike/validation/validate_android_structure.py`
   - `python3 shike/validation/validate_android_unit_tests.py`
   - `python3 shike/validation/validate_action_execution.py`
   - `python3 shike/validation/validate_today_ranking.py`
   - `python3 shike/validation/validate_model_eval_cases.py`
   - `python3 shike/validation/validate_vivo_multimodal_contract.py`
   - `python3 shike/validation/validate_advanced_product_beta.py`
   - `python3 shike/validation/validate_real_world_ready.py`
   - `python3 shike/validation/validate_demo_acceptance.py`
   - `python3 shike/backend/verify_backend.py`
   - `python3 shike/validation/validate_backend_audit_log.py`
   - `python3 shike/spike/run_spike.py --all`
7. Before release handoff, also re-run:
   - `python3 shike/validation/validate_cloud_device_package.py`
   - `python3 shike/validation/validate_live_smoke_evidence.py`
   - `python3 shike/scripts/run_release_handoff_checks.py --strict`
   - `python3 shike/validation/validate_requirement_matrix.py`
   - `python3 shike/validation/validate_release_evidence_index.py`
   - `python3 shike/validation/validate_landing_release_candidate.py`
   - `python3 shike/validation/validate_release_blocking_report.py`
   - `python3 shike/validation/validate_landing_release_candidate.py --strict` (expected to remain blocked at `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7` until real cloud-device recordings and filled report are collected)
