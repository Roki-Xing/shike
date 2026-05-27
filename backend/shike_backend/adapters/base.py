"""Adapter interface and shared helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from shike_backend.schemas import AnalyzeRequest, AnalyzeResponse


class ModelAdapter(Protocol):
    """Backend-side adapter interface.

    The FastAPI route depends only on this protocol so providers can be swapped
    without touching `/v1/analyze`.
    """

    def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        """Analyze one request and return a schema-compliant response."""


@dataclass(frozen=True)
class AdapterError(Exception):
    """Raised by adapters when the provider fails (network/auth/parse)."""

    message: str


def manual_review_response(reason: str) -> AnalyzeResponse:
    """Return a safe low-confidence response that forces user confirmation."""

    return AnalyzeResponse(
        scene_type="unknown",
        confidence=0.41,
        title="未确认碎片",
        time=None,
        location=None,
        task={"summary": "需要人工确认", "priority": "low", "topic": "unknown"},
        suggested_actions=[{"type": "reminder", "label": "稍后确认", "requires_permission": True}],
        missing_fields=["scene_type", "time", "location", reason],
        explanation="云侧增强暂不可用，已进入待确认以避免误执行。",
    )

