"""Evidence-backed location enrichment for Shike action cards."""

from __future__ import annotations

import re
from typing import Any


_LOCATION_PATTERNS = (
    re.compile(r"([A-Za-z]地点(?:在)?\d{2,4})"),
    re.compile(r"(?:教室是|教室|地点是|地点在|地点|在)\s*([A-Za-z]?\d{2,4})"),
    re.compile(r"(?:教室是|教室|地点是|地点在|地点|在)\s*([A-Za-z一-龥]*[A-Z]\d{2,4}[A-Za-z一-龥]*)"),
    re.compile(r"([A-Z]\d{2,4})"),
    re.compile(r"(?:教室是|教室|地点是|地点在|地点|在)\s*([\u4e00-\u9fa5]{1,10}(?:教室|报告厅|会议室|教学楼)[A-Z]?\d{0,4})"),
)
_LOCATION_MISSING_FIELDS = {"location", "missing_location", "location.raw", "location.map_query"}


def extract_location_from_text(text: str) -> str | None:
    """Extract a concrete location from OCR evidence.

    Args:
        text: OCR or user-provided text.

    Returns:
        Location string such as `303` or `B336`, if supported by evidence.
    """

    for pattern in _LOCATION_PATTERNS:
        match = pattern.search(text)
        if match:
            location = match.group(1).strip(" ，,。；;")
            location = re.sub(r"^([A-Za-z]地点)在(\d{2,4})$", r"\1\2", location)
            if _is_usable_location_text(location):
                return location
    return None


def enrich_location_payload(payload: dict[str, Any], evidence_texts: list[str]) -> dict[str, Any]:
    """Return a response payload with evidence-backed location filled.

    Args:
        payload: Schema-compatible response payload.
        evidence_texts: OCR/user/model text that can support a location.

    Returns:
        Copy of `payload` with location and map action filled when safe.
    """

    enriched = dict(payload)
    source_text = "\n".join([*_payload_texts(enriched), *evidence_texts])
    if _has_cancelled_location_context(source_text):
        return payload
    if not _should_enrich_location(enriched, source_text):
        return payload

    existing = _normalized_location(enriched.get("location"))
    evidence_location = extract_location_from_text("\n".join(evidence_texts))
    location = _prefer_specific_location(existing, evidence_location)
    if not location:
        return payload

    enriched["location"] = _location_payload(location, enriched.get("location"))
    enriched["missing_fields"] = _clean_location_missing_fields(enriched.get("missing_fields"))
    enriched["suggested_actions"] = _ensure_map_action(enriched.get("suggested_actions"), location)
    return enriched


def _should_enrich_location(payload: dict[str, Any], source_text: str) -> bool:
    scene_type = str(payload.get("scene_type") or "")
    task = payload.get("task")
    topic = str(task.get("topic") or "") if isinstance(task, dict) else ""
    title = str(payload.get("title") or "")
    return (
        scene_type in {"course_notice", "exam_notice"}
        or topic == "course"
        or any(token in f"{title}\n{source_text}" for token in ("高数", "上课", "考试", "教室"))
    )


def _has_cancelled_location_context(text: str) -> bool:
    if "不用去" not in text and "取消" not in text:
        return False
    return not any(token in text for token in ("改到", "调整到", "地点改", "上课地点改", "改为"))


def _normalized_location(value: object) -> str | None:
    if not isinstance(value, dict):
        return None
    raw = str(value.get("raw") or value.get("map_query") or "").strip()
    return raw if _is_usable_location_text(raw) else None


def _location_payload(location: str, existing: object) -> dict[str, object]:
    confidence = 0.76
    if isinstance(existing, dict):
        try:
            confidence = max(float(existing.get("confidence") or confidence), confidence)
        except (TypeError, ValueError):
            confidence = 0.76
    return {"raw": location, "map_query": location, "confidence": min(confidence, 0.95)}


def _prefer_specific_location(existing: str | None, evidence: str | None) -> str | None:
    if existing and evidence and _is_more_specific_location(evidence, existing):
        return evidence
    return existing or evidence


def _is_more_specific_location(candidate: str, current: str) -> bool:
    return candidate != current and current in candidate and len(candidate) > len(current)


def _clean_location_missing_fields(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item) not in _LOCATION_MISSING_FIELDS]


def _ensure_map_action(value: object, location: str) -> list[dict[str, object]]:
    actions = [dict(item) for item in value if isinstance(item, dict)] if isinstance(value, list) else []
    if not any(action.get("type") == "map" for action in actions):
        actions.append({"type": "map", "label": f"导航到{location}", "requires_permission": True})
    return actions


def _payload_texts(payload: dict[str, Any]) -> list[str]:
    task = payload.get("task")
    actions = payload.get("suggested_actions")
    texts = [str(payload.get("title") or ""), str(payload.get("explanation") or "")]
    if isinstance(task, dict):
        texts.append(str(task.get("summary") or ""))
    if isinstance(actions, list):
        texts.extend(str(action.get("label") or "") for action in actions if isinstance(action, dict))
    return texts


def _is_usable_location_text(value: str) -> bool:
    if not value or value in {"待确认", "null"}:
        return False
    if len(value) > 24:
        return False
    return True
