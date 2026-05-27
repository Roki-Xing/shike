"""Privacy utilities (redaction/masking for logs).

Redaction is best-effort and intentionally conservative: we avoid emitting raw
OCR content or backend secrets in logs.
"""

from __future__ import annotations

import re


_PHONE_RE = re.compile(r"\b1\d{10}\b")
_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_ID_RE = re.compile(r"\b\d{15,18}\b")


def mask_secret(value: str | None) -> str:
    if not value:
        return "***"
    if len(value) <= 8:
        return "***"
    return f"{value[:4]}***{value[-4:]}"


def redact_ocr_text(text: str, max_len: int = 160) -> str:
    """Redact common PII patterns and truncate for logging."""

    cleaned = text
    cleaned = _PHONE_RE.sub("[PHONE]", cleaned)
    cleaned = _EMAIL_RE.sub("[EMAIL]", cleaned)
    cleaned = _ID_RE.sub("[ID]", cleaned)
    cleaned = cleaned.replace("\n", " ").strip()
    if len(cleaned) > max_len:
        cleaned = cleaned[: max_len - 3] + "..."
    return cleaned

