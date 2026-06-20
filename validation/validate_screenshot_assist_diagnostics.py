#!/usr/bin/env python3
"""Validate screenshot assist diagnostics are visible in settings."""

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
    diagnostics = read("android-mvp/app/src/main/java/cn/shike/app/system/ScreenshotAssistDiagnostics.kt")
    notification = read("android-mvp/app/src/main/java/cn/shike/app/system/ScreenshotNotification.kt")
    service = read("android-mvp/app/src/main/java/cn/shike/app/system/ScreenshotAssistService.kt")
    controller = read("android-mvp/app/src/main/java/cn/shike/app/ScreenshotAssistController.kt")
    main_activity = read("android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt")
    lifecycle = read("android-mvp/app/src/main/java/cn/shike/app/MainActivityLifecycleActions.kt")
    screen_host = read("android-mvp/app/src/main/java/cn/shike/app/ShikeScreenHost.kt")
    app = read("android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt")
    main_screen = read("android-mvp/app/src/main/java/cn/shike/app/ui/ShikeMainScreen.kt")
    flow = read("android-mvp/app/src/main/java/cn/shike/app/ui/MainFlowScreens.kt")
    settings = read("android-mvp/app/src/main/java/cn/shike/app/ui/ReadinessSections.kt")
    home = read("android-mvp/app/src/main/java/cn/shike/app/ui/HomeActionScreen.kt")

    checks = [
        ("diagnostics_file_exists", exists("android-mvp/app/src/main/java/cn/shike/app/system/ScreenshotAssistDiagnostics.kt")),
        (
            "diagnostics_model_tracks_required_statuses",
            "data class ScreenshotAssistDiagnostics" in diagnostics
            and "mediaPermissionGranted" in diagnostics
            and "notificationPermissionGranted" in diagnostics
            and "serviceRunning" in diagnostics
            and "lastDetectedAtText" in diagnostics
            and "lastNotificationStatus" in diagnostics,
        ),
        (
            "diagnostics_reads_permissions",
            "screenshotAssistDiagnostics(" in diagnostics
            and "hasScreenshotMediaPermission(context)" in diagnostics
            and "canPostScreenshotAssistNotification(context)" in diagnostics,
        ),
        (
            "diagnostics_records_last_detected_and_notification",
            "recordScreenshotAssistDetected" in diagnostics
            and "recordScreenshotAssistNotification" in diagnostics
            and "loadScreenshotAssistDiagnostics" in diagnostics
            and "最近检测截图" in diagnostics
            and "最近通知" in diagnostics,
        ),
        (
            "notification_updates_diagnostics_status",
            "recordScreenshotAssistNotification" in notification
            and "已发送" in notification
            and "通知权限未开启" in notification,
        ),
        (
            "observer_updates_detected_timestamp",
            "recordScreenshotAssistDetected" in controller + service
            and "candidate.createdAtMillis" in controller + service,
        ),
        (
            "activity_tracks_service_running",
            "screenshotAssistServiceRunning" in main_activity + lifecycle
            and "handleScreenshotAssistServiceRunningChanged" in lifecycle
            and "startScreenshotAssistService(this)" in lifecycle,
        ),
        (
            "diagnostics_wired_to_settings",
            "screenshotAssistDiagnostics" in app + screen_host + main_screen + flow
            and "PrivacySettingsScreen(" in main_screen
            and "PrivacyPanel(" in flow
            and "ScreenshotAssistDiagnosticsPanel" in settings,
        ),
        (
            "settings_copy_is_user_facing",
            "截图助手诊断" in settings
            and "图片权限" in settings
            and "通知权限" in settings
            and "后台服务" in settings
            and "最近检测截图" in settings
            and "最近通知" in settings
            and "MediaStore" not in settings
            and "provider" not in settings
            and "debug" not in settings.lower(),
        ),
        (
            "home_does_not_show_diagnostics",
            "ScreenshotAssistDiagnosticsPanel" not in home
            and "后台服务" not in home
            and "最近通知" not in home,
        ),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"SCREENSHOT_ASSIST_DIAGNOSTICS_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
