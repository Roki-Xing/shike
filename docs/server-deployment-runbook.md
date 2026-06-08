# Shike Server Deployment Runbook

This runbook turns the desktop deep-review Goal B into an operator checklist for
deploying the Shike backend behind HTTPS. It is documentation-only: it does not
prove that `roky.chat` is live, and it does not store credentials.

## Scope

Use this runbook when preparing the backend that vivo cloud devices will call
during recording.

Required public routes:

```text
GET  /health
GET  /v1/schema
POST /v1/ocr
POST /v1/analyze
```

Expected cloud-device endpoint:

```text
https://roky.chat
```

Optional split endpoint:

```text
https://api.roky.chat
```

## Secret Boundary

Allowed locations:

- Local shell session during smoke testing
- Server environment file such as `/etc/shike/shike-backend.env`
- CI or platform secret store

Forbidden locations:

- Android source, resources, BuildConfig, assets, APK
- README, docs, materials, validation fixtures, prototype files
- Git commit messages, screenshots, videos, backend logs

Recommended environment-file permission:

```bash
sudo install -d -m 750 -o root -g www-data /etc/shike
sudo install -m 640 -o root -g www-data /dev/null /etc/shike/shike-backend.env
```

Example redacted environment file:

```bash
SHIKE_MODEL_PROVIDER=bluelm
SHIKE_ALLOW_MOCK_FALLBACK=true
SHIKE_ALLOW_OCR_FALLBACK=true

VIVO_APP_ID=***
VIVO_APP_KEY=***
VIVO_CHAT_BASE_URL=https://api-ai.vivo.com.cn/v1
VIVO_CHAT_MODEL=Volc-DeepSeek-V3.2

BLUELM_APP_ID=***
BLUELM_APP_KEY=***
BLUELM_BASE_URL=https://api-ai.vivo.com.cn
BLUELM_URI=/v1/chat/completions
BLUELM_MODEL=Volc-DeepSeek-V3.2
BLUELM_TIMEOUT_SECONDS=12
BLUELM_MAX_RETRIES=1
BLUELM_TEMPERATURE=0.2
BLUELM_THINKING_MODE=provider_default
BLUELM_REQUEST_ID_PARAM=requestId
BLUELM_RESPONSE_FORMAT=true

VIVO_AIGC_APP_ID=***
VIVO_AIGC_APP_KEY=***

VIVO_OCR_APP_ID=***
VIVO_OCR_APP_KEY=***
VIVO_OCR_BASE_URL=https://api-ai.vivo.com.cn
VIVO_OCR_URI=/ocr/general_recognition
VIVO_OCR_TIMEOUT_SECONDS=8
VIVO_OCR_MAX_RETRIES=1

VIVO_MULTIMODAL_APP_ID=***
VIVO_MULTIMODAL_APP_KEY=***
VIVO_MULTIMODAL_BASE_URL=https://api-ai.vivo.com.cn
VIVO_MULTIMODAL_URI=/v1/chat/completions
VIVO_MULTIMODAL_MODEL=Volc-DeepSeek-V3.2
VIVO_MULTIMODAL_MODELS=Volc-DeepSeek-V3.2,Doubao-Seed-2.0-mini,Doubao-Seed-2.0-lite,Doubao-Seed-2.0-pro,qwen3.5-plus
VIVO_MULTIMODAL_TIMEOUT_SECONDS=60
VIVO_MULTIMODAL_MAX_RETRIES=1

# Optional OCR-first text structuring provider. DeepSeek does not replace OCR;
# it consumes OCR text and returns the same Shike JSON Schema.
DEEPSEEK_API_KEY=***
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_URI=/chat/completions
DEEPSEEK_MODEL=deepseek-v4-flash
DEEPSEEK_TIMEOUT_SECONDS=20
DEEPSEEK_MAX_RETRIES=1
DEEPSEEK_TEMPERATURE=0.1
DEEPSEEK_THINKING_ENABLED=false
DEEPSEEK_RESPONSE_FORMAT=true
```

`VIVO_APP_ID`, `VIVO_APP_KEY`, `VIVO_CHAT_BASE_URL`, and `VIVO_CHAT_MODEL` match
the Android 16 implementation guide and are accepted as backend-only aliases.
More specific `BLUELM_*`, `VIVO_OCR_*`, and `VIVO_MULTIMODAL_*` values override
the aliases when present. Keep all real values only in the server env file or a
secret store.

If `VIVO_MULTIMODAL_MODELS` is omitted, the backend still tries the built-in
candidate chain in this order: `VIVO_MULTIMODAL_MODEL`, `vivo-BlueLM-V-2.0`,
`BlueLM-Vision-prd`, `Volc-DeepSeek-V3.2`, `Doubao-Seed-2.0-mini`,
`Doubao-Seed-2.0-lite`, `Doubao-Seed-2.0-pro`, and `qwen3.5-plus`. This keeps a
fresh server deploy usable with only the primary model configured while
preserving explicit candidate ordering for operators who need to override it.

## Server Layout

Recommended target layout:

```text
/opt/shike/
  backend/
    shike_backend/
    requirements.txt
    .venv/
  logs/
    backend-redacted-access.log

/etc/shike/
  shike-backend.env
```

Do not place SSH keys under `/opt/shike` or inside the repository.

## Build And Install

Run on the server after copying the backend source:

```bash
cd /opt/shike/backend
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
PYTHONPATH=/opt/shike/backend python -m shike_backend.eval.live_smoke --skip-ocr --timeout-seconds 20
PYTHONPATH=/opt/shike/backend python -m shike_backend.eval.http_server_smoke --timeout-seconds 35
```

The smoke command must print only redacted evidence fields. It must not print
AppKEY, `Authorization`, base64 image payloads, or full OCR text.

## systemd Service

Use a non-root runtime user such as `www-data`.

```ini
[Unit]
Description=Shike Backend API
After=network.target

[Service]
WorkingDirectory=/opt/shike/backend
EnvironmentFile=/etc/shike/shike-backend.env
ExecStart=/opt/shike/backend/.venv/bin/python -m uvicorn shike_backend.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=3
User=www-data
Group=www-data
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Install and start:

```bash
sudo install -m 644 shike-backend.service /etc/systemd/system/shike-backend.service
sudo systemctl daemon-reload
sudo systemctl enable --now shike-backend
sudo systemctl status shike-backend --no-pager
```

## Nginx HTTPS Proxy

Minimal reverse proxy:

```nginx
server {
    listen 80;
    server_name roky.chat api.roky.chat;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Issue certificates:

```bash
sudo apt update
sudo apt install -y nginx certbot python3-certbot-nginx
sudo certbot --nginx -d roky.chat -d api.roky.chat
```

If only one DNS name is available, issue the certificate for `roky.chat` only.

## Public Verification

Run from a machine outside the server:

```bash
curl -fsS https://roky.chat/health
curl -fsS https://roky.chat/v1/schema
curl -fsS https://roky.chat/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"input_id":"cloud-smoke-001","source_type":"screenshot","ocr_text":"高数A班今晚18:30改到B203，作业第5章今晚22:00前提交。","scene_hint":"course_notice","locale":"zh-CN","user_timezone":"Asia/Shanghai"}'
```

Expected result:

- `/health` returns `200` and `{"status":"ok"}`
- `/v1/schema` returns the Shike model-output schema
- `/v1/analyze` returns schema-compatible JSON
- Backend logs remain redacted

## Redacted Access Log Shape

Recommended line format:

```text
provider=bluelm
model=Volc-DeepSeek-V3.2
request_id=...
source_type=screenshot
ocr_length=34
result_schema_valid=true
latency_ms=1234
fallback_used=false
```

For OCR smoke:

```text
provider=vivo_general_ocr
request_id=...
image_persisted=false
image_cleared=true
ocr_text_length=160
latency_ms=323
```

Never log:

- `Authorization`
- AppKEY or backend token
- full OCR text
- base64 image payload
- phone number, email, student ID, group message, personal notification

## Cloud-Device Handoff Gate

Before recording cloud-device videos:

```bash
python3 shike/validation/validate_cloud_backend_ready.py
python3 shike/scripts/prepare_cloud_device_evidence.py
python3 shike/scripts/run_release_handoff_checks.py --strict
```

This proves the local handoff package is ready and that strict evidence remains
honest. It does not replace the real external proof: nine cloud-device MP4
recordings, a filled report with no placeholders, and non-placeholder redacted
logcat.
