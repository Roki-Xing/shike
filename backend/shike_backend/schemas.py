"""Pydantic request/response schemas for the Shike backend."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


CONTRACT_SCHEMA_PATH = Path(__file__).resolve().parents[2] / "contracts/model-output.schema.json"
LOW_CONFIDENCE_THRESHOLD = 0.65


def load_model_output_schema() -> dict[str, object]:
    """Load the canonical model output JSON Schema (SSOT)."""

    return json.loads(CONTRACT_SCHEMA_PATH.read_text(encoding="utf-8"))


class AnalyzeRequest(BaseModel):
    """Analyze endpoint request."""

    model_config = ConfigDict(extra="forbid")

    input_id: str
    source_type: Literal["screenshot", "camera", "share_text", "manual"]
    ocr_text: str
    locale: str = "zh-CN"
    # Keep this flexible: clients may send extra hint values for experiments,
    # but the response contract (`scene_type`) is still enforced separately.
    scene_hint: str | None = None
    user_timezone: str = "Asia/Shanghai"


class Action(BaseModel):
    """Suggested action returned by the model adapter."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["calendar", "reminder", "map"]
    label: str = Field(min_length=1)
    requires_permission: bool


class TimePayload(BaseModel):
    """Normalized time fields returned by the model adapter."""

    model_config = ConfigDict(extra="forbid")

    start_text: str | None
    deadline_text: str | None
    normalized_start: str | None
    normalized_deadline: str | None


class LocationPayload(BaseModel):
    """Normalized location fields returned by the model adapter."""

    model_config = ConfigDict(extra="forbid")

    raw: str | None
    map_query: str | None
    confidence: float = Field(ge=0, le=1)


class TaskPayload(BaseModel):
    """Task summary fields returned by the model adapter."""

    model_config = ConfigDict(extra="forbid")

    summary: str = Field(min_length=1)
    priority: Literal["low", "medium", "high"]
    topic: Literal["course", "event", "unknown"]


class AnalyzeResponse(BaseModel):
    """Structured model response used by Android."""

    model_config = ConfigDict(extra="forbid")

    scene_type: Literal["course_notice", "event_poster", "unknown"]
    confidence: float = Field(ge=0, le=1)
    title: str = Field(min_length=1)
    time: TimePayload | None
    location: LocationPayload | None
    task: TaskPayload
    suggested_actions: list[Action] = Field(min_length=1)
    missing_fields: list[str]
    explanation: str = Field(min_length=1)
