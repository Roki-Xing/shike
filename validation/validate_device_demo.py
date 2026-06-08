#!/usr/bin/env python3
"""Validate whether Shike is ready for a real device demo.

This check focuses on demo-critical Android entry points instead of general
deliverable completeness.
"""

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


def file_nonempty(relative: str) -> bool:
    """Check whether a project-relative file exists and is non-empty.

    Args:
        relative: File path under `shike`.

    Returns:
        True when the file exists and has content.
    """

    path = ROOT / relative
    return path.is_file() and path.stat().st_size > 0


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
    manifest = read("android-mvp/app/src/main/AndroidManifest.xml")
    docs = "\n".join(
        read(path)
        for path in [
            "docs/android-mvp-implementation.md",
            "docs/device-runbook.md",
            "README.md",
        ]
    )

    checks = [
        ("android_apk_exists", file_nonempty("android-mvp/app/build/outputs/apk/debug/app-debug.apk")),
        ("android_build_report_passed", "状态: 通过" in read("android-mvp/build-report.md")),
        ("landable_checks_pass", command_passes(["python3", "shike/validation/validate_landable.py"])),
        ("share_import_present", "ACTION_SEND" in android_source and "Intent.EXTRA_TEXT" in android_source),
        (
            "gallery_picker_present",
            (
                "ActivityResultContracts.PickVisualMedia" in android_source
                and "PickVisualMedia.ImageOnly" in android_source
            )
            or ("ActivityResultContracts.GetContent" in android_source and "image/*" in android_source),
        ),
        ("camera_preview_present", "ActivityResultContracts.TakePicturePreview" in android_source),
        ("camera_permission_runtime_present", "RequestPermission" in android_source and "Manifest.permission.CAMERA" in android_source),
        ("capture_source_feedback_present", "captureSource" in android_source and "采集来源" in android_source),
        ("captured_preview_rendered", "asImageBitmap" in android_source and "contentDescription = \"拍照预览\"" in android_source),
        ("offline_sample_fallback_present", "离线兜底样例" in android_source and "课程样例" in android_source and "活动样例" in android_source),
        ("camera_permission_manifest_present", "android.permission.CAMERA" in manifest),
        ("device_runbook_capture_steps", "选择截图" in docs and "拍照导入" in docs and "相册" in docs),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"DEVICE_DEMO_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
