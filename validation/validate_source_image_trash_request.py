#!/usr/bin/env python3
"""Validate source screenshots are moved to system trash with confirmation."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    """Read a UTF-8 project file."""

    path = ROOT / relative
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def exists(relative: str) -> bool:
    """Return true when the project-relative file exists."""

    return (ROOT / relative).is_file()


def main() -> int:
    manager = read("android-mvp/app/src/main/java/cn/shike/app/system/SourceImageCleanupManager.kt")
    cleanup = read("android-mvp/app/src/main/java/cn/shike/app/system/MediaCleanupActions.kt")
    activity = read("android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt")
    system_actions = read("android-mvp/app/src/main/java/cn/shike/app/MainActivitySystemActions.kt")
    prompt = read("android-mvp/app/src/main/java/cn/shike/app/ui/ScreenshotCleanupPrompt.kt")
    actions = read("android-mvp/app/src/main/java/cn/shike/app/ShikeAppActions.kt")
    execution = read("android-mvp/app/src/main/java/cn/shike/app/ui/ExecutionResultState.kt")

    combined_cleanup = manager + cleanup

    checks = [
        ("source_image_cleanup_manager_exists", exists("android-mvp/app/src/main/java/cn/shike/app/system/SourceImageCleanupManager.kt")),
        (
            "uses_mediastore_create_trash_request",
            "MediaStore.createTrashRequest" in combined_cleanup
            and "createDeleteRequest" not in combined_cleanup
            and ".delete(" not in combined_cleanup,
        ),
        (
            "trash_request_requires_android_11",
            "Build.VERSION_CODES.R" in combined_cleanup
            and (
                "Build.VERSION.SDK_INT < Build.VERSION_CODES.R" in combined_cleanup
                or "Build.VERSION.SDK_INT >= Build.VERSION_CODES.R" in combined_cleanup
            ),
        ),
        (
            "only_mediastore_content_uri_is_trashable",
            "isMediaStoreUri" in combined_cleanup
            and ("content://media" in combined_cleanup or "MediaStore.AUTHORITY" in combined_cleanup)
            and "NOT_SUPPORTED" in combined_cleanup,
        ),
        (
            "manager_returns_clear_status",
            "sealed class SourceImageCleanupRequest" in manager
            and "SystemTrashConfirmation" in manager
            and "NotSupported" in manager
            and "IntentSender" in manager,
        ),
        (
            "activity_launches_intent_sender_for_result",
            "StartIntentSenderForResult" in activity
            and "deleteScreenshotLauncher" in activity
            and "IntentSenderRequest.Builder" in system_actions,
        ),
        (
            "unsupported_is_not_reported_as_system_failure",
            "ImageCleanupStatus.NOT_SUPPORTED" in system_actions
            and "handleImageCleanupStatusFromSystem(ImageCleanupStatus.FAILED)" not in system_actions,
        ),
        (
            "system_result_maps_to_deleted_or_kept",
            "result.resultCode == RESULT_OK" in activity
            and "ImageCleanupStatus.DELETED" in activity
            and "ImageCleanupStatus.USER_KEPT" in activity,
        ),
        (
            "ui_copy_says_system_trash_confirmation",
            "移入系统回收站" in prompt
            and "系统会弹出确认" in prompt
            and "不会静默删除" in prompt,
        ),
        (
            "execution_results_record_cleanup_outcome",
            "imageCleanupRequestedResult" in actions + execution
            and "imageCleanupDeletedResult" in actions + execution
            and "imageCleanupKeptResult" in actions + execution,
        ),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"SOURCE_IMAGE_TRASH_REQUEST_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
