#!/usr/bin/env python3
"""Validate Shike as a real-world demo-ready MVP across all deliverables."""

from __future__ import annotations

import subprocess
from pathlib import Path

from source_tree import read_android_source

WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "shike"
ISSUES = WORKSPACE / "issues/2026-04-24_11-41-14-aigc-shike.csv"


def read(path: Path) -> str:
    """Read a UTF-8 text file.

    Args:
        path: Absolute file path.

    Returns:
        File content.
    """

    return path.read_text(encoding="utf-8")


def command_passes(command: list[str]) -> bool:
    """Run one validation command from the workspace root.

    Args:
        command: Command and arguments.

    Returns:
        True when the command exits with status code 0.
    """

    result = subprocess.run(command, cwd=WORKSPACE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return result.returncode == 0


def main() -> int:
    android_source = read_android_source(ROOT)
    runbook = read(ROOT / "docs/device-runbook.md")
    readme = read(ROOT / "README.md")
    csv = read(ISSUES)

    checks = [
        ("manual_review_checks_pass", command_passes(["python3", "shike/validation/validate_manual_review.py"])),
        ("backend_config_checks_pass", command_passes(["python3", "shike/validation/validate_backend_config.py"])),
        ("demo_acceptance_checks_pass", command_passes(["python3", "shike/validation/validate_demo_acceptance.py"])),
        ("ocr_input_checks_pass", command_passes(["python3", "shike/validation/validate_ocr_input.py"])),
        ("model_bridge_checks_pass", command_passes(["python3", "shike/validation/validate_model_bridge.py"])),
        ("persistence_checks_pass", command_passes(["python3", "shike/validation/validate_persistence.py"])),
        ("action_execution_checks_pass", command_passes(["python3", "shike/validation/validate_action_execution.py"])),
        ("android_unit_tests_check_passes", command_passes(["python3", "shike/validation/validate_android_unit_tests.py"])),
        ("device_demo_checks_pass", command_passes(["python3", "shike/validation/validate_device_demo.py"])),
        ("landable_checks_pass", command_passes(["python3", "shike/validation/validate_landable.py"])),
        ("backend_smoke_passes", command_passes(["python3", "shike/backend/verify_backend.py"])),
        ("deliverables_pass", command_passes(["python3", "shike/validation/validate_deliverables.py"])),
        ("spike_passes", command_passes(["python3", "shike/spike/run_spike.py", "--all"])),
        ("apk_exists", (ROOT / "android-mvp/app/build/outputs/apk/debug/app-debug.apk").is_file()),
        ("runbook_has_device_install", "adb install -r" in runbook and "真机验证路径" in runbook),
        ("runbook_has_backend_and_fallback", "10.0.2.2:8000" in runbook and "回退本地 MockModelAdapter" in runbook),
        ("runbook_has_real_device_backend_config", "保存后端地址" in runbook and "192.168.1.10:8000" in runbook),
        ("demo_checklist_has_recording_evidence", "device-demo-checklist.md" in readme and (ROOT / "materials/device-demo-checklist.md").is_file()),
        ("android_has_confirm_before_execute", "先确认字段；未确认前不会打开外部日历、通知或地图。" in android_source),
        ("android_has_real_inputs_and_actions", all(token in android_source for token in ["GetContent", "TakePicturePreview", "CalendarContract", "NotificationCompat", "geo:"])),
        (
            "readme_has_real_world_commands",
            all(
                token in readme
                for token in [
                    "validate_real_world_ready.py",
                    "可落地总体验收",
                    "validate_android_structure.py",
                    "validate_android_unit_tests.py",
                    "ANDROID_STRUCTURE_METRIC 31/31",
                    "ANDROID_UNIT_TEST_METRIC 64/64",
                ]
            ),
        ),
        ("csv_mentions_all_readiness_metrics", all(token in csv for token in ["落地指标 15/15", "真机演示指标 12/12", "本地恢复指标 12/12", "模型桥接指标 14/14", "OCR 输入指标 12/12", "手动确认指标 12/12"])),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"REAL_WORLD_READY_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
