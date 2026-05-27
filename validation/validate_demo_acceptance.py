#!/usr/bin/env python3
"""Validate the repeatable device demo acceptance package."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    """Read a UTF-8 text file under `shike`.

    Args:
        relative: File path under `shike`.

    Returns:
        File content.
    """

    return (ROOT / relative).read_text(encoding="utf-8")


def main() -> int:
    checklist = read("materials/device-demo-checklist.md")
    submission = read("materials/submission-checklist.md")
    readme = read("README.md")
    runbook = read("docs/device-runbook.md")
    demo = read("prototype/demo.html")
    evidence_files = [
        "01-install-and-open.mp4",
        "02-course-gallery-backend.mp4",
        "03-event-camera-actions.mp4",
        "04-fallback-offline.mp4",
        "05-restart-restore.mp4",
        "06-delivery-readiness.mp4",
    ]
    workspace_commands = [
        "python3 shike/validation/validate_android_structure.py",
        "python3 shike/validation/validate_android_unit_tests.py",
        "python3 shike/validation/validate_action_execution.py",
        "python3 shike/validation/validate_demo_acceptance.py",
        "python3 shike/validation/validate_real_world_ready.py",
        "python3 shike/scripts/verify_core20_package.py",
    ]

    checks = [
        ("device_demo_checklist_exists", (ROOT / "materials/device-demo-checklist.md").is_file()),
        ("preparation_commands_present", "build_apk.sh" in checklist and "validate_real_world_ready.py" in checklist and "backend_passed" in checklist),
        ("adb_install_documented", "adb install -r" in checklist),
        ("evidence_directory_documented", "shike/materials/evidence/" in checklist),
        ("recording_files_named", all(name in checklist for name in evidence_files)),
        ("course_flow_documented", all(token in checklist for token in ["选择截图", "OCR 文本草稿", "后端解析课程", "确认修正", "加日历"])),
        ("event_flow_documented", all(token in checklist for token in ["拍照导入", "后端解析活动", "提醒", "地图"])),
        ("fallback_flow_documented", all(token in checklist for token in ["后端不可用", "MockModelAdapter", "相机权限拒绝", "已忽略"])),
        ("restart_restore_documented", "SharedPreferences" in checklist and "后端地址" in checklist),
        ("final_acceptance_commands_present", "validate_demo_acceptance.py" in checklist and "validate_real_world_ready.py" in checklist),
        ("submission_references_demo_checklist", "device-demo-checklist.md" in submission or "device-demo-checklist.md" in readme or "device-demo-checklist.md" in runbook),
        ("demo_page_checked", "拾刻 Demo 控制台" in demo and "validate_demo_acceptance.py" in demo and "prototype/index.html" in demo),
        ("demo_page_flows_match_checklist", all(token in demo for token in ["后端解析课程", "后端解析活动", "06-delivery-readiness.mp4"])),
        ("android_structure_guard_listed", all(token in checklist and token in readme and token in demo for token in ["validate_android_structure.py", "ANDROID_STRUCTURE_METRIC"])),
        ("workspace_command_style_consistent", all(command in checklist and command in readme and command in demo for command in workspace_commands)),
        ("six_recordings_documented_in_readme", "六段证据文件" in readme),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"DEMO_ACCEPTANCE_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
