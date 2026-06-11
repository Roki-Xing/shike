"""V2 image-analysis schemas for Shike backend."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ImagePayload(BaseModel):
    """Image payload accepted by `/v2/analyze-image`."""

    model_config = ConfigDict(extra="forbid")

    data_url: str | None = None
    mime: Literal["image/jpeg", "image/png", "image/webp"]
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    sha256: str = Field(min_length=8)


class OcrBlock(BaseModel):
    """OCR text block with image coordinates."""

    model_config = ConfigDict(extra="forbid")

    text: str
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: float | None = Field(default=None, ge=0, le=1)


class AnalyzeImageRequest(BaseModel):
    """Request contract for multimodal screenshot/photo analysis."""

    model_config = ConfigDict(extra="forbid")

    input_id: str
    source_type: Literal[
        "screenshot_share",
        "photo_picker",
        "camera",
        "manual",
        "in_app_screen_capture",
        "recent_screenshot_assist",
    ]
    image: ImagePayload | None = None
    ocr_text_hint: str | None = None
    ocr_blocks: list[OcrBlock] = Field(default_factory=list)
    user_timezone: str = "Asia/Shanghai"
    current_date: str
    locale: str = "zh-CN"
    scene_hint: str | None = None
    allow_cloud_image: bool = True


class EvidenceSpan(BaseModel):
    """Field-level evidence returned for user review."""

    model_config = ConfigDict(extra="forbid")

    field: str
    text: str
    source: Literal["vision", "ocr", "user_edit", "rule"]
    box: list[float] | None = None


class ParsedActionCard(BaseModel):
    """Response contract for the user-confirmed Shike action draft."""

    model_config = ConfigDict(extra="forbid")

    title: str
    scene_type: Literal[
        "course_notice",
        "event_poster",
        "meeting_notice",
        "assignment_deadline",
        "exam_notice",
        "travel_ticket",
        "unknown",
    ]
    confidence: float = Field(ge=0, le=1)
    time: dict | None
    location: dict | None
    task: dict
    suggested_actions: list[dict]
    missing_fields: list[str]
    preparation_items: list[str] = Field(default_factory=list)
    checklist_items: list[dict] = Field(default_factory=list)
    risks: list[str]
    evidence: list[EvidenceSpan]
    ignored_regions: list[str]
    explanation: str


def analyze_image_response_schema() -> dict[str, object]:
    """Return JSON Schema for v2 image-analysis responses.

    Args:
        None.

    Returns:
        Pydantic-generated JSON Schema for `ParsedActionCard`.
    """

    return ParsedActionCard.model_json_schema()


def manual_review_action_card(reason: str) -> ParsedActionCard:
    """Build a safe fallback card that requires user confirmation.

    Args:
        reason: Non-secret fallback reason.

    Returns:
        Low-confidence action card with disabled action guidance.
    """

    return ParsedActionCard(
        title="待确认碎片",
        scene_type="unknown",
        confidence=0.32,
        time=None,
        location=None,
        task={"summary": "需要人工确认后再安排", "priority": "low", "topic": "unknown"},
        suggested_actions=[
            {
                "type": "reminder",
                "label": "稍后确认",
                "requires_permission": True,
                "disabled_reason": "用户确认前不可执行",
            }
        ],
        missing_fields=["title", "time", "location", "manual_review"],
        risks=[reason],
        evidence=[],
        ignored_regions=["top_status_bar", "bottom_navigation_bar"],
        explanation="云端图片理解暂不可用，已进入待确认状态，避免误写日历、提醒或地图。",
    )
