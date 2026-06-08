"""DeepSeek text adapter for OCR-to-action-card parsing."""

from __future__ import annotations

from datetime import datetime
import json
import uuid
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

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
        lines = [line for line in candidate.splitlines() if not line.strip().startswith("```")]
        candidate = "\n".join(lines).strip()
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        start = candidate.find("{")
        end = candidate.rfind("}")
        if start >= 0 and end > start:
            return json.loads(candidate[start : end + 1])
        raise


def _current_date_for_timezone(user_timezone: str) -> str:
    """Return the current local date for relative-time normalization."""

    try:
        zone = ZoneInfo(user_timezone)
    except ZoneInfoNotFoundError:
        zone = ZoneInfo("Asia/Shanghai")
    return datetime.now(zone).date().isoformat()


def build_deepseek_payload(
    *,
    model: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float,
    thinking_enabled: bool,
    response_format_enabled: bool,
) -> dict[str, Any]:
    """Build a DeepSeek OpenAI-compatible chat-completions payload.

    Args:
        model: DeepSeek model id.
        system_prompt: System prompt content.
        user_prompt: User prompt content.
        temperature: Sampling temperature.
        thinking_enabled: Whether DeepSeek thinking mode is enabled.
        response_format_enabled: Whether to request JSON Output mode.

    Returns:
        Request JSON body for `/chat/completions`.
    """

    payload: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "temperature": temperature,
        "thinking": {"type": "enabled" if thinking_enabled else "disabled"},
    }
    if response_format_enabled:
        payload["response_format"] = {"type": "json_object"}
    return payload


class DeepSeekModelAdapter:
    """Call DeepSeek text chat completions for OCR text structuring."""

    def __init__(
        self,
        *,
        api_key: str | None,
        base_url: str,
        uri: str,
        model: str,
        timeout_seconds: int,
        max_retries: int,
        temperature: float,
        thinking_enabled: bool,
        response_format_enabled: bool,
    ) -> None:
        self._api_key = (api_key or "").strip()
        self._base_url = base_url.rstrip("/")
        self._uri = uri if uri.startswith("/") else f"/{uri}"
        self._model = model
        self._timeout_seconds = max(1, timeout_seconds)
        self._max_retries = max(0, max_retries)
        self._temperature = temperature
        self._thinking_enabled = thinking_enabled
        self._response_format_enabled = response_format_enabled
        self._system_prompt = _read_prompt(_SYSTEM_PROMPT_PATH)
        self._user_template = _read_prompt(_USER_TEMPLATE_PATH)
        self._schema = load_model_output_schema()

    def is_configured(self) -> bool:
        """Return whether a backend-only DeepSeek API key is configured."""

        if not self._api_key:
            return False
        if self._api_key in {"***", "..."}:
            return False
        return True

    def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        """Analyze OCR text with DeepSeek and validate the Shike schema.

        Args:
            request: OCR text and scene hint.

        Returns:
            Schema-valid Shike model output.

        Raises:
            AdapterError: If credentials, provider response, or schema validation
                fail.
        """

        if not self.is_configured():
            raise AdapterError("deepseek_not_configured")

        user_prompt = self._user_template.format(
            input_id=request.input_id,
            source_type=request.source_type,
            locale=request.locale,
            scene_hint=request.scene_hint or "",
            user_timezone=request.user_timezone,
            current_date=_current_date_for_timezone(request.user_timezone),
            ocr_text=request.ocr_text,
            ocr_text_redacted=redact_ocr_text(request.ocr_text),
            schema_json=json.dumps(self._schema, ensure_ascii=False),
        )
        payload = build_deepseek_payload(
            model=self._model,
            system_prompt=self._system_prompt,
            user_prompt=user_prompt,
            temperature=self._temperature,
            thinking_enabled=self._thinking_enabled,
            response_format_enabled=self._response_format_enabled,
        )
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        url = f"{self._base_url}{self._uri}"
        request_id = str(uuid.uuid4())

        last_error: str | None = None
        for _ in range(self._max_retries + 1):
            try:
                response = requests.post(
                    url,
                    json=payload,
                    headers=headers,
                    params={"request_id": request_id},
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
                content = str(obj["choices"][0]["message"]["content"] or "")
            except Exception:
                last_error = "invalid_deepseek_response_shape"
                continue

            try:
                parsed = _extract_json(content)
            except Exception:
                last_error = "model_output_not_json"
                continue

            try:
                return AnalyzeResponse.model_validate(parsed)
            except Exception:
                last_error = "model_output_schema_mismatch"
                continue

        raise AdapterError(last_error or "deepseek_failed")
