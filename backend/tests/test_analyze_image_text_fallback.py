"""Tests for `/v2/analyze-image` text fallback after OCR enrichment."""

from __future__ import annotations

import unittest
from typing import Any

from fastapi.testclient import TestClient

import shike_backend.main as main_module
from shike_backend.adapters.base import AdapterError
from shike_backend.adapters.vivo_ocr_adapter import OcrDetail
from shike_backend.main import app
from shike_backend.schemas import AnalyzeRequest, AnalyzeResponse, OcrResponse
from shike_backend.schemas_v2 import AnalyzeImageRequest, OcrBlock, ParsedActionCard


class FakeOcrAdapter:
    """Fake OCR adapter returning text usable by the text model fallback."""

    def recognize_detail(self, request: Any) -> OcrDetail:
        """Return OCR text and blocks for the image request.

        Args:
            request: Backend OCR request.

        Returns:
            OCR detail with one status-bar block and one content block.
        """

        return OcrDetail(
            response=OcrResponse(
                text="服务端OCR：今晚18:30 项目讨论 B203",
                confidence=0.92,
                engine="fake_server_ocr",
                is_redacted=False,
                image_cleared=True,
                failure_hint=None,
                request_id=request.input_id,
            ),
            blocks=[
                OcrBlock(text="09:50", x1=8, y1=10, x2=90, y2=40, confidence=0.98),
                OcrBlock(text="今晚18:30 项目讨论 B203", x1=80, y1=640, x2=900, y2=710, confidence=0.91),
            ],
        )


class FailingMultimodalAdapter:
    """Fake multimodal adapter matching the live provider image-support failure."""

    def is_configured(self) -> bool:
        """Return configured state for audit metadata."""

        return True

    def analyze_image(self, request: AnalyzeImageRequest, schema_json: dict[str, object]) -> Any:
        """Fail with the provider image-support boundary.

        Args:
            request: Enriched image request.
            schema_json: Response schema.

        Raises:
            AdapterError: Always raised to force fallback.
        """

        raise AdapterError("provider_model_does_not_support_image")


class LegacyUnauthorizedMultimodalAdapter:
    """Fake multimodal adapter matching signed VisionChat authorization failure."""

    def is_configured(self) -> bool:
        """Return configured state for audit metadata."""

        return True

    def analyze_image(self, request: AnalyzeImageRequest, schema_json: dict[str, object]) -> Any:
        """Fail with a legacy VisionChat authorization boundary.

        Args:
            request: Enriched image request.
            schema_json: Response schema.

        Raises:
            AdapterError: Always raised to force text fallback.
        """

        raise AdapterError("legacy_http_status:401")


class ExplodingOcrAdapter:
    """OCR adapter that must not be called when cloud image upload is disabled."""

    def recognize_detail(self, request: Any) -> OcrDetail:
        """Fail if server-side OCR is attempted.

        Args:
            request: Backend OCR request.

        Raises:
            AssertionError: Always, because this adapter is a test guard.
        """

        raise AssertionError("server OCR must not run when allow_cloud_image=false")


class ExplodingMultimodalAdapter:
    """Multimodal adapter that must not be called when cloud image upload is disabled."""

    def is_configured(self) -> bool:
        """Return configured state for audit metadata."""

        return True

    def analyze_image(self, request: AnalyzeImageRequest, schema_json: dict[str, object]) -> Any:
        """Fail if cloud multimodal image analysis is attempted.

        Args:
            request: Image request.
            schema_json: Response schema.

        Raises:
            AssertionError: Always, because this adapter is a test guard.
        """

        raise AssertionError("multimodal image analysis must not run when allow_cloud_image=false")


class SuccessfulMultimodalAdapter:
    """Fake multimodal adapter returning a schema-valid image result."""

    def __init__(self) -> None:
        self.calls = 0

    def is_configured(self) -> bool:
        """Return configured state for audit metadata."""

        return True

    def analyze_image(self, request: AnalyzeImageRequest, schema_json: dict[str, object]) -> ParsedActionCard:
        """Return a valid card and capture that the candidate was called.

        Args:
            request: Enriched image request.
            schema_json: Response schema.

        Returns:
            A valid parsed action card.
        """

        self.calls += 1
        return ParsedActionCard(
            title="图片模型识别成功",
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
                },
                {
                    "type": "map",
                    "label": "打开地图",
                    "requires_permission": False,
                    "disabled_reason": "模型声称可直接执行",
                }
            ],
            missing_fields=[],
            risks=[],
            evidence=[],
            ignored_regions=["Top synthetic screenshot fixture text", "top_status_bar"],
            explanation="由第二个图片模型候选识别，仍需用户确认。",
        )


class CourseOcrAdapter:
    """Fake OCR adapter with the user's reported course screenshot content."""

    def recognize_detail(self, request: Any) -> OcrDetail:
        """Return OCR evidence for a course at 21:00 in B203.

        Args:
            request: Backend OCR request.

        Returns:
            OCR detail whose main content includes subject, relative time, and
            classroom.
        """

        return OcrDetail(
            response=OcrResponse(
                text="服务端OCR：今晚九点上高数，教室是B203",
                confidence=0.94,
                engine="fake_server_ocr",
                is_redacted=False,
                image_cleared=True,
                failure_hint=None,
                request_id=request.input_id,
            ),
            blocks=[
                OcrBlock(text="19:16", x1=8, y1=10, x2=90, y2=40, confidence=0.98),
                OcrBlock(text="今晚九点上高数", x1=80, y1=640, x2=740, y2=710, confidence=0.92),
                OcrBlock(text="教室是B203", x1=80, y1=720, x2=520, y2=780, confidence=0.93),
            ],
        )


class IncompleteCourseMultimodalAdapter:
    """Fake image model that reproduces the reported partial extraction bug."""

    def is_configured(self) -> bool:
        """Return configured state for audit metadata."""

        return True

    def analyze_image(self, request: AnalyzeImageRequest, schema_json: dict[str, object]) -> ParsedActionCard:
        """Return B203 while dropping the subject and using the wrong hour.

        Args:
            request: Enriched image request.
            schema_json: Response schema.

        Returns:
            A schema-valid but semantically incomplete image card.
        """

        return ParsedActionCard(
            title="B203",
            scene_type="course_notice",
            confidence=0.74,
            time={
                "start_text": "今晚九点",
                "deadline_text": None,
                "normalized_start": "2026-06-08T09:00:00+08:00",
                "normalized_deadline": None,
            },
            location={"raw": "B203", "map_query": "B203", "confidence": 0.88},
            task={"summary": "去B203", "priority": "medium", "topic": "course"},
            suggested_actions=[
                {"type": "calendar", "label": "加入日历", "requires_permission": True},
                {"type": "reminder", "label": "设置提醒", "requires_permission": True},
                {"type": "map", "label": "查看地点", "requires_permission": False},
            ],
            missing_fields=[],
            risks=[],
            evidence=[],
            ignored_regions=[],
            explanation="图片模型只稳定识别到地点。",
        )


class CorrectingCourseTextAdapter:
    """Fake text fallback adapter that preserves OCR subject and relative time."""

    def __init__(self) -> None:
        self.request: AnalyzeRequest | None = None

    def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        """Return the corrected course card from OCR text.

        Args:
            request: OCR-enriched text fallback request.

        Returns:
            A course card whose subject and normalized time match OCR evidence.
        """

        self.request = request
        return AnalyzeResponse(
            scene_type="course_notice",
            confidence=0.9,
            title="高数课",
            time={
                "start_text": "今晚九点",
                "deadline_text": None,
                "normalized_start": "2026-06-08T21:00:00+08:00",
                "normalized_deadline": None,
            },
            location={"raw": "B203", "map_query": "B203", "confidence": 0.9},
            task={"summary": "今晚九点上高数课，教室是B203", "priority": "medium", "topic": "course"},
            suggested_actions=[
                {"type": "calendar", "label": "加入日历", "requires_permission": True},
                {"type": "reminder", "label": "设置提醒", "requires_permission": True},
                {"type": "map", "label": "查看地点", "requires_permission": False},
            ],
            missing_fields=[],
            explanation="由 OCR 文本修复图片模型漏字段。",
        )


class CapturingTextAdapter:
    """Fake BlueLM-style text adapter for fallback assertions."""

    def __init__(self) -> None:
        self.request: AnalyzeRequest | None = None

    def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        """Capture the fallback request and return a structured action card.

        Args:
            request: Text model request derived from OCR.

        Returns:
            A valid structured response.
        """

        self.request = request
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


class AnalyzeImageTextFallbackTest(unittest.TestCase):
    """Verify image analysis can fall back to OCR text parsing."""

    def test_analyze_image_uses_text_model_when_provider_does_not_support_image(self) -> None:
        original_ocr_adapter = main_module._OCR_ADAPTER
        original_multimodal_adapter = main_module._MULTIMODAL_ADAPTER
        original_adapter = main_module._ADAPTER
        text_adapter = CapturingTextAdapter()
        main_module._OCR_ADAPTER = FakeOcrAdapter()  # type: ignore[assignment]
        main_module._MULTIMODAL_ADAPTER = FailingMultimodalAdapter()  # type: ignore[assignment]
        main_module._ADAPTER = text_adapter
        try:
            response = TestClient(app).post(
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

        self.assertEqual(200, response.status_code)
        payload = response.json()
        self.assertEqual("项目讨论", payload["title"])
        self.assertEqual("course_notice", payload["scene_type"])
        self.assertNotIn("manual_review", payload["missing_fields"])
        self.assertIn("top_status_bar", payload["ignored_regions"])
        self.assertIn("bottom_navigation_bar", payload["ignored_regions"])
        self.assertTrue(any("provider_model_does_not_support_image" in risk for risk in payload["risks"]))
        self.assertTrue(all(action["disabled_reason"] == "用户确认前不可执行" for action in payload["suggested_actions"]))
        self.assertIsNotNone(text_adapter.request)
        assert text_adapter.request is not None
        self.assertEqual("screenshot", text_adapter.request.source_type)
        self.assertIn("客户端OCR：今晚18:30 项目讨论 B203", text_adapter.request.ocr_text)
        self.assertIn("服务端OCR：今晚18:30 项目讨论 B203", text_adapter.request.ocr_text)

    def test_analyze_image_uses_text_model_when_vision_chat_is_unauthorized(self) -> None:
        original_ocr_adapter = main_module._OCR_ADAPTER
        original_multimodal_adapter = main_module._MULTIMODAL_ADAPTER
        original_adapter = main_module._ADAPTER
        text_adapter = CapturingTextAdapter()
        main_module._OCR_ADAPTER = FakeOcrAdapter()  # type: ignore[assignment]
        main_module._MULTIMODAL_ADAPTER = LegacyUnauthorizedMultimodalAdapter()  # type: ignore[assignment]
        main_module._ADAPTER = text_adapter
        try:
            response = TestClient(app).post(
                "/v2/analyze-image",
                json={
                    "input_id": "image-visionchat-unauthorized-001",
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

        self.assertEqual(200, response.status_code)
        payload = response.json()
        self.assertEqual("项目讨论", payload["title"])
        self.assertEqual("course_notice", payload["scene_type"])
        self.assertNotIn("manual_review", payload["missing_fields"])
        self.assertTrue(any("legacy_http_status:401" in risk for risk in payload["risks"]))
        self.assertTrue(all(action["disabled_reason"] == "用户确认前不可执行" for action in payload["suggested_actions"]))
        self.assertIsNotNone(text_adapter.request)

    def test_analyze_image_tries_next_multimodal_candidate_before_text_fallback(self) -> None:
        original_ocr_adapter = main_module._OCR_ADAPTER
        original_multimodal_adapter = main_module._MULTIMODAL_ADAPTER
        original_adapter = main_module._ADAPTER
        text_adapter = CapturingTextAdapter()
        second_adapter = SuccessfulMultimodalAdapter()
        main_module._OCR_ADAPTER = FakeOcrAdapter()  # type: ignore[assignment]
        main_module._MULTIMODAL_ADAPTER = [FailingMultimodalAdapter(), second_adapter]  # type: ignore[assignment]
        main_module._ADAPTER = text_adapter
        try:
            response = TestClient(app).post(
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

        self.assertEqual(200, response.status_code)
        payload = response.json()
        self.assertEqual("图片模型识别成功", payload["title"])
        self.assertEqual("meeting_notice", payload["scene_type"])
        self.assertEqual(1, second_adapter.calls)
        self.assertIsNone(text_adapter.request)
        self.assertFalse(any(risk.startswith("text_fallback:") for risk in payload["risks"]))
        self.assertTrue(all(action["disabled_reason"] == "用户确认前不可执行" for action in payload["suggested_actions"]))
        self.assertEqual(["top_status_bar", "bottom_navigation_bar"], payload["ignored_regions"])

    def test_analyze_image_repairs_partial_image_result_from_ocr_evidence(self) -> None:
        original_ocr_adapter = main_module._OCR_ADAPTER
        original_multimodal_adapter = main_module._MULTIMODAL_ADAPTER
        original_adapter = main_module._ADAPTER
        text_adapter = CorrectingCourseTextAdapter()
        main_module._OCR_ADAPTER = CourseOcrAdapter()  # type: ignore[assignment]
        main_module._MULTIMODAL_ADAPTER = IncompleteCourseMultimodalAdapter()  # type: ignore[assignment]
        main_module._ADAPTER = text_adapter
        try:
            response = TestClient(app).post(
                "/v2/analyze-image",
                json={
                    "input_id": "image-course-ocr-repair-001",
                    "source_type": "screenshot_share",
                    "image": {
                        "data_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB",
                        "mime": "image/png",
                        "width": 1080,
                        "height": 2400,
                        "sha256": "placeholder-sha256",
                    },
                    "ocr_text_hint": "客户端OCR：教室是B203",
                    "ocr_blocks": [],
                    "current_date": "2026-06-08",
                    "user_timezone": "Asia/Shanghai",
                    "scene_hint": "course_notice",
                },
            )
        finally:
            main_module._OCR_ADAPTER = original_ocr_adapter
            main_module._MULTIMODAL_ADAPTER = original_multimodal_adapter
            main_module._ADAPTER = original_adapter

        self.assertEqual(200, response.status_code)
        payload = response.json()
        self.assertIn("高数", payload["title"])
        self.assertEqual("2026-06-08T21:00:00+08:00", payload["time"]["normalized_start"])
        self.assertEqual("B203", payload["location"]["raw"])
        self.assertTrue(any("ocr_evidence_repair:ocr_subject_missing" in risk for risk in payload["risks"]))
        self.assertTrue(any("ocr_evidence_repair:ocr_time_mismatch" in risk for risk in payload["risks"]))
        self.assertTrue(all(action["disabled_reason"] == "用户确认前不可执行" for action in payload["suggested_actions"]))
        self.assertIsNotNone(text_adapter.request)
        assert text_adapter.request is not None
        self.assertIn("今晚九点上高数", text_adapter.request.ocr_text)

    def test_analyze_image_uses_ocr_hint_only_when_cloud_image_disabled(self) -> None:
        original_ocr_adapter = main_module._OCR_ADAPTER
        original_multimodal_adapter = main_module._MULTIMODAL_ADAPTER
        original_adapter = main_module._ADAPTER
        text_adapter = CapturingTextAdapter()
        main_module._OCR_ADAPTER = ExplodingOcrAdapter()  # type: ignore[assignment]
        main_module._MULTIMODAL_ADAPTER = ExplodingMultimodalAdapter()  # type: ignore[assignment]
        main_module._ADAPTER = text_adapter
        try:
            response = TestClient(app).post(
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
                        {
                            "text": "今晚18:30 项目讨论 B203",
                            "x1": 80,
                            "y1": 640,
                            "x2": 800,
                            "y2": 720,
                            "confidence": 0.92,
                        },
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

        self.assertEqual(200, response.status_code)
        payload = response.json()
        self.assertEqual("项目讨论", payload["title"])
        self.assertEqual("course_notice", payload["scene_type"])
        self.assertTrue(any("cloud_image_disabled" in risk for risk in payload["risks"]))
        self.assertTrue(all(action["disabled_reason"] == "用户确认前不可执行" for action in payload["suggested_actions"]))
        self.assertIsNotNone(text_adapter.request)
        assert text_adapter.request is not None
        self.assertEqual("screenshot", text_adapter.request.source_type)
        self.assertEqual("客户端OCR：今晚18:30 项目讨论 B203", text_adapter.request.ocr_text)


if __name__ == "__main__":
    unittest.main()
