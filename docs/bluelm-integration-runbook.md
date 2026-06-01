# BlueLM / vivo AIGC Integration Runbook

This runbook documents how the Shike backend talks to vivo AIGC (contest doc center),
and how to verify it end-to-end without leaking secrets.

## 1. Scope

- This repo keeps Android **free of AppKEY**. All vivo credentials are backend-only.
- Android 不得持有 `BLUELM_APP_ID`、`BLUELM_APP_KEY` 或任何 AppKEY；这些值只能由后端从环境变量读取。
- Backend route contract stays stable:
  - `GET /health`
  - `GET /v1/schema`
  - `POST /v1/analyze`
- `/v1/analyze` accepts `source_type` values `screenshot`, `camera`, `share_text`, and `manual`; scene output is still governed by `contracts/model-output.schema.json`.
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

Doc center source checked on 2026-05-29:

- `https://aigc.vivo.com.cn/#/document/index?id=1677` for auth.
- `https://aigc.vivo.com.cn/#/document/index?id=1745` for `/v1/chat/completions`.

The document center is a SPA; the underlying read-only doc API used for this
check was `/vstack/webapi/service/doc/info/v1?docId=1745&businessCode=...`.
Do not place credentials in that URL or in repo files.

Doc center model list:

- `Volc-DeepSeek-V3.2`
- `Doubao-Seed-2.0-mini`
- `Doubao-Seed-2.0-lite`
- `Doubao-Seed-2.0-pro`
- `qwen3.5-plus`

Important: some body fields differ by model:

- DeepSeek / Doubao use `thinking.type`.
  - The doc table labels the field as `thinking.type : "enable"` and also explains
    `enabled` / `disabled` as the semantic values.
  - Because provider examples and live behavior can diverge, Shike does **not**
    hard-code this field by default.
- qwen uses `enable_thinking: true|false`.

The adapter defaults are conservative for compatibility:

- `BLUELM_THINKING_MODE=provider_default` by default, so no model-specific
  thinking field is sent unless the operator explicitly opts in.
- `BLUELM_THINKING_MODE=disabled` maps to:
  - DeepSeek / Doubao: `thinking.type="disabled"`
  - qwen: `enable_thinking=false`
- `BLUELM_THINKING_MODE=enabled` maps to:
  - DeepSeek / Doubao: `thinking.type="enabled"`
  - qwen: `enable_thinking=true`
- `BLUELM_THINKING_MODE=enable` maps to:
  - DeepSeek / Doubao: `thinking.type="enable"` for doc-table compatibility.
  - qwen: `enable_thinking=true`
- `BLUELM_RESPONSE_FORMAT=true` sends `response_format={"type":"json_object"}`
  to reduce fenced Markdown when the endpoint supports OpenAI-compatible JSON mode.
  Set `BLUELM_RESPONSE_FORMAT=false` if a model rejects that field.

Request ID parameter:

- The parameter table says `requestId`.
- Python examples in the same doc also show `request_id`.
- Shike defaults to `BLUELM_REQUEST_ID_PARAM=requestId` and exposes the env var so
  a deployment can switch without code changes if a key/model requires `request_id`.

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
export BLUELM_THINKING_MODE="provider_default"
export BLUELM_REQUEST_ID_PARAM="requestId"
export BLUELM_RESPONSE_FORMAT="true"
```

Useful body-compatibility overrides:

```bash
# Keep provider defaults; safest first live test.
export BLUELM_THINKING_MODE="provider_default"

# Force no deep thinking for structured extraction, if the selected model accepts it.
export BLUELM_THINKING_MODE="disabled"

# If the selected qwen model rejects response_format, disable it without code changes.
export BLUELM_RESPONSE_FORMAT="false"
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

5. Optional: generate a 110-case report (synthetic cases only):

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
