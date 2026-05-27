"""Backend settings loaded from environment variables.

This module is intentionally dependency-light: it uses only stdlib to avoid
making local smoke checks depend on extra packages.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name, default)
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


@dataclass(frozen=True)
class Settings:
    """Runtime settings for the Shike backend."""

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
    recorded_dir: str

    @staticmethod
    def from_env() -> "Settings":
        provider = (_env("SHIKE_MODEL_PROVIDER", "mock") or "mock").lower()
        allow_mock_fallback = _env_bool("SHIKE_ALLOW_MOCK_FALLBACK", True)

        bluelm_app_id = _env("BLUELM_APP_ID")
        bluelm_app_key = _env("BLUELM_APP_KEY")

        # Defaults follow common community examples; they can be overridden at runtime.
        # NOTE: The exact API surface is subject to official vivo documentation and may change.
        bluelm_base_url = _env("BLUELM_BASE_URL", "https://api-ai.vivo.com.cn") or "https://api-ai.vivo.com.cn"
        # The contest doc center currently recommends OpenAI-compatible `/v1/chat/completions`.
        # Keep env override to allow older `/vivogpt/completions` if the key has that permission.
        bluelm_uri = _env("BLUELM_URI", "/v1/chat/completions") or "/v1/chat/completions"
        # Default to a model name shown in doc center and observed to be accessible for contest keys.
        bluelm_model = _env("BLUELM_MODEL", "Volc-DeepSeek-V3.2") or "Volc-DeepSeek-V3.2"

        bluelm_timeout_seconds = _env_int("BLUELM_TIMEOUT_SECONDS", 12)
        bluelm_max_retries = _env_int("BLUELM_MAX_RETRIES", 1)

        temperature_raw = _env("BLUELM_TEMPERATURE", "0.2") or "0.2"
        try:
            temperature = float(temperature_raw)
        except ValueError:
            temperature = 0.2

        default_recorded_dir = str((Path(__file__).resolve().parent / "eval/recordings").resolve())
        recorded_dir = _env("SHIKE_RECORDED_DIR", default_recorded_dir) or default_recorded_dir

        return Settings(
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
