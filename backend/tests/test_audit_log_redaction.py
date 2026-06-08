import unittest
import hashlib

from shike_backend.schemas_v2 import AnalyzeImageRequest

try:
    from shike_backend.audit_log import build_analyze_image_audit_event
except ModuleNotFoundError:
    build_analyze_image_audit_event = None


class AnalyzeImageAuditLogTest(unittest.TestCase):
    def test_analyze_image_audit_event_uses_redacted_metadata_only(self) -> None:
        self.assertIsNotNone(build_analyze_image_audit_event)

        request = AnalyzeImageRequest(
            input_id="capture-13800138000-test@example.com-2026123456",
            source_type="screenshot_share",
            image={
                "data_url": "data:image/png;base64,abcdefghijklmnopqrstuvwxyz123456",
                "mime": "image/png",
                "width": 1080,
                "height": 2400,
                "sha256": "a13f8b7c4d5e6f901234567890abcdef",
            },
            ocr_text_hint="张三 手机 13800138000 学号 2026123456 明天18:30上高数到B203",
            ocr_blocks=[
                {"text": "09:50", "x1": 0, "y1": 0, "x2": 80, "y2": 40, "confidence": 0.99},
                {"text": "明天18:30上高数到B203", "x1": 100, "y1": 400, "x2": 600, "y2": 460},
            ],
            current_date="2026-06-06",
            user_timezone="Asia/Shanghai",
        )

        event = build_analyze_image_audit_event(
            request,
            provider="vivo_cloud_multimodal",
            key_present=True,
            duration_ms=1832,
            status="schema_valid",
            repair_risks=["ocr_evidence_repair:ocr_time_mismatch"],
        )
        serialized = str(event)

        self.assertEqual(event["provider"], "vivo_cloud_multimodal")
        self.assertEqual(
            event["input_id_hash"],
            hashlib.sha256(request.input_id.encode("utf-8")).hexdigest()[:16],
        )
        self.assertEqual(event["source_type"], "screenshot_share")
        self.assertEqual(event["image_present"], True)
        self.assertEqual(event["image_sha256_prefix"], "a13f8b7c")
        self.assertEqual(event["ocr_block_count"], 2)
        self.assertEqual(event["ocr_hint_length"], len(request.ocr_text_hint or ""))
        self.assertEqual(event["key_present"], True)
        self.assertEqual(event["duration_ms"], 1832)
        self.assertEqual(event["status"], "schema_valid")
        self.assertEqual(event["ocr_has_course_signal"], True)
        self.assertEqual(event["ocr_has_time_signal"], True)
        self.assertEqual(event["ocr_has_location_signal"], True)
        self.assertEqual(event["ocr_repair_applied"], True)
        self.assertEqual(event["ocr_repair_reasons"], ["ocr_time_mismatch"])

        self.assertNotIn("Authorization", serialized)
        self.assertNotIn("AppKEY", serialized)
        self.assertNotIn("abcdefghijklmnopqrstuvwxyz123456", serialized)
        self.assertNotIn("13800138000", serialized)
        self.assertNotIn("test@example.com", serialized)
        self.assertNotIn("2026123456", serialized)
        self.assertNotIn("张三", serialized)
        self.assertNotIn("明天18:30上高数到B203", serialized)
        self.assertNotIn(request.input_id, serialized)


if __name__ == "__main__":
    unittest.main()
