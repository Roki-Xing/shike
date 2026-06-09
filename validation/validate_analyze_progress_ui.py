#!/usr/bin/env python3
"""Validate the screenshot-to-action analyze progress UI."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI_ROOT = ROOT / "android-mvp/app/src/main/java/cn/shike/app/ui"


def read(relative: str) -> str:
    return (UI_ROOT / relative).read_text(encoding="utf-8")


def main() -> int:
    progress = read("AnalyzeProgressPanel.kt")
    home = read("HomeActionScreen.kt")
    main_screen = read("ShikeMainScreen.kt")

    checks = [
        ("progress_file_present", (UI_ROOT / "AnalyzeProgressPanel.kt").is_file()),
        ("progress_state_model_present", "data class AnalyzeProgressState" in progress and "analyzeProgressStateFor" in progress),
        ("four_steps_present", all(token in progress for token in ["读取图片", "OCR识别", "结构化解析", "生成行动卡"])),
        ("progress_panel_copy_present", "正在把截图变成行动卡" in progress),
        ("home_uses_progress_panel", "AnalyzeProgressPanel(" in home and "hasPendingImage" in home),
        ("home_keeps_candidate_prompt", "ScreenshotDetectedSheet" in home and "VisibleScreenCapturePromptCard" in home),
        ("screenshot_candidate_does_not_force_import_tab", "selectedSection = ShikeMainSection.Import" not in main_screen),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"ANALYZE_PROGRESS_UI_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
