#!/usr/bin/env python3
"""Verify the Shike FastAPI backend without starting a server."""

from __future__ import annotations

import json
import os
from typing import Any

from fastapi.testclient import TestClient

for key in [
    "SHIKE_BACKEND_ENV_FILE",
    "BLUELM_APP_ID",
    "BLUELM_APP_KEY",
    "VIVO_AIGC_APP_ID",
    "VIVO_AIGC_APP_KEY",
    "VIVO_OCR_APP_ID",
    "VIVO_OCR_APP_KEY",
    "VIVO_MULTIMODAL_APP_ID",
    "VIVO_MULTIMODAL_APP_KEY",
    "DEEPSEEK_API_KEY",
    "DEEPSEEK_BASE_URL",
    "DEEPSEEK_URI",
    "DEEPSEEK_MODEL",
]:
    os.environ.pop(key, None)
os.environ["SHIKE_BACKEND_ENV_FILE"] = "/dev/null"
os.environ["SHIKE_MODEL_PROVIDER"] = "mock"
os.environ["SHIKE_ALLOW_MOCK_FALLBACK"] = "true"

import shike_backend.main as main_module
from shike_backend.adapters.vivo_ocr_adapter import OcrDetail
from shike_backend.adapters.base import AdapterError
from shike_backend.main import app
from shike_backend.schemas import AnalyzeRequest, AnalyzeResponse, OcrResponse
from shike_backend.schemas_v2 import AnalyzeImageRequest, OcrBlock, ParsedActionCard


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


class FakeOcrAdapter:
    """Fake server OCR adapter used to assert v2 enrichment behavior."""

    def recognize_detail(self, request: Any) -> OcrDetail:
        """Return stable OCR text and blocks for the v2 route.

        Args:
            request: OCR request built from the image data URL.

        Returns:
            Synthetic OCR detail with image-cleared metadata.
        """

        assert request.image_base64 == "iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB"
        return OcrDetail(
            response=OcrResponse(
                text="服务端OCR补充：今晚20:00 自习室C301",
                confidence=0.86,
                engine="fake_server_ocr",
                is_redacted=False,
                image_cleared=True,
                failure_hint=None,
                request_id=request.input_id,
            ),
            blocks=[
                OcrBlock(text="09:50", x1=8, y1=10, x2=90, y2=40, confidence=0.98),
                OcrBlock(text="服务端OCR块：今晚20:00 自习室C301", x1=80, y1=640, x2=900, y2=710, confidence=0.91),
            ],
        )

    def recognize(self, request: Any) -> OcrResponse:
        """Return a compatible v1 OCR response."""

        return self.recognize_detail(request).response


class CapturingMultimodalAdapter:
    """Fake multimodal adapter that captures the enriched request."""

    captured_request: AnalyzeImageRequest | None = None

    def analyze_image(self, request: AnalyzeImageRequest, schema_json: dict[str, object]) -> ParsedActionCard:
        """Capture the request and return a valid manual-review card.

        Args:
            request: Enriched v2 request.
            schema_json: Response schema supplied by the route.

        Returns:
            A low-risk action card requiring user confirmation.
        """

        assert "properties" in schema_json
        self.captured_request = request
        return ParsedActionCard(
            title="待确认碎片",
            scene_type="unknown",
            confidence=0.41,
            time=None,
            location=None,
            task={"summary": "需要用户确认", "priority": "low", "topic": "unknown"},
            suggested_actions=[
                {
                    "type": "reminder",
                    "label": "稍后确认",
                    "requires_permission": True,
                    "disabled_reason": "用户确认前不可执行",
                }
            ],
            missing_fields=["manual_review"],
            risks=[],
            evidence=[],
            ignored_regions=[],
            explanation="测试服务端 OCR enrichment 后仍需用户确认。",
        )


class FailingMultimodalAdapter:
    """Fake multimodal adapter used to prove OCR text fallback behavior."""

    def is_configured(self) -> bool:
        """Return configured state for audit metadata."""

        return True

    def analyze_image(self, request: AnalyzeImageRequest, schema_json: dict[str, object]) -> ParsedActionCard:
        """Raise the same image-support boundary seen in live smoke.

        Args:
            request: Enriched v2 image request.
            schema_json: Response schema supplied by the route.

        Raises:
            AdapterError: Always, to force the text fallback.
        """

        raise AdapterError("provider_model_does_not_support_image")


class ExplodingOcrAdapter:
    """OCR adapter that must not run when cloud image analysis is disabled."""

    def recognize_detail(self, request: Any) -> OcrDetail:
        """Fail if route code tries server-side OCR.

        Args:
            request: OCR request.

        Raises:
            AssertionError: Always, because this is a route guard.
        """

        raise AssertionError("server OCR must not run when allow_cloud_image=false")


class ExplodingMultimodalAdapter:
    """Multimodal adapter that must not run when cloud image analysis is disabled."""

    def is_configured(self) -> bool:
        """Return configured state for audit metadata."""

        return True

    def analyze_image(self, request: AnalyzeImageRequest, schema_json: dict[str, object]) -> ParsedActionCard:
        """Fail if route code calls the image model.

        Args:
            request: Image request.
            schema_json: Response schema supplied by the route.

        Raises:
            AssertionError: Always, because this is a route guard.
        """

        raise AssertionError("multimodal image analysis must not run when allow_cloud_image=false")


class SuccessfulMultimodalAdapter:
    """Fake multimodal adapter used to prove candidate chaining behavior."""

    calls = 0

    def is_configured(self) -> bool:
        """Return configured state for audit metadata."""

        return True

    def analyze_image(self, request: AnalyzeImageRequest, schema_json: dict[str, object]) -> ParsedActionCard:
        """Return a valid card from a later image-model candidate.

        Args:
            request: Enriched v2 image request.
            schema_json: Response schema supplied by the route.

        Returns:
            Structured v2 card without using the text fallback.
        """

        assert "properties" in schema_json
        self.calls += 1
        return ParsedActionCard(
            title="图片候选模型识别成功",
            scene_type="meeting_notice",
            confidence=0.88,
            time=None,
            location={"raw": "B203", "map_query": "B203", "confidence": 0.8},
            task={"summary": "参加项目讨论", "priority": "medium", "topic": "meeting"},
            suggested_actions=[
                {
                    "type": "calendar",
                    "label": "加入日历",
                    "requires_permission": False,
                    "disabled_reason": "用户确认前不可执行",
                }
            ],
            missing_fields=[],
            risks=[],
            evidence=[],
            ignored_regions=[],
            explanation="第二个图片模型候选返回结构化结果，仍需用户确认。",
        )


class CapturingTextAdapter:
    """Fake text adapter used to assert the v2 OCR fallback request."""

    captured_request: AnalyzeRequest | None = None

    def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        """Capture the fallback OCR text request and return a valid card.

        Args:
            request: Text model request derived from the enriched OCR hint.

        Returns:
            Structured response used by the v2 route.
        """

        self.captured_request = request
        return AnalyzeResponse(
            scene_type="course_notice",
            confidence=0.82,
            title="项目讨论",
            time={
                "start_text": "今晚18:30",
                "deadline_text": None,
                "normalized_start": "2026-06-06T18:30:00+08:00",
                "normalized_deadline": None,
            },
            location={"raw": "B203", "map_query": "B203", "confidence": 0.85},
            task={"summary": "参加项目讨论", "priority": "medium", "topic": "course"},
            suggested_actions=[
                {"type": "calendar", "label": "加入日历", "requires_permission": False},
                {"type": "reminder", "label": "设置提醒", "requires_permission": True},
                {"type": "map", "label": "查看地点", "requires_permission": False},
            ],
            missing_fields=[],
            explanation="由 OCR 文本兜底解析，仍需用户确认。",
        )


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

    schema_v2 = client.get("/v2/schema")
    assert schema_v2.status_code == 200
    schema_v2_payload = schema_v2.json()
    assert "properties" in schema_v2_payload
    assert "ignored_regions" in schema_v2_payload["properties"]

    ocr_response = client.post(
        "/v1/ocr",
        json={
            "input_id": "ocr-fallback-001",
            "source_type": "screenshot",
            "image_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB",
            "locale": "zh-CN",
            "pos": 2,
        },
    )
    assert ocr_response.status_code == 200
    ocr_payload = ocr_response.json()
    assert ocr_payload["engine"] == "manual_fallback"
    assert ocr_payload["image_cleared"] is True
    assert "手动粘贴" in ocr_payload["failure_hint"]

    image_response = client.post(
        "/v2/analyze-image",
        json={
            "input_id": "image-fallback-001",
            "source_type": "screenshot_share",
            "image": {
                "data_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB",
                "mime": "image/png",
                "width": 1080,
                "height": 2400,
                "sha256": "placeholder-sha256",
            },
            "ocr_text_hint": "09:50\n首页\n今晚18:30 讲座 B203",
            "ocr_blocks": [
                {"text": "09:50", "x1": 12, "y1": 12, "x2": 90, "y2": 42, "confidence": 0.99},
                {"text": "首页", "x1": 20, "y1": 2300, "x2": 80, "y2": 2360, "confidence": 0.99},
                {"text": "今晚18:30 讲座 B203", "x1": 80, "y1": 640, "x2": 800, "y2": 720, "confidence": 0.92},
            ],
            "current_date": "2026-06-06",
            "user_timezone": "Asia/Shanghai",
        },
    )
    assert image_response.status_code == 200
    image_payload = image_response.json()
    assert image_payload["scene_type"] == "unknown"
    assert "manual_review" in image_payload["missing_fields"]
    assert "top_status_bar" in image_payload["ignored_regions"]
    assert "bottom_navigation_bar" in image_payload["ignored_regions"]
    assert image_payload["suggested_actions"][0]["disabled_reason"] == "用户确认前不可执行"
    assert any("server_ocr_unavailable" in risk for risk in image_payload["risks"])

    original_ocr_adapter = main_module._OCR_ADAPTER
    original_multimodal_adapter = main_module._MULTIMODAL_ADAPTER
    capturing_adapter = CapturingMultimodalAdapter()
    main_module._OCR_ADAPTER = FakeOcrAdapter()  # type: ignore[assignment]
    main_module._MULTIMODAL_ADAPTER = capturing_adapter  # type: ignore[assignment]
    try:
        enriched_response = client.post(
            "/v2/analyze-image",
            json={
                "input_id": "image-enriched-001",
                "source_type": "screenshot_share",
                "image": {
                    "data_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB",
                    "mime": "image/png",
                    "width": 1080,
                    "height": 2400,
                    "sha256": "placeholder-sha256",
                },
                "ocr_text_hint": "客户端OCR：今晚18:30 讲座 B203",
                "ocr_blocks": [],
                "current_date": "2026-06-06",
                "user_timezone": "Asia/Shanghai",
            },
        )
    finally:
        main_module._OCR_ADAPTER = original_ocr_adapter
        main_module._MULTIMODAL_ADAPTER = original_multimodal_adapter

    assert enriched_response.status_code == 200
    assert capturing_adapter.captured_request is not None
    captured_hint = capturing_adapter.captured_request.ocr_text_hint or ""
    assert "客户端OCR：今晚18:30 讲座 B203" in captured_hint
    assert "服务端OCR补充：今晚20:00 自习室C301" in captured_hint
    assert capturing_adapter.captured_request.ocr_blocks
    assert all(block.text != "09:50" for block in capturing_adapter.captured_request.ocr_blocks)
    assert any(block.text == "服务端OCR块：今晚20:00 自习室C301" for block in capturing_adapter.captured_request.ocr_blocks)
    for block in capturing_adapter.captured_request.ocr_blocks:
        assert block.text
    assert enriched_response.json()["risks"] == []

    original_ocr_adapter = main_module._OCR_ADAPTER
    original_multimodal_adapter = main_module._MULTIMODAL_ADAPTER
    original_adapter = main_module._ADAPTER
    text_adapter = CapturingTextAdapter()
    main_module._OCR_ADAPTER = FakeOcrAdapter()  # type: ignore[assignment]
    main_module._MULTIMODAL_ADAPTER = FailingMultimodalAdapter()  # type: ignore[assignment]
    main_module._ADAPTER = text_adapter
    try:
        text_fallback_response = client.post(
            "/v2/analyze-image",
            json={
                "input_id": "image-text-fallback-001",
                "source_type": "screenshot_share",
                "image": {
                    "data_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB",
                    "mime": "image/png",
                    "width": 1080,
                    "height": 2400,
                    "sha256": "placeholder-sha256",
                },
                "ocr_text_hint": "客户端OCR：今晚18:30 项目讨论 B203",
                "ocr_blocks": [],
                "current_date": "2026-06-06",
                "user_timezone": "Asia/Shanghai",
            },
        )
    finally:
        main_module._OCR_ADAPTER = original_ocr_adapter
        main_module._MULTIMODAL_ADAPTER = original_multimodal_adapter
        main_module._ADAPTER = original_adapter

    assert text_fallback_response.status_code == 200
    text_fallback_payload = text_fallback_response.json()
    assert text_fallback_payload["title"] == "项目讨论"
    assert text_fallback_payload["scene_type"] == "course_notice"
    assert "manual_review" not in text_fallback_payload["missing_fields"]
    assert "top_status_bar" in text_fallback_payload["ignored_regions"]
    assert "bottom_navigation_bar" in text_fallback_payload["ignored_regions"]
    assert any("provider_model_does_not_support_image" in risk for risk in text_fallback_payload["risks"])
    assert all(action["disabled_reason"] == "用户确认前不可执行" for action in text_fallback_payload["suggested_actions"])
    assert text_adapter.captured_request is not None
    assert text_adapter.captured_request.source_type == "screenshot"
    assert "客户端OCR：今晚18:30 项目讨论 B203" in text_adapter.captured_request.ocr_text
    assert "服务端OCR补充：今晚20:00 自习室C301" in text_adapter.captured_request.ocr_text

    original_ocr_adapter = main_module._OCR_ADAPTER
    original_multimodal_adapter = main_module._MULTIMODAL_ADAPTER
    original_adapter = main_module._ADAPTER
    text_adapter = CapturingTextAdapter()
    successful_multimodal_adapter = SuccessfulMultimodalAdapter()
    main_module._OCR_ADAPTER = FakeOcrAdapter()  # type: ignore[assignment]
    main_module._MULTIMODAL_ADAPTER = [FailingMultimodalAdapter(), successful_multimodal_adapter]
    main_module._ADAPTER = text_adapter
    try:
        multimodal_candidate_response = client.post(
            "/v2/analyze-image",
            json={
                "input_id": "image-multimodal-candidates-001",
                "source_type": "screenshot_share",
                "image": {
                    "data_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB",
                    "mime": "image/png",
                    "width": 1080,
                    "height": 2400,
                    "sha256": "placeholder-sha256",
                },
                "ocr_text_hint": "客户端OCR：今晚18:30 项目讨论 B203",
                "ocr_blocks": [],
                "current_date": "2026-06-06",
                "user_timezone": "Asia/Shanghai",
            },
        )
    finally:
        main_module._OCR_ADAPTER = original_ocr_adapter
        main_module._MULTIMODAL_ADAPTER = original_multimodal_adapter
        main_module._ADAPTER = original_adapter

    assert multimodal_candidate_response.status_code == 200
    multimodal_candidate_payload = multimodal_candidate_response.json()
    assert multimodal_candidate_payload["title"] == "图片候选模型识别成功"
    assert successful_multimodal_adapter.calls == 1
    assert text_adapter.captured_request is None
    assert not any(risk.startswith("text_fallback:") for risk in multimodal_candidate_payload["risks"])

    original_ocr_adapter = main_module._OCR_ADAPTER
    original_multimodal_adapter = main_module._MULTIMODAL_ADAPTER
    original_adapter = main_module._ADAPTER
    text_adapter = CapturingTextAdapter()
    main_module._OCR_ADAPTER = ExplodingOcrAdapter()  # type: ignore[assignment]
    main_module._MULTIMODAL_ADAPTER = ExplodingMultimodalAdapter()  # type: ignore[assignment]
    main_module._ADAPTER = text_adapter
    try:
        cloud_disabled_response = client.post(
            "/v2/analyze-image",
            json={
                "input_id": "image-cloud-disabled-001",
                "source_type": "screenshot_share",
                "image": {
                    "data_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB",
                    "mime": "image/png",
                    "width": 1080,
                    "height": 2400,
                    "sha256": "placeholder-sha256",
                },
                "ocr_text_hint": "客户端OCR：今晚18:30 项目讨论 B203",
                "ocr_blocks": [
                    {"text": "09:50", "x1": 12, "y1": 12, "x2": 90, "y2": 42, "confidence": 0.99},
                    {"text": "今晚18:30 项目讨论 B203", "x1": 80, "y1": 640, "x2": 800, "y2": 720, "confidence": 0.92},
                ],
                "allow_cloud_image": False,
                "current_date": "2026-06-06",
                "user_timezone": "Asia/Shanghai",
            },
        )
    finally:
        main_module._OCR_ADAPTER = original_ocr_adapter
        main_module._MULTIMODAL_ADAPTER = original_multimodal_adapter
        main_module._ADAPTER = original_adapter

    assert cloud_disabled_response.status_code == 200
    cloud_disabled_payload = cloud_disabled_response.json()
    assert cloud_disabled_payload["title"] == "项目讨论"
    assert cloud_disabled_payload["scene_type"] == "course_notice"
    assert any("cloud_image_disabled" in risk for risk in cloud_disabled_payload["risks"])
    assert all(action["disabled_reason"] == "用户确认前不可执行" for action in cloud_disabled_payload["suggested_actions"])
    assert text_adapter.captured_request is not None
    assert text_adapter.captured_request.source_type == "screenshot"
    assert text_adapter.captured_request.ocr_text == "客户端OCR：今晚18:30 项目讨论 B203"

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

    short_math_response = client.post(
        "/v1/analyze",
        json={
            "input_id": "course-short-need-math-001",
            "source_type": "manual",
            "ocr_text": "今天晚上需要上高数A",
            "scene_hint": "course_notice",
        },
    )
    assert short_math_response.status_code == 200
    short_math_payload = short_math_response.json()
    assert_model_output_schema(schema_payload, short_math_payload)
    assert short_math_payload["scene_type"] == "course_notice"
    assert "高数" in short_math_payload["title"]
    assert short_math_payload["time"]["start_text"] == "今天晚上"
    assert short_math_payload["time"]["normalized_start"] is None
    assert short_math_payload["location"] is None
    assert {"exact_start_time", "location"}.issubset(short_math_payload["missing_fields"])
    assert {"reminder"} == {item["type"] for item in short_math_payload["suggested_actions"]}
    short_math_json = json.dumps(short_math_payload, ensure_ascii=False)
    for forbidden in ["B203", "18:30", "22:00", "第5章", "相册导入的课程通知"]:
        assert forbidden not in short_math_json

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
