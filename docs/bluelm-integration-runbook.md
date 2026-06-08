# BlueLM / vivo AIGC Integration Runbook

This runbook documents how the Shike backend talks to vivo AIGC (contest doc center),
and how to verify it end-to-end without leaking secrets.

## 1. Scope

- This repo keeps Android **free of AppKEY**. All vivo credentials are backend-only.
- Android 不得持有 `BLUELM_APP_ID`、`BLUELM_APP_KEY` 或任何 AppKEY；这些值只能由后端从环境变量读取。
- Backend route contract stays stable:
  - `GET /health`
  - `GET /v1/schema`
  - `POST /v1/ocr`
  - `POST /v1/analyze`
- `/v1/analyze` accepts `source_type` values `screenshot`, `camera`, `share_text`, and `manual`; scene output is still governed by `contracts/model-output.schema.json`.
- `/v1/ocr` accepts screenshot/camera `image_base64` imports and returns redacted OCR text or a manual-continuation fallback.
- `/v2/analyze-image` accepts Android image data URLs plus OCR hints; the backend may run server-side vivo OCR first, merge OCR text and coordinate blocks into the v2 request, filter device chrome blocks, then call the vivo multimodal adapter.
- Provider is selected via `SHIKE_MODEL_PROVIDER`:
  - `mock` (default)
  - `bluelm`
  - `recorded_bluelm`

## 2. Current Auth Choice

The contest doc center for LLM calls uses **Bearer AppKey** for authentication.
The contest doc center for General OCR also uses **Bearer AppKey** with a form body.

Backend adapter implementation: `backend/shike_backend/adapters/bluelm_adapter.py`
OCR adapter implementation: `backend/shike_backend/adapters/vivo_ocr_adapter.py`

Notes:
- `backend/shike_backend/adapters/vivo_auth.py` implements **AI Gateway signature headers**.
  It is used by the signed VisionChat fallback for `/vivogpt/completions` and is
  kept as a reference for other vivo endpoints. The current `/v1/chat/completions`
  and `/ocr/general_recognition` adapter paths still use Bearer AppKey.

## 3. Endpoint & Required Params

Default base URL:

- `BLUELM_BASE_URL=https://api-ai.vivo.com.cn`

Default URI (OpenAI-compatible):

- `BLUELM_URI=/v1/chat/completions`

Required headers:

- `Authorization` header using the backend-only `BLUELM_APP_KEY`
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

## 5. vivo OCR Import Endpoint & Required Params

Doc center source checked on 2026-06-03:

- `https://aigc.vivo.com.cn/#/document/index?id=1746` for the AI ability list.
- `https://aigc.vivo.com.cn/#/document/index?id=1737` for General OCR.
- `https://aigc.vivo.com.cn/#/document/index?id=1677` for Bearer AppKey auth.

Default OCR base URL:

- `VIVO_OCR_BASE_URL=https://api-ai.vivo.com.cn`

Default OCR URI:

- `VIVO_OCR_URI=/ocr/general_recognition`

Required headers:

- `Authorization` header using the backend-only `VIVO_OCR_APP_KEY`
- `Content-type: application/x-www-form-urlencoded`

Required query:

- `requestId=<uuid>`

Required form body:

```text
image=<base64 jpg/png/bmp>
pos=2
businessid=aigc + AppID
sessid=<uuid>
```

Shike backend route:

```http
POST /v1/ocr
Content-Type: application/json
```

```json
{
  "input_id": "cloud-ocr-001",
  "source_type": "screenshot",
  "image_base64": "base64-image-content",
  "locale": "zh-CN",
  "pos": 2
}
```

The backend does not persist the base64 image. If credentials are missing or OCR
fails, `SHIKE_ALLOW_OCR_FALLBACK=true` returns the user-safe message:

```text
未识别到稳定文字，可手动粘贴通知内容继续
```

Android 不得持有 `VIVO_OCR_APP_ID`、`VIVO_OCR_APP_KEY`、`VIVO_AIGC_APP_KEY`、
`BLUELM_APP_KEY` or any AppKEY.

`POST /v2/analyze-image` reuses the same backend-only OCR adapter as an enrichment step when `image.data_url` contains inline base64 image data. The route extracts only the base64 segment needed for the provider call, does not persist the image, merges redacted OCR text into `ocr_text_hint`, merges vivo coordinate blocks into `ocr_blocks`, and filters top status-bar / bottom-navigation blocks before the multimodal prompt is built. The route then tries `VIVO_MULTIMODAL_MODELS` in order. When no list is configured, settings build the default chain from `VIVO_MULTIMODAL_MODEL`, `vivo-BlueLM-V-2.0`, `BlueLM-Vision-prd`, `Volc-DeepSeek-V3.2`, `Doubao-Seed-2.0-mini`, `Doubao-Seed-2.0-lite`, `Doubao-Seed-2.0-pro`, and `qwen3.5-plus`. If the OpenAI-compatible image route rejects image input or returns provider authorization errors, the adapter also tries the signed VisionChat `/vivogpt/completions` body with `contentType=text/image`. OCR failure stays non-blocking by adding a non-secret risk marker such as `server_ocr_unavailable:*`. All downstream calendar, reminder, and map actions remain disabled until the user confirms the parsed card.

## 6. Environment Variables (Backend Only)

Example (DO NOT COMMIT REAL VALUES):

```bash
export SHIKE_MODEL_PROVIDER="bluelm"
export SHIKE_ALLOW_MOCK_FALLBACK="true"

export VIVO_APP_ID="***"
export VIVO_APP_KEY="***"
export VIVO_CHAT_BASE_URL="https://api-ai.vivo.com.cn/v1"
export VIVO_CHAT_MODEL="Volc-DeepSeek-V3.2"

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

export VIVO_OCR_APP_ID="***"
export VIVO_OCR_APP_KEY="***"
export VIVO_OCR_BASE_URL="https://api-ai.vivo.com.cn"
export VIVO_OCR_URI="/ocr/general_recognition"
export VIVO_OCR_TIMEOUT_SECONDS="8"
export VIVO_OCR_MAX_RETRIES="1"
export SHIKE_ALLOW_OCR_FALLBACK="true"

export VIVO_MULTIMODAL_MODEL="Volc-DeepSeek-V3.2"
export VIVO_MULTIMODAL_MODELS="Volc-DeepSeek-V3.2,Doubao-Seed-2.0-mini,Doubao-Seed-2.0-lite"
```

The Android 16 guide-style aliases `VIVO_APP_ID`, `VIVO_APP_KEY`,
`VIVO_CHAT_BASE_URL`, and `VIVO_CHAT_MODEL` are accepted for backend-only local
and server runs. `VIVO_CHAT_BASE_URL=https://api-ai.vivo.com.cn/v1` is normalized
internally to `BLUELM_BASE_URL=https://api-ai.vivo.com.cn` plus
`BLUELM_URI=/v1/chat/completions`. More specific `BLUELM_*`, `VIVO_OCR_*`, and
`VIVO_MULTIMODAL_*` values still take precedence when present.

If the same contest credential has both LLM and OCR abilities, operators may set
shared backend-only `VIVO_AIGC_APP_ID` / `VIVO_AIGC_APP_KEY`. `VIVO_OCR_*` takes
precedence when present. Never commit real values.

Local backend processes also auto-load a private env file before reading
settings:

```bash
chmod 600 "${HOME}/.config/shike/bluelm.env"
python3 -m uvicorn shike_backend.main:app --host 0.0.0.0 --port 8000
```

Default private file:

```text
~/.config/shike/bluelm.env
```

Override path when needed:

```bash
export SHIKE_BACKEND_ENV_FILE="/etc/shike/shike-backend.env"
```

The file may use `KEY=value` or `export KEY=value` lines. 进程环境变量优先于
private env file values, so operators can override one key for a single smoke
run without editing the file. Never commit real values, and never paste the
file contents into issue logs, README, materials, APK resources, or screenshots.

Useful body-compatibility overrides:

```bash
# Keep provider defaults; safest first live test.
export BLUELM_THINKING_MODE="provider_default"

# Force no deep thinking for structured extraction, if the selected model accepts it.
export BLUELM_THINKING_MODE="disabled"

# If the selected qwen model rejects response_format, disable it without code changes.
export BLUELM_RESPONSE_FORMAT="false"
```

## 7. Verification Checklist

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
python3 shike/validation/validate_vivo_ocr_adapter.py
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

6. Optional live smoke with real backend-only credentials:

```bash
PYTHONPATH=shike/backend \
SHIKE_MODEL_PROVIDER=bluelm \
SHIKE_ALLOW_MOCK_FALLBACK=false \
python3 shike/backend/shike_backend/eval/live_smoke.py \
  --ocr-image /path/to/synthetic-course-notice.png \
  --timeout-seconds 20
```

The script prints only redacted evidence fields such as `provider=bluelm`,
`result_schema_valid=true`, `ocr_provider=vivo_general_ocr`,
`image_persisted=false`, and `live_smoke_metric`. Do not pass real personal
screenshots; use a synthetic course notice image.

7. Optional live smoke for vivo image understanding (`/v2/analyze-image`):

```bash
PYTHONPATH=shike/backend \
python3 shike/backend/shike_backend/eval/live_smoke.py \
  --skip-bluelm \
  --skip-ocr \
  --multimodal \
  --multimodal-image /tmp/shike-live-smoke-synthetic.png \
  --timeout-seconds 25
```

This uses backend environment variables only. Expected redacted fields include
`multimodal_provider`, `multimodal_model`, `multimodal_configured`,
`multimodal_status`, and `multimodal_error`. The live smoke tries the configured
or default candidate models in order and stops at the first schema-valid image
result. The current secret-safe synthetic smoke records
`Volc-DeepSeek-V3.2` as `provider_model_does_not_support_image`, then selects
`Doubao-Seed-2.0-mini` with `multimodal_status=pass`,
`multimodal_scene_type=meeting_notice`, `multimodal_schema_valid=True`, and
`live_smoke_metric=1/1`. If all image candidates fail and the route has an OCR
hint, the backend should use the same OCR text with the BlueLM text adapter to
create a schema-valid action card. Every downstream action must stay disabled
until user confirmation. If OCR text is unavailable or any other provider error
occurs, the backend should keep manual review. The backend must never fall back
to a fixed training sample.

The official doc-center entry `docId=1745` describes image understanding through
`/v1/chat/completions` with `messages[].content` entries of type `text` and
`image_url`; this project mirrors that request shape in the backend adapter.

## 8. Safe Logging Rules

If you add logs around online calls, keep them minimal and redacted:

```text
provider=bluelm
ocr_provider=vivo_general_ocr
request_id=...
key_present=true
ocr_length=...
result_schema_valid=true
image_base64_present=true
image_persisted=false
```

Never log:
- `BLUELM_APP_KEY` value
- `VIVO_OCR_APP_KEY` value
- signature strings
- base64 image content
- full OCR text (use length only, or a redacted sample if absolutely needed)
