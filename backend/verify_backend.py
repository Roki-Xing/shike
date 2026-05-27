#!/usr/bin/env python3
"""Verify the Shike FastAPI backend without starting a server."""

from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient

from shike_backend.main import app


def assert_model_output_schema(schema: dict[str, Any], payload: dict[str, Any]) -> None:
    """Validate a backend response against the local JSON Schema subset.

    Args:
        schema: Model output JSON Schema returned by `/v1/schema`.
        payload: `/v1/analyze` response payload.

    Returns:
        None.
    """

    assert set(schema["required"]).issubset(payload)
    assert payload["scene_type"] in schema["properties"]["scene_type"]["enum"]
    assert 0 <= payload["confidence"] <= 1
    assert isinstance(payload["title"], str) and payload["title"]
    assert isinstance(payload["task"], dict)
    assert set(schema["properties"]["task"]["required"]).issubset(payload["task"])
    assert isinstance(payload["suggested_actions"], list) and payload["suggested_actions"]
    for action in payload["suggested_actions"]:
        assert set(schema["properties"]["suggested_actions"]["items"]["required"]).issubset(action)
        assert action["type"] in schema["properties"]["suggested_actions"]["items"]["properties"]["type"]["enum"]
    assert isinstance(payload["missing_fields"], list)
    assert isinstance(payload["explanation"], str) and payload["explanation"]


def main() -> int:
    """Run backend smoke checks.

    Args:
        None.

    Returns:
        Process exit code.
    """

    client = TestClient(app)
    health = client.get("/health")
    assert health.status_code == 200
    schema = client.get("/v1/schema")
    assert schema.status_code == 200
    schema_payload = schema.json()
    assert "$schema" in schema_payload
    assert "properties" in schema_payload
    assert "scene_type" in schema_payload["properties"]
    assert "suggested_actions" in schema_payload["required"]

    course_response = client.post(
        "/v1/analyze",
        json={
            "input_id": "sample-course-001",
            "source_type": "screenshot",
            "ocr_text": "高数A班今晚18:30改到B203，作业第5章今晚22:00前提交。",
            "scene_hint": "course_notice",
        },
    )
    assert course_response.status_code == 200
    course_payload = course_response.json()
    assert_model_output_schema(schema_payload, course_payload)
    assert course_payload["scene_type"] == "course_notice"
    assert {"calendar", "reminder", "map"} == {item["type"] for item in course_payload["suggested_actions"]}

    event_response = client.post(
        "/v1/analyze",
        json={
            "input_id": "sample-event-001",
            "source_type": "camera",
            "ocr_text": "AI应用分享会 4月24日19:30 图书馆报告厅 报名截止今晚22:00",
            "scene_hint": "event_poster",
        },
    )
    assert event_response.status_code == 200
    event_payload = event_response.json()
    assert_model_output_schema(schema_payload, event_payload)
    assert event_payload["scene_type"] == "event_poster"
    assert "registration_url" in event_payload["missing_fields"]

    unknown_response = client.post(
        "/v1/analyze",
        json={
            "input_id": "sample-unknown-001",
            "source_type": "screenshot",
            "ocr_text": "备忘一下这件事后面再看",
        },
    )
    assert unknown_response.status_code == 200
    unknown_payload = unknown_response.json()
    assert_model_output_schema(schema_payload, unknown_payload)
    assert unknown_payload["scene_type"] == "unknown"
    assert unknown_payload["confidence"] < 0.65

    bad = client.post(
        "/v1/analyze",
        json={
            "input_id": "bad-empty",
            "source_type": "screenshot",
            "ocr_text": "",
        },
    )
    assert bad.status_code == 422
    print("backend_passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
