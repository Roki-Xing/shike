#!/usr/bin/env python3
"""Validate cloud/release provider fallback cannot return fixed mock samples."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
FORBIDDEN = ("18:30", "22:00", "第5章", "教室变更")


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def probe(runtime_mode: str, provider: str) -> dict[str, object] | None:
    script = """
import json
import shike_backend.main as main_module
import shike_backend.settings as settings_module
from fastapi.testclient import TestClient
from shike_backend.main import app
settings_module._CACHED = None
main_module._ADAPTER = None
response = TestClient(app).post('/v1/analyze', json={
    'input_id': 'provider-fallback-course-nine-001',
    'source_type': 'screenshot',
    'ocr_text': '今晚九点上高数，教室是B203',
    'scene_hint': 'course_notice',
    'user_timezone': 'Asia/Shanghai',
})
print(json.dumps(response.json(), ensure_ascii=False))
"""
    env = {
        **os.environ,
        "PYTHONPATH": str(ROOT / "backend"),
        "SHIKE_BACKEND_ENV_FILE": "/dev/null",
        "SHIKE_RUNTIME_MODE": runtime_mode,
        "SHIKE_MODEL_PROVIDER": provider,
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


def safe_provider_payload(payload: dict[str, object] | None) -> bool:
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
        and all(token not in serialized for token in FORBIDDEN)
    )


def main() -> int:
    settings_source = read("backend/shike_backend/settings.py")
    main_source = read("backend/shike_backend/main.py")
    mock_source = read("backend/shike_backend/adapters/mock_adapter.py")
    checks = [
        ("settings_declares_runtime_mode", "runtime_mode" in settings_source and "SHIKE_RUNTIME_MODE" in settings_source),
        ("runtime_modes_include_cloud_release_demo", all(token in settings_source for token in ["cloud_device_test", "release_user", "demo_mode"])),
        ("main_gates_demo_samples", "allows_demo_samples" in main_source and "MockModelAdapter(allow_demo_samples=" in main_source),
        ("mock_adapter_supports_evidence_only_mode", "allow_demo_samples" in mock_source and "evidence_only" in mock_source),
        ("cloud_device_deepseek_failure_safe", safe_provider_payload(probe("cloud_device_test", "deepseek"))),
        ("release_bluelm_failure_safe", safe_provider_payload(probe("release_user", "bluelm"))),
    ]
    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"PROVIDER_NOT_MOCK_IN_CLOUD_MODE_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
