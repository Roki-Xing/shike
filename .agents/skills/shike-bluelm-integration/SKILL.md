---
name: shike-bluelm-integration
description: Integrate vivo BlueLM (蓝心大模型) via backend-only adapters with strict secret hygiene and contract validation; Android must never contain AppKEY.
---

# shike-bluelm-integration

## When to use

Use this skill when implementing or changing any BlueLM/蓝心 related behavior, including:

- Adding backend environment-variable configuration for BlueLM (AppID/AppKEY, base URL, model name, timeout/retries).
- Implementing a `BlueLMModelAdapter` (and optional recorded adapter) behind a `ModelAdapter` abstraction.
- Adding signature/auth header generation for vivo gateway (exact algorithm is project-specific; must come from official docs; mark anything not confirmed as "未确认").
- Adding fallback behavior for timeouts/429/auth failures while preserving `/v1/analyze` contract.
- Adding validators and tests to prove secrets are not leaked and mock fallback still works.

## Must read first

1. `AGENTS.md` (red lines)
2. `docs/SHIKE_LANDING_APP_OPTIMIZATION_GUIDE.md` (BlueLM sections + secret rules)
3. `contracts/model-output.schema.json` (contract SSOT)
4. `contracts/model-adapter.md` (adapter boundary guidance)
5. `backend/shike_backend/main.py` (current mock behavior SSOT)
6. `backend/verify_backend.py`
7. `validation/validate_model_bridge.py`
8. `validation/validate_real_world_ready.py`

## Existing project facts (from repo)

- Backend already has a `ModelAdapter` boundary and includes `BlueLMModelAdapter` + `RecordedBlueLMAdapter` skeletons. Default remains mock; BlueLM is enabled only via env (see `backend/shike_backend/main.py` + `backend/shike_backend/settings.py`).
- Android must not contain BlueLM AppKEY. Android only points to the Shike backend (`README.md`, plus repo red lines).
- The repo's current docs propose env vars like `BLUELM_APP_ID`, `BLUELM_APP_KEY`, `BLUELM_TIMEOUT_SECONDS`, `BLUELM_MAX_RETRIES` as placeholders.
- `validation/validate_secret_hygiene.py` exists and must remain green before/after any BlueLM work.
- Landable gates exist for BlueLM plumbing and contract strictness:
  - `python3 shike/validation/validate_bluelm_adapter.py`
  - `python3 shike/validation/validate_model_contract_strict.py`
  - `python3 shike/validation/validate_cloud_backend_ready.py`

## Recommended workflow (safe + landable)

1. Build guardrails first (before any network calls):
   - Keep the secret hygiene validator green (`validation/validate_secret_hygiene.py`) and run it before any BlueLM-related change.
   - Ensure no secrets can accidentally land in Android, docs, materials, prototype, tests, logs, or skills.
2. Introduce adapter boundary:
   - Add a `ModelAdapter` abstraction in backend.
   - Keep `MockModelAdapter` as the default and as fallback.
3. Implement `BlueLMModelAdapter`:
   - Read BlueLM secrets only from backend environment variables.
   - Add strict response validation: Pydantic + JSON Schema alignment with `contracts/model-output.schema.json`.
   - On failure, return a safe “needs manual review” or fallback output that still matches contract.
4. Evidence for reviewers:
   - Provide deterministic smoke tests without real keys.
   - Provide demo flow where "cloud enhancement" can be toggled and gracefully degraded.

## Reusable modules or commands

- Backend smoke:
  - `python3 shike/backend/verify_backend.py`
- Bridge & readiness:
  - `python3 shike/validation/validate_model_bridge.py`
  - `python3 shike/validation/validate_real_world_ready.py`
- Secret hygiene gate:
  - `python3 shike/validation/validate_secret_hygiene.py`
- BlueLM adapter gates (no real keys required):
  - `python3 shike/validation/validate_bluelm_adapter.py`
  - `python3 shike/validation/validate_model_contract_strict.py`
  - `python3 shike/validation/validate_cloud_backend_ready.py`
- Model eval (writes report):
  - `python3 shike/backend/shike_backend/eval/run_model_eval.py`
- Recording helper (requires real keys):
  - `python3 shike/backend/shike_backend/eval/record_cases.py`
- Manual grep (quick check):
  - `rg -n --hidden --no-ignore -S "BLUELM_APP_KEY|AppKEY|sk-" shike`

## High-risk mistakes

- Putting AppKEY or any secret into Android sources/resources/APK.
- Logging or printing request headers, signatures, tokens, or raw OCR.
- Making BlueLM a hard dependency (breaking offline demos); always keep mock fallback.
- Breaking `/health`, `/v1/schema`, `/v1/analyze` routes or `contracts/model-output.schema.json`.

## Validation

Minimum:

```bash
python3 shike/backend/verify_backend.py
python3 shike/validation/validate_model_bridge.py
python3 shike/validation/validate_real_world_ready.py
```

Before adding BlueLM calls:

- `python3 shike/validation/validate_secret_hygiene.py` (must be PASS).
