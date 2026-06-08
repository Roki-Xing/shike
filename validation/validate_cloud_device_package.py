#!/usr/bin/env python3
"""Validate the cloud-device evidence package for Shike.

Default mode checks the package skeleton and redaction surfaces.
Use ``--strict`` after collecting the actual cloud-device recordings.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "shike"
EVIDENCE_ROOT = ROOT / "materials/evidence/cloud-device"

MANIFEST_PATH = EVIDENCE_ROOT / "cloud-device-manifest.md"
REPORT_PATH = EVIDENCE_ROOT / "cloud-device-test-report.md"
LOGCAT_PATH = EVIDENCE_ROOT / "cloud-device-logcat.txt"
ACCESS_LOG_PATH = EVIDENCE_ROOT / "backend-redacted-access-log.txt"
APK_SHA_PATH = EVIDENCE_ROOT / "apk-sha256.txt"
PACKAGE_README_PATH = EVIDENCE_ROOT / "README.md"
CAPTURE_TODO_PATH = EVIDENCE_ROOT / "cloud-device-capture-todo.md"
ROOT_README_PATH = ROOT / "README.md"
CURRENT_STATUS_PATH = ROOT / "docs/current-validation-status.md"
RUNBOOK_PATH = ROOT / "docs/device-runbook.md"
PREP_SCRIPT_PATH = ROOT / "scripts/prepare_cloud_device_evidence.py"
COLLECT_SCRIPT_PATH = ROOT / "scripts/collect_cloud_device_evidence.py"
COLLECT_TEST_PATH = ROOT / "scripts/test_collect_cloud_device_evidence.py"
PREFLIGHT_SCRIPT_PATH = ROOT / "scripts/preflight_cloud_backend.py"
PREFLIGHT_TEST_PATH = ROOT / "scripts/test_preflight_cloud_backend.py"
HANDOFF_SCRIPT_PATH = ROOT / "scripts/run_release_handoff_checks.py"

REQUIRED_VIDEO_NAMES = [
    "01-cloud-install-open.mp4",
    "02-cloud-gallery-bluelm.mp4",
    "03-cloud-camera-bluelm.mp4",
    "04-cloud-share-text.mp4",
    "05-cloud-permission-fallback.mp4",
    "06-cloud-backend-failure.mp4",
    "07-cloud-restart-restore.mp4",
    "08-cloud-ui-polish.mp4",
    "09-cloud-final-route.mp4",
]

REQUIRED_ANDROID16_GUIDE_RECORDING_TOKENS = (
    "## Android 16 Guide Acceptance Coverage",
    "14.1 无假信息",
    "14.2 截图分享导入",
    "14.3 确认后打开日历",
    "14.4 通知权限与提醒",
    "14.5 地图",
    "14.6 删除原截图",
    "14.7 最近截图助手",
    "系统截图浮层分享",
    "04-cloud-share-text.mp4",
    "09-cloud-final-route.mp4",
)

REQUIRED_TEXT_ARTIFACTS = [
    "cloud-device-test-report.md",
    "cloud-device-logcat.txt",
    "backend-redacted-access-log.txt",
    "apk-sha256.txt",
    "cloud-device-capture-todo.md",
    "README.md",
]

REQUIRED_MANIFEST_HANDOFF_TOKENS = (
    "python3 shike/scripts/prepare_cloud_device_evidence.py",
    "CLOUD_DEVICE_PREP_METRIC 5/5",
    "CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9",
    "materials/evidence/release-evidence-index.md",
    "RELEASE_EVIDENCE_INDEX_METRIC 10/10",
    "docs/optimization-log.md",
    "README public entrypoint",
    "/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md",
    "materials/evidence/requirement-matrix.md",
    "REQUIREMENT_MATRIX_METRIC 9/9",
    "Before recording",
    "Pre-recording Evidence Gate",
    "all 9 real cloud-device MP4 files",
    "no placeholder fields remain after capture",
    "must not be treated as release-ready strict evidence",
    "materials/evidence/blocking-report.md",
    "LANDING_RELEASE_CANDIDATE_METRIC 63/63",
    "LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7",
)

REQUIRED_REPORT_FIELDS = ("机型", "Android 版本", "测试时间", "后端地址", "结果")
REQUIRED_REPORT_HANDOFF_TOKENS = (
    "## Pre-recording Evidence Gate",
    "/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md",
    "/mnt/c/Users/Xing/Desktop/SHIKE_ANDROID16_REAL_IMPLEMENTATION_GUIDE (1).md",
    "ANDROID16_REAL_IMPLEMENTATION_GUIDE_METRIC 12/12",
    "ANDROID16_DOD_COVERAGE_METRIC 28/28",
    "materials/evidence/requirement-matrix.md",
    "REQUIREMENT_MATRIX_METRIC 9/9",
    "LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7",
    "9 real cloud-device MP4",
    "no placeholder fields",
    *REQUIRED_ANDROID16_GUIDE_RECORDING_TOKENS,
)
REQUIRED_REPORT_TODO_GATE_TOKENS = (
    "### Report Evidence Gate Fields",
    "Pre-recording Evidence Gate",
    "Desktop guidance source checked",
    "Android 16 real implementation guide checked",
    "Android 16 Definition of Done checked",
    "Requirement matrix checked",
    "Requirement matrix gate",
    "Android 16 guide gate",
    "Android 16 DoD gate",
    "Strict release gate before filling this report",
    "All 9 real cloud-device MP4 files present",
    "No placeholder fields remain after capture",
)
REQUIRED_REPORT_VIDEO_TOKENS = (
    "## Video Evidence",
    *REQUIRED_VIDEO_NAMES,
)
REQUIRED_CAPTURE_TODO_TOKENS = (
    "## Current Missing Evidence",
    "Missing videos:",
    "Report fields still TBD:",
    "Report video evidence still TBD:",
    "### Missing Videos",
    "### Report Fields Still TBD",
    "### Report Video Evidence Still TBD",
    "generated from the current evidence package",
    "## Required Videos",
        "## Android 16 Guide Acceptance Coverage",
        "desktop guide section 14 manual acceptance scripts",
        *REQUIRED_ANDROID16_GUIDE_RECORDING_TOKENS,
        "## Report Fields",
        "### Report Evidence Gate Fields",
    "## Report Video Evidence Section",
    "Add a `## Video Evidence` section",
    "List all 9 MP4 filenames",
    "Replace every video evidence `TBD` note",
    "## Pre-capture Checks",
    "## Release Handoff",
    "python3 shike/scripts/prepare_cloud_device_evidence.py",
    "python3 shike/scripts/collect_cloud_device_evidence.py --list",
    "python3 shike/scripts/collect_cloud_device_evidence.py --record <1-9> --duration-seconds 180",
    "python3 shike/scripts/collect_cloud_device_evidence.py --capture-logcat --write-report-draft --backend-url https://roky.chat",
    "python3 shike/scripts/test_collect_cloud_device_evidence.py",
    "python3 shike/scripts/test_preflight_cloud_backend.py",
    "python3 shike/scripts/preflight_cloud_backend.py --base-url https://roky.chat",
    "python3 shike/scripts/collect_cloud_device_evidence.py --preflight-backend --backend-url https://roky.chat",
    "--allow-cloud-image",
    "CLOUD_BACKEND_PREFLIGHT_METRIC",
    "python3 shike/validation/validate_android16_real_implementation_guide.py",
    "python3 shike/validation/validate_android16_definition_of_done.py",
    "CLOUD_DEVICE_PREP_METRIC 5/5",
    "ANDROID16_REAL_IMPLEMENTATION_GUIDE_METRIC 12/12",
    "ANDROID16_DOD_COVERAGE_METRIC 28/28",
    "CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9",
    "HTTPS backend URL",
    "provider=bluelm",
    "result_schema_valid=true",
    "permission fallback path",
    "backend failure fallback path",
    "restart-restore path",
    "materials/evidence/release-evidence-index.md",
    "RELEASE_EVIDENCE_INDEX_METRIC 10/10",
    "docs/optimization-log.md",
    "README public entrypoint",
    "/mnt/c/Users/Xing/Desktop/SHIKE_ANDROID16_REAL_IMPLEMENTATION_GUIDE (1).md",
    "SHIKE-P0-001 through SHIKE-P1-012",
    "/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md",
    "materials/evidence/requirement-matrix.md",
    "REQUIREMENT_MATRIX_METRIC 9/9",
    "materials/evidence/blocking-report.md",
    "LANDING_RELEASE_CANDIDATE_METRIC 63/63",
    "LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7",
    "All 9 real cloud-device MP4 files present",
    "No placeholder fields remain after capture",
    "validate_cloud_device_package.py",
    "validate_release_evidence_index.py",
    "validate_live_smoke_evidence.py",
    "LIVE_SMOKE_EVIDENCE_METRIC 7/7",
    "run_release_handoff_checks.py",
    "Keep AppKEY",
    "RELEASE_EVIDENCE_INDEX_METRIC 10/10",
    "docs/optimization-log.md",
    "README public entrypoint",
)
SECRET_TOKENS = ("BLUELM_APP_KEY", "AppKEY", "API_KEY", "api_key", "password", "credential", "secret", "token")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def file_nonempty(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def contains_all(text: str, tokens: list[str] | tuple[str, ...]) -> bool:
    return all(token in text for token in tokens)


def commands_in_expected_order(text: str, commands: tuple[str, ...]) -> bool:
    marker = "Before release handoff, also re-run:"
    if marker not in text:
        return False
    section = text.split(marker, 1)[1]
    cursor = -1
    for command in commands:
        index = section.find(command)
        if index <= cursor:
            return False
        cursor = index
    return True


def contains_secret(text: str) -> bool:
    lowered = text.lower()
    if any(token.lower() in lowered for token in SECRET_TOKENS):
        return True
    if re.search(r"\bsk-[A-Za-z0-9]{8,}\b", text):
        return True
    if re.search(r"\b1[3-9]\d{9}\b", text):
        return True
    if re.search(r"[\w.\-]+@[\w.\-]+\.\w+", text):
        return True
    return False


def command_passes(command: list[str]) -> bool:
    """Run a validator command from the workspace root."""

    result = subprocess.run(command, cwd=WORKSPACE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return result.returncode == 0


def has_valid_sha256(text: str) -> bool:
    return re.search(r"\b[a-fA-F0-9]{64}\b", text) is not None


def build_checks(strict: bool) -> list[tuple[str, bool, str]]:
    manifest_text = read(MANIFEST_PATH) if MANIFEST_PATH.is_file() else ""
    report_text = read(REPORT_PATH) if REPORT_PATH.is_file() else ""
    logcat_text = read(LOGCAT_PATH) if LOGCAT_PATH.is_file() else ""
    access_log_text = read(ACCESS_LOG_PATH) if ACCESS_LOG_PATH.is_file() else ""
    apk_sha_text = read(APK_SHA_PATH) if APK_SHA_PATH.is_file() else ""
    capture_todo_text = read(CAPTURE_TODO_PATH) if CAPTURE_TODO_PATH.is_file() else ""
    runbook_text = read(RUNBOOK_PATH) if RUNBOOK_PATH.is_file() else ""
    root_readme_text = read(ROOT_README_PATH) if ROOT_README_PATH.is_file() else ""
    current_status_text = read(CURRENT_STATUS_PATH) if CURRENT_STATUS_PATH.is_file() else ""
    package_readme_text = read(PACKAGE_README_PATH) if PACKAGE_README_PATH.is_file() else ""
    prep_script_text = read(PREP_SCRIPT_PATH) if PREP_SCRIPT_PATH.is_file() else ""
    collect_script_text = read(COLLECT_SCRIPT_PATH) if COLLECT_SCRIPT_PATH.is_file() else ""
    preflight_script_text = read(PREFLIGHT_SCRIPT_PATH) if PREFLIGHT_SCRIPT_PATH.is_file() else ""
    current_status_handoff_commands = (
        "python3 shike/validation/validate_cloud_device_package.py",
        "python3 shike/validation/validate_live_smoke_evidence.py",
        "python3 shike/validation/validate_requirement_matrix.py",
        "python3 shike/validation/validate_release_evidence_index.py",
        "python3 shike/validation/validate_landing_release_candidate.py",
        "python3 shike/validation/validate_release_blocking_report.py",
        "python3 shike/validation/validate_landing_release_candidate.py --strict",
    )

    checks = [
        ("evidence_root_exists", EVIDENCE_ROOT.is_dir(), str(EVIDENCE_ROOT)),
        ("package_readme_exists", file_nonempty(PACKAGE_README_PATH), "README.md"),
        ("manifest_exists", file_nonempty(MANIFEST_PATH), "cloud-device-manifest.md"),
        ("report_exists", file_nonempty(REPORT_PATH), "cloud-device-test-report.md"),
        ("logcat_exists", file_nonempty(LOGCAT_PATH), "cloud-device-logcat.txt"),
        ("access_log_exists", file_nonempty(ACCESS_LOG_PATH), "backend-redacted-access-log.txt"),
        ("apk_sha_exists", file_nonempty(APK_SHA_PATH), "apk-sha256.txt"),
        ("capture_todo_exists", file_nonempty(CAPTURE_TODO_PATH), "cloud-device-capture-todo.md"),
        (
            "prep_script_exists",
            file_nonempty(PREP_SCRIPT_PATH)
            and file_nonempty(COLLECT_SCRIPT_PATH)
            and file_nonempty(COLLECT_TEST_PATH)
            and file_nonempty(PREFLIGHT_SCRIPT_PATH)
            and file_nonempty(PREFLIGHT_TEST_PATH)
            and command_passes(["python3", "shike/scripts/test_collect_cloud_device_evidence.py"]),
            "prep + adb collection + backend preflight scripts",
        ),
        (
            "preflight_script_passes",
            command_passes(["python3", "shike/scripts/test_preflight_cloud_backend.py"])
            and contains_all(
                preflight_script_text,
                (
                    "https://roky.chat",
                    "/health",
                    "/v2/schema",
                    "/v2/analyze-image",
                    "allow_cloud_image",
                    "CLOUD_BACKEND_PREFLIGHT_METRIC",
                    "HOST_REDACTED",
                    "CONFIRMATION_DISABLED_REASON",
                ),
            ),
            "public backend preflight",
        ),
        ("manifest_lists_video_names", contains_all(manifest_text, REQUIRED_VIDEO_NAMES), "video names"),
        ("manifest_lists_text_artifacts", contains_all(manifest_text, REQUIRED_TEXT_ARTIFACTS), "text artifacts"),
        ("manifest_links_release_handoff", contains_all(manifest_text, REQUIRED_MANIFEST_HANDOFF_TOKENS), "release handoff"),
        ("capture_todo_lists_video_names", contains_all(capture_todo_text, REQUIRED_VIDEO_NAMES), "capture todo"),
        (
            "capture_todo_lists_report_fields",
            contains_all(capture_todo_text, REQUIRED_REPORT_FIELDS + REQUIRED_REPORT_TODO_GATE_TOKENS),
            "capture todo report fields + report evidence gate",
        ),
        ("capture_todo_has_precapture_checks", contains_all(capture_todo_text, REQUIRED_CAPTURE_TODO_TOKENS), "capture todo prechecks"),
        ("prep_script_lists_video_names", contains_all(prep_script_text, REQUIRED_VIDEO_NAMES), "prep script"),
        ("prep_script_lists_report_fields", contains_all(prep_script_text, REQUIRED_REPORT_FIELDS), "prep script report fields"),
        (
            "prep_script_keeps_release_handoff_current",
            contains_all(
                prep_script_text + collect_script_text + preflight_script_text,
                (
                    "RELEASE_EVIDENCE_INDEX_METRIC 10/10",
                    "docs/optimization-log.md",
                    "README public entrypoint",
                    "/mnt/c/Users/Xing/Desktop/SHIKE_ANDROID16_REAL_IMPLEMENTATION_GUIDE (1).md",
                    "ANDROID16_REAL_IMPLEMENTATION_GUIDE_METRIC 12/12",
                    "ANDROID16_DOD_COVERAGE_METRIC 28/28",
                    "/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md",
                    "REQUIREMENT_MATRIX_METRIC 9/9",
                    "run_release_handoff_checks.py",
                    "collect_cloud_device_evidence.py",
                    "preflight_cloud_backend.py",
                    "preflight-backend",
                    "build_preflight_commands",
                    "--allow-cloud-image",
                    "CLOUD_BACKEND_PREFLIGHT_METRIC",
                    "REQUIRED_SCENARIOS",
                    "screenrecord",
                    "cloud-device-logcat.txt",
                    "redact_log_text",
                    "write_report_draft",
                    "ANDROID16_GUIDE_RECORDING_COVERAGE",
                ),
            ),
            "prep + collection script release handoff",
        ),
        ("handoff_script_exists", file_nonempty(HANDOFF_SCRIPT_PATH), "scripts/run_release_handoff_checks.py"),
        (
            "handoff_script_lists_release_commands",
            contains_all(
                read(HANDOFF_SCRIPT_PATH) if HANDOFF_SCRIPT_PATH.is_file() else "",
                (
                    "validate_requirement_matrix.py",
                    "validate_release_blocking_report.py",
                    "validate_release_evidence_index.py",
                    "validate_cloud_device_package.py",
                    "validate_android16_real_implementation_guide.py",
                    "validate_image_semantic_cases.py",
                    "validate_landing_release_candidate.py",
                    "validate_secret_hygiene.py",
                    "test_collect_cloud_device_evidence.py",
                    "test_preflight_cloud_backend.py",
                    "--disable-cloud-image",
                    "--strict-ready",
                    "RELEASE_HANDOFF_CHECKS_METRIC",
                ),
            ),
            "release handoff runner",
        ),
        (
            "report_has_required_fields",
            contains_all(report_text, REQUIRED_REPORT_FIELDS + REQUIRED_REPORT_HANDOFF_TOKENS),
            "report fields + pre-recording gate",
        ),
        (
            "access_log_redacted",
            not contains_secret(access_log_text)
            and contains_all(
                access_log_text,
                (
                    "public-live-image-preflight-redacted",
                    "allow_cloud_image=true",
                    "actions_disabled=true",
                    "CLOUD_BACKEND_PREFLIGHT_METRIC=1/1",
                ),
            ),
            "redaction + public live image preflight",
        ),
        ("runbook_has_cloud_sections", contains_all(runbook_text, ("模拟器", "USB 真机", "云真机", "https://your-domain.example.com")), "runbook"),
        (
            "runbook_links_release_handoff_gates",
            contains_all(
                runbook_text,
                (
                    "prepare_cloud_device_evidence.py",
                    "CLOUD_DEVICE_PREP_METRIC 5/5",
                    "CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9",
                    "CLOUD_DEVICE_PACKAGE_METRIC 30/30",
                    "RELEASE_EVIDENCE_INDEX_METRIC 10/10",
                    "/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md",
                    "materials/evidence/requirement-matrix.md",
                    "REQUIREMENT_MATRIX_METRIC 9/9",
                    "docs/optimization-log.md",
                    "release handoff",
                    "validate_release_evidence_index.py",
                    "validate_live_smoke_evidence.py",
                    "validate_cloud_device_package.py --strict",
                    "LIVE_SMOKE_EVIDENCE_METRIC 7/7",
                    "9 个真实云真机 MP4",
                    "cloud-device-test-report.md",
                ),
            ),
            "runbook release handoff",
        ),
        (
            "root_readme_mentions_cloud_package",
            contains_all(
                root_readme_text,
                (
                    "validate_cloud_device_package.py",
                    "materials/evidence/cloud-device/",
                    "CLOUD_DEVICE_PACKAGE_METRIC 30/30",
                    "materials/evidence/release-evidence-index.md",
                    "materials/evidence/blocking-report.md",
                    "LANDING_RELEASE_CANDIDATE_METRIC 63/63",
                    "LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7",
                    "/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md",
                    "materials/evidence/requirement-matrix.md",
                    "REQUIREMENT_MATRIX_METRIC 9/9",
                ),
            ),
            "README",
        ),
        (
            "current_status_mentions_cloud_package_handoff",
            contains_all(
                current_status_text,
                (
                    "validate_cloud_device_package.py",
                    "CLOUD_DEVICE_PACKAGE_METRIC 30/30",
                    "validate_release_blocking_report.py",
                    "RELEASE_BLOCKING_REPORT_METRIC 8/8",
                    "validate_release_evidence_index.py",
                    "RELEASE_EVIDENCE_INDEX_METRIC 10/10",
                    "validate_live_smoke_evidence.py",
                    "LIVE_SMOKE_EVIDENCE_METRIC 7/7",
                    "prepare_cloud_device_evidence.py",
                    "CLOUD_DEVICE_PREP_METRIC 5/5",
                    "CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9",
                    "REQUIREMENT_MATRIX_METRIC 9/9",
                    "LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7",
                    "Before release handoff, also re-run:",
                    "30-item non-strict handoff gate",
                    "dependency-safe handoff order",
                    "validate_landing_release_candidate.py --strict",
                ),
            ),
            "docs/current-validation-status.md",
        ),
        (
            "current_status_orders_release_handoff",
            commands_in_expected_order(current_status_text, current_status_handoff_commands),
            "dependency-safe handoff order",
        ),
        (
            "package_readme_mentions_prep_and_strict_mode",
            "prepare_cloud_device_evidence.py" in package_readme_text
            and "collect_cloud_device_evidence.py --list" in package_readme_text
            and "collect_cloud_device_evidence.py --preflight-backend --backend-url https://roky.chat" in package_readme_text
            and "validate_live_smoke_evidence.py" in package_readme_text
            and "LIVE_SMOKE_EVIDENCE_METRIC 7/7" in package_readme_text
            and "collect_cloud_device_evidence.py --record 1" in package_readme_text
            and "preflight_cloud_backend.py --base-url https://roky.chat" in package_readme_text
            and "--allow-cloud-image" in package_readme_text
            and "allow_cloud_image=true" in package_readme_text
            and "CLOUD_BACKEND_PREFLIGHT_METRIC" in package_readme_text
            and "test_collect_cloud_device_evidence.py" in package_readme_text
            and "test_preflight_cloud_backend.py" in package_readme_text
            and "CLOUD_DEVICE_PREP_METRIC 5/5" in package_readme_text
            and "CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9" in package_readme_text
            and "--strict" in package_readme_text
            and "cloud-device-test-report.md" in package_readme_text,
            "package README",
        ),
        (
            "package_readme_links_release_handoff",
            contains_all(
                package_readme_text,
                (
                    "materials/evidence/release-evidence-index.md",
                    "materials/evidence/blocking-report.md",
                    "CLOUD_DEVICE_PACKAGE_METRIC 30/30",
                    "RELEASE_EVIDENCE_INDEX_METRIC 10/10",
                    "LIVE_SMOKE_EVIDENCE_METRIC 7/7",
                    "docs/optimization-log.md",
                    "README public entrypoint",
                    "/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md",
                    "materials/evidence/requirement-matrix.md",
                    "REQUIREMENT_MATRIX_METRIC 9/9",
                    "Pre-recording Evidence Gate",
                    "all 9 real cloud-device MP4 files",
                    "no placeholder fields remain after capture",
                    "LANDING_RELEASE_CANDIDATE_METRIC 63/63",
                    "LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7",
                    "AppKEY",
                    "backend tokens",
                    "full OCR text",
                    "Android 16 Guide Acceptance Coverage",
                    "14.2 截图分享导入",
                ),
            ),
            "package README release handoff",
        ),
    ]

    if strict:
        checks.extend(
            [
                (
                    "strict_video_files_present",
                    all(file_nonempty(EVIDENCE_ROOT / name) for name in REQUIRED_VIDEO_NAMES),
                    "video files",
                ),
                ("strict_report_filled", not any(marker in report_text for marker in ("TBD", "待补录", "待采集", "TODO")), "report filled"),
                (
                    "strict_report_lists_video_evidence",
                    contains_all(report_text, REQUIRED_REPORT_VIDEO_TOKENS),
                    "report video evidence",
                ),
                ("strict_text_artifacts_redacted", not any(contains_secret(text) for text in (report_text, logcat_text, access_log_text)), "report/log redaction"),
                ("strict_logcat_not_placeholder", "placeholder" not in logcat_text.lower(), "logcat content"),
                ("strict_apk_sha_valid", has_valid_sha256(apk_sha_text), "apk sha256"),
            ]
        )

    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the Shike cloud-device evidence package.")
    parser.add_argument("--strict", action="store_true", help="Require the actual cloud-device videos and filled report fields.")
    args = parser.parse_args()

    checks = build_checks(args.strict)
    passed = sum(1 for _, ok, _ in checks if ok)

    for name, ok, evidence in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}\t{evidence}")

    print(f"CLOUD_DEVICE_PACKAGE_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
