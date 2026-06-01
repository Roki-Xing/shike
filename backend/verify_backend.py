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

    share_response = client.post(
        "/v1/analyze",
        json={
            "input_id": "sample-share-001",
            "source_type": "share_text",
            "ocr_text": "AI应用分享会 4月24日19:30 图书馆报告厅 报名截止今晚22:00",
            "scene_hint": "event_poster",
        },
    )
    assert share_response.status_code == 200
    share_payload = share_response.json()
    assert_model_output_schema(schema_payload, share_payload)
    assert share_payload["scene_type"] == "event_poster"

    manual_response = client.post(
        "/v1/analyze",
        json={
            "input_id": "sample-manual-001",
            "source_type": "manual",
            "ocr_text": "高数A班今晚18:30改到B203，作业第5章今晚22:00前提交。",
            "scene_hint": "course_notice",
        },
    )
    assert manual_response.status_code == 200
    manual_payload = manual_response.json()
    assert_model_output_schema(schema_payload, manual_payload)
    assert manual_payload["scene_type"] == "course_notice"

    assignment_response = client.post(
        "/v1/analyze",
        json={
            "input_id": "sample-assignment-001",
            "source_type": "share_text",
            "ocr_text": "数据库实验报告今晚22:00前通过教学平台提交，逾期将标记为迟交。",
            "scene_hint": "assignment_deadline",
        },
    )
    assert assignment_response.status_code == 200
    assignment_payload = assignment_response.json()
    assert_model_output_schema(schema_payload, assignment_payload)
    assert assignment_payload["scene_type"] == "unknown"
    assert assignment_payload["task"]["topic"] == "unknown"

    meeting_response = client.post(
        "/v1/analyze",
        json={
            "input_id": "sample-meeting-001",
            "source_type": "manual",
            "ocr_text": "项目周会定于今晚10:00在腾讯会议进行，请准备进展和待协调事项。",
            "scene_hint": "meeting_notice",
        },
    )
    assert meeting_response.status_code == 200
    meeting_payload = meeting_response.json()
    assert_model_output_schema(schema_payload, meeting_payload)
    assert meeting_payload["scene_type"] == "unknown"
    assert meeting_payload["task"]["topic"] == "unknown"

    interview_response = client.post(
        "/v1/analyze",
        json={
            "input_id": "sample-interview-001",
            "source_type": "screenshot",
            "ocr_text": "HR通知：明天14:00线上会议室进行产品实习生面试，请提前准备简历。",
            "scene_hint": "interview_notice",
        },
    )
    assert interview_response.status_code == 200
    interview_payload = interview_response.json()
    assert_model_output_schema(schema_payload, interview_payload)
    assert interview_payload["scene_type"] == "unknown"
    assert interview_payload["task"]["topic"] == "unknown"

    travel_response = client.post(
        "/v1/analyze",
        json={
            "input_id": "sample-travel-001",
            "source_type": "camera",
            "ocr_text": "高铁出行今晚10:00在西安北站集合，提前15分钟到达并检查证件。",
            "scene_hint": "travel_ticket",
        },
    )
    assert travel_response.status_code == 200
    travel_payload = travel_response.json()
    assert_model_output_schema(schema_payload, travel_payload)
    assert travel_payload["scene_type"] == "unknown"
    assert travel_payload["task"]["topic"] == "unknown"

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
