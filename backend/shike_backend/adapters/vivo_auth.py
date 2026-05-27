"""vivo AI Gateway signing headers.

This implements the "统一鉴权" header signing described in vivo developer docs.

Important: do NOT log AppKEY, signatures, or raw OCR text.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import random
import string
import time
from dataclasses import dataclass
from typing import Mapping
from urllib.parse import quote


SIGNED_HEADERS = "x-ai-gateway-app-id;x-ai-gateway-timestamp;x-ai-gateway-nonce"


def _now_seconds() -> str:
    # vivo AI Gateway docs describe the timestamp as a Unix timestamp in seconds.
    return str(int(time.time()))


def _nonce(length: int = 8) -> str:
    # Use lowercase letters + digits to match common vivo sample code and
    # avoid any potential canonicalization quirks on the gateway side.
    alphabet = string.ascii_lowercase + string.digits
    return "".join(random.choice(alphabet) for _ in range(length))


def canonical_query_string(query: Mapping[str, str] | None) -> str:
    """Return sorted + URL-escaped canonical query string."""

    if not query:
        return ""
    items = [(str(k), str(v)) for k, v in query.items()]
    items.sort(key=lambda kv: kv[0])
    return "&".join(f"{quote(k)}={quote(v)}" for k, v in items)


def signed_headers_string(app_id: str, timestamp: str, nonce: str) -> str:
    return (
        f"x-ai-gateway-app-id:{app_id}\n"
        f"x-ai-gateway-timestamp:{timestamp}\n"
        f"x-ai-gateway-nonce:{nonce}"
    )


def signing_string(method: str, uri: str, canonical_qs: str, app_id: str, timestamp: str, signed_headers: str) -> str:
    return f"{method.upper()}\n{uri}\n{canonical_qs}\n{app_id}\n{timestamp}\n{signed_headers}"


def signature_base64(app_key: str, signing_str: str) -> str:
    """Compute Base64(HMAC-SHA256(app_key, signing_str))."""

    digest = hmac.new(app_key.encode("utf-8"), signing_str.encode("utf-8"), hashlib.sha256).digest()
    return base64.b64encode(digest).decode("utf-8")


@dataclass(frozen=True)
class VivoAuthHeaders:
    app_id: str
    timestamp: str
    nonce: str
    signed_headers: str
    signature: str

    def as_http_headers(self) -> dict[str, str]:
        return {
            "X-AI-GATEWAY-APP-ID": self.app_id,
            "X-AI-GATEWAY-TIMESTAMP": self.timestamp,
            "X-AI-GATEWAY-NONCE": self.nonce,
            "X-AI-GATEWAY-SIGNED-HEADERS": self.signed_headers,
            "X-AI-GATEWAY-SIGNATURE": self.signature,
        }


def gen_sign_headers(
    *,
    app_id: str,
    app_key: str,
    method: str,
    uri: str,
    query: Mapping[str, str] | None = None,
    timestamp: str | None = None,
    nonce: str | None = None,
) -> VivoAuthHeaders:
    """Generate vivo AI Gateway signing headers.

    Args:
        app_id: Gateway AppID.
        app_key: Gateway AppKEY (secret).
        method: HTTP method, e.g. GET/POST.
        uri: Path part of URL, e.g. "/vivogpt/completions".
        query: Query parameters included in the request URL.
        timestamp: Optional override for testing.
        nonce: Optional override for testing.
    """

    ts = timestamp or _now_seconds()
    n = nonce or _nonce()
    cqs = canonical_query_string(query)
    sh = signed_headers_string(app_id, ts, n)
    ss = signing_string(method, uri, cqs, app_id, ts, sh)
    sig = signature_base64(app_key, ss)
    return VivoAuthHeaders(app_id=app_id, timestamp=ts, nonce=n, signed_headers=SIGNED_HEADERS, signature=sig)


def verify_official_sample(*, app_key: str, expected_signature: str, timestamp: str = "1629255133") -> bool:
    """Self-check against an official sample signature (no network needed).

    The official docs have multiple examples; to avoid committing any key-like
    strings or assuming which example is authoritative, the caller supplies:
    - `app_key`: from the chosen official example
    - `expected_signature`: the expected signature string from that example
    - `timestamp`: matching the example (default uses a commonly shown seconds-based sample)
    """

    app_id = "3033188851"
    method = "GET"
    uri = "/ocr/ocr"
    query = {"image": "https://www.vivo.com.cn/test.png"}
    nonce = "1WD8U8OQ"

    headers = gen_sign_headers(
        app_id=app_id,
        app_key=app_key,
        method=method,
        uri=uri,
        query=query,
        timestamp=timestamp,
        nonce=nonce,
    )

    return headers.signature == expected_signature
