#!/usr/bin/env python3
"""Validate OCR evidence routes into action cards without sample pollution."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
FORBIDDEN_WITHOUT_EVIDENCE = ("18:30", "22:00", "第5章", "教室变更")


def command_passes(command: list[str]) -> bool:
    env = {**os.environ, "PYTHONPATH": str(ROOT / "backend")}
    result = subprocess.run(command, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return result.returncode == 0


def run_probe(script: str) -> dict[str, object] | None:
    env = {
        **os.environ,
        "PYTHONPATH": str(ROOT / "backend"),
        "SHIKE_BACKEND_ENV_FILE": "/dev/null",
        "SHIKE_RUNTIME_MODE": "release_user",
        "SHIKE_MODEL_PROVIDER": "mock",
        "SHIKE_ALLOW_MOCK_FALLBACK": "true",
    }
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=WORKSPACE,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if result.returncode != 0:
        return None
    lines = result.stdout.strip().splitlines()
    if not lines:
        return None
    return json.loads(lines[-1])


def v1_course_nine_payload() -> dict[str, object] | None:
    return run_probe(
        """
import json
import shike_backend.main as main_module
import shike_backend.settings as settings_module
from fastapi.testclient import TestClient
from shike_backend.main import app
settings_module._CACHED = None
main_module._ADAPTER = None
response = TestClient(app).post('/v1/analyze', json={
    'input_id': 'real-ocr-course-nine-001',
    'source_type': 'screenshot',
    'ocr_text': '今晚九点上高数，教室是B203',
    'scene_hint': 'course_notice',
    'user_timezone': 'Asia/Shanghai',
})
print(json.dumps(response.json(), ensure_ascii=False))
"""
    )


def v2_text_fallback_payload() -> dict[str, object] | None:
    return run_probe(
        """
import json
import shike_backend.main as main_module
import shike_backend.settings as settings_module
from fastapi.testclient import TestClient
from shike_backend.main import app
settings_module._CACHED = None
main_module._ADAPTER = None
main_module._OCR_ADAPTER = None
main_module._MULTIMODAL_ADAPTER = None
response = TestClient(app).post('/v2/analyze-image', json={
    'input_id': 'real-ocr-image-course-nine-001',
    'source_type': 'screenshot_share',
    'image': {
        'data_url': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB',
        'mime': 'image/png',
        'width': 1080,
        'height': 2400,
        'sha256': 'placeholder-sha256',
    },
    'ocr_text_hint': '今晚九点上高数，教室是B203',
    'ocr_blocks': [
        {'text': '09:50', 'x1': 10, 'y1': 10, 'x2': 88, 'y2': 38, 'confidence': 0.98},
        {'text': '今晚九点上高数，教室是B203', 'x1': 80, 'y1': 640, 'x2': 820, 'y2': 720, 'confidence': 0.92},
    ],
    'allow_cloud_image': False,
    'current_date': '2026-06-09',
    'user_timezone': 'Asia/Shanghai',
    'scene_hint': 'course_notice',
})
print(json.dumps(response.json(), ensure_ascii=False))
"""
    )


def keeps_ocr_evidence(payload: dict[str, object] | None) -> bool:
    if payload is None:
        return False
    serialized = json.dumps(payload, ensure_ascii=False)
    time_payload = payload.get("time")
    location_payload = payload.get("location")
    if not isinstance(time_payload, dict) or not isinstance(location_payload, dict):
        return False
    return (
        "高数" in str(payload.get("title", ""))
        and "今晚九点" in str(time_payload.get("start_text", ""))
        and location_payload.get("raw") == "B203"
        and all(token not in serialized for token in FORBIDDEN_WITHOUT_EVIDENCE)
    )


def main() -> int:
    v1_payload = v1_course_nine_payload()
    v2_payload = v2_text_fallback_payload()
    checks = [
        ("v1_course_ocr_keeps_subject_time_location", keeps_ocr_evidence(v1_payload)),
        ("v2_text_fallback_keeps_ocr_subject_time_location", keeps_ocr_evidence(v2_payload)),
        ("backend_unit_runtime_mode_passes", command_passes(["python3", "-m", "unittest", "backend.tests.test_runtime_mode_no_sample_fallback"])),
    ]
    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"REAL_OCR_ROUTING_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
