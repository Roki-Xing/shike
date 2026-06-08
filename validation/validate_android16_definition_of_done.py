#!/usr/bin/env python3
"""Validate Android 16 guide Definition of Done coverage.

This gate maps section 19 of the desktop Android 16 guide to executable
evidence. It keeps strict cloud-device evidence honest: local readiness passes
only when missing MP4/report/logcat proof is explicitly tracked as a blocker.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent


@dataclass(frozen=True)
class Check:
    """One Definition of Done validation result."""

    name: str
    ok: bool
    evidence: str


_COMMAND_CACHE: dict[tuple[str, ...], bool] = {}


def read(relative: str) -> str:
    """Read a UTF-8 project file.

    Args:
        relative: File path under the Shike root.

    Returns:
        File content, or an empty string when absent.
    """

    path = ROOT / relative
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def command_passes(command: tuple[str, ...]) -> bool:
    """Run a validation command from the workspace root.

    Args:
        command: Command and arguments.

    Returns:
        True when the command exits successfully.
    """

    if command not in _COMMAND_CACHE:
        result = subprocess.run(
            command,
            cwd=WORKSPACE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        _COMMAND_CACHE[command] = result.returncode == 0
    return _COMMAND_CACHE[command]


def contains_all(text: str, tokens: tuple[str, ...]) -> bool:
    """Return whether every token appears in the text."""

    return all(token in text for token in tokens)


def has_valid_sha256(text: str) -> bool:
    """Return whether text contains a SHA-256 hex digest."""

    return re.search(r"\b[a-fA-F0-9]{64}\b", text) is not None


def main() -> int:
    """Run the Android 16 Definition of Done coverage gate."""

    command_ok = {
        "no_fake_device_chrome": command_passes(("python3", "shike/validation/validate_no_fake_device_chrome.py")),
        "android16_screenshot_flow": command_passes(
            ("python3", "shike/validation/validate_android16_screenshot_flow.py")
        ),
        "no_default_image_upload": command_passes(
            ("python3", "shike/validation/validate_no_default_image_upload.py")
        ),
        "vivo_multimodal_contract": command_passes(
            ("python3", "shike/validation/validate_vivo_multimodal_contract.py")
        ),
        "android_image_preprocess": command_passes(
            ("python3", "shike/validation/validate_android_image_preprocess.py")
        ),
        "image_semantic_cases": command_passes(("python3", "shike/validation/validate_image_semantic_cases.py")),
        "action_execution": command_passes(("python3", "shike/validation/validate_action_execution.py")),
        "screenshot_cleanup": command_passes(("python3", "shike/validation/validate_screenshot_cleanup.py")),
        "inbox_workbench": command_passes(("python3", "shike/validation/validate_inbox_workbench_landing.py")),
        "persistence": command_passes(("python3", "shike/validation/validate_persistence.py")),
        "home_one_screen": command_passes(("python3", "shike/validation/validate_home_one_screen.py")),
        "no_sample_contamination": command_passes(
            ("python3", "shike/validation/validate_no_sample_contamination.py")
        ),
        "secret_hygiene": command_passes(("python3", "shike/validation/validate_secret_hygiene.py")),
        "apk_secret_hygiene": command_passes(("python3", "shike/validation/validate_apk_secret_hygiene.py")),
        "backend_audit_log": command_passes(("python3", "shike/validation/validate_backend_audit_log.py")),
        "cloud_device_package": command_passes(("python3", "shike/validation/validate_cloud_device_package.py")),
        "release_blocking_report": command_passes(
            ("python3", "shike/validation/validate_release_blocking_report.py")
        ),
    }

    guide = read("docs/optimization-log.md") + "\n" + read("materials/evidence/release-evidence-index.md")
    launchers = read("android-mvp/app/src/main/java/cn/shike/app/CaptureLaunchers.kt")
    capture_mapper = read("android-mvp/app/src/main/java/cn/shike/app/data/CaptureImportMapper.kt")
    parse_confirm = read("android-mvp/app/src/main/java/cn/shike/app/ui/ParseConfirmPanel.kt")
    review_actions = read("android-mvp/app/src/main/java/cn/shike/app/ui/ReviewDecisionActions.kt")
    inbox_entities = read("android-mvp/app/src/main/java/cn/shike/app/data/InboxEntities.kt")
    inbox_workbench = read("android-mvp/app/src/main/java/cn/shike/app/ui/InboxWorkbench.kt")
    execution_result = read("android-mvp/app/src/main/java/cn/shike/app/ui/ExecutionResult.kt")
    backend_log = read("materials/evidence/cloud-device/backend-redacted-access-log.txt")
    cloud_logcat = read("materials/evidence/cloud-device/cloud-device-logcat.txt")
    blocking_report = read("materials/evidence/blocking-report.md")
    capture_todo = read("materials/evidence/cloud-device/cloud-device-capture-todo.md")
    cloud_report = read("materials/evidence/cloud-device/cloud-device-test-report.md")
    apk_sha = read("materials/evidence/cloud-device/apk-sha256.txt")
    device_checklist = read("materials/device-demo-checklist.md")

    strict_blockers_explicit = (
        "strict_cloud_videos_present" in blocking_report
        and "strict_report_has_no_tbd" in blocking_report
        and "cloud-device-logcat.txt" in blocking_report
        and "LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE" in blocking_report
        and "No placeholder fields remain after capture" in capture_todo
    )
    redacted_backend_log_ok = (
        contains_all(backend_log, ("provider=bluelm", "result_schema_valid=true"))
        and all(token not in backend_log for token in ("sk-", "Authorization", "data:image", "base64,"))
    )
    failure_downgrade_video_plan_ok = contains_all(
        device_checklist + "\n" + capture_todo,
        (
            "05-cloud-permission-fallback.mp4",
            "06-cloud-backend-failure.mp4",
            "09-cloud-final-route.mp4",
            "后端失败",
        ),
    )

    checks = [
        Check(
            "function_dod_no_fake_device_chrome",
            command_ok["no_fake_device_chrome"] and command_ok["android16_screenshot_flow"],
            "no fake status bar, battery, or fixed date",
        ),
        Check(
            "function_dod_screenshot_share_image_import",
            command_ok["android16_screenshot_flow"],
            "image/* ACTION_SEND plus shared-image candidate import",
        ),
        Check(
            "function_dod_photo_picker_import",
            command_ok["android16_screenshot_flow"],
            "Photo Picker image-only import path",
        ),
        Check(
            "function_dod_camera_import",
            contains_all(launchers, ("ActivityResultContracts.TakePicturePreview", "hasCameraPermission"))
            and "Camera" in capture_mapper,
            "camera preview CaptureDraft path",
        ),
        Check(
            "function_dod_backend_image_understanding",
            command_ok["vivo_multimodal_contract"],
            "/v2/analyze-image sends image payload, not OCR text only",
        ),
        Check(
            "function_dod_ocr_blocks_filtering",
            command_ok["vivo_multimodal_contract"] and command_ok["android_image_preprocess"],
            "OCR block enrichment plus status/nav filtering",
        ),
        Check(
            "function_dod_status_bar_time_not_task_time",
            command_ok["image_semantic_cases"],
            "negative/status-region cases forbid status-bar extraction",
        ),
        Check(
            "function_dod_editable_review_fields",
            contains_all(
                parse_confirm + review_actions,
                ("draftTitle", "draftTime", "draftLocation", "OutlinedTextField", "onValueChange"),
            ),
            "editable title/time/location review fields",
        ),
        Check(
            "function_dod_confirm_before_actions",
            command_ok["action_execution"],
            "calendar/reminder/map require confirmed fields",
        ),
        Check(
            "function_dod_calendar_opens_system_insert",
            command_ok["action_execution"],
            "system calendar insert page, user saves in Calendar",
        ),
        Check(
            "function_dod_notification_reminder_schedules",
            command_ok["action_execution"],
            "POST_NOTIFICATIONS fallback and AlarmManager scheduling",
        ),
        Check(
            "function_dod_map_opens_or_copies",
            command_ok["action_execution"],
            "map deeplink with clipboard fallback",
        ),
        Check(
            "function_dod_system_confirmed_screenshot_delete",
            command_ok["screenshot_cleanup"],
            "MediaStore system confirmation, no silent delete",
        ),
        Check(
            "function_dod_cache_clear_separate_from_original_delete",
            command_ok["screenshot_cleanup"],
            "cache clear and original screenshot deletion are distinct",
        ),
        Check(
            "function_dod_inbox_tracks_execution_delete_archive",
            command_ok["inbox_workbench"]
            and command_ok["persistence"]
            and contains_all(inbox_entities + inbox_workbench, ("ExecutionResultEntity", "archived", "archive"))
            and contains_all(capture_mapper + execution_result, ("deleteState", "ImageCleanupStatus", "原截图")),
            "inbox persistence plus current-card execution/delete/archive state",
        ),
        Check(
            "function_dod_debug_mock_samples_hidden_from_main_path",
            command_ok["home_one_screen"] and command_ok["no_sample_contamination"],
            "debug/sample controls stay out of the primary path",
        ),
        Check(
            "evidence_dod_logcat_strict_blocker_tracked",
            command_ok["cloud_device_package"]
            and strict_blockers_explicit
            and "placeholder" in cloud_logcat.lower()
            and "strict_logcat_not_placeholder" in blocking_report,
            "redacted logcat is required and currently tracked as strict blocker",
        ),
        Check(
            "evidence_dod_backend_redacted_access_log",
            redacted_backend_log_ok,
            "backend-redacted-access-log.txt has provider/schema proof without secrets",
        ),
        Check(
            "evidence_dod_android16_cloud_recordings_blocked",
            strict_blockers_explicit and "9 real cloud-device MP4 files" in cloud_report,
            "Android 16 cloud recordings remain explicit strict external evidence",
        ),
        Check(
            "evidence_dod_apk_sha256",
            has_valid_sha256(apk_sha),
            "cloud-device APK SHA-256 present",
        ),
        Check(
            "evidence_dod_validation_scripts_listed",
            "RELEASE_HANDOFF_CHECKS_METRIC" in guide
            and "validate_android16_real_implementation_guide.py" in guide
            and "validate_image_semantic_cases.py" in guide,
            "validation script outputs are release evidence",
        ),
        Check(
            "evidence_dod_failure_downgrade_recording_plan",
            failure_downgrade_video_plan_ok,
            "permission/backend/map fallback capture plan is explicit",
        ),
        Check(
            "safety_dod_git_has_no_appkey",
            command_ok["secret_hygiene"],
            "repository secret hygiene gate",
        ),
        Check(
            "safety_dod_apk_has_no_appkey",
            command_ok["apk_secret_hygiene"],
            "APK secret hygiene gate",
        ),
        Check(
            "safety_dod_logs_have_no_appkey",
            command_ok["backend_audit_log"] and redacted_backend_log_ok,
            "metadata-only audit logs and redacted live evidence",
        ),
        Check(
            "safety_dod_no_default_background_image_upload",
            command_ok["no_default_image_upload"],
            "image upload only after explicit user analyze action",
        ),
        Check(
            "safety_dod_original_image_delete_needs_system_confirmation",
            command_ok["screenshot_cleanup"],
            "MediaStore delete confirmation required",
        ),
        Check(
            "safety_dod_no_action_before_user_confirmation",
            command_ok["action_execution"] and command_ok["vivo_multimodal_contract"],
            "backend and Android both keep actions disabled before user confirmation",
        ),
    ]

    passed = sum(1 for check in checks if check.ok)
    for check in checks:
        print(f"{'PASS' if check.ok else 'FAIL'}\t{check.name}\t{check.evidence}")
    print(f"ANDROID16_DOD_COVERAGE_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
