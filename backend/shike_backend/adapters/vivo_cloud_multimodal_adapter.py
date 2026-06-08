"""vivo cloud multimodal adapter for `/v2/analyze-image`."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

import requests

from shike_backend.adapters.base import AdapterError
from shike_backend.adapters.vivo_auth import gen_sign_headers
from shike_backend.schemas_v2 import AnalyzeImageRequest, ParsedActionCard


_PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"
_SYSTEM_PROMPT_PATH = _PROMPTS_DIR / "analyze_image_system_prompt.txt"
_USER_TEMPLATE_PATH = _PROMPTS_DIR / "analyze_image_user_template.txt"
_LEGACY_VISION_CHAT_URI = "/vivogpt/completions"
_LEGACY_FALLBACK_ERRORS = {
    "provider_model_does_not_support_image",
    "provider_error:401",
    "provider_error:403",
    "http_status:400",
    "http_status:404",
    "http_status:422",
}


def _read_prompt(path: Path) -> str:
    if not path.is_file():
        raise AdapterError(f"missing_prompt_file:{path.name}")
    return path.read_text(encoding="utf-8")


def _extract_json_object(text: str) -> Any:
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


class VivoCloudMultimodalAdapter:
    """Call vivo OpenAI-compatible chat completions with image content."""

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

    def is_configured(self) -> bool:
        """Return whether usable backend-only credentials are configured."""

        if not self._app_id or not self._app_key:
            return False
        if self._app_id in {"***", "..."} or self._app_key in {"***", "..."}:
            return False
        return True

    def analyze_image(self, request: AnalyzeImageRequest, schema_json: dict[str, object]) -> ParsedActionCard:
        """Analyze one image request with vivo multimodal chat completions.

        Args:
            request: Image request and OCR hints.
            schema_json: Response schema supplied to the model.

        Returns:
            Parsed action card validated by Pydantic.
        """

        if not self.is_configured():
            raise AdapterError("vivo_multimodal_not_configured")
        if not request.allow_cloud_image:
            raise AdapterError("cloud_image_not_allowed")
        if request.image is None or not request.image.data_url:
            raise AdapterError("image_required_for_multimodal")
        if not _is_supported_image_url(request.image.data_url):
            raise AdapterError("image_url_required")

        request_id = str(uuid.uuid4())
        user_prompt = self._user_template.format(
            current_date=request.current_date,
            user_timezone=request.user_timezone,
            locale=request.locale,
            source_type=request.source_type,
            scene_hint=request.scene_hint or "",
            ocr_text_hint=request.ocr_text_hint or "",
            ocr_blocks_json=json.dumps([block.model_dump() for block in request.ocr_blocks], ensure_ascii=False),
            schema_json=json.dumps(schema_json, ensure_ascii=False),
        )
        payload: dict[str, Any] = {
            "model": self._model,
            "stream": False,
            "temperature": self._temperature,
            "max_tokens": 2048,
            "messages": [
                {"role": "system", "content": self._system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {"type": "image_url", "image_url": {"url": request.image.data_url}},
                    ],
                },
            ],
        }
        headers = {
            "Authorization": f"Bearer {self._app_key}",
            "X-App-Id": self._app_id,
            "Content-Type": "application/json",
        }
        url = f"{self._base_url}{self._uri}"

        last_error: str | None = None
        for _ in range(self._max_retries + 1):
            try:
                response = requests.post(
                    url,
                    headers=headers,
                    params={"request_id": request_id},
                    json=payload,
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
                content = _content_from_provider_response(obj)
                parsed = _extract_json_object(content)
                return ParsedActionCard.model_validate(parsed)
            except AdapterError as exc:
                last_error = exc.message
                continue
            except Exception:
                last_error = "invalid_vivo_response_shape"
                continue

        if last_error in _LEGACY_FALLBACK_ERRORS:
            return self._analyze_image_with_legacy_vision_chat(
                request=request,
                schema_json=schema_json,
                user_prompt=user_prompt,
            )

        raise AdapterError(last_error or "vivo_multimodal_failed")

    def _analyze_image_with_legacy_vision_chat(
        self,
        *,
        request: AnalyzeImageRequest,
        schema_json: dict[str, object],
        user_prompt: str,
    ) -> ParsedActionCard:
        """Analyze an image through vivo's signed VisionChat gateway shape.

        Args:
            request: Image request and OCR hints.
            schema_json: Response schema supplied to the model.
            user_prompt: Already rendered image-analysis prompt.

        Returns:
            Parsed action card validated by Pydantic.
        """

        if request.image is None or not request.image.data_url:
            raise AdapterError("image_required_for_multimodal")

        request_id = str(uuid.uuid4())
        query = {"requestId": request_id}
        auth_headers = gen_sign_headers(
            app_id=self._app_id,
            app_key=self._app_key,
            method="POST",
            uri=_LEGACY_VISION_CHAT_URI,
            query=query,
        ).as_http_headers()
        headers = {
            **auth_headers,
            "Content-Type": "application/json",
        }
        payload: dict[str, Any] = {
            "model": self._model,
            "sessionId": request.input_id,
            "systemPrompt": self._system_prompt,
            "messages": [
                {
                    "role": "user",
                    "contentType": "text",
                    "content": user_prompt,
                },
                {
                    "role": "user",
                    "contentType": "image",
                    "content": request.image.data_url,
                },
            ],
        }
        response = requests.post(
            f"{self._base_url}{_LEGACY_VISION_CHAT_URI}",
            headers=headers,
            params=query,
            json=payload,
            timeout=self._timeout_seconds,
        )
        if response.status_code != 200:
            raise AdapterError(f"legacy_http_status:{response.status_code}")
        try:
            obj = response.json()
            content = _content_from_provider_response(obj)
            parsed = _extract_json_object(content)
            return ParsedActionCard.model_validate(parsed)
        except AdapterError:
            raise
        except Exception as exc:
            raise AdapterError("invalid_legacy_vivo_response_shape") from exc


def _is_supported_image_url(value: str) -> bool:
    """Return whether an image URL is supported by vivo chat-completions docs."""

    return value.startswith("data:image") or value.startswith("https://") or value.startswith("http://")


def _content_from_provider_response(obj: Any) -> str:
    """Extract model content or raise a classified provider error.

    Args:
        obj: Provider JSON response.

    Returns:
        Text content from a chat-completions style response.
    """

    if not isinstance(obj, dict):
        raise AdapterError("invalid_vivo_response_shape")

    error = obj.get("error")
    if isinstance(error, dict):
        message = str(error.get("message", "")).lower()
        code = str(error.get("code", "")).strip()
        if "do not support image" in message or "not support image" in message:
            raise AdapterError("provider_model_does_not_support_image")
        if code == "1010":
            raise AdapterError("provider_model_does_not_support_image")
        raise AdapterError(f"provider_error:{code or 'unknown'}")

    if isinstance(obj.get("choices"), list):
        try:
            return str(obj["choices"][0]["message"]["content"])
        except Exception as exc:
            raise AdapterError("invalid_vivo_response_shape") from exc

    if obj.get("code") == 0 and isinstance(obj.get("data"), dict):
        content = obj["data"].get("content")
        if content:
            return str(content)

    raise AdapterError("invalid_vivo_response_shape")
