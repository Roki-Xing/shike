#!/usr/bin/env python3
"""Validate the strict release blocking report is actionable."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "materials/evidence/blocking-report.md"

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

REQUIRED_PLACEHOLDER_FIELDS = (
    "机型: TBD",
    "Android 版本: TBD",
    "测试时间: TBD",
    "后端地址: TBD",
    "后端地址脱敏: TBD",
    "结果: TBD",
    "安装与打开: TBD",
    "相册导入: TBD",
    "拍照导入: TBD",
    "分享导入: TBD",
    "权限降级: TBD",
    "后端失败回退: TBD",
    "重启恢复: TBD",
    "UI 体验: TBD",
    "01-cloud-install-open.mp4`: TBD",
    "02-cloud-gallery-bluelm.mp4`: TBD",
    "03-cloud-camera-bluelm.mp4`: TBD",
    "04-cloud-share-text.mp4`: TBD",
    "05-cloud-permission-fallback.mp4`: TBD",
    "06-cloud-backend-failure.mp4`: TBD",
    "07-cloud-restart-restore.mp4`: TBD",
    "08-cloud-ui-polish.mp4`: TBD",
    "09-cloud-final-route.mp4`: TBD",
)

REQUIRED_ACTION_TOKENS = (
    "HTTPS backend URL",
    "redacted real device evidence",
    "prepare_cloud_device_evidence.py",
    "CLOUD_DEVICE_PREP_METRIC 5/5",
    "CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9",
    "validate_cloud_device_package.py",
    "CLOUD_DEVICE_PACKAGE_METRIC 30/30",
    "validate_release_evidence_index.py",
    "validate_requirement_matrix.py",
    "desktop guidance stages A-E",
    "Pre-recording Evidence Gate",
    "/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md",
    "materials/evidence/requirement-matrix.md",
    "REQUIREMENT_MATRIX_METRIC 9/9",
    "LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7",
    "all 9 real cloud-device MP4 files",
    "no placeholder fields remain after capture",
    "Keep AppKEY",
    "validate_landing_release_candidate.py --strict",
)


def read_report() -> str:
    """Read the generated strict release blocking report.

    Returns:
        UTF-8 report text, or an empty string when the report is absent.
    """

    if not REPORT_PATH.is_file():
        return ""
    return REPORT_PATH.read_text(encoding="utf-8")


def main() -> int:
    """Run blocking-report quality checks.

    Returns:
        0 when the blocking report contains actionable external-evidence steps.
    """

    text = read_report()
    checks = [
        ("blocking_report_exists", bool(text), str(REPORT_PATH.relative_to(ROOT))),
        ("has_missing_evidence_section", "## Missing Evidence" in text, "Missing Evidence"),
        ("has_missing_cloud_videos_section", "## Missing Cloud Videos" in text, "Missing Cloud Videos"),
        (
            "lists_all_required_cloud_videos",
            all(f"materials/evidence/cloud-device/{name}" in text for name in REQUIRED_VIDEO_NAMES),
            "9 cloud mp4 names",
        ),
        (
            "has_report_placeholder_section",
            "## Report Fields Still Placeholder" in text,
            "Report Fields Still Placeholder",
        ),
        (
            "lists_report_placeholder_fields",
            all(field in text for field in REQUIRED_PLACEHOLDER_FIELDS),
            "report TBD fields",
        ),
        (
            "has_required_next_actions",
            "## Required Next Actions" in text and all(token in text for token in REQUIRED_ACTION_TOKENS),
            "strict next actions",
        ),
        (
            "keeps_secret_redaction_warning",
            all(token in text for token in ("AppKEY", "backend tokens", "phone numbers", "emails", "student IDs")),
            "redaction warning",
        ),
    ]

    passed = sum(1 for _, ok, _ in checks if ok)
    for name, ok, evidence in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}\t{evidence}")
    print(f"RELEASE_BLOCKING_REPORT_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
