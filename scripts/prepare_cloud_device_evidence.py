#!/usr/bin/env python3
"""Prepare the Shike cloud-device evidence package.

This helper does not create fake recordings. It refreshes the APK hash and
writes a capture TODO file that lists the exact videos still required before
``validate_cloud_device_package.py --strict`` can pass.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_APK = ROOT / "android-mvp/app/build/outputs/apk/debug/app-debug.apk"
DEFAULT_EVIDENCE_ROOT = ROOT / "materials/evidence/cloud-device"
REPORT_NAME = "cloud-device-test-report.md"

REQUIRED_VIDEO_NAMES = [
    "01-cloud-install-open.mp4",
    "02-cloud-gallery-bluelm.mp4",
    "03-cloud-camera-bluelm.mp4",
    "04-cloud-share-text.mp4",
    "05-cloud-permission-fallback.mp4",
    "06-cloud-backend-failure.mp4",
    "07-cloud-restart-restore.mp4",
    "08-cloud-ui-polish.mp4",
    "09-cloud-final-route.mp4",
]

REQUIRED_REPORT_FIELDS = [
    "机型",
    "Android 版本",
    "测试时间",
    "后端地址",
    "后端地址脱敏",
    "结果",
    "安装与打开",
    "相册导入",
    "拍照导入",
    "分享导入",
    "权限降级",
    "后端失败回退",
    "重启恢复",
    "UI 体验",
]

REQUIRED_REPORT_GATE_FIELDS = [
    "Pre-recording Evidence Gate",
    "Desktop guidance source checked",
    "Requirement matrix checked",
    "Requirement matrix gate",
    "Strict release gate before filling this report",
    "All 9 real cloud-device MP4 files present",
    "No placeholder fields remain after capture",
]


def sha256(path: Path) -> str:
    """Hash a file with SHA-256.

    Args:
        path: File to hash.

    Returns:
        Hex digest string.
    """

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def missing_videos(evidence_root: Path) -> list[str]:
    """List required cloud-device videos that are still absent or empty.

    Args:
        evidence_root: Evidence package directory.

    Returns:
        Required video names that do not exist as non-empty files.
    """

    return [name for name in REQUIRED_VIDEO_NAMES if not (evidence_root / name).is_file() or (evidence_root / name).stat().st_size == 0]


def missing_report_fields(evidence_root: Path) -> list[str]:
    """List report fields that are still blank placeholders.

    Args:
        evidence_root: Evidence package directory.

    Returns:
        Report field names whose current line still contains a placeholder.
    """

    report_path = evidence_root / REPORT_NAME
    if not report_path.is_file():
        return list(REQUIRED_REPORT_FIELDS)

    text = report_path.read_text(encoding="utf-8", errors="replace")
    missing: list[str] = []
    for field in REQUIRED_REPORT_FIELDS:
        field_pattern = f"- {field}:"
        field_line = next((line for line in text.splitlines() if line.startswith(field_pattern)), "")
        if not field_line or any(marker in field_line for marker in ("TBD", "待补录", "待采集", "TODO")):
            missing.append(field)
    return missing


def missing_report_video_evidence(evidence_root: Path) -> list[str]:
    """List report video evidence rows that are still blank placeholders.

    Args:
        evidence_root: Evidence package directory.

    Returns:
        Required video names whose report evidence line still contains a placeholder.
    """

    report_path = evidence_root / REPORT_NAME
    if not report_path.is_file():
        return list(REQUIRED_VIDEO_NAMES)

    text = report_path.read_text(encoding="utf-8", errors="replace")
    missing: list[str] = []
    for name in REQUIRED_VIDEO_NAMES:
        video_pattern = f"- `{name}`:"
        video_line = next((line for line in text.splitlines() if line.startswith(video_pattern)), "")
        if not video_line or any(marker in video_line for marker in ("TBD", "待补录", "待采集", "TODO")):
            missing.append(name)
    return missing


def write_apk_sha(apk_path: Path, evidence_root: Path) -> Path:
    """Write the current debug APK hash into the evidence package.

    Args:
        apk_path: Debug APK path.
        evidence_root: Evidence package directory.

    Returns:
        Path to the written hash file.
    """

    output = evidence_root / "apk-sha256.txt"
    digest = sha256(apk_path)
    output.write_text(
        "\n".join(
            [
                "APK path: shike/android-mvp/app/build/outputs/apk/debug/app-debug.apk",
                f"APK SHA-256: {digest}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return output


def write_capture_todo(
    evidence_root: Path,
    missing: list[str],
    missing_report: list[str],
    missing_report_videos: list[str],
) -> Path:
    """Write the strict-mode capture TODO file.

    Args:
        evidence_root: Evidence package directory.
        missing: Required video names still missing.
        missing_report: Report body fields that still contain placeholders.
        missing_report_videos: Report video evidence rows that still contain placeholders.

    Returns:
        Path to the written TODO file.
    """

    output = evidence_root / "cloud-device-capture-todo.md"
    lines = [
        "# Cloud Device Capture TODO",
        "",
        "Use this file as the operator checklist before running strict validation.",
        "",
        "## Current Missing Evidence",
        f"- Missing videos: {len(missing)}/{len(REQUIRED_VIDEO_NAMES)}",
        f"- Report fields still TBD: {len(missing_report)}/{len(REQUIRED_REPORT_FIELDS)}",
        f"- Report video evidence still TBD: {len(missing_report_videos)}/{len(REQUIRED_VIDEO_NAMES)}",
        "- Rerun this helper after adding MP4 files or editing the report; this section is generated from the current evidence package.",
        "",
        "### Missing Videos",
    ]
    for name in missing:
        lines.append(f"- `{name}`")
    if not missing:
        lines.append("- None")
    lines.extend(
        [
            "",
            "### Report Fields Still TBD",
        ]
    )
    for field in missing_report:
        lines.append(f"- {field}")
    if not missing_report:
        lines.append("- None")
    lines.extend(
        [
            "",
            "### Report Video Evidence Still TBD",
        ]
    )
    for name in missing_report_videos:
        lines.append(f"- `{name}`")
    if not missing_report_videos:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Required Videos",
        ]
    )
    for name in REQUIRED_VIDEO_NAMES:
        marker = "[ ]" if name in missing else "[x]"
        lines.append(f"- {marker} `{name}`")
    lines.extend(
        [
            "",
            "## Report Fields",
        ]
    )
    for field in REQUIRED_REPORT_FIELDS:
        marker = "[ ]" if field in missing_report else "[x]"
        lines.append(f"- {marker} {field}")
    lines.extend(
        [
            "",
            "### Report Evidence Gate Fields",
        ]
    )
    for field in REQUIRED_REPORT_GATE_FIELDS:
        lines.append(f"- [ ] {field}")
    lines.extend(
        [
            "",
            "## Report Video Evidence Section",
            "- [ ] Add a `## Video Evidence` section to `cloud-device-test-report.md`.",
            "- [ ] List all 9 MP4 filenames in that section after recording.",
            "- [ ] Replace every video evidence `TBD` note with a concise redacted result note.",
            "- [ ] Keep video notes concise and redacted; do not paste backend tokens, raw OCR text, or personal data.",
            "",
            "## Pre-capture Checks",
            "- [ ] Run `python3 shike/scripts/prepare_cloud_device_evidence.py` before capture and confirm `CLOUD_DEVICE_PREP_METRIC 5/5`.",
            "- [ ] Confirm `CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9` is the expected pre-capture state until the real cloud-device recordings are present.",
            "- [ ] Use a HTTPS backend URL that the cloud device can reach.",
            "- [ ] Keep AppKEY, backend tokens, full OCR text, phone numbers, emails, and student IDs out of videos, logs, and filenames.",
            "- [ ] Capture one backend success path with `provider=bluelm` and `result_schema_valid=true` in the redacted backend log.",
            "- [ ] Capture one permission fallback path, one backend failure fallback path, and one restart-restore path.",
            "",
            "## Release Handoff",
            "- [ ] Confirm `materials/evidence/release-evidence-index.md` references this capture package.",
            "- [ ] Confirm `RELEASE_EVIDENCE_INDEX_METRIC 10/10` still passes, including `docs/optimization-log.md` current handoff summary and README public entrypoint checks.",
            "- [ ] Confirm `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md` remains the desktop guidance source before recording.",
            "- [ ] Confirm `materials/evidence/requirement-matrix.md` still maps stages A-E to local evidence and strict cloud-device blockers, then confirm `REQUIREMENT_MATRIX_METRIC 9/9`.",
            "- [ ] Confirm `materials/evidence/blocking-report.md` still lists any missing strict evidence.",
            "- [ ] Keep the default local gate at `LANDING_RELEASE_CANDIDATE_METRIC 52/52`.",
            "- [ ] Keep strict release blocked at `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7` until real recordings and the filled report are collected.",
            "",
            "## Strict Validation",
            "",
            "```bash",
            "python3 shike/validation/validate_cloud_device_package.py",
            "python3 shike/validation/validate_release_evidence_index.py",
            "python3 shike/validation/validate_cloud_device_package.py --strict",
            "python3 shike/validation/validate_landing_release_candidate.py --strict",
            "```",
        ]
    )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments.

    Returns:
        Parsed arguments.
    """

    parser = argparse.ArgumentParser(description="Prepare Shike cloud-device evidence package files.")
    parser.add_argument("--apk", type=Path, default=DEFAULT_APK, help="Debug APK path.")
    parser.add_argument("--evidence-root", type=Path, default=DEFAULT_EVIDENCE_ROOT, help="Cloud-device evidence directory.")
    return parser.parse_args()


def main() -> int:
    """Prepare the cloud-device package and print a concise metric.

    Returns:
        0 when preparation files were written, 1 when the APK is missing.
    """

    args = parse_args()
    evidence_root = args.evidence_root.resolve()
    apk_path = args.apk.resolve()
    evidence_root.mkdir(parents=True, exist_ok=True)

    checks: list[tuple[str, bool, str]] = []
    checks.append(("evidence_root_exists", evidence_root.is_dir(), str(evidence_root)))

    apk_exists = apk_path.is_file() and apk_path.stat().st_size > 0
    checks.append(("debug_apk_exists", apk_exists, str(apk_path)))
    if apk_exists:
        sha_path = write_apk_sha(apk_path, evidence_root)
        checks.append(("apk_sha_written", sha_path.is_file() and sha_path.stat().st_size > 0, str(sha_path)))
    else:
        checks.append(("apk_sha_written", False, str(evidence_root / "apk-sha256.txt")))

    missing = missing_videos(evidence_root)
    missing_report = missing_report_fields(evidence_root)
    missing_report_videos = missing_report_video_evidence(evidence_root)
    todo_path = write_capture_todo(evidence_root, missing, missing_report, missing_report_videos)
    checks.append(("capture_todo_written", todo_path.is_file() and todo_path.stat().st_size > 0, str(todo_path)))
    checks.append(("required_video_names_listed", all(name in todo_path.read_text(encoding="utf-8") for name in REQUIRED_VIDEO_NAMES), "cloud-device-capture-todo.md"))

    for name, ok, evidence in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}\t{evidence}")
    print(f"CLOUD_DEVICE_PREP_MISSING_VIDEOS\t{len(missing)}/{len(REQUIRED_VIDEO_NAMES)}")
    print(f"CLOUD_DEVICE_PREP_REPORT_TBD_FIELDS\t{len(missing_report)}/{len(REQUIRED_REPORT_FIELDS)}")
    print(f"CLOUD_DEVICE_PREP_REPORT_VIDEO_TBD_FIELDS\t{len(missing_report_videos)}/{len(REQUIRED_VIDEO_NAMES)}")
    print(f"CLOUD_DEVICE_PREP_METRIC\t{sum(1 for _, ok, _ in checks if ok)}/{len(checks)}")
    return 0 if all(ok for _, ok, _ in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
