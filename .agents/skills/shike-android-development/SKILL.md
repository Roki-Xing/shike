---
name: shike-android-development
description: Work on Shike Android (Kotlin/Compose) safely: preserve confirm-before-execute, persistence boundaries, permissions, reminders, backend calls, and keep Android validators green.
---

# shike-android-development

## When to use

Use this skill for any Android-side work in `shike/android-mvp/`, including:

- Compose UI changes (screen split, navigation, visual polish, state flow).
- System actions: calendar insert, reminder scheduling, map deeplink and fallbacks.
- Permissions, receivers, intent-filters, share/camera/gallery entrypoints.
- Local persistence (inbox snapshot, backend base URL, reminder payload) and "clear local data" semantics.
- Backend bridge (`/v1/analyze`) request/response mapping and failure fallback.

## Must read first

1. `AGENTS.md` (red lines + commands)
2. `android-mvp/app/src/main/AndroidManifest.xml`
3. `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt`
4. Confirmation gating + execution controls:
   - `android-mvp/app/src/main/java/cn/shike/app/ui/ExecutionActionGate.kt`
   - `android-mvp/app/src/main/java/cn/shike/app/ui/ConfirmBannerActions.kt`
   - `android-mvp/app/src/main/java/cn/shike/app/ui/ActionPlannerExecutionControls.kt`
5. System actions & fallbacks:
   - `android-mvp/app/src/main/java/cn/shike/app/system/SystemActions.kt`
6. Persistence boundaries:
   - `android-mvp/app/src/main/java/cn/shike/app/data/LocalInboxStore.kt`
   - `android-mvp/app/src/main/java/cn/shike/app/data/BackendConfigStore.kt`
   - `android-mvp/app/src/main/java/cn/shike/app/system/ReminderScheduler.kt`
7. Privacy redaction:
   - `android-mvp/app/src/main/java/cn/shike/app/data/PrivacyRedaction.kt`

## Existing project facts (from repo)

- Stack:
  - Kotlin + Jetpack Compose.
  - JUnit4 local JVM tests (`junit:junit:4.13.2`). See `android-mvp/app/build.gradle.kts`.
- Manifest:
  - Permissions include `INTERNET`, `POST_NOTIFICATIONS`, `RECEIVE_BOOT_COMPLETED`, `CAMERA`.
  - `MainActivity` supports `ACTION_SEND` + `text/plain`.
  - Receivers: `ReminderReceiver` and `BootReminderReceiver`. See `android-mvp/app/src/main/AndroidManifest.xml`.
- Confirm-before-execute red line:
  - Execution enablement is enforced in UI via `executionActionGateFor(item, isConfirmed)` and related UI controls.
  - System intents are launched from `MainActivity` and do not re-check confirmation; therefore UI gating must not regress.
- System actions:
  - Calendar uses insert intent (`Intent.ACTION_INSERT` to `CalendarContract.Events.CONTENT_URI`) and must not claim "saved".
  - Map uses `geo:0,0?q=...` deeplink; on failure, copies location as fallback and preserves the card.
  - Reminder uses `AlarmManager`; Android 12+ exact-alarm may be unavailable and must degrade gracefully.
  - See `android-mvp/app/src/main/java/cn/shike/app/system/SystemActions.kt` and `ReminderScheduler.kt`.
- Local persistence is intentionally split into namespaces:
  - Inbox snapshot: `shike_inbox_state` in `LocalInboxStore.kt`.
  - Backend override: `shike_backend_config` in `BackendConfigStore.kt`.
  - Reminder payload: `shike_reminder_state` in `ReminderScheduler.kt`.
  - Inbox snapshot clear must remove only snapshot keys and must not call `.clear()`. See `LocalInboxStore.kt`.
- Backend bridge:
  - Android calls backend `/v1/analyze` via `HttpURLConnection` (timeouts configured), and on failures falls back to local mock copy and remains editable. See `ModelApiClient.kt` and `BackendAnalysisRunner.kt`.
- Secrets:
  - No BlueLM AppKEY is present in Android source (repo must keep it that way). Any secret must stay in backend env only.

## Recommended workflow

1. Identify which layer you are changing:
   - UI (`cn.shike.app.ui`), system (`cn.shike.app.system`), data (`cn.shike.app.data`), or tests (`app/src/test`).
2. Preserve invariants:
   - No system action executes before user confirmation.
   - Do not weaken fallbacks for permission denial or missing apps.
   - Do not merge preference namespaces back together; do not reintroduce `.clear()` wipes for inbox snapshot clear.
3. Make changes small and verifiable.
4. Update or add JVM unit tests when behavior changes.
5. Run validators in this order:
   - Narrow: `validate_android_structure.py` -> `validate_android_unit_tests.py` -> `validate_action_execution.py`
   - Broad: `validate_real_world_ready.py`

## Reusable modules or commands

Reusable code modules:

- Confirmation gating: `android-mvp/app/src/main/java/cn/shike/app/ui/ExecutionActionGate.kt`
- System actions & fallbacks: `android-mvp/app/src/main/java/cn/shike/app/system/SystemActions.kt`
- Reminder scheduling/recovery: `android-mvp/app/src/main/java/cn/shike/app/system/ReminderScheduler.kt`
- Inbox snapshot persistence: `android-mvp/app/src/main/java/cn/shike/app/data/LocalInboxStore.kt`
- Backend endpoint persistence: `android-mvp/app/src/main/java/cn/shike/app/data/BackendConfigStore.kt`
- Backend API client: `android-mvp/app/src/main/java/cn/shike/app/data/ModelApiClient.kt`
- Redaction: `android-mvp/app/src/main/java/cn/shike/app/data/PrivacyRedaction.kt`

Reusable commands:

```bash
bash shike/android-mvp/build_apk.sh
python3 shike/validation/validate_android_structure.py
python3 shike/validation/validate_android_unit_tests.py
python3 shike/validation/validate_action_execution.py
python3 shike/validation/validate_real_world_ready.py
```

## High-risk mistakes

- Accidentally enabling calendar/reminder/map buttons before user confirmation.
- Launching intents from Compose components directly (bypassing centralized fallbacks in `MainActivity`/`SystemActions`).
- Logging or persisting raw OCR/PII without redaction.
- Introducing BlueLM secrets or any `sk-...` strings into Android sources, resources, docs, materials, prototype, tests, logs, or APK.
- Breaking reminder recovery (app start / device reboot) and clear-local-data semantics.
- Changing UI copy that validators grep for without updating validators/docs.

## Validation

Minimum set for Android changes:

```bash
python3 shike/validation/validate_android_structure.py
python3 shike/validation/validate_android_unit_tests.py
python3 shike/validation/validate_action_execution.py
python3 shike/validation/validate_real_world_ready.py
```

