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
    service = read("android-mvp/app/src/main/java/cn/shike/app/system/ScreenshotAssistService.kt")
    controller = read("android-mvp/app/src/main/java/cn/shike/app/ScreenshotAssistController.kt")
    lifecycle = read("android-mvp/app/src/main/java/cn/shike/app/MainActivityLifecycleActions.kt")
    intents = read("android-mvp/app/src/main/java/cn/shike/app/ActivityImportIntents.kt")
    content = read("android-mvp/app/src/main/java/cn/shike/app/MainActivityContent.kt")
    store = read("android-mvp/app/src/main/java/cn/shike/app/data/ScreenshotCandidateStore.kt")
    settings = read("android-mvp/app/src/main/java/cn/shike/app/ui/ReadinessSections.kt")
    app = read("android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt")
    activity = read("android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt")
    main_screen = read("android-mvp/app/src/main/java/cn/shike/app/ui/ShikeMainScreen.kt")
    main_routes = read("android-mvp/app/src/main/java/cn/shike/app/ui/MainScreenRoutes.kt")
    flow_screens = read("android-mvp/app/src/main/java/cn/shike/app/ui/MainFlowScreens.kt")
    manifest = read("android-mvp/app/src/main/AndroidManifest.xml")
    guide = read("docs/SHIKE_CLOUD_DEVICE_PRODUCT_FIX_GUIDE.md")

    checks = [
        ("observer_file_exists", file_exists("android-mvp/app/src/main/java/cn/shike/app/system/ScreenshotObserver.kt")),
        ("notification_file_exists", file_exists("android-mvp/app/src/main/java/cn/shike/app/system/ScreenshotNotification.kt")),
        ("foreground_service_file_exists", file_exists("android-mvp/app/src/main/java/cn/shike/app/system/ScreenshotAssistService.kt")),
        ("candidate_store_file_exists", file_exists("android-mvp/app/src/main/java/cn/shike/app/data/ScreenshotCandidateStore.kt")),
        (
            "settings_has_screenshot_assist_switch",
            "截图助手" in settings
            and "screenshotAssistEnabled" in app
            and "loadScreenshotAssistEnabled" in activity
            and "saveScreenshotAssistEnabled" in controller
            and "clearScreenshotAssistPreference" in lifecycle
            and "KEY_SCREENSHOT_ASSIST_ENABLED" in store,
        ),
        (
            "manifest_has_media_and_notification_permissions",
            "android.permission.READ_MEDIA_IMAGES" in manifest
            and "android.permission.POST_NOTIFICATIONS" in manifest
            and "android.permission.FOREGROUND_SERVICE" in manifest,
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
            "检测到截图，是否交给拾刻？" in notification
            and "生成可确认的行动卡" in notification
            and "PendingIntent" in notification,
        ),
        (
            "foreground_service_observes_screenshots_after_permission",
            "class ScreenshotAssistService : Service()" in service
            and "startForeground" in service
            and "ScreenshotObserver(contentResolver" in service
            and "showScreenshotDetectedNotification(this, candidate)" in service
            and "startScreenshotAssistService" in controller + lifecycle
            and "canPostScreenshotAssistNotification(activity)" in controller
            and 'android:name=".system.ScreenshotAssistService"' in manifest,
        ),
        (
            "activity_registers_observer_when_enabled",
            "ScreenshotObserver(" in controller
            and ".register()" in controller
            and ".unregister()" in controller
            and "screenshotAssistEnabled" in activity + controller
            and "registerScreenshotObserverIfAllowed()" in activity + lifecycle,
        ),
        (
            "activity_shows_notification_for_detected_candidate",
            "showScreenshotDetectedNotification" in controller
            and "onScreenshotCandidate" in controller,
        ),
        (
            "activity_deduplicates_repeated_candidate_notifications",
            "lastNotifiedScreenshotUri" in controller
            and "shouldNotifyScreenshotCandidate(candidate, lastNotifiedScreenshotUri)" in controller
            and "lastNotifiedScreenshotUri = candidate.contentUri" in controller,
        ),
        (
            "notification_import_intent_is_handled",
            "ACTION_IMPORT_SCREENSHOT" in intents
            and "EXTRA_SCREENSHOT_URI" in intents
            and "EXTRA_SCREENSHOT_WIDTH" in intents + notification
            and "EXTRA_SCREENSHOT_HEIGHT" in intents + notification
            and "EXTRA_SCREENSHOT_CREATED_AT_MILLIS" in intents + notification
            and "EXTRA_SCREENSHOT_DISPLAY_NAME_DIGEST" in intents + notification
            and "screenshotCandidateFromNotificationImport" in intents + store
            and "onNewIntent" in activity,
        ),
        (
            "foreground_candidate_sheet_is_reachable",
            "ScreenshotDetectedSheet" in flow_screens + read("android-mvp/app/src/main/java/cn/shike/app/ui/HomeActionScreen.kt")
            and "pendingScreenshotCandidate" in app + content
            and "onImportScreenshotCandidate" in app + content
            and "HomeActionScreen" in main_routes
            and "pendingScreenshotCandidate?.let { candidate ->" in read("android-mvp/app/src/main/java/cn/shike/app/ui/HomeActionScreen.kt"),
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
