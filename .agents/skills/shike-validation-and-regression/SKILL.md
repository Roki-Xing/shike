---
name: shike-validation-and-regression
description: Maintain and extend Shike validators/regression suites without weakening gates; run the right checks for Android/backend/contracts/demo readiness.
---

# shike-validation-and-regression

## When to use

Use this skill when you:

- modify any `validation/*.py` script or anything they check,
- diagnose why a validator failed,
- change Android UI copy/paths that validators grep for,
- change contracts/schema or backend response shape,
- add new regression cases or tighten acceptance criteria.

## Must read first

1. `AGENTS.md`
2. `README.md` (mechanical acceptance command list)
3. `docs/current-validation-status.md`
4. `validation/validate_real_world_ready.py` (aggregator)
5. Key validators by domain:
   - `validation/validate_android_structure.py`
   - `validation/validate_android_unit_tests.py`
   - `validation/validate_action_execution.py`
   - `validation/validate_model_bridge.py`
   - `validation/validate_demo_acceptance.py`
   - `validation/validate_deliverables.py`
   - `validation/validate_landable.py`

## Existing project facts (from repo)

- Validators are treated as deliverables; do not delete or weaken them.
- `validate_real_world_ready.py` is the broad readiness aggregator and should remain green.
- Demo acceptance is enforced by `validate_demo_acceptance.py` and ties to:
  - `materials/device-demo-checklist.md`
  - `prototype/demo.html`
  - command-style consistency across README/checklist/demo console.
- Android structure and unit test gates are numeric metrics:
  - `ANDROID_STRUCTURE_METRIC 31/31`
  - `ANDROID_UNIT_TEST_METRIC 61/61`
- Execution safety gate is a numeric metric:
  - `ACTION_EXECUTION_METRIC 17/17`
- Model bridge gate checks Android -> backend `/v1/analyze` existence and calls backend smoke:
  - `MODEL_BRIDGE_METRIC 14/14`

## Recommended workflow

1. Classify the change:
   - Android-only: run structure + unit tests + action execution.
   - Backend-only: run `verify_backend.py` + model bridge.
   - Contract changes: update schema + samples + backend + Android mapping, then run model bridge + readiness.
   - Materials/prototype changes: run demo acceptance + readiness.
2. Never "fix" a failing validator by loosening it unless the requirement truly changed.
3. Prefer adding narrow checks close to the bug you are preventing; keep the aggregator intact.
4. If validators grep for exact Chinese tokens, update them intentionally and update docs/checklists consistently.

## Reusable modules or commands

Run from workspace root:

```bash
python3 shike/validation/validate_android_structure.py
python3 shike/validation/validate_android_unit_tests.py
python3 shike/validation/validate_action_execution.py
python3 shike/validation/validate_model_bridge.py
python3 shike/validation/validate_demo_acceptance.py
python3 shike/validation/validate_real_world_ready.py
python3 shike/validation/validate_deliverables.py
python3 shike/validation/validate_landable.py
python3 shike/backend/verify_backend.py
python3 shike/spike/run_spike.py --all
```

## High-risk mistakes

- Changing commands in README but not in `materials/device-demo-checklist.md` or `prototype/demo.html`.
- Changing schema but not updating samples, backend response, Android mapping, and validators.
- Making validators depend on real secrets or external accounts.
- Removing regression coverage when refactoring (prefer updating guard expectations instead).

## Validation

- For validator changes, always run:
  - the changed validator itself,
  - the nearest broader gate (often `validate_real_world_ready.py`).

```bash
python3 shike/validation/validate_real_world_ready.py
```

