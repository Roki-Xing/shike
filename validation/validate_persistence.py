#!/usr/bin/env python3
"""Validate whether Shike preserves demo state locally across app restarts."""

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


def extract_kotlin_function_body(source: str, function_name: str) -> str:
    """Extract a Kotlin function body (including braces) from source text.

    This is a lightweight guard for regression checks. It is not a full parser.
    Returns an empty string when the function cannot be located or is malformed.
    """

    # Match exact signature prefix so an internal overload (if added later) does not
    # accidentally satisfy the guard while the Context-based entrypoint regresses.
    start = source.find(f"fun {function_name}(context: Context)")
    if start == -1:
        return ""
    brace_open = source.find("{", start)
    if brace_open == -1:
        return ""
    depth = 0
    for index in range(brace_open, len(source)):
        char = source[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return source[brace_open : index + 1]
    return ""


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
    local_inbox_store = read("android-mvp/app/src/main/java/cn/shike/app/data/LocalInboxStore.kt")
    backend_config_store = read("android-mvp/app/src/main/java/cn/shike/app/data/BackendConfigStore.kt")
    reminder_scheduler = read("android-mvp/app/src/main/java/cn/shike/app/system/ReminderScheduler.kt")
    docs = "\n".join(
        read(path)
        for path in [
            "docs/android-mvp-implementation.md",
            "docs/device-runbook.md",
            "README.md",
        ]
    )

    clear_inbox_snapshot_body = extract_kotlin_function_body(local_inbox_store, "clearInboxSnapshot")
    clear_inbox_snapshot_removes_only_snapshot_keys = bool(clear_inbox_snapshot_body) and all(
        token in clear_inbox_snapshot_body
        for token in [
            ".remove(KEY_TITLE)",
            ".remove(KEY_SCENE)",
            ".remove(KEY_TIME)",
            ".remove(KEY_LOCATION)",
            ".remove(KEY_STATUS)",
            ".remove(KEY_ACTIONS)",
            ".remove(KEY_START)",
            ".remove(KEY_RAW_TEXT)",
            ".remove(KEY_CAPTURE_SOURCE)",
        ]
    )
    clear_inbox_snapshot_does_not_clear_all = bool(clear_inbox_snapshot_body) and ".clear()" not in clear_inbox_snapshot_body

    checks = [
        ("device_demo_checks_pass", command_passes(["python3", "shike/validation/validate_device_demo.py"])),
        ("shared_preferences_imported", "SharedPreferences" in android_source),
        (
            "preferences_namespace_present",
            "INBOX_PREFERENCES_NAME = \"shike_inbox_state\"" in local_inbox_store
            and "BACKEND_PREFERENCES_NAME = \"shike_backend_config\"" in backend_config_store
            and "REMINDER_PREFERENCES_NAME = \"shike_reminder_state\"" in reminder_scheduler,
        ),
        (
            "save_snapshot_present",
            "fun saveSnapshot" in local_inbox_store
            and ".putString(KEY_TITLE" in local_inbox_store
            and clear_inbox_snapshot_removes_only_snapshot_keys
            and clear_inbox_snapshot_does_not_clear_all,
        ),
        ("load_saved_item_present", "fun loadSavedItem" in android_source and "prefs.getString(KEY_TITLE" in android_source),
        ("capture_source_persisted", "KEY_CAPTURE_SOURCE" in android_source and "loadSavedCaptureSource" in android_source),
        ("gallery_persists_selection", "相册图片" in android_source and "persistSelection(item, source)" in android_source),
        ("camera_persists_selection", "相机拍照预览" in android_source and "persistSelection(item, source)" in android_source),
        ("sample_fallback_persists", "persistSelection(sampleCourse()" in android_source and "persistSelection(sampleEvent()" in android_source),
        ("share_import_waits_for_confirmation", "文本分享入口（待确认，未落盘）" in android_source and "saveSnapshot(importedItem" not in android_source),
        ("restore_feedback_visible", "本地恢复" in android_source and "已保存到收件箱缓存" in android_source),
        ("persistence_documented", "SharedPreferences" in docs and "重启" in docs and "收件箱缓存" in docs),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"PERSISTENCE_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
