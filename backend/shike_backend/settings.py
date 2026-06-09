"""Backend settings loaded from environment variables.

This module is intentionally dependency-light: it uses only stdlib to avoid
making local smoke checks depend on extra packages.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


DEFAULT_BACKEND_ENV_FILE = Path.home() / ".config/shike/bluelm.env"
DEFAULT_VIVO_MULTIMODAL_MODEL = "vivo-BlueLM-V-2.0"
DEFAULT_VIVO_MULTIMODAL_MODEL_CANDIDATES = (
    "BlueLM-Vision-prd",
    "Volc-DeepSeek-V3.2",
    "Doubao-Seed-2.0-mini",
    "Doubao-Seed-2.0-lite",
    "Doubao-Seed-2.0-pro",
    "qwen3.5-plus",
)
VALID_RUNTIME_MODES = {"demo_mode", "cloud_device_test", "release_user"}


def _unique_nonempty(values: tuple[str | None, ...]) -> tuple[str, ...]:
    """Return non-empty values while preserving the first occurrence.

    Args:
        values: Candidate values from environment variables or defaults.

    Returns:
        Tuple of unique non-empty values in original priority order.
    """

    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        item = (value or "").strip()
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return tuple(result)


def _parse_env_file_line(line: str) -> tuple[str, str] | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    if stripped.startswith("export "):
        stripped = stripped[len("export ") :].strip()
    if "=" not in stripped:
        return None
    key, value = stripped.split("=", 1)
    key = key.strip()
    value = value.strip()
    if not key:
        return None
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return key, value


def _private_env_file_values() -> dict[str, str]:
    explicit_path = os.getenv("SHIKE_BACKEND_ENV_FILE")
    env_path = Path(explicit_path).expanduser() if explicit_path else DEFAULT_BACKEND_ENV_FILE
    if not env_path.is_file():
        return {}
    values: dict[str, str] = {}
    for line in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
        parsed = _parse_env_file_line(line)
        if parsed is None:
            continue
        key, value = parsed
        values[key] = value
    return values


def _env(name: str, default: str | None = None) -> str | None:
    file_values = _private_env_file_values()
    value = os.getenv(name)
    if value is None:
        value = file_values.get(name, default)
    if value is None:
        return None
    value = value.strip()
    return value if value else None


def _env_int(name: str, default: int) -> int:
    raw = _env(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _env_bool(name: str, default: bool) -> bool:
    raw = _env(name)
    if raw is None:
        return default
    return raw.lower() in {"1", "true", "yes", "y", "on"}


def _env_csv(name: str) -> tuple[str, ...]:
    raw = _env(name)
    if raw is None:
        return ()
    values = tuple(item.strip() for item in raw.split(",") if item.strip())
    return values


def _split_vivo_chat_base_url(value: str) -> tuple[str, str]:
    """Split Android16 guide-style chat base URL into base URL and URI.

    Args:
        value: URL such as `https://api-ai.vivo.com.cn/v1`.

    Returns:
        Backend base URL and chat-completions URI.
    """

    normalized = value.rstrip("/")
    if normalized.endswith("/v1"):
        return normalized[: -len("/v1")], "/v1/chat/completions"
    if normalized.endswith("/v1/chat/completions"):
        return normalized[: -len("/v1/chat/completions")], "/v1/chat/completions"
    return normalized, "/v1/chat/completions"


@dataclass(frozen=True)
class Settings:
    """Runtime settings for the Shike backend."""

    runtime_mode: str
    model_provider: str
    allow_mock_fallback: bool

    bluelm_app_id: str | None
    bluelm_app_key: str | None
    bluelm_base_url: str
    bluelm_uri: str
    bluelm_model: str
    bluelm_timeout_seconds: int
    bluelm_max_retries: int
    bluelm_temperature: float
    bluelm_thinking_mode: str
    bluelm_request_id_param: str
    bluelm_response_format_enabled: bool
    vivo_ocr_app_id: str | None
    vivo_ocr_app_key: str | None
    vivo_ocr_base_url: str
    vivo_ocr_uri: str
    vivo_ocr_timeout_seconds: int
    vivo_ocr_max_retries: int
    allow_ocr_fallback: bool
    vivo_multimodal_app_id: str | None
    vivo_multimodal_app_key: str | None
    vivo_multimodal_base_url: str
    vivo_multimodal_uri: str
    vivo_multimodal_model: str
    vivo_multimodal_models: tuple[str, ...]
    vivo_multimodal_timeout_seconds: int
    vivo_multimodal_max_retries: int
    vivo_multimodal_temperature: float
    deepseek_api_key: str | None
    deepseek_base_url: str
    deepseek_uri: str
    deepseek_model: str
    deepseek_timeout_seconds: int
    deepseek_max_retries: int
    deepseek_temperature: float
    deepseek_thinking_enabled: bool
    deepseek_response_format_enabled: bool
    recorded_dir: str

    @property
    def allows_demo_samples(self) -> bool:
        """Return whether fixed demo sample fields may be used.

        Args:
            None.

        Returns:
            True only for explicit offline demo mode.
        """

        return self.runtime_mode == "demo_mode"

    @staticmethod
    def from_env() -> "Settings":
        runtime_mode = (_env("SHIKE_RUNTIME_MODE", "release_user") or "release_user").lower()
        if runtime_mode not in VALID_RUNTIME_MODES:
            runtime_mode = "release_user"
        provider = (_env("SHIKE_MODEL_PROVIDER", "mock") or "mock").lower()
        allow_mock_fallback = _env_bool("SHIKE_ALLOW_MOCK_FALLBACK", True)
        allow_ocr_fallback = _env_bool("SHIKE_ALLOW_OCR_FALLBACK", True)

        vivo_app_id = _env("VIVO_APP_ID")
        vivo_app_key = _env("VIVO_APP_KEY")
        bluelm_app_id = _env("BLUELM_APP_ID") or vivo_app_id
        bluelm_app_key = _env("BLUELM_APP_KEY") or vivo_app_key

        # Defaults follow common community examples; they can be overridden at runtime.
        # NOTE: The exact API surface is subject to official vivo documentation and may change.
        guide_chat_base_url = _env("VIVO_CHAT_BASE_URL")
        default_bluelm_base_url, default_bluelm_uri = (
            _split_vivo_chat_base_url(guide_chat_base_url)
            if guide_chat_base_url
            else ("https://api-ai.vivo.com.cn", "/v1/chat/completions")
        )
        bluelm_base_url = _env("BLUELM_BASE_URL", default_bluelm_base_url) or default_bluelm_base_url
        # The contest doc center currently recommends OpenAI-compatible `/v1/chat/completions`.
        # Keep env override to allow older `/vivogpt/completions` if the key has that permission.
        bluelm_uri = _env("BLUELM_URI", default_bluelm_uri) or default_bluelm_uri
        # Default to a model name shown in doc center and observed to be accessible for contest keys.
        bluelm_model = _env("BLUELM_MODEL") or _env("VIVO_CHAT_MODEL") or "Volc-DeepSeek-V3.2"

        bluelm_timeout_seconds = _env_int("BLUELM_TIMEOUT_SECONDS", 12)
        bluelm_max_retries = _env_int("BLUELM_MAX_RETRIES", 1)

        temperature_raw = _env("BLUELM_TEMPERATURE", "0.2") or "0.2"
        try:
            temperature = float(temperature_raw)
        except ValueError:
            temperature = 0.2

        bluelm_thinking_mode = _env("BLUELM_THINKING_MODE", "provider_default") or "provider_default"
        bluelm_request_id_param = _env("BLUELM_REQUEST_ID_PARAM", "requestId") or "requestId"
        bluelm_response_format_enabled = _env_bool("BLUELM_RESPONSE_FORMAT", True)

        # vivo General OCR uses the same contest AppID/AppKEY shape, but keeps
        # independent env names so deployments can rotate or scope abilities.
        vivo_ocr_app_id = _env("VIVO_OCR_APP_ID") or _env("VIVO_AIGC_APP_ID") or vivo_app_id or bluelm_app_id
        vivo_ocr_app_key = _env("VIVO_OCR_APP_KEY") or _env("VIVO_AIGC_APP_KEY") or vivo_app_key or bluelm_app_key
        vivo_ocr_base_url = _env("VIVO_OCR_BASE_URL", "https://api-ai.vivo.com.cn") or "https://api-ai.vivo.com.cn"
        vivo_ocr_uri = _env("VIVO_OCR_URI", "/ocr/general_recognition") or "/ocr/general_recognition"
        vivo_ocr_timeout_seconds = _env_int("VIVO_OCR_TIMEOUT_SECONDS", 8)
        vivo_ocr_max_retries = _env_int("VIVO_OCR_MAX_RETRIES", 1)

        vivo_multimodal_app_id = _env("VIVO_MULTIMODAL_APP_ID") or _env("VIVO_AIGC_APP_ID") or vivo_app_id or bluelm_app_id
        vivo_multimodal_app_key = _env("VIVO_MULTIMODAL_APP_KEY") or _env("VIVO_AIGC_APP_KEY") or vivo_app_key or bluelm_app_key
        vivo_multimodal_base_url = (
            _env("VIVO_MULTIMODAL_BASE_URL", "https://api-ai.vivo.com.cn") or "https://api-ai.vivo.com.cn"
        )
        vivo_multimodal_uri = _env("VIVO_MULTIMODAL_URI", "/v1/chat/completions") or "/v1/chat/completions"
        vivo_multimodal_model = _env("VIVO_MULTIMODAL_MODEL", DEFAULT_VIVO_MULTIMODAL_MODEL) or DEFAULT_VIVO_MULTIMODAL_MODEL
        vivo_multimodal_models = _env_csv("VIVO_MULTIMODAL_MODELS") or _unique_nonempty(
            (vivo_multimodal_model, *DEFAULT_VIVO_MULTIMODAL_MODEL_CANDIDATES)
        )
        vivo_multimodal_timeout_seconds = _env_int("VIVO_MULTIMODAL_TIMEOUT_SECONDS", 60)
        vivo_multimodal_max_retries = _env_int("VIVO_MULTIMODAL_MAX_RETRIES", 1)
        vivo_multimodal_temperature_raw = _env("VIVO_MULTIMODAL_TEMPERATURE", "0.1") or "0.1"
        try:
            vivo_multimodal_temperature = float(vivo_multimodal_temperature_raw)
        except ValueError:
            vivo_multimodal_temperature = 0.1

        deepseek_api_key = _env("DEEPSEEK_API_KEY")
        deepseek_base_url = _env("DEEPSEEK_BASE_URL", "https://api.deepseek.com") or "https://api.deepseek.com"
        deepseek_uri = _env("DEEPSEEK_URI", "/chat/completions") or "/chat/completions"
        deepseek_model = _env("DEEPSEEK_MODEL", "deepseek-v4-flash") or "deepseek-v4-flash"
        deepseek_timeout_seconds = _env_int("DEEPSEEK_TIMEOUT_SECONDS", 20)
        deepseek_max_retries = _env_int("DEEPSEEK_MAX_RETRIES", 1)
        deepseek_temperature_raw = _env("DEEPSEEK_TEMPERATURE", "0.1") or "0.1"
        try:
            deepseek_temperature = float(deepseek_temperature_raw)
        except ValueError:
            deepseek_temperature = 0.1
        deepseek_thinking_enabled = _env_bool("DEEPSEEK_THINKING_ENABLED", False)
        deepseek_response_format_enabled = _env_bool("DEEPSEEK_RESPONSE_FORMAT", True)

        default_recorded_dir = str((Path(__file__).resolve().parent / "eval/recordings").resolve())
        recorded_dir = _env("SHIKE_RECORDED_DIR", default_recorded_dir) or default_recorded_dir

        return Settings(
            runtime_mode=runtime_mode,
            model_provider=provider,
            allow_mock_fallback=allow_mock_fallback,
            bluelm_app_id=bluelm_app_id,
            bluelm_app_key=bluelm_app_key,
            bluelm_base_url=bluelm_base_url,
            bluelm_uri=bluelm_uri,
            bluelm_model=bluelm_model,
            bluelm_timeout_seconds=bluelm_timeout_seconds,
            bluelm_max_retries=bluelm_max_retries,
            bluelm_temperature=temperature,
            bluelm_thinking_mode=bluelm_thinking_mode,
            bluelm_request_id_param=bluelm_request_id_param,
            bluelm_response_format_enabled=bluelm_response_format_enabled,
            vivo_ocr_app_id=vivo_ocr_app_id,
            vivo_ocr_app_key=vivo_ocr_app_key,
            vivo_ocr_base_url=vivo_ocr_base_url,
            vivo_ocr_uri=vivo_ocr_uri,
            vivo_ocr_timeout_seconds=vivo_ocr_timeout_seconds,
            vivo_ocr_max_retries=vivo_ocr_max_retries,
            allow_ocr_fallback=allow_ocr_fallback,
            vivo_multimodal_app_id=vivo_multimodal_app_id,
            vivo_multimodal_app_key=vivo_multimodal_app_key,
            vivo_multimodal_base_url=vivo_multimodal_base_url,
            vivo_multimodal_uri=vivo_multimodal_uri,
            vivo_multimodal_model=vivo_multimodal_model,
            vivo_multimodal_models=vivo_multimodal_models,
            vivo_multimodal_timeout_seconds=vivo_multimodal_timeout_seconds,
            vivo_multimodal_max_retries=vivo_multimodal_max_retries,
            vivo_multimodal_temperature=vivo_multimodal_temperature,
            deepseek_api_key=deepseek_api_key,
            deepseek_base_url=deepseek_base_url,
            deepseek_uri=deepseek_uri,
            deepseek_model=deepseek_model,
            deepseek_timeout_seconds=deepseek_timeout_seconds,
            deepseek_max_retries=deepseek_max_retries,
            deepseek_temperature=deepseek_temperature,
            deepseek_thinking_enabled=deepseek_thinking_enabled,
            deepseek_response_format_enabled=deepseek_response_format_enabled,
            recorded_dir=recorded_dir,
        )


_CACHED: Settings | None = None


def get_settings() -> Settings:
    """Return cached settings.

    This keeps request paths stable in tests and avoids re-reading env on every call.
    """

    global _CACHED
    if _CACHED is None:
        _CACHED = Settings.from_env()
    return _CACHED
