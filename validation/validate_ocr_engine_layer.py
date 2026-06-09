#!/usr/bin/env python3
"""Validate OCR engine layering for capture/import flows."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def command_passes(command: list[str]) -> bool:
    result = subprocess.run(command, cwd=WORKSPACE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return result.returncode == 0


def main() -> int:
    ocr_engine = read("android-mvp/app/src/main/java/cn/shike/app/data/OcrEngine.kt")
    capture_mapper = read("android-mvp/app/src/main/java/cn/shike/app/data/CaptureImportMapper.kt")
    share_mapper = read("android-mvp/app/src/main/java/cn/shike/app/data/ShareImportMapper.kt")
    ocr_test = read("android-mvp/app/src/test/java/cn/shike/app/data/OcrEngineTest.kt")
    docs = read("docs/android-mvp-implementation.md")

    checks = [
        (
            "ocr_contracts_present",
            all(token in ocr_engine for token in ["interface OcrEngine", "data class CaptureInput", "data class OcrResult"]),
            "OcrEngine contracts",
        ),
        (
            "manual_and_mock_engines_present",
            "class ManualOcrEngine" in ocr_engine and "class MockOcrEngine" in ocr_engine,
            "Manual/Mock",
        ),
        (
            "capture_draft_records_required_metadata",
            all(
                token in capture_mapper
                for token in [
                    "val sourceType: CaptureSourceType",
                    "val ocrText: String",
                    "val ocrConfidence: Float",
                    "val privacyLevel: PrivacyLevel",
                    "val cloudAllowed: Boolean",
                    "val imageCleared: Boolean",
                ]
            ),
            "CaptureDraft metadata",
        ),
        (
            "gallery_and_camera_start_pending_until_backend_image_analysis",
            "MockOcrEngine()" in capture_mapper
            and "pendingImageOcrResult" in ocr_engine
            and "engineName = \"image_pending\"" in ocr_engine
            and "pendingImageItem" in capture_mapper
            and "相册导入的课程通知" not in capture_mapper,
            "gallery/camera pending",
        ),
        (
            "share_uses_manual_ocr_without_cloud",
            "ManualOcrEngine()" in share_mapper and "allowCloudEnhancement = false" in share_mapper,
            "share manual",
        ),
        (
            "ocr_failure_copy_present",
            "未识别到稳定文字" in ocr_engine and "手动粘贴" in ocr_engine,
            "failure copy",
        ),
        (
            "unit_tests_cover_ocr_layer",
            all(
                token in ocr_test
                for token in ["ManualOcrEngine", "MockOcrEngine", "captureDraftFromInput", "image_pending"]
            ),
            "OcrEngineTest",
        ),
        (
            "docs_describe_ocr_layer",
            "OCR 分层" in docs and "ManualOcrEngine" in docs and "image_pending" in docs,
            "docs",
        ),
        (
            "android_unit_guard_passes",
            command_passes(["python3", "shike/validation/validate_android_unit_tests.py"]),
            "validate_android_unit_tests.py",
        ),
    ]

    passed = sum(1 for _, ok, _ in checks if ok)
    for name, ok, evidence in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}\t{evidence}")
    print(f"OCR_ENGINE_LAYER_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
