#!/usr/bin/env python3
"""Validate screenshot assist mode product and permission boundaries."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def file_exists(relative: str) -> bool:
    return (ROOT / relative).is_file()


def main() -> int:
    observer = read("android-mvp/app/src/main/java/cn/shike/app/system/ScreenshotObserver.kt")
    notification = read("android-mvp/app/src/main/java/cn/shike/app/system/ScreenshotNotification.kt")
    store = read("android-mvp/app/src/main/java/cn/shike/app/data/ScreenshotCandidateStore.kt")
    settings = read("android-mvp/app/src/main/java/cn/shike/app/ui/ReadinessSections.kt")
    app = read("android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt")
    activity = read("android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt")
    main_screen = read("android-mvp/app/src/main/java/cn/shike/app/ui/ShikeMainScreen.kt")
    flow_screens = read("android-mvp/app/src/main/java/cn/shike/app/ui/MainFlowScreens.kt")
    manifest = read("android-mvp/app/src/main/AndroidManifest.xml")
    guide = read("docs/SHIKE_CLOUD_DEVICE_PRODUCT_FIX_GUIDE.md")

    checks = [
        ("observer_file_exists", file_exists("android-mvp/app/src/main/java/cn/shike/app/system/ScreenshotObserver.kt")),
        ("notification_file_exists", file_exists("android-mvp/app/src/main/java/cn/shike/app/system/ScreenshotNotification.kt")),
        ("candidate_store_file_exists", file_exists("android-mvp/app/src/main/java/cn/shike/app/data/ScreenshotCandidateStore.kt")),
        (
            "settings_has_screenshot_assist_switch",
            "截图助手模式" in settings
            and "screenshotAssistEnabled" in app
            and "loadScreenshotAssistEnabled" in activity
            and "saveScreenshotAssistEnabled" in activity
            and "clearScreenshotAssistPreference" in activity
            and "KEY_SCREENSHOT_ASSIST_ENABLED" in store,
        ),
        (
            "manifest_has_media_and_notification_permissions",
            "android.permission.READ_MEDIA_IMAGES" in manifest and "android.permission.POST_NOTIFICATIONS" in manifest,
        ),
        (
            "observer_uses_mediastore_content_observer",
            "ContentObserver" in observer
            and "MediaStore.Images.Media.EXTERNAL_CONTENT_URI" in observer
            and "registerContentObserver" in observer,
        ),
        (
            "screenshot_detection_is_bounded",
            "DATE_ADDED" in observer
            and "SCREENSHOT_ASSIST_LOOKBACK_SECONDS = 30L" in store
            and "nowSeconds - SCREENSHOT_ASSIST_LOOKBACK_SECONDS" in observer
            and "isLikelyScreenshot" in store
            and "displayNameDigest" in store,
        ),
        (
            "screenshot_detection_requires_name_or_path_signal",
            "displayName.contains(token, ignoreCase = true)" in store
            and "path.contains(token, ignoreCase = true)" in store
            and "screenWidth" not in store
            and "screenHeight" not in store
            and "setOf(width, height)" not in store
        ),
        (
            "notification_prompts_user_confirmation",
            "拾刻检测到一张新截图" in notification
            and "是否交给拾刻生成行动卡" in notification
            and "PendingIntent" in notification,
        ),
        (
            "activity_registers_observer_when_enabled",
            "ScreenshotObserver(" in activity
            and ".register()" in activity
            and ".unregister()" in activity
            and "screenshotAssistEnabled" in activity
            and "registerScreenshotObserverIfAllowed()" in activity,
        ),
        (
            "activity_shows_notification_for_detected_candidate",
            "showScreenshotDetectedNotification" in activity
            and "onScreenshotCandidate" in activity,
        ),
        (
            "activity_deduplicates_repeated_candidate_notifications",
            "lastNotifiedScreenshotUri" in activity
            and "shouldNotifyScreenshotCandidate(candidate, lastNotifiedScreenshotUri)" in activity
            and "lastNotifiedScreenshotUri = candidate.contentUri" in activity,
        ),
        (
            "notification_import_intent_is_handled",
            "ACTION_IMPORT_SCREENSHOT" in activity
            and "EXTRA_SCREENSHOT_URI" in activity
            and "EXTRA_SCREENSHOT_WIDTH" in activity + notification
            and "EXTRA_SCREENSHOT_HEIGHT" in activity + notification
            and "EXTRA_SCREENSHOT_CREATED_AT_MILLIS" in activity + notification
            and "EXTRA_SCREENSHOT_DISPLAY_NAME_DIGEST" in activity + notification
            and "screenshotCandidateFromNotificationImport" in activity + store
            and "onNewIntent" in activity,
        ),
        (
            "foreground_candidate_sheet_is_reachable",
            "ScreenshotDetectedSheet" in flow_screens
            and "pendingScreenshotCandidate" in app
            and "onImportScreenshotCandidate" in app
            and "CaptureHubScreen" in main_screen,
        ),
        (
            "no_overlay_or_accessibility_main_path",
            "SYSTEM_ALERT_WINDOW" not in manifest
            and "BIND_ACCESSIBILITY_SERVICE" not in manifest
            and "悬浮窗" in guide,
        ),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"SCREENSHOT_ASSIST_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
