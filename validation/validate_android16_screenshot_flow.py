#!/usr/bin/env python3
"""Validate Android 16 screenshot, sharing, and inset implementation boundaries."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    """Read a project file as UTF-8.

    Args:
        relative: Path under the Shike root.

    Returns:
        File content, or an empty string when missing.
    """

    path = ROOT / relative
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def file_exists(relative: str) -> bool:
    """Return whether a project file exists."""

    return (ROOT / relative).is_file()


def main() -> int:
    """Run Android 16 flow checks.

    Returns:
        Process exit code.
    """

    build_gradle = read("android-mvp/app/build.gradle.kts")
    manifest = read("android-mvp/app/src/main/AndroidManifest.xml")
    activity = read("android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt")
    main_screen = read("android-mvp/app/src/main/java/cn/shike/app/ui/ShikeMainScreen.kt")
    flow_screens = read("android-mvp/app/src/main/java/cn/shike/app/ui/MainFlowScreens.kt")
    launchers = read("android-mvp/app/src/main/java/cn/shike/app/CaptureLaunchers.kt")
    cleanup = read("android-mvp/app/src/main/java/cn/shike/app/system/MediaCleanupActions.kt")
    callback = read("android-mvp/app/src/main/java/cn/shike/app/system/ScreenCaptureCallbackHelper.kt")
    visible_prompt = read("android-mvp/app/src/main/java/cn/shike/app/system/VisibleScreenCapturePrompt.kt")
    visible_prompt_card = read("android-mvp/app/src/main/java/cn/shike/app/ui/VisibleScreenCapturePromptCard.kt")
    settings = read("android-mvp/app/src/main/java/cn/shike/app/ui/ReadinessSections.kt")
    app = read("android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt")

    checks = [
        ("compile_sdk_36", "compileSdk = 36" in build_gradle),
        ("target_sdk_36", "targetSdk = 36" in build_gradle),
        ("manifest_accepts_image_share", "android.intent.action.SEND" in manifest and 'android:mimeType="image/*"' in manifest),
        ("manifest_declares_screen_capture_permission", "android.permission.DETECT_SCREEN_CAPTURE" in manifest),
        ("activity_uses_edge_to_edge", "enableEdgeToEdge()" in activity),
        ("scaffold_uses_safe_drawing_insets", "WindowInsets.safeDrawing" in main_screen and "contentWindowInsets" in main_screen),
        ("fake_status_row_removed_from_home", "SystemStatusRow()" not in flow_screens),
        ("photo_picker_primary_path", "ActivityResultContracts.PickVisualMedia" in launchers and "PickVisualMedia.ImageOnly" in launchers),
        ("activity_handles_shared_image_uri", "Intent.EXTRA_STREAM" in activity and "consumeSharedImageIntent" in activity),
        (
            "activity_handles_runtime_text_share",
            "pendingSharedText" in activity
            and "sharedTextFrom(intent)" in activity
            and "onNewIntent(intent: Intent)" in activity
            and "pendingSharedText: String?" in app
            and "buildRuntimeSharedTextSelection" in app,
        ),
        ("visible_screen_capture_callback_file", file_exists("android-mvp/app/src/main/java/cn/shike/app/system/ScreenCaptureCallbackHelper.kt")),
        (
            "visible_screen_capture_callback_registered",
            "registerScreenCaptureCallback" in callback
            and "unregisterScreenCaptureCallback" in callback
            and "onStart()" in activity
            and "onStop()" in activity,
        ),
        (
            "callback_is_visible_only_copy",
            "onVisibleScreenCaptured" in callback
            and "Toast" not in callback
            and "后台监听" not in callback
            and "全局监听" not in callback,
        ),
        (
            "visible_callback_page_prompt",
            "visibleScreenCapturePromptState" in activity
            and "visibleScreenCapturePrompt()" in activity
            and "visibleScreenCapturePrompt: VisibleScreenCapturePrompt?" in app
            and "visibleScreenCapturePrompt: VisibleScreenCapturePrompt?" in main_screen
            and "visibleScreenCapturePrompt: VisibleScreenCapturePrompt?" in flow_screens
            and "VisibleScreenCapturePromptCard" in visible_prompt_card + flow_screens,
        ),
        (
            "visible_callback_photo_picker_action",
            "captureLaunchers.launchGallery()" in app
            and "不会直接获得图片" in visible_prompt
            and "导入页选择这张截图" in visible_prompt
            and "移入回收站" in visible_prompt
            and "自动读取" not in visible_prompt,
        ),
        (
            "mediastore_delete_confirmation",
            "MediaStore.createDeleteRequest" in cleanup and "createTrashRequest" not in cleanup,
        ),
        (
            "screenshot_assist_privacy_copy",
            "截图提醒" in settings
            and "不会自动上传" in settings
            and "screenshotAssistEnabled" in app
            and "loadScreenshotAssistEnabled" in activity
            and "saveScreenshotAssistEnabled" in activity
            and "clearScreenshotAssistPreference" in activity,
        ),
        (
            "android_does_not_hold_provider_secret_names",
            "BLUELM_APP_KEY" not in manifest + activity + main_screen + launchers
            and "VIVO_AIGC_APP_KEY" not in manifest + activity + main_screen + launchers,
        ),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"ANDROID16_SCREENSHOT_FLOW_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
