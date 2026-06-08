# Shike Product Manager Deep Review Guide

Source reference: `/mnt/c/Users/Xing/Desktop/SHIKE_PRODUCT_MANAGER_DEEP_REVIEW_GUIDE.md`

This repository copy keeps the product-manager review actionable without storing
secrets. The desktop file is the full source; this file records the project
implementation contract and current execution priorities.

## Current Product Judgment

Shike is past idea prototype and is now a local release-candidate / contest
landing candidate. The strongest proof is not another concept deck; it is a
working Android APK, a backend model-orchestration service, schema-validated AI
output, cloud-device evidence, and a safe fallback path.

The remaining final-release gaps are evidence gaps, not feature-name gaps:

- real cloud-device MP4 recordings,
- a filled cloud-device report with no placeholders,
- redacted online BlueLM/OCR logs,
- HTTPS backend evidence reachable by vivo cloud devices,
- user research and scoring material backed by real data instead of claims.

## Product Experience Direction

The normal user home screen should answer one question: what should I handle
today?

Keep on the home/import/confirm/action/inbox surfaces:

- today action card,
- upcoming deadline,
- pending confirmation,
- gallery screenshot import,
- camera poster import,
- share-text import,
- manual paste fallback,
- field confirmation and risk labels,
- calendar/reminder/map action state,
- inbox search, filters, archive and restore.

Move engineering-only controls into `DebugDemoScreen` or advanced settings:

- backend URL,
- sample buttons,
- validation copy,
- delivery self-check,
- three-minute demo route,
- raw debug logs.

All actions must remain user-confirmed. Do not claim automatic calendar writes;
use "opened system calendar insert page; user saves it".

## vivo AIGC API Contract

Official docs checked on 2026-06-03:

- `id=1746`: usage guide and AI ability list.
- `id=1677`: Bearer AppKey authentication.
- `id=1745`: LLM `/v1/chat/completions`.
- `id=1737`: General OCR `/ocr/general_recognition`.

Backend-only chain:

```text
Android APK
  -> Shike backend /v1/ocr and /v1/analyze
  -> vivo AIGC OCR / BlueLM APIs
```

Forbidden chain:

```text
Android APK
  -> vivo AIGC APIs directly
```

Reason: Android APK must never contain AppKEY, Authorization headers, gateway
signatures, or provider secrets.

### LLM

Implementation: `backend/shike_backend/adapters/bluelm_adapter.py`

- Endpoint: `https://api-ai.vivo.com.cn/v1/chat/completions`
- Header: `Authorization` header using backend-only `BLUELM_APP_KEY`
- Query: `requestId=<uuid>`
- Body: OpenAI-compatible `model`, `messages`, `stream`, optional
  `response_format`, model-specific `thinking.type` or `enable_thinking`.

### OCR Import

Implementation: `backend/shike_backend/adapters/vivo_ocr_adapter.py`

- Endpoint: `https://api-ai.vivo.com.cn/ocr/general_recognition`
- Header: `Authorization` header using backend-only `VIVO_OCR_APP_KEY`
- Query: `requestId=<uuid>`
- Form body: `image`, `pos`, `businessid=aigc + AppID`, `sessid`.
- Shike route: `POST /v1/ocr`
- Fallback: manual paste message, no image persistence.

## Cloud Device Evidence

Strict release still requires nine real cloud-device recordings under
`materials/evidence/cloud-device/`:

```text
01-cloud-install-open.mp4
02-cloud-gallery-bluelm.mp4
03-cloud-camera-bluelm.mp4
04-cloud-share-text.mp4
05-cloud-permission-fallback.mp4
06-cloud-backend-failure.mp4
07-cloud-restart-restore.mp4
08-cloud-ui-polish.mp4
09-cloud-final-route.mp4
```

The cloud-device report must include device, APK hash, HTTPS backend status,
provider mode, video evidence, result, and blockers. It must not contain AppKEY,
tokens, full OCR text, real personal data, or raw base64 images.

## User Research Evidence

Do not fabricate interview data. Until interviews are complete, mark it as a
plan. Recommended sample:

- 4 college students,
- 2 club or event organizers,
- 2 interns / young professionals,
- 2 frequent event or travel users.

Track:

- task screenshots in the past week,
- how many were handled,
- missed events caused by screenshots sleeping in album,
- willingness to try confirmable action cards,
- privacy and wrong-action concerns.

## Validation Gates

Run from workspace root:

```bash
python3 shike/validation/validate_secret_hygiene.py
python3 shike/backend/verify_backend.py
python3 shike/validation/validate_bluelm_adapter.py
python3 shike/validation/validate_vivo_ocr_adapter.py
python3 shike/validation/validate_release_evidence_index.py
python3 shike/validation/validate_landing_release_candidate.py
```

Strict gates remain external-evidence gates:

```bash
python3 shike/validation/validate_cloud_device_package.py --strict
python3 shike/validation/validate_landing_release_candidate.py --strict
```

If strict evidence is missing, keep `materials/evidence/blocking-report.md`
explicit. Do not fabricate recordings, logs, report fields, credentials, or user
research.
