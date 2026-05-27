#!/usr/bin/env python3
"""Validate user confirmation and manual correction readiness."""

from __future__ import annotations

import subprocess
from pathlib import Path

from source_tree import read_android_source

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    """Read a UTF-8 text file under `shike`.

    Args:
        relative: File path under `shike`.

    Returns:
        File content.
    """

    return (ROOT / relative).read_text(encoding="utf-8")


def command_passes(command: list[str]) -> bool:
    """Run a command from the workspace root and return its pass status.

    Args:
        command: Command and arguments.

    Returns:
        True when the command exits with status code 0.
    """

    result = subprocess.run(command, cwd=ROOT.parent, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return result.returncode == 0


def main() -> int:
    android_source = read_android_source(ROOT)
    docs = "\n".join(
        read(path)
        for path in [
            "docs/android-mvp-implementation.md",
            "docs/device-runbook.md",
            "README.md",
        ]
    )

    checks = [
        ("ocr_input_checks_pass", command_passes(["python3", "shike/validation/validate_ocr_input.py"])),
        ("review_callback_present", "onReviewed" in android_source and "updateReviewedItem" in android_source),
        ("editable_title_present", "draftTitle" in android_source and "任务标题" in android_source),
        ("editable_time_present", "draftTime" in android_source and "label = { Text(\"时间\") }" in android_source),
        ("editable_location_present", "draftLocation" in android_source and "label = { Text(\"地点\") }" in android_source),
        ("editable_status_present", "draftStatus" in android_source and "label = { Text(\"状态\") }" in android_source),
        ("confirm_button_present", "确认修正" in android_source),
        ("ignore_button_present", "Text(\"忽略\")" in android_source and "已忽略" in android_source),
        ("confirmed_item_persisted", "persistSelection(reviewedItem, \"用户确认修正" in android_source),
        ("manual_review_updates_model_status", "模型编排：用户已确认" in android_source and "模型编排：用户已忽略" in android_source),
        ("execution_guard_copy_present", "未确认前不会打开外部日历、通知或地图" in android_source),
        ("manual_review_documented", "确认修正" in docs and "已忽略" in docs and "手动修正" in docs),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"MANUAL_REVIEW_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
