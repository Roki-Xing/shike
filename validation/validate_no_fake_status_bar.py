#!/usr/bin/env python3
"""Validate ordinary UI does not render fake phone status bars or chrome."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI_ROOT = ROOT / "android-mvp/app/src/main/java/cn/shike/app/ui"
FAKE_STATUS_TOKENS = ("10:28", "09:50", "100%", "假电量", "假状态栏", "状态栏时间", "手机壳")
ORDINARY_UI_FILES = {
    "ShikeMainScreen.kt",
    "MainFlowScreens.kt",
    "HomeAgendaList.kt",
    "CaptureEntryPanel.kt",
    "ReadinessSections.kt",
    "ActionPlannerPanel.kt",
    "ConfirmBanner.kt",
    "InboxPanel.kt",
}


def read_ui(name: str) -> str:
    return (UI_ROOT / name).read_text(encoding="utf-8")


def main() -> int:
    offending = []
    for name in ORDINARY_UI_FILES:
        text = read_ui(name)
        if any(token in text for token in FAKE_STATUS_TOKENS):
            offending.append(name)
    checks = [
        ("ordinary_ui_has_no_fake_status_tokens", not offending),
        ("existing_no_fake_device_chrome_validator_exists", (ROOT / "validation/validate_no_fake_device_chrome.py").is_file()),
        ("main_screen_uses_real_window_insets", "WindowInsets.safeDrawing" in read_ui("ShikeMainScreen.kt")),
    ]
    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    if offending:
        print("OFFENDING_UI_FILES\t" + ",".join(sorted(offending)))
    print(f"NO_FAKE_STATUS_BAR_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
