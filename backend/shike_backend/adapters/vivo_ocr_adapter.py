"""Server-side vivo OCR adapter for capture/import flows."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any

import requests

from shike_backend.adapters.base import AdapterError
from shike_backend.privacy import redact_ocr_text
from shike_backend.schemas import OcrRequest, OcrResponse
from shike_backend.schemas_v2 import OcrBlock


OFFICIAL_GENERAL_OCR_URI = "/ocr/general_recognition"


@dataclass(frozen=True)
class OcrDetail:
    """Internal OCR result with text and coordinate blocks."""

    response: OcrResponse
    blocks: list[OcrBlock]


def _collect_words(result: Any) -> list[str]:
    """Extract OCR words from vivo's pos=0/1/2 response variants.

    Args:
        result: The `result` object returned by vivo OCR.

    Returns:
        Ordered text fragments with empty fragments removed.
    """

    if not isinstance(result, dict):
        return []

    words: list[str] = []
    simple_words = result.get("words")
    if isinstance(simple_words, list):
        for item in simple_words:
            if isinstance(item, dict):
                value = str(item.get("words", "")).strip()
                if value:
                    words.append(value)

    positioned_words = result.get("OCR")
    if isinstance(positioned_words, list):
        for item in positioned_words:
            if isinstance(item, dict):
                value = str(item.get("words", "")).strip()
                if value:
                    words.append(value)

    return words


def _number(value: Any) -> float | None:
    """Parse a numeric coordinate from provider payloads."""

    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def _box_from_provider_item(item: dict[str, Any]) -> list[float] | None:
    """Extract a bounding box from common vivo OCR coordinate variants."""

    direct_keys = ("x1", "y1", "x2", "y2")
    direct = [_number(item.get(key)) for key in direct_keys]
    if all(value is not None for value in direct):
        return [float(value) for value in direct if value is not None]

    left = _number(item.get("left", item.get("x")))
    top = _number(item.get("top", item.get("y")))
    width = _number(item.get("width", item.get("w")))
    height = _number(item.get("height", item.get("h")))
    if None not in (left, top, width, height):
        return [left, top, left + width, top + height]  # type: ignore[operator]

    points = item.get("location") or item.get("points") or item.get("pos")
    if isinstance(points, list):
        xs: list[float] = []
        ys: list[float] = []
        for point in points:
            if isinstance(point, dict):
                x = _number(point.get("x"))
                y = _number(point.get("y"))
            elif isinstance(point, (list, tuple)) and len(point) >= 2:
                x = _number(point[0])
                y = _number(point[1])
            else:
                x = y = None
            if x is not None and y is not None:
                xs.append(x)
                ys.append(y)
        if xs and ys:
            return [min(xs), min(ys), max(xs), max(ys)]

    return None


def _collect_blocks(result: Any) -> list[OcrBlock]:
    """Extract OCR blocks with coordinates from vivo pos=2 payloads."""

    if not isinstance(result, dict):
        return []

    candidates: list[Any] = []
    for key in ("OCR", "words"):
        value = result.get(key)
        if isinstance(value, list):
            candidates.extend(value)

    blocks: list[OcrBlock] = []
    for item in candidates:
        if not isinstance(item, dict):
            continue
        text = str(item.get("words", item.get("text", ""))).strip()
        if not text:
            continue
        box = _box_from_provider_item(item)
        if box is None:
            continue
        confidence = _number(item.get("confidence", item.get("score", item.get("probability"))))
        blocks.append(
            OcrBlock(
                text=redact_ocr_text(text),
                x1=box[0],
                y1=box[1],
                x2=box[2],
                y2=box[3],
                confidence=confidence if confidence is not None and 0 <= confidence <= 1 else None,
            )
        )

    return blocks


class VivoOcrAdapter:
    """Call vivo AIGC General OCR from the backend only."""

    def __init__(
        self,
        *,
        app_id: str | None,
        app_key: str | None,
        base_url: str,
        uri: str,
        timeout_seconds: int,
        max_retries: int,
    ) -> None:
        self._app_id = (app_id or "").strip()
        self._app_key = (app_key or "").strip()
        self._base_url = base_url.rstrip("/")
        self._uri = uri if uri.startswith("/") else f"/{uri}"
        self._timeout_seconds = max(1, timeout_seconds)
        self._max_retries = max(0, max_retries)

    def is_configured(self) -> bool:
        """Return whether real vivo OCR credentials are configured."""

        if not self._app_id or not self._app_key:
            return False
        if self._app_id in {"***", "..."} or self._app_key in {"***", "..."}:
            return False
        return True

    def recognize_detail(self, request: OcrRequest) -> OcrDetail:
        """Recognize base64 image text and coordinate blocks using vivo General OCR.

        Args:
            request: Base64 image payload and capture source metadata.

        Returns:
            Redacted OCR text response plus coordinate blocks for v2 prompts.
        """

        if not self.is_configured():
            raise AdapterError("vivo_ocr_not_configured")

        request_id = str(uuid.uuid4())
        form_data = {
            "image": request.image_base64,
            "pos": str(request.pos),
            "businessid": f"aigc{self._app_id}",
            "sessid": str(uuid.uuid4()),
        }
        headers = {
            "Authorization": f"Bearer {self._app_key}",
            "Content-type": "application/x-www-form-urlencoded",
        }
        params = {"requestId": request_id}
        url = f"{self._base_url}{self._uri}"

        last_error: str | None = None
        for _ in range(self._max_retries + 1):
            try:
                response = requests.post(
                    url,
                    data=form_data,
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
                payload = response.json()
            except ValueError:
                last_error = "invalid_json_response"
                continue

            if not isinstance(payload, dict):
                last_error = "invalid_ocr_payload"
                continue

            error_code = payload.get("error_code", payload.get("code", 0))
            if error_code not in (0, "0"):
                last_error = "ocr_provider_error"
                continue

            words = _collect_words(payload.get("result"))
            text = "\n".join(words).strip()
            if not text:
                last_error = "ocr_empty_result"
                continue

            redacted = redact_ocr_text(text)
            return OcrDetail(
                response=OcrResponse(
                    text=redacted,
                    confidence=0.86,
                    engine="vivo_general_ocr",
                    is_redacted=redacted != text,
                    image_cleared=True,
                    failure_hint=None,
                    request_id=request_id,
                ),
                blocks=_collect_blocks(payload.get("result")),
            )

        raise AdapterError(last_error or "vivo_ocr_failed")

    def recognize(self, request: OcrRequest) -> OcrResponse:
        """Recognize base64 image text using vivo General OCR.

        Args:
            request: Base64 image payload and capture source metadata.

        Returns:
            Redacted OCR text response for Shike capture/import flow.
        """

        return self.recognize_detail(request).response


def fallback_ocr_response(request: OcrRequest, *, reason: str = "ocr_unavailable") -> OcrResponse:
    """Return a safe manual-continuation OCR response.

    Args:
        request: Original OCR request.
        reason: Short non-secret failure reason.

    Returns:
        Response that keeps the action card flow alive without raw image retention.
    """

    return OcrResponse(
        text="",
        confidence=0.0,
        engine="manual_fallback",
        is_redacted=False,
        image_cleared=True,
        failure_hint=f"未识别到稳定文字，可手动粘贴通知内容继续（{reason}）",
        request_id=request.input_id,
    )
