#!/usr/bin/env python3
"""Validate that real OCR text is not polluted by offline sample fields."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
FORBIDDEN = ["B203", "18:30", "22:00", "第5章", "相册导入的课程通知", "MockModelAdapter"]
USER_REPORTED_TEXT = "晚上九点上 高数 B地点在303"


def command_passes(command: list[str]) -> bool:
    result = subprocess.run(
        command,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return result.returncode == 0


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def backend_short_math_payload() -> dict[str, object] | None:
    probe = """
import json
from fastapi.testclient import TestClient
from shike_backend.main import app

client = TestClient(app)
response = client.post('/v1/analyze', json={
    'input_id': 'course-short-need-math-001',
    'source_type': 'manual',
    'ocr_text': '今天晚上需要上高数A',
    'scene_hint': 'course_notice',
})
print(response.status_code)
print(json.dumps(response.json(), ensure_ascii=False))
"""
    result = subprocess.run(
        [sys.executable, "-c", probe],
        cwd=WORKSPACE,
        env={"PYTHONPATH": str(ROOT / "backend")},
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if result.returncode != 0:
        return None
    lines = result.stdout.strip().splitlines()
    if len(lines) < 2 or lines[-2] != "200":
        return None
    return json.loads(lines[-1])


def backend_user_reported_payload() -> dict[str, object] | None:
    probe = f"""
import json
from fastapi.testclient import TestClient
from shike_backend.main import app

client = TestClient(app)
response = client.post('/v1/analyze', json={{
    'input_id': 'course-user-reported-20260609',
    'source_type': 'manual',
    'ocr_text': {USER_REPORTED_TEXT!r},
    'scene_hint': 'course_notice',
}})
print(response.status_code)
print(json.dumps(response.json(), ensure_ascii=False))
"""
    result = subprocess.run(
        [sys.executable, "-c", probe],
        cwd=WORKSPACE,
        env={"PYTHONPATH": str(ROOT / "backend")},
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if result.returncode != 0:
        return None
    lines = result.stdout.strip().splitlines()
    if len(lines) < 2 or lines[-2] != "200":
        return None
    return json.loads(lines[-1])


def main() -> int:
    payload = backend_short_math_payload()
    reported_payload = backend_user_reported_payload()
    payload_text = json.dumps(payload, ensure_ascii=False) if payload is not None else ""
    reported_payload_text = json.dumps(reported_payload, ensure_ascii=False) if reported_payload is not None else ""
    ocr_engine = read("android-mvp/app/src/main/java/cn/shike/app/data/OcrEngine.kt")
    capture_mapper = read("android-mvp/app/src/main/java/cn/shike/app/data/CaptureImportMapper.kt")
    capture_mapper_test = read("android-mvp/app/src/test/java/cn/shike/app/data/CaptureImportMapperTest.kt")
    capture_result_test = read("android-mvp/app/src/test/java/cn/shike/app/CaptureResultActionsTest.kt")
    backend_runner = read("android-mvp/app/src/main/java/cn/shike/app/data/BackendAnalysisRunner.kt")
    backend_runner_test = read("android-mvp/app/src/test/java/cn/shike/app/BackendAnalysisRunnerTest.kt")
    verify_backend = read("backend/verify_backend.py")
    regression_cases = read("validation/regression-cases.json")

    checks = [
        ("backend_short_math_returns_payload", payload is not None),
        ("backend_keeps_math_title", payload is not None and "高数" in str(payload.get("title", ""))),
        (
            "backend_marks_missing_time_and_location",
            payload is not None
            and {"exact_start_time", "location"}.issubset(set(payload.get("missing_fields", [])))
            and payload.get("location") is None,
        ),
        (
            "backend_uses_reminder_only",
            payload is not None
            and {item.get("type") for item in payload.get("suggested_actions", [])} == {"reminder"},
        ),
        ("backend_forbids_sample_tokens", all(token not in payload_text for token in FORBIDDEN)),
        ("backend_user_reported_returns_payload", reported_payload is not None),
        (
            "backend_user_reported_extracts_time_and_location_from_evidence",
            reported_payload is not None
            and "高数" in str(reported_payload.get("title", ""))
            and "九点" in json.dumps(reported_payload.get("time"), ensure_ascii=False)
            and "303" in json.dumps(reported_payload.get("location"), ensure_ascii=False),
        ),
        ("backend_user_reported_forbids_sample_tokens", all(token not in reported_payload_text for token in FORBIDDEN)),
        (
            "android_image_import_starts_neutral_pending",
            "pendingImageOcrResult" in ocr_engine
            and "engineName = \"image_pending\"" in ocr_engine
            and "pendingImageItem" in capture_mapper
            and "待解析截图" in capture_mapper
            and "待解析照片" in capture_mapper
            and "相册导入的课程通知" not in capture_mapper,
        ),
        (
            "android_gallery_tests_forbid_sample_tokens",
            "gallerySelectionFromImage_startsPendingImageDraftWithoutCourseSample" in capture_mapper_test
            and "applyGalleryImageSelection_persistsPendingImageDraftWithoutSampleFields" in capture_result_test
            and all(token in capture_mapper_test + capture_result_test for token in ["B203", "18:30", "22:00", "第5章"])
            and "assertFalse(item.title.contains(\"相册导入的课程通知\"))" in capture_result_test,
        ),
        (
            "android_failure_fallback_forbids_sample_tokens",
            "fallbackItemForRealDraft" in backend_runner
            and "今天晚上（需确认具体时间）" in backend_runner
            and "先存入待确认" in backend_runner
            and "云侧暂不可用，已切换为本地确认" in backend_runner
            and "backendFailureOutcomeForRealMathDraft_doesNotInjectCourseSampleFields" in backend_runner_test,
        ),
        (
            "backend_verify_contains_regression",
            "course-short-need-math-001" in verify_backend
            and all(token in verify_backend for token in FORBIDDEN[:-1]),
        ),
        (
            "regression_case_documented",
            "course-short-need-math-001" in regression_cases
            and "forbidden_output_tokens" in regression_cases,
        ),
        ("backend_smoke_passes", command_passes(["python3", "backend/verify_backend.py"])),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"NO_SAMPLE_CONTAMINATION_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
