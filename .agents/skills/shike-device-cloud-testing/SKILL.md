---
name: shike-device-cloud-testing
description: Run Shike on emulator, USB real device, and (when available) cloud devices; produce repeatable recordings and keep demo/readiness validators aligned with runbook/checklists.
---

# shike-device-cloud-testing

## When to use

- Installing APK on emulator or real device and verifying core flows end-to-end.
- Rehearsing the competition demo and producing the required evidence recordings.
- Debugging device-only issues: camera/gallery, permissions, reminders, calendar/map intents, reboot recovery.
- Attempting cloud-device testing: first confirm what is supported by repo evidence; mark unknown parts as "未确认".

## Must read first

1. `AGENTS.md`
2. `docs/device-runbook.md`
3. `materials/device-demo-checklist.md`
4. `README.md`
5. `backend/verify_backend.py`

## Existing project facts (from repo)

- APK path:
  - `android-mvp/app/build/outputs/apk/debug/app-debug.apk`
- ADB install (documented):
  - `adb install -r shike/android-mvp/app/build/outputs/apk/debug/app-debug.apk`
- Backend start (LAN only):
  - `cd shike/backend && python3 -m uvicorn shike_backend.main:app --host 0.0.0.0 --port 8000`
- Backend endpoints expected:
  - `/health`, `/v1/schema`, `/v1/analyze`
- Android backend connectivity:
  - Emulator default: `http://10.0.2.2:8000/v1/analyze`
  - Real device: user-entered LAN IP `http://192.168.x.x:8000` saved in app
- Required recordings (per checklist) under `shike/materials/evidence/`:
  - `01-install-and-open.mp4`
  - `02-course-gallery-backend.mp4`
  - `03-event-camera-actions.mp4`
  - `04-fallback-offline.mp4`
  - `05-restart-restore.mp4`
  - `06-delivery-readiness.mp4`
- Cloud device / device farm support:
  - Not explicitly documented in current runbook/checklist/README; treat as **未确认** unless proven.

## Recommended workflow

1. Pre-flight (run validators before recording):
   - `bash shike/android-mvp/build_apk.sh`
   - `python3 shike/backend/verify_backend.py`
   - `python3 shike/validation/validate_demo_acceptance.py`
   - `python3 shike/validation/validate_real_world_ready.py`
2. Start backend (LAN only):
   - `cd shike/backend && python3 -m uvicorn shike_backend.main:app --host 0.0.0.0 --port 8000`
3. Install APK and run the flows as per the checklist; record each segment with the required filename.
4. For cloud devices:
   - Do not assume local LAN backend is reachable.
   - Preferred approach (from the landing guide): deployed HTTPS backend or a safe HTTPS tunnel (details not implemented in repo; treat as 未确认 until implemented).

## Reusable modules or commands

```bash
bash shike/android-mvp/build_apk.sh
python3 shike/backend/verify_backend.py
python3 shike/validation/validate_demo_acceptance.py
python3 shike/validation/validate_real_world_ready.py
```

## High-risk mistakes

- Exposing backend to the public internet when using `--host 0.0.0.0` (runbook positions this for LAN only).
- Recording real personal data in videos/screenshots (must use synthetic demo data).
- Assuming cloud devices can access `10.0.2.2` or LAN IP.
- Showing AppKEY / tunnel tokens / secrets in screen recordings.
- Claiming calendar events were saved when only the insert page was opened.

## Validation

- `python3 shike/validation/validate_demo_acceptance.py`
- `python3 shike/validation/validate_real_world_ready.py`

