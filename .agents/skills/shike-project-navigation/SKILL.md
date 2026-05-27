---
name: shike-project-navigation
description: Navigate the Shike repo safely: understand directory ownership, entry points, invariants, and which validators must stay green before changing code or docs.
---

# shike-project-navigation

## When to use

Use this skill whenever you:

- enter `shike/` and need to orient yourself before making changes,
- plan to touch more than one module (Android + backend + docs),
- are unsure which file owns a behavior,
- need to find the authoritative validator for a requirement,
- are about to change contracts or anything that might break demo/readiness checks.

## Must read first

1. `AGENTS.md`
2. `README.md`
3. `docs/SHIKE_LANDING_APP_OPTIMIZATION_GUIDE.md`
4. `docs/product-spec.md`
5. `docs/mvp-scope.md`
6. `contracts/model-output.schema.json`
7. `docs/device-runbook.md`
8. `materials/device-demo-checklist.md`

## Existing project facts (from repo)

- Core product loop (must not break): capture -> analyze -> user confirm -> action orchestration -> inbox/today tracking. (See `README.md`, `docs/product-spec.md`.)
- Android entry points:
  - `android-mvp/app/src/main/AndroidManifest.xml`
  - `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt`
  - `android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt`
- Backend entry points:
  - `backend/shike_backend/main.py` provides `/health`, `/v1/schema`, `/v1/analyze`.
  - `backend/verify_backend.py` is the backend smoke test (no server required).
- Contract SSOT:
  - `contracts/model-output.schema.json` is the canonical output schema used across Android + backend.
- Validation scripts are part of deliverables (not optional). The readiness aggregator is:
  - `validation/validate_real_world_ready.py`

## Recommended workflow

1. Identify your change type:
   - `docs-only`, `android-only`, `backend-only`, or `cross-cutting`.
2. Locate ownership:
   - UI/interaction: `android-mvp/app/src/main/java/cn/shike/app/ui/`
   - System actions: `android-mvp/app/src/main/java/cn/shike/app/system/`
   - Persistence: `android-mvp/app/src/main/java/cn/shike/app/data/`
   - Backend routes/models: `backend/shike_backend/main.py`
   - Contract: `contracts/model-output.schema.json`
3. Before editing, grep for validators mentioning your target behavior:
   - `rg -n "<keyword>" shike/validation shike/docs shike/README.md`
4. Make the smallest verifiable patch.
5. Run narrow validators first, then the aggregator:
   - Narrow (examples): `validate_android_structure.py`, `validate_android_unit_tests.py`, `validate_action_execution.py`, `validate_model_bridge.py`, `verify_backend.py`.
   - Broad: `python3 shike/validation/validate_real_world_ready.py`.
6. If you change user-visible copy that validators grep for, update validators/docs together.

## Reusable modules or commands

Commands (run from workspace root):

```bash
python3 shike/validation/validate_android_structure.py
python3 shike/validation/validate_android_unit_tests.py
python3 shike/validation/validate_action_execution.py
python3 shike/validation/validate_model_bridge.py
python3 shike/backend/verify_backend.py
python3 shike/validation/validate_demo_acceptance.py
python3 shike/validation/validate_real_world_ready.py
python3 shike/scripts/verify_core20_package.py "/path/to/core20-package"
```

## High-risk mistakes

- Breaking confirmation gating so calendar/reminder/map can execute before user confirmation.
- Introducing secrets into Android/APK, docs, materials, prototype, logs, tests, or skills.
- Changing schema/contracts without updating backend + Android mapping + validators + samples.
- Weakening or deleting validators instead of fixing the underlying regression.
- Assuming cloud-device support exists without repo evidence; mark as "未确认" unless proven.

## Validation

Minimum for any non-trivial change:

```bash
python3 shike/validation/validate_real_world_ready.py
```

If your change is doc-only:

```bash
# If git is available, prefer:
#   git diff -- shike/AGENTS.md shike/.agents/skills shike/docs shike/README.md
# In this workspace git may be unavailable; in that case, list touched files and run:
python3 shike/validation/validate_secret_hygiene.py
python3 shike/validation/validate_real_world_ready.py
```
