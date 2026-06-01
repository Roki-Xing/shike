#!/usr/bin/env python3
"""Validate the release evidence index covers handoff-critical proof."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "materials/evidence/release-evidence-index.md"
OPTIMIZATION_LOG_PATH = ROOT / "docs/optimization-log.md"
README_PATH = ROOT / "README.md"
CURRENT_STATUS_PATH = ROOT / "docs/current-validation-status.md"

REQUIRED_TOKENS = (
    "LANDING_RELEASE_CANDIDATE_METRIC 52/52",
    "REAL_WORLD_READY_METRIC 22/22",
    "CLOUD_DEVICE_PREP_METRIC 5/5",
    "CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9",
    "CLOUD_DEVICE_PREP_REPORT_VIDEO_TBD_FIELDS 9/9",
    "CLOUD_DEVICE_PACKAGE_METRIC 27/27",
    "RELEASE_BLOCKING_REPORT_METRIC 8/8",
    "BLUELM_ADAPTER_METRIC 7/7",
    "REQUIREMENT_MATRIX_METRIC 9/9",
    "DELIVERABLES_METRIC 10/10",
    "PASS secret_hygiene",
    "MODEL_EVAL_METRIC 110/110",
    "BLUELM_THINKING_MODE=provider_default",
    "thinking.type",
    "enable_thinking",
    "provider=bluelm",
    "result_schema_valid=true",
    "LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7",
    "Before cloud-device recording",
    "still passes `REQUIREMENT_MATRIX_METRIC 9/9`",
    "must not be treated as release-ready strict proof",
    "materials/evidence/cloud-device/apk-sha256.txt",
    "materials/evidence/cloud-device/cloud-device-capture-todo.md",
    "materials/evidence/blocking-report.md",
    "materials/evidence/requirement-matrix.md",
    "materials/evidence/desktop-guidance-source-status.md",
    "/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md",
    "stages A-E",
    "validation/traceability.md",
    "SHIKE-070",
    "The SHIKE-070 row links submission materials to `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md`",
    "docs/optimization-log.md",
    "Current handoff summary",
    "Historical optimization-log entries keep their original evidence values",
    "validate_landing_release_candidate.py --strict",
    "Nine real cloud-device MP4 recordings",
    "placeholders removed",
)

REQUIRED_COMMANDS = (
    "python3 shike/scripts/prepare_cloud_device_evidence.py",
    "python3 shike/validation/validate_cloud_device_package.py",
    "python3 shike/validation/validate_requirement_matrix.py",
    "python3 shike/validation/validate_deliverables.py",
    "python3 shike/validation/validate_release_evidence_index.py",
    "python3 shike/validation/validate_bluelm_adapter.py",
    "python3 shike/validation/validate_landing_release_candidate.py",
    "python3 shike/validation/validate_release_blocking_report.py",
    "python3 shike/validation/validate_landing_release_candidate.py --strict",
    "python3 shike/validation/validate_real_world_ready.py",
    "python3 shike/validation/validate_secret_hygiene.py",
)

REDACTION_TOKENS = (
    "AppKEY",
    "backend tokens",
    "full OCR text",
    "phone numbers",
    "emails",
    "student IDs",
    "synthetic screenshots",
)

OPTIMIZATION_LOG_TOKENS = (
    "Goal: Bring the public validation status up to the current materials evidence package.",
    "scoring evidence map",
    "preliminary deck landing evidence package",
    "docs/delivery-boundary-and-scoring.md",
    "materials/preliminary-deck.md",
    "CLOUD_DEVICE_PACKAGE_METRIC\t27/27",
    "RELEASE_EVIDENCE_INDEX_METRIC\t10/10",
    "REQUIREMENT_MATRIX_METRIC\t9/9",
    "DEMO_ACCEPTANCE_METRIC\t18/18",
    "LANDING_RELEASE_CANDIDATE_METRIC\t52/52",
    "LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE\t3/7",
    "/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md",
    "materials/evidence/requirement-matrix.md",
    "No cloud recordings, report values, credentials, or personal data were fabricated.",
)


def read_index() -> str:
    """Read the release evidence index.

    Returns:
        UTF-8 index text, or an empty string when the file is absent.
    """

    if not INDEX_PATH.is_file():
        return ""
    return INDEX_PATH.read_text(encoding="utf-8")


def read_file(path: Path) -> str:
    """Read a UTF-8 text file.

    Args:
        path: Absolute file path.

    Returns:
        UTF-8 text, or an empty string when absent.
    """

    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def command_passes(command: list[str]) -> bool:
    """Run a release evidence sub-gate.

    Args:
        command: Command list executed from the workspace root.

    Returns:
        True when the command exits successfully.
    """

    result = subprocess.run(
        command,
        cwd=ROOT.parent,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return result.returncode == 0


def commands_in_expected_order(text: str) -> bool:
    """Check rebuild commands use dependency-safe ordering.

    Args:
        text: Release evidence index text.

    Returns:
        True when each command appears after the command it depends on.
    """

    marker = "## Rebuild Evidence Checklist"
    if marker not in text:
        return False
    checklist = text.split(marker, 1)[1]
    cursor = -1
    for command in REQUIRED_COMMANDS:
        index = checklist.find(command)
        if index <= cursor:
            return False
        cursor = index
    return True


def main() -> int:
    """Run release evidence index checks.

    Returns:
        0 when the index covers local gates, model proof, strict blockers, and redaction.
    """

    text = read_index()
    optimization_log_head = read_file(OPTIMIZATION_LOG_PATH)[:2500]
    readme = read_file(README_PATH)
    current_status = read_file(CURRENT_STATUS_PATH)
    checks = [
        ("release_evidence_index_exists", bool(text), str(INDEX_PATH.relative_to(ROOT))),
        (
            "requirement_matrix_passes",
            command_passes(["python3", "shike/validation/validate_requirement_matrix.py"])
            and command_passes(["python3", "shike/validation/validate_deliverables.py"]),
            "validate_requirement_matrix.py + validate_deliverables.py",
        ),
        ("lists_required_metrics", all(token in text for token in REQUIRED_TOKENS), "readiness/model/strict evidence"),
        ("lists_rebuild_commands", all(command in text for command in REQUIRED_COMMANDS), "rebuild commands"),
        ("orders_rebuild_commands", commands_in_expected_order(text), "dependency-safe rebuild order"),
        ("lists_redaction_rules", all(token in text for token in REDACTION_TOKENS), "redaction rules"),
        (
            "optimization_log_has_current_handoff_summary",
            all(token in optimization_log_head for token in OPTIMIZATION_LOG_TOKENS),
            "docs/optimization-log.md current handoff summary",
        ),
        (
            "readme_lists_current_release_evidence_gate",
            (
                all(
                token in readme
                for token in (
                    "RELEASE_EVIDENCE_INDEX_METRIC 10/10",
                    "prepare_cloud_device_evidence.py",
                    "CLOUD_DEVICE_PREP_METRIC 5/5",
                    "CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9",
                    "CLOUD_DEVICE_PACKAGE_METRIC 27/27",
                    "docs/optimization-log.md",
                    "当前交接摘要",
                    "依赖安全重跑命令",
                    "validation/traceability.md",
                    "SHIKE-070",
                    "Pre-recording Evidence Gate",
                    "all 9 real cloud-device MP4 files",
                    "no placeholder fields remain after capture",
                    "/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md",
                    "materials/evidence/requirement-matrix.md",
                    "REQUIREMENT_MATRIX_METRIC 9/9",
                )
                )
            )
            and (
                all(
                token in current_status
                for token in (
                    "RELEASE_EVIDENCE_INDEX_METRIC 10/10",
                    "validate_deliverables.py",
                    "validation/traceability.md",
                    "SHIKE-070",
                    "dependency-safe rebuild commands",
                    "README public entrypoint",
                    "scoring evidence map",
                    "preliminary deck landing evidence package",
                    "materials/evidence/blocking-report.md",
                    "Required Next Actions",
                    "Pre-recording Evidence Gate",
                    "all 9 real cloud-device MP4 files",
                    "no placeholder fields remain after capture",
                    "/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md",
                    "materials/evidence/requirement-matrix.md",
                    "REQUIREMENT_MATRIX_METRIC 9/9",
                    "before cloud-device recording",
                    )
                )
            ),
            "README.md + docs/current-validation-status.md release evidence gate",
        ),
        (
            "references_existing_evidence_files",
            all((ROOT / relative).is_file() for relative in (
                "materials/evidence/cloud-device/apk-sha256.txt",
                "materials/evidence/cloud-device/backend-redacted-access-log.txt",
                "materials/evidence/cloud-device/cloud-device-capture-todo.md",
                "materials/evidence/blocking-report.md",
                "materials/evidence/requirement-matrix.md",
                "materials/evidence/desktop-guidance-source-status.md",
            )),
            "evidence files",
        ),
        (
            "does_not_embed_secret_like_value",
            re.search(r"\bsk-[A-Za-z0-9]{12,}\b", text) is None,
            "no sk token",
        ),
    ]

    passed = sum(1 for _, ok, _ in checks if ok)
    for name, ok, evidence in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}\t{evidence}")
    print(f"RELEASE_EVIDENCE_INDEX_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
