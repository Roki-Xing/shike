# BlueLM / vivo AIGC Integration Runbook

This runbook documents how the Shike backend talks to vivo AIGC (contest doc center),
and how to verify it end-to-end without leaking secrets.

## 1. Scope

- This repo keeps Android **free of AppKEY**. All vivo credentials are backend-only.
- Backend route contract stays stable:
  - `GET /health`
  - `GET /v1/schema`
  - `POST /v1/analyze`
- Provider is selected via `SHIKE_MODEL_PROVIDER`:
  - `mock` (default)
  - `bluelm`
  - `recorded_bluelm`

## 2. Current Auth Choice

The contest doc center for LLM calls uses **Bearer AppKey** for authentication.

Backend adapter implementation: `backend/shike_backend/adapters/bluelm_adapter.py`

Notes:
- `backend/shike_backend/adapters/vivo_auth.py` implements **AI Gateway signature headers**.
  It is kept as a fallback/reference for other vivo endpoints, but **is not used** by
  the current `/v1/chat/completions` adapter path.

## 3. Endpoint & Required Params

Default base URL:

- `BLUELM_BASE_URL=https://api-ai.vivo.com.cn`

Default URI (OpenAI-compatible):

- `BLUELM_URI=/v1/chat/completions`

Required headers:

- `Authorization: Bearer ${BLUELM_APP_KEY}`
- `Content-Type: application/json`

Required query:

- `requestId=<uuid>`

## 4. Model Names & Model-Specific Body Fields

Doc center model list (examples):

- `Volc-DeepSeek-V3.2`
- `Doubao-Seed-2.0-mini`
- `Doubao-Seed-2.0-lite`
- `Doubao-Seed-2.0-pro`
- `qwen3.5-plus`

Important: some body fields differ by model:

- DeepSeek / Doubao:
  - deep-thinking switch uses `thinking.type` with values:
    - `enabled`
    - `disabled`
- qwen:
  - deep-thinking switch uses `enable_thinking: true|false`

The adapter defaults are conservative for structured extraction:
- `thinking.type=disabled` for non-qwen models
- `enable_thinking=false` for qwen models
- `response_format={"type":"json_object"}` when supported, to reduce ``` fences.

## 5. Environment Variables (Backend Only)

Example (DO NOT COMMIT REAL VALUES):

```bash
export SHIKE_MODEL_PROVIDER="bluelm"
export SHIKE_ALLOW_MOCK_FALLBACK="true"

export BLUELM_APP_ID="***"
export BLUELM_APP_KEY="***"
export BLUELM_BASE_URL="https://api-ai.vivo.com.cn"
export BLUELM_URI="/v1/chat/completions"
export BLUELM_MODEL="Volc-DeepSeek-V3.2"
export BLUELM_TIMEOUT_SECONDS="12"
export BLUELM_MAX_RETRIES="1"
export BLUELM_TEMPERATURE="0.2"
```

## 6. Verification Checklist

1. No secrets in repo:

```bash
python3 shike/validation/validate_secret_hygiene.py
```

2. Backend still healthy and contract still valid:

```bash
python3 shike/backend/verify_backend.py
```

3. Adapter plumbing gates:

```bash
python3 shike/validation/validate_bluelm_adapter.py
python3 shike/validation/validate_model_contract_strict.py
```

4. Live run (backend server):

```bash
python3 -m uvicorn shike_backend.main:app --host 0.0.0.0 --port 8000
```

5. Optional: generate a 100-case report (synthetic cases only):

```bash
python3 shike/backend/shike_backend/eval/run_model_eval.py
```

## 7. Safe Logging Rules

If you add logs around online calls, keep them minimal and redacted:

```text
provider=bluelm
request_id=...
key_present=true
ocr_length=...
result_schema_valid=true
```

Never log:
- `BLUELM_APP_KEY` value
- signature strings
- full OCR text (use length only, or a redacted sample if absolutely needed)

