#!/usr/bin/env python3
"""Validate first-run permission onboarding for the real app path."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def exists(relative: str) -> bool:
    return (ROOT / relative).is_file()


def main() -> int:
    onboarding_path = "android-mvp/app/src/main/java/cn/shike/app/ui/PermissionOnboarding.kt"
    store_path = "android-mvp/app/src/main/java/cn/shike/app/data/PermissionOnboardingStore.kt"
    onboarding = read(onboarding_path) if exists(onboarding_path) else ""
    store = read(store_path) if exists(store_path) else ""
    main_activity = read("android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt")
    shike_app = read("android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt")
    main_flow = read("android-mvp/app/src/main/java/cn/shike/app/ui/MainFlowScreens.kt")
    notification = read("android-mvp/app/src/main/java/cn/shike/app/system/ScreenshotNotification.kt")

    checks = [
        ("permission_onboarding_component_exists", exists(onboarding_path)),
        ("permission_onboarding_store_exists", exists(store_path)),
        (
            "onboarding_explains_required_permissions",
            all(token in onboarding for token in ["通知权限", "图片权限", "相机权限", "日历", "地图"]),
        ),
        (
            "onboarding_has_explicit_screenshot_assist_choice",
            "开启截图助手" in onboarding and "稍后再说" in onboarding,
        ),
        (
            "onboarding_says_no_default_upload",
            "不默认上传原图" in onboarding and "用户确认后" in onboarding,
        ),
        (
            "shike_app_wires_first_run_onboarding",
            "onboardingDismissed" in shike_app and "PermissionOnboarding" in main_flow,
        ),
        (
            "main_activity_persists_onboarding_state",
            "loadPermissionOnboardingDismissed" in main_activity and "savePermissionOnboardingDismissed" in main_activity,
        ),
        (
            "screenshot_notification_prompts_handoff",
            "是否交给拾刻" in notification and "生成行动卡" in notification,
        ),
    ]
    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"PERMISSION_ONBOARDING_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
