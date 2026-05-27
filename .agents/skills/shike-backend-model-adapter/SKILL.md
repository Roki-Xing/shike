---
name: shike-backend-model-adapter
description: Work on Shike backend (FastAPI) and model adapter evolution while preserving /health, /v1/schema, /v1/analyze, and contracts/model-output.schema.json.
---

# shike-backend-model-adapter

## When to use

Use this skill for backend/API/contract work, including:

- Editing FastAPI routes: `GET /health`, `GET /v1/schema`, `POST /v1/analyze`.
- Keeping backend `AnalyzeResponse` aligned with `contracts/model-output.schema.json` (SSOT).
- Migrating `/v1/analyze` from rule/mock responses to a swappable `ModelAdapter` architecture (Mock / BlueLM / OpenAI compatible), while keeping mock fallback.
- Improving smoke tests, contract validation, error handling, and safe logging.

## Must read first

1. `AGENTS.md`
2. `backend/shike_backend/main.py`
3. `contracts/model-output.schema.json`
4. `backend/verify_backend.py`
5. `contracts/model-adapter.md`
6. `validation/validate_model_bridge.py`
7. `docs/device-runbook.md`
8. `README.md`

## Existing project facts (from repo)

- Backend entry is `backend/shike_backend/main.py` (FastAPI).
- Implemented routes:
  - `GET /health` returns `{"status":"ok"}`.
  - `GET /v1/schema` returns the JSON loaded from `contracts/model-output.schema.json`.
  - `POST /v1/analyze` returns `AnalyzeResponse` for `AnalyzeRequest` (Pydantic v2 models; `extra="forbid"` is applied on output models, not guaranteed on the request model).
- Current `/v1/analyze` behavior is rule/mock-style (keyword + `scene_hint` routing), not a real model adapter.
- Contract SSOT:
  - `contracts/model-output.schema.json` has required top-level keys:
    `scene_type`, `confidence`, `title`, `time`, `location`, `task`, `suggested_actions`, `missing_fields`, `explanation`.
  - `time` and `location` may be `null`, but the keys must exist in the payload.
  - `additionalProperties=false` is part of the contract.
- Smoke test:
  - `backend/verify_backend.py` uses `fastapi.testclient.TestClient` and validates `/health`, `/v1/schema`, `/v1/analyze` without starting a server.
  - `validation/validate_model_bridge.py` calls `python3 shike/backend/verify_backend.py` to keep the bridge stable.

## Recommended workflow

1. Lock the contract first:
   - Read `contracts/model-output.schema.json` and ensure required keys remain present.
   - Do not loosen `additionalProperties=false` unless you also update Android mapping + validators + docs.
2. Preserve route stability:
   - Do not rename or remove `/health`, `/v1/schema`, or `/v1/analyze`.
3. If introducing adapters:
   - Keep `/v1/analyze` as a thin orchestrator: adapter call -> validation -> response.
   - Keep `MockModelAdapter` as fallback; do not make BlueLM a hard dependency for demos/tests.
4. Logging and privacy:
   - Do not log raw OCR or secrets.
   - If you need diagnostics, log masked metadata only (e.g., `key_present=true`, lengths, statuses).

## Reusable modules or commands

Commands (run from workspace root):

```bash
python3 shike/backend/verify_backend.py
python3 shike/validation/validate_model_bridge.py
python3 shike/validation/validate_real_world_ready.py
```

Local server (LAN only, per `docs/device-runbook.md`):

```bash
cd shike/backend
python3 -m uvicorn shike_backend.main:app --host 0.0.0.0 --port 8000
```

## High-risk mistakes

- Breaking contracts:
  - Removing required keys or changing enums without updating schema/samples/Android/validators/docs.
  - Returning payloads missing `time`/`location` keys (even if values can be null).
  - Weakening Pydantic `extra="forbid"` or schema `additionalProperties=false` without a coordinated migration.
- Secret leakage:
  - Printing any AppKEY/token/signature or raw OCR in logs, docs, tests, materials, prototype, or skills.
- Hard dependency on online model:
  - Making BlueLM mandatory breaks offline demos; keep mock fallback.

## Validation

Minimum:

```bash
python3 shike/backend/verify_backend.py
python3 shike/validation/validate_model_bridge.py
```

Recommended full check after meaningful changes:

```bash
python3 shike/validation/validate_real_world_ready.py
```
