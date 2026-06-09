#!/usr/bin/env python3
"""Validate screenshot cleanup uses system confirmation and never silent delete."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def file_exists(relative: str) -> bool:
    return (ROOT / relative).is_file()


def main() -> int:
    media_cleanup = read("android-mvp/app/src/main/java/cn/shike/app/system/MediaCleanupActions.kt")
    capture = read("android-mvp/app/src/main/java/cn/shike/app/data/CaptureImportMapper.kt")
    prompt = read("android-mvp/app/src/main/java/cn/shike/app/ui/ScreenshotCleanupPrompt.kt")
    settings = read("android-mvp/app/src/main/java/cn/shike/app/ui/ReadinessSections.kt")
    local_data_clear = read("android-mvp/app/src/main/java/cn/shike/app/LocalDataClearActions.kt")
    activity = read("android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt")
    activity_system = read("android-mvp/app/src/main/java/cn/shike/app/MainActivitySystemActions.kt")
    app = read("android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt")
    app_state = read("android-mvp/app/src/main/java/cn/shike/app/ShikeAppState.kt")
    app_actions = read("android-mvp/app/src/main/java/cn/shike/app/ShikeAppActions.kt")
    planner = read("android-mvp/app/src/main/java/cn/shike/app/ui/ActionPlannerPanel.kt")
    main_screen = read("android-mvp/app/src/main/java/cn/shike/app/ui/ShikeMainScreen.kt")
    cleanup_state_test = read("android-mvp/app/src/test/java/cn/shike/app/ShikeAppStateCleanupTest.kt")
    guide = read("docs/SHIKE_CLOUD_DEVICE_PRODUCT_FIX_GUIDE.md")

    checks = [
        ("media_cleanup_file_exists", file_exists("android-mvp/app/src/main/java/cn/shike/app/system/MediaCleanupActions.kt")),
        ("cleanup_prompt_file_exists", file_exists("android-mvp/app/src/main/java/cn/shike/app/ui/ScreenshotCleanupPrompt.kt")),
        (
            "capture_draft_tracks_cleanup_status",
            "enum class ImageCleanupStatus" in capture
            and "sourceMediaStoreUri" in capture
            and "imageCleanupStatus" in capture,
        ),
        (
            "uses_delete_request_not_silent_delete",
            "MediaStore.createDeleteRequest" in media_cleanup
            and "createTrashRequest" not in media_cleanup
            and ".delete(" not in media_cleanup,
        ),
        (
            "system_confirmation_boundary_present",
            "IntentSender" in media_cleanup and "Build.VERSION_CODES.R" in media_cleanup,
        ),
        (
            "cleanup_prompt_requires_user_choice",
            "是否把原图移入系统回收站" in prompt
            and "移入回收站" in prompt
            and "保留原图" in prompt,
        ),
        (
            "cleanup_prompt_uses_user_facing_status_copy",
            "fun cleanupStatusLabel(status: ImageCleanupStatus): String" in prompt
            and "status.name" not in prompt
            and all(
                token in prompt
                for token in [
                    "当前来源不支持直接移入回收站",
                    "等待你的选择",
                    "已选择保留原图",
                    "正在等待系统确认",
                    "已移入系统回收站",
                    "系统确认未完成",
                ]
            ),
        ),
        (
            "settings_has_cleanup_preference",
            "导入后处理原截图" in settings and "每次询问（推荐）" in settings,
        ),
        (
            "settings_separates_cache_clear_from_original_screenshot_delete",
            "清除拾刻缓存" in settings
            and "确认清除" in settings
            and "不会删除系统相册原截图" in settings
            and "LocalDataClearConfirmationState" in local_data_clear
            and "shouldClearLocalData = state.isAwaitingConfirmation" in local_data_clear
            and "MediaStore" not in local_data_clear
            and "createDeleteRequest" not in local_data_clear,
        ),
        (
            "cleanup_prompt_reachable_after_confirmed_action",
            "ScreenshotCleanupPrompt" in planner
            and "onDeleteSourceImage" in planner
            and "onKeepSourceImage" in planner
            and "sourceImageCleanupStatus" in main_screen
            and "selectedSourceMediaStoreUri" in app_state,
        ),
        (
            "cleanup_state_survives_analysis_and_confirmation",
            "private fun ShikeAppState.persistedImageCleanupStatus" in app_state
            and "sourceMediaStoreUri = sourceMediaStoreUri" in app_state
            and "imageCleanupStatus = imageCleanupStatus" in app_state
            and "applyBackendOutcome_preservesSourceImageCleanupState" in cleanup_state_test
            and "updateReviewedItem_preservesSourceImageCleanupStateAfterConfirmation" in cleanup_state_test
            and "ImageCleanupStatus.NOT_REQUESTED" in cleanup_state_test,
        ),
        (
            "delete_request_invoked_by_activity_result",
            "createScreenshotDeleteRequest" in activity_system
            and "StartIntentSenderForResult" in activity
            and "deleteScreenshotLauncher" in activity,
        ),
        (
            "cleanup_status_updates_after_system_confirmation",
            "state.sourceImageCleanupStatus = ImageCleanupStatus.DELETE_REQUESTED" in app_actions
            and "imageCleanupStatusFromSystem" in app
            and "ImageCleanupStatus.DELETED -> state.executionResults.recordExecutionResult" in app_actions
            and "ImageCleanupStatus.FAILED -> state.executionResults.recordExecutionResult" in app_actions
            and "handleImageCleanupStatusFromSystem(ImageCleanupStatus.FAILED)" in activity_system
            and "原截图清理：已移入系统回收站" in activity_system
            and "ImageCleanupStatus.DELETED" in activity
            and "ImageCleanupStatus.FAILED" in activity,
        ),
        (
            "unsupported_source_copy_present",
            "当前来源不支持直接清理原图" in media_cleanup,
        ),
        (
            "guide_keeps_no_silent_delete_boundary",
            "不能偷偷删除用户相册里的图片" in guide and "系统确认" in guide,
        ),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"SCREENSHOT_CLEANUP_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
