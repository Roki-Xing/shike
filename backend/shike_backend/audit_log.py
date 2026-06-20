"""Secret-safe audit metadata for backend image analysis."""

from __future__ import annotations

import re
import hashlib
from typing import Any

from shike_backend.schemas_v2 import AnalyzeImageRequest, ParsedActionCard


_PHONE_RE = re.compile(r"1[3-9]\d{9}")
_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_NUMERIC_ID_RE = re.compile(r"\b\d{8,12}\b")
_COURSE_RE = re.compile(r"(高数|数学|课程|上课|教室|补课|调课|实验|签到)")
_TIME_RE = re.compile(r"(今天|今晚|明天|明晚|本周|下周|周[一二三四五六日天]|[0-2]?\d[:：][0-5]\d|[一二三四五六七八九十两\d]+点)")
_LOCATION_RE = re.compile(r"([A-Z][0-9]{2,4}|教室|教学楼|实验楼|报告厅|会议室|校区|中心|腾讯会议|线上)")


def _stable_hash_prefix(value: str, length: int = 16) -> str:
    """Return a stable non-reversible identifier for audit correlation.

    Args:
        value: Potentially user-controlled identifier.
        length: Number of hexadecimal characters to keep.

    Returns:
        SHA-256 prefix for metadata-only logs.
    """

    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:length]


def redact_log_text(text: str, max_len: int = 300) -> str:
    """Return a short, redacted diagnostic text sample.

    Args:
        text: Potentially sensitive OCR, user, or provider text.
        max_len: Maximum returned length.

    Returns:
        Text with common PII patterns removed and newlines collapsed.
    """

    redacted = _PHONE_RE.sub("手机号***", text)
    redacted = _NUMERIC_ID_RE.sub("学号/编号***", redacted)
    redacted = _EMAIL_RE.sub("邮箱***", redacted)
    redacted = " ".join(redacted.split())
    if len(redacted) > max_len:
        redacted = redacted[: max_len - 3] + "..."
    return redacted


def _ocr_signal_summary(text: str) -> dict[str, bool]:
    """Return coarse OCR semantic signals without copying OCR text.

    Args:
        text: OCR hint that may contain user content.

    Returns:
        Boolean signal flags for operational debugging.
    """

    return {
        "ocr_has_course_signal": bool(_COURSE_RE.search(text)),
        "ocr_has_time_signal": bool(_TIME_RE.search(text)),
        "ocr_has_location_signal": bool(_LOCATION_RE.search(text)),
    }


def _result_summary(card: ParsedActionCard | None) -> dict[str, Any]:
    """Return non-content result fields for operational diagnosis.

    Args:
        card: Final parsed action card, after evidence repair.

    Returns:
        Metadata-only result summary without title, OCR text, or raw location.
    """

    if card is None:
        return {}
    time_payload = card.time if isinstance(card.time, dict) else {}
    location_payload = card.location if isinstance(card.location, dict) else {}
    normalized_start = str(time_payload.get("normalized_start") or "")
    raw_location = str(location_payload.get("raw") or location_payload.get("map_query") or "")
    return {
        "result_scene_type": card.scene_type,
        "result_has_start_time": bool(time_payload.get("start_text") or normalized_start),
        "result_normalized_start_hour": _normalized_start_hour(normalized_start),
        "result_has_location": bool(raw_location),
        "result_location_kind": _location_kind(raw_location),
        "result_missing_time": "time" in card.missing_fields or "exact_start_time" in card.missing_fields,
        "result_missing_location": "location" in card.missing_fields,
    }


def _normalized_start_hour(value: str) -> int | None:
    """Extract hour from an ISO datetime string without logging full value."""

    match = re.search(r"T([0-2]\d):[0-5]\d", value)
    return int(match.group(1)) if match else None


def _location_kind(value: str) -> str:
    """Classify a location without copying the raw location into logs."""

    if not value:
        return "missing"
    if re.fullmatch(r"[A-Za-z]?\d{2,4}", value):
        return "room_code"
    if re.fullmatch(r"[A-Za-z]地点\d{2,4}", value):
        return "labeled_room_code"
    if any(token in value for token in ("线上", "腾讯会议", "QQ群", "邮箱")):
        return "online"
    return "named_place"


def build_analyze_image_audit_event(
    request: AnalyzeImageRequest,
    *,
    provider: str,
    key_present: bool,
    duration_ms: int,
    status: str,
    repair_risks: list[str] | None = None,
    result_card: ParsedActionCard | None = None,
) -> dict[str, Any]:
    """Build redacted `/v2/analyze-image` request evidence.

    Args:
        request: Parsed v2 request. Raw image and OCR content are not copied.
        provider: Backend provider label.
        key_present: Whether provider credentials were configured.
        duration_ms: Handler/provider duration in milliseconds.
        status: Non-secret request outcome.
        repair_risks: Non-secret OCR evidence repair reason codes.
        result_card: Final action card used only for metadata summary.

    Returns:
        Metadata-only event suitable for backend access logs.
    """

    image = request.image
    repair_reason_codes = [
        item.split(":", 1)[1]
        for item in (repair_risks or [])
        if item.startswith("ocr_evidence_repair:") and len(item.split(":", 1)) == 2
    ]
    return {
        "input_id_hash": _stable_hash_prefix(request.input_id),
        "provider": provider,
        "image_present": image is not None,
        "image_sha256_prefix": image.sha256[:8] if image is not None else "",
        "ocr_block_count": len(request.ocr_blocks),
        "source_type": request.source_type,
        "key_present": bool(key_present),
        "duration_ms": max(duration_ms, 0),
        "status": status,
        "ocr_hint_length": len(request.ocr_text_hint or ""),
        **_ocr_signal_summary(request.ocr_text_hint or ""),
        "ocr_repair_applied": bool(repair_reason_codes),
        "ocr_repair_reasons": repair_reason_codes,
        **_result_summary(result_card),
    }
