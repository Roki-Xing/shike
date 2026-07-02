#!/usr/bin/env python3
"""Validate screenshot assist uses a high-priority notification entry."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    """Read a UTF-8 project file.

    Args:
        relative: Project-relative path.

    Returns:
        File content, or an empty string when missing.
    """

    path = ROOT / relative
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def exists(relative: str) -> bool:
    """Check whether a project-relative file exists."""

    return (ROOT / relative).is_file()


def main() -> int:
    notification = read("android-mvp/app/src/main/java/cn/shike/app/system/ScreenshotNotification.kt")
    service = read("android-mvp/app/src/main/java/cn/shike/app/system/ScreenshotAssistService.kt")
    controller = read("android-mvp/app/src/main/java/cn/shike/app/ScreenshotAssistController.kt")
    activity = read("android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt")
    lifecycle = read("android-mvp/app/src/main/java/cn/shike/app/MainActivityLifecycleActions.kt")
    content = read("android-mvp/app/src/main/java/cn/shike/app/MainActivityContent.kt")
    intents = read("android-mvp/app/src/main/java/cn/shike/app/ActivityImportIntents.kt")
    app = read("android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt")
    actions = read("android-mvp/app/src/main/java/cn/shike/app/ShikeAppActions.kt")
    main_screen = read("android-mvp/app/src/main/java/cn/shike/app/ui/ShikeMainScreen.kt")
    routes = read("android-mvp/app/src/main/java/cn/shike/app/ui/MainScreenRoutes.kt")
    manifest = read("android-mvp/app/src/main/AndroidManifest.xml")

    checks = [
        ("notification_file_exists", exists("android-mvp/app/src/main/java/cn/shike/app/system/ScreenshotNotification.kt")),
        (
            "channel_is_high_importance",
            "NotificationManager.IMPORTANCE_HIGH" in notification
            and "SCREENSHOT_ASSIST_CHANNEL_ID" in notification
            and "拾刻截图助手" in notification,
        ),
        (
            "detected_notification_has_user_actions",
            "发现新截图" in notification
            and "要生成一张行动卡吗？" in notification
            and "交给拾刻" in notification
            and "忽略" in notification
            and "ACTION_IMPORT_SCREENSHOT" in notification
            and "ACTION_IGNORE_SCREENSHOT" in notification
            and "PendingIntent.getActivity" in notification
            and "PendingIntent.getBroadcast" in notification,
        ),
        (
            "notification_payload_preserves_media_uri",
            "EXTRA_SCREENSHOT_URI" in notification + intents
            and "candidate.contentUri" in notification
            and "screenshotCandidateFromNotificationImport" in intents
            and "sourceLabel = SCREENSHOT_ASSIST_IMPORT_SOURCE_LABEL" in read(
                "android-mvp/app/src/main/java/cn/shike/app/data/ScreenshotCandidateStore.kt"
            ),
        ),
        (
            "foreground_service_observes_mediastore",
            "class ScreenshotAssistService : Service()" in service
            and "startForeground(" in service
            and "START_NOT_STICKY" in service
            and "ScreenshotObserver(contentResolver" in service
            and "showScreenshotDetectedNotification(this, candidate)" in service,
        ),
        (
            "foreground_service_copy_is_user_facing",
            "拾刻截图提醒运行中" in service
            and "只在本机检测新截图，不会自动上传图片" in service
            and "Service is running" not in service + notification
            and "observer" not in notification.lower(),
        ),
        (
            "onboarding_requests_media_then_notification_permissions",
            "enableScreenshotAssistFromOnboarding" in lifecycle
            and "updateScreenshotAssistEnabled(true)" in lifecycle
            and "Manifest.permission.READ_MEDIA_IMAGES" in controller
            and "Manifest.permission.POST_NOTIFICATIONS" in controller
            and "requestNotificationPermissionIfNeeded()" in lifecycle + controller,
        ),
        (
            "permission_success_starts_service",
            "handleScreenshotMediaPermissionResult" in lifecycle
            and "startScreenshotAssistService(this)" in lifecycle
            and "registerScreenshotObserverIfAllowed()" in lifecycle,
        ),
        (
            "notification_intent_consumed_by_activity",
            "consumeScreenshotImportIntent(intent)" in activity
            and "onNewIntent" in activity
            and "pendingScreenshotCandidate" in activity + content + app,
        ),
        (
            "notification_handoff_directs_to_import_flow",
            "onImportScreenshotCandidate(candidate)" in main_screen
            and "selectedSection = ShikeMainSection.Import" in main_screen
            and "actions::applyScreenshotCandidate" in app
            and "state.applyScreenshotCandidate(candidate" in actions
            and "analyzeCurrentDraftWithBackend()" in actions
            and "ImportRouteStage.Analyzing" in routes,
        ),
        (
            "no_overlay_permission_in_main_path",
            "SYSTEM_ALERT_WINDOW" not in manifest
            and "BIND_ACCESSIBILITY_SERVICE" not in manifest,
        ),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"SCREENSHOT_ASSIST_NOTIFICATION_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
