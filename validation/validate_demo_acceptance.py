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
    extended_scene_tokens = [
        "assignment_deadline",
        "meeting_notice",
        "interview_notice",
        "travel_ticket",
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
        ("course_flow_documented", all(token in checklist for token in ["选择截图", "OCR 文本草稿", "解析当前草稿", "确认并安排", "打开日历"])),
        ("event_flow_documented", all(token in checklist for token in ["拍照导入", "活动样例解析", "设置提醒", "查看路线"])),
        (
            "extended_scene_flow_documented",
            all(token in checklist for token in extended_scene_tokens)
            and all(token in read("materials/demo-script.md") for token in extended_scene_tokens)
            and all(token in submission for token in extended_scene_tokens),
        ),
        ("fallback_flow_documented", all(token in checklist for token in ["后端不可用", "MockModelAdapter", "相机权限拒绝", "已忽略"])),
        ("restart_restore_documented", "SharedPreferences" in checklist and "后端地址" in checklist),
        ("final_acceptance_commands_present", "validate_demo_acceptance.py" in checklist and "validate_real_world_ready.py" in checklist),
        (
            "cloud_strict_handoff_documented",
            all(
                token in checklist
                for token in [
                    "materials/evidence/cloud-device/",
                    "materials/evidence/release-evidence-index.md",
                    "RELEASE_EVIDENCE_INDEX_METRIC 10/10",
                    "docs/optimization-log.md",
                    "README 公开入口",
                    "validation/traceability.md",
                    "SHIKE-070",
                    "DELIVERABLES_METRIC 10/10",
                    "prepare_cloud_device_evidence.py",
                    "CLOUD_DEVICE_PREP_METRIC 5/5",
                    "CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9",
                    "test_collect_cloud_device_evidence.py",
                    "test_preflight_cloud_backend.py",
                    "preflight_cloud_backend.py --base-url https://roky.chat",
                    "collect_cloud_device_evidence.py --preflight-backend --backend-url https://roky.chat",
                    "--allow-cloud-image",
                    "CLOUD_BACKEND_PREFLIGHT_METRIC",
                    "collect_cloud_device_evidence.py --list",
                    "collect_cloud_device_evidence.py --record <1-9>",
                    "collect_cloud_device_evidence.py --capture-logcat --write-report-draft",
                    "validate_cloud_device_package.py",
                    "CLOUD_DEVICE_PACKAGE_METRIC 30/30",
                    "ANDROID16_REAL_IMPLEMENTATION_GUIDE_METRIC 12/12",
                    "RELEASE_HANDOFF_CHECKS_METRIC 24/24",
                    "LIVE_SMOKE_EVIDENCE_METRIC 7/7",
                    "/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md",
                    "materials/evidence/requirement-matrix.md",
                    "REQUIREMENT_MATRIX_METRIC 9/9",
                    "--strict-ready",
                    "validate_requirement_matrix.py",
                    "materials/evidence/blocking-report.md",
                    "Pre-recording Evidence Gate",
                    "all 9 real cloud-device MP4 files",
                    "no placeholder fields remain after capture",
                    "LANDING_RELEASE_CANDIDATE_METRIC 63/63",
                    "LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7",
                    "01-cloud-install-open.mp4",
                    "09-cloud-final-route.mp4",
                    "HTTPS 后端地址",
                    "SHIKE_ANDROID16_REAL_IMPLEMENTATION_GUIDE (1).md",
                    "14.1 无假信息",
                    "14.2 截图分享导入",
                    "系统截图浮层分享合成图片",
                    "14.3 确认后打开日历",
                    "14.4 通知权限与提醒",
                    "14.5 地图",
                    "14.6 删除原截图",
                    "14.7 最近截图助手",
                    "AppKEY",
                    "backend tokens",
                ]
            ),
        ),
        ("submission_references_demo_checklist", "device-demo-checklist.md" in submission or "device-demo-checklist.md" in readme or "device-demo-checklist.md" in runbook),
        (
            "demo_page_checked",
            "拾刻 Demo 控制台" in demo
            and "validate_demo_acceptance.py" in demo
            and "prototype/index.html" in demo
            and "DEMO_ACCEPTANCE_METRIC" in demo
            and "18/18" in demo
            and "/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md" in demo
            and "materials/evidence/requirement-matrix.md" in demo
            and "REQUIREMENT_MATRIX_METRIC 9/9" in demo
            and "LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7" in demo
            and "17/17" not in demo,
        ),
        (
            "demo_page_flows_match_checklist",
            all(token in demo for token in ["解析当前草稿", "活动样例解析", "06-delivery-readiness.mp4"])
            and all(token in demo for token in extended_scene_tokens),
        ),
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
