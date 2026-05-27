#!/usr/bin/env python3
"""Validate whether Shike is closer to a device-testable MVP."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from source_tree import read_android_source

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    """Read a UTF-8 text file.

    Args:
        relative: File path under `shike`.

    Returns:
        File content.
    """

    return (ROOT / relative).read_text(encoding="utf-8")


def file_nonempty(relative: str) -> bool:
    return (ROOT / relative).is_file() and (ROOT / relative).stat().st_size > 0


def command_passes(command: list[str]) -> bool:
    result = subprocess.run(command, cwd=ROOT.parent, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return result.returncode == 0


def main() -> int:
    android_source = read_android_source(ROOT)
    backend = read("backend/shike_backend/main.py")
    docs = "\n".join(
        read(path)
        for path in [
            "docs/android-mvp-implementation.md",
            "docs/fallback-and-finals-roadmap.md",
            "docs/device-runbook.md",
            "README.md",
        ]
    )
    cases = json.loads(read("validation/regression-cases.json"))

    checks = [
        ("android_apk_exists", file_nonempty("android-mvp/app/build/outputs/apk/debug/app-debug.apk")),
        ("android_build_report_passed", "状态: 通过" in read("android-mvp/build-report.md")),
        ("backend_smoke_passes", command_passes(["python3", "shike/backend/verify_backend.py"])),
        ("deliverables_pass", command_passes(["python3", "shike/validation/validate_deliverables.py"])),
        ("spike_passes", command_passes(["python3", "shike/spike/run_spike.py", "--all"])),
        ("calendar_intent_present", "CalendarContract" in android_source or "Intent.ACTION_INSERT" in android_source),
        ("reminder_notification_present", "NotificationCompat" in android_source or "AlarmManager" in android_source),
        ("map_deeplink_present", "geo:" in android_source or "Uri.encode" in android_source),
        ("share_import_present", "ACTION_SEND" in android_source or "Intent.EXTRA_TEXT" in android_source),
        ("backend_schema_endpoint_present", "/v1/schema" in backend or "model-output.schema.json" in backend),
        ("backend_has_error_cases", "HTTPException" in backend and "missing_fields" in backend),
        ("regression_case_count", len(cases) >= 10),
        ("device_runbook_present", file_nonempty("docs/device-runbook.md")),
        ("privacy_permissions_documented", "POST_NOTIFICATIONS" in docs and "无日历读写权限" in docs and "CAMERA" in docs),
        ("offline_mock_documented", "MockModelAdapter" in docs and "离线" in docs),
        ("structure_guard_runbook_documented", "validate_android_structure.py" in docs and "ANDROID_STRUCTURE_METRIC 31/31" in docs),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"LANDABLE_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
