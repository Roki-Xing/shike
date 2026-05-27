---
name: shike-security-privacy
description: Prevent secrets/PII leakage across Shike Android/backend/docs/materials/prototype/tests/logs; enforce confirm-before-execute and backend-only secret handling.
---

# shike-security-privacy

## When to use

- Any work involving secrets, environment variables, request/response logging, or cloud-model providers.
- Any change that touches OCR text persistence/display, demo recordings, or materials content.
- Any change to "clear local data" semantics, privacy copy, or permissions.
- Before implementing BlueLM: run and enforce secret hygiene checks.

## Must read first

1. `AGENTS.md`
2. `docs/SHIKE_LANDING_APP_OPTIMIZATION_GUIDE.md` (secret rules + red lines)
3. `README.md` (synthetic data requirement)
4. Android redaction implementation:
   - `android-mvp/app/src/main/java/cn/shike/app/data/PrivacyRedaction.kt`
   - `android-mvp/app/src/test/java/cn/shike/app/data/PrivacyRedactionTest.kt`
5. Execution safety validator:
   - `validation/validate_action_execution.py`

## Existing project facts (from repo)

- Android has `redactSensitiveLogText()` which redacts phone/email/student-id/LAN-IP patterns and is unit-tested.
- Android does not contain BlueLM secrets in source (must remain true).
- Backend currently does not implement BlueLM, and therefore does not yet have env-based secret loading (must be added later).
- `validation/validate_secret_hygiene.py` exists and is the default guardrail for "no secrets committed".
  - Current scan targets include: `android-mvp/`, `backend/`, `contracts/`, `docs/`, `materials/`, `prototype/`, `validation/`, `.agents/`, plus `AGENTS.md` and `README.md`.
  - Note: it is filesystem-only and skips binaries (e.g. `.apk`), so it does **not** prove packaged APKs are secret-free or that runtime logs never emit secrets.

## Recommended workflow

1. Establish "no secrets in repo" guardrails first:
   - Keep `validation/validate_secret_hygiene.py` green before any BlueLM integration work.
   - Ensure it scans the current targets listed above and never prints raw matched values.
2. Keep secrets backend-only:
   - Android must only know the backend base URL; never AppKEY/token/signature.
   - Backend must read secrets from environment variables and never print them.
3. Treat demo artifacts as risky:
   - Record with synthetic data only.
   - Do not show LAN IPs, notifications, accounts, or secrets on screen.
4. Preserve confirm-before-execute invariant:
   - Calendar/reminder/map must remain disabled until user confirms.

## Reusable modules or commands

- Android redaction: `android-mvp/app/src/main/java/cn/shike/app/data/PrivacyRedaction.kt`
- Validators:
  - `python3 shike/validation/validate_android_unit_tests.py`
  - `python3 shike/validation/validate_action_execution.py`
  - `python3 shike/validation/validate_real_world_ready.py`
- Secret hygiene gate:
  - `python3 shike/validation/validate_secret_hygiene.py`
- Fallback quick scan (when you need a manual grep):
  - `rg -n --hidden --no-ignore -S "BLUELM_APP_KEY=|AppKEY=|sk-" shike`

## High-risk mistakes

- Writing keys into Android (sources/resources/APK) or into docs/materials/prototype/tests/logs.
- Logging raw OCR text or personal information.
- Adding debug print statements that include request headers or tokens and forgetting to remove them.
- Weakening validators to "make it pass" instead of keeping the product safe.

## Validation

Minimum:

```bash
python3 shike/validation/validate_action_execution.py
python3 shike/validation/validate_android_unit_tests.py
python3 shike/validation/validate_real_world_ready.py
```

```bash
python3 shike/validation/validate_secret_hygiene.py
```
