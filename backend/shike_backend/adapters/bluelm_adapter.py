"""BlueLM adapter (server-side) using vivo AIGC API.

This adapter is designed to be optional:
- Default backend behavior remains the deterministic Mock adapter.
- When `SHIKE_MODEL_PROVIDER=bluelm` and credentials are configured, it calls
  vivo AIGC API and validates the output against the Shike contract.
- On failure it raises AdapterError so the route can degrade safely.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

import requests

from shike_backend.adapters.base import AdapterError
from shike_backend.privacy import redact_ocr_text
from shike_backend.schemas import AnalyzeRequest, AnalyzeResponse, load_model_output_schema


_PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"
_SYSTEM_PROMPT_PATH = _PROMPTS_DIR / "analyze_system_prompt.txt"
_USER_TEMPLATE_PATH = _PROMPTS_DIR / "analyze_user_template.txt"


def _read_prompt(path: Path) -> str:
    if not path.is_file():
        raise AdapterError(f"missing_prompt_file:{path.name}")
    return path.read_text(encoding="utf-8")


def _extract_json(text: str) -> Any:
    candidate = text.strip()
    if candidate.startswith("```"):
        # Strip fenced code block if present.
        lines = [line for line in candidate.splitlines() if not line.strip().startswith("```")]
        candidate = "\n".join(lines).strip()
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        start = candidate.find("{")
        end = candidate.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(candidate[start : end + 1])
        raise


class BlueLMModelAdapter:
    def __init__(
        self,
        *,
        app_id: str | None,
        app_key: str | None,
        base_url: str,
        uri: str,
        model: str,
        timeout_seconds: int,
        max_retries: int,
        temperature: float,
    ) -> None:
        self._app_id = (app_id or "").strip()
        self._app_key = (app_key or "").strip()
        self._base_url = base_url.rstrip("/")
        self._uri = uri if uri.startswith("/") else f"/{uri}"
        self._model = model
        self._timeout_seconds = max(1, timeout_seconds)
        self._max_retries = max(0, max_retries)
        self._temperature = temperature

        self._system_prompt = _read_prompt(_SYSTEM_PROMPT_PATH)
        self._user_template = _read_prompt(_USER_TEMPLATE_PATH)
        self._schema = load_model_output_schema()

    def is_configured(self) -> bool:
        if not self._app_id or not self._app_key:
            return False
        if self._app_id in {"***", "..."} or self._app_key in {"***", "..."}:
            return False
        return True

    def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        if not self.is_configured():
            raise AdapterError("bluelm_not_configured")

        request_id = str(uuid.uuid4())
        session_id = str(uuid.uuid4())
        # Doc center requires requestId as a query param. Empirically both `requestId` and
        # `request_id` are accepted, but we follow the doc spelling.
        params = {"requestId": request_id}

        user_prompt = self._user_template.format(
            input_id=request.input_id,
            source_type=request.source_type,
            locale=request.locale,
            scene_hint=request.scene_hint or "",
            user_timezone=request.user_timezone,
            ocr_text=request.ocr_text,
            ocr_text_redacted=redact_ocr_text(request.ocr_text),
            schema_json=json.dumps(self._schema, ensure_ascii=False),
        )

        payload: dict[str, Any] = {
            "messages": [
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "model": self._model,
            # These fields are tolerated by the OpenAI-compatible endpoint, and may be required
            # by legacy endpoints. Keep them to reduce friction when switching URIs.
            "sessionId": session_id,
            "extra": {"temperature": self._temperature},
            # Reduce “helpful formatting”: when supported, this makes the model emit raw JSON
            # without ``` fences. Unknown fields are typically ignored, but if a given model
            # rejects it we'll fall back to parsing anyway.
            "response_format": {"type": "json_object"},
            "stream": False,
            "temperature": self._temperature,
        }

        # "Deep thinking" flags differ by model (per doc center).
        # Keep defaults conservative: we don't need deep reasoning for schema filling.
        model_name = (self._model or "").lower()
        if "qwen" in model_name:
            payload["enable_thinking"] = False
        else:
            payload["thinking"] = {"type": "disabled"}

        # AIGC doc "鉴权方式" uses Bearer AppKey (not gateway signature headers).
        # Keep headers minimal and never log/return secrets.
        headers = {
            "Authorization": f"Bearer {self._app_key}",
            "X-App-Id": self._app_id,
            "Content-Type": "application/json",
        }

        url = f"{self._base_url}{self._uri}"

        last_error: str | None = None
        for attempt in range(self._max_retries + 1):
            try:
                response = requests.post(
                    url,
                    json=payload,
                    headers=headers,
                    params=params,
                    timeout=self._timeout_seconds,
                )
            except requests.RequestException as exc:
                last_error = f"network_error:{type(exc).__name__}"
                continue

            if response.status_code != 200:
                last_error = f"http_status:{response.status_code}"
                continue

            try:
                obj = response.json()
            except ValueError:
                last_error = "invalid_json_response"
                continue

            content: str | None = None

            # Endpoint A (legacy): {code,msg,data:{content:"..."}} with code==0 on success.
            if isinstance(obj, dict) and obj.get("code") == 0 and isinstance(obj.get("data"), dict):
                content = str(obj["data"].get("content", "") or "")

            # Endpoint B (OpenAI-compatible): {choices:[{message:{content:"..."}}]} on success,
            # or {error:{code,message}} on failure.
            if content is None and isinstance(obj, dict) and isinstance(obj.get("choices"), list):
                try:
                    content = str(obj["choices"][0]["message"]["content"])
                except Exception:
                    content = None

            if content is None:
                # Provider-specific error; keep it generic to avoid leaking sensitive details.
                msg: str | None = None
                if isinstance(obj, dict):
                    if isinstance(obj.get("msg"), str):
                        msg = obj["msg"]
                    elif isinstance(obj.get("error"), dict) and isinstance(obj["error"].get("message"), str):
                        msg = obj["error"]["message"]

                if isinstance(msg, str) and "permission" in msg.lower():
                    last_error = "provider_permission_denied"
                else:
                    last_error = "provider_error"
                continue

            try:
                parsed = _extract_json(str(content))
            except Exception:
                last_error = "model_output_not_json"
                continue

            try:
                return AnalyzeResponse.model_validate(parsed)
            except Exception:
                last_error = "model_output_schema_mismatch"
                continue

        raise AdapterError(last_error or "bluelm_failed")
