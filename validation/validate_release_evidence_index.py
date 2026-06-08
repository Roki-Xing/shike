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
    "LANDING_RELEASE_CANDIDATE_METRIC 63/63",
    "REAL_WORLD_READY_METRIC 22/22",
    "CLOUD_DEVICE_PREP_METRIC 5/5",
    "CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9",
    "CLOUD_DEVICE_PREP_REPORT_VIDEO_TBD_FIELDS 9/9",
    "CLOUD_BACKEND_READY_METRIC 9/9",
    "http_server_smoke_metric=1/1",
    "shike_backend.eval.http_server_smoke",
    "--disable-cloud-image",
    "RELEASE_HANDOFF_CHECKS_METRIC 24/24",
    "BACKEND_AUDIT_LOG_METRIC 8/8",
    "validate_backend_audit_log.py",
    "LIVE_SMOKE_EVIDENCE_METRIC 7/7",
    "validate_live_smoke_evidence.py",
    "CLOUD_DEVICE_PACKAGE_METRIC 30/30",
    "CLOUD_BACKEND_PREFLIGHT_METRIC",
    "test_preflight_cloud_backend.py",
    "RELEASE_BLOCKING_REPORT_METRIC 8/8",
    "BLUELM_ADAPTER_METRIC 8/8",
    "VIVO_MULTIMODAL_CONTRACT_METRIC 28/28",
    "signed VisionChat fallback",
    "ignored-region metadata allowlist",
    "final server-side user-confirmation action gate",
    "overwrites model-claimed executable actions",
    "allow_cloud_image=false",
    "cloud_image_disabled",
    "REQUIREMENT_MATRIX_METRIC 9/9",
    "USER_RESEARCH_EVIDENCE_METRIC 8/8",
    "DELIVERABLES_METRIC 10/10",
    "PASS secret_hygiene",
    "APK_SECRET_HYGIENE_METRIC 8/8",
    "validate_apk_secret_hygiene.py",
    "NO_DEFAULT_IMAGE_UPLOAD_METRIC 12/12",
    "validate_no_default_image_upload.py",
    "ANDROID16_REAL_IMPLEMENTATION_GUIDE_METRIC 12/12",
    "validate_android16_real_implementation_guide.py",
    "/mnt/c/Users/Xing/Desktop/SHIKE_ANDROID16_REAL_IMPLEMENTATION_GUIDE (1).md",
    "SHIKE-P0-001 through SHIKE-P1-012",
    "ANDROID16_DOD_COVERAGE_METRIC 28/28",
    "validate_android16_definition_of_done.py",
    "Definition of Done",
    "ANDROID16_SCREENSHOT_FLOW_METRIC 18/18",
    "validate_android16_screenshot_flow.py",
    "SCREENSHOT_ASSIST_METRIC 15/15",
    "validate_screenshot_assist.py",
    "repeated-candidate notification dedupe",
    "requires filename or path screenshot signals",
    "NO_FAKE_DEVICE_CHROME_METRIC 1/1",
    "validate_no_fake_device_chrome.py",
    "HOME_ONE_SCREEN_METRIC 9/9",
    "validate_home_one_screen.py",
    "SCREENSHOT_CLEANUP_METRIC 14/14",
    "validate_screenshot_cleanup.py",
    "ANDROID_IMAGE_PREPROCESS_METRIC 15/15",
    "validate_android_image_preprocess.py",
    "IMAGE_SEMANTIC_CASES_METRIC 9/9",
    "MODEL_EVAL_CASES_METRIC 9/9",
    "MODEL_EVAL_METRIC 110/110",
    "BLUELM_THINKING_MODE=provider_default",
    "thinking.type",
    "enable_thinking",
    "provider=bluelm",
    "result_schema_valid=true",
    "--route-v2",
    "route_v2_http_status=200",
    "route_v2_schema_valid=true",
    "route_v2_actions_disabled=true",
    "route_v2_ignored_regions_allowed=true",
    "route_v2_ignored_regions=top_status_bar,bottom_navigation_bar",
    "live_smoke_metric=4/4",
    "live_smoke_metric=1/1",
    "http_smoke_ignored_regions_allowed=True",
    "LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7",
    "Before cloud-device recording",
    "still passes `REQUIREMENT_MATRIX_METRIC 9/9`",
    "must not be treated as release-ready strict proof",
    "materials/evidence/cloud-device/apk-sha256.txt",
    "materials/evidence/cloud-device/cloud-device-capture-todo.md",
    "materials/evidence/blocking-report.md",
    "materials/evidence/requirement-matrix.md",
    "docs/server-deployment-runbook.md",
    "https://roky.chat",
    "https://api.roky.chat",
    "/etc/shike/shike-backend.env",
    "/opt/shike/backend",
    "certbot",
    "materials/evidence/scoring-evidence-map.md",
    "docs/user-research-plan.md",
    "docs/user-interview-summary.md",
    "real interviews, survey counts, privacy preferences, and missed-action examples remain `待采集`",
    "do not fabricate interview data",
    "materials/evidence/desktop-guidance-source-status.md",
    "/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md",
    "stages A-E",
    "validation/traceability.md",
    "validation/fixtures/image_cases.json",
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
    "python3 shike/scripts/test_collect_cloud_device_evidence.py",
    "python3 shike/scripts/test_preflight_cloud_backend.py",
    "python3 shike/validation/validate_cloud_backend_ready.py",
    "python3 shike/validation/validate_backend_audit_log.py",
    "python3 shike/validation/validate_cloud_device_package.py",
    "python3 shike/validation/validate_live_smoke_evidence.py",
    "python3 shike/scripts/run_release_handoff_checks.py --strict",
    "python3 shike/validation/validate_user_research_evidence.py",
    "python3 shike/validation/validate_requirement_matrix.py",
    "python3 shike/validation/validate_deliverables.py",
    "python3 shike/validation/validate_release_evidence_index.py",
    "python3 shike/validation/validate_bluelm_adapter.py",
    "python3 shike/validation/validate_vivo_ocr_adapter.py",
    "python3 shike/validation/validate_vivo_multimodal_contract.py",
    "python3 shike/validation/validate_image_semantic_cases.py",
    "python3 shike/validation/validate_model_eval_cases.py",
    "python3 shike/validation/validate_landing_release_candidate.py",
    "python3 shike/validation/validate_release_blocking_report.py",
    "python3 shike/validation/validate_landing_release_candidate.py --strict",
    "python3 shike/validation/validate_real_world_ready.py",
    "python3 shike/validation/validate_apk_secret_hygiene.py",
    "python3 shike/validation/validate_no_default_image_upload.py",
    "python3 shike/validation/validate_android16_real_implementation_guide.py",
    "python3 shike/validation/validate_android16_definition_of_done.py",
    "python3 shike/validation/validate_android16_screenshot_flow.py",
    "python3 shike/validation/validate_screenshot_assist.py",
    "python3 shike/validation/validate_no_fake_device_chrome.py",
    "python3 shike/validation/validate_home_one_screen.py",
    "python3 shike/validation/validate_screenshot_cleanup.py",
    "python3 shike/validation/validate_android_image_preprocess.py",
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
    "Goal: Promote Android image preprocessing to release handoff evidence.",
    "Round focus: Add signed VisionChat fallback for vivo image models",
    "scoring evidence map",
    "preliminary deck landing evidence package",
    "docs/delivery-boundary-and-scoring.md",
    "materials/preliminary-deck.md",
    "CLOUD_DEVICE_PACKAGE_METRIC\t30/30",
    "RELEASE_HANDOFF_CHECKS_METRIC\t24/24",
    "LIVE_SMOKE_EVIDENCE_METRIC\t7/7",
    "CLOUD_BACKEND_PREFLIGHT_METRIC",
    "BACKEND_CONFIG_METRIC\t19/19",
    "RELEASE_EVIDENCE_INDEX_METRIC\t10/10",
    "REQUIREMENT_MATRIX_METRIC\t9/9",
    "DEMO_ACCEPTANCE_METRIC\t18/18",
    "APK_SECRET_HYGIENE_METRIC\t8/8",
    "VIVO_MULTIMODAL_CONTRACT_METRIC\t28/28",
    "signed VisionChat fallback",
    "ignored-region metadata allowlist",
    "final server-side user-confirmation action gate",
    "model-claimed executable actions",
    "allow_cloud_image=false",
    "cloud_image_disabled",
                    "NO_DEFAULT_IMAGE_UPLOAD_METRIC\t12/12",
                    "ANDROID16_REAL_IMPLEMENTATION_GUIDE_METRIC\t12/12",
                    "SHIKE-P0-001 through SHIKE-P1-012",
                    "ANDROID16_DOD_COVERAGE_METRIC\t28/28",
                    "SCREENSHOT_ASSIST_METRIC\t15/15",
    "ANDROID_IMAGE_PREPROCESS_METRIC\t15/15",
    "LANDING_RELEASE_CANDIDATE_METRIC\t63/63",
    "Real HTTP server smoke is now part of the unified handoff runner",
    "http_smoke_actions_disabled=True",
    "http_smoke_ignored_regions_allowed=True",
    "http_server_smoke_metric=1/1",
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
    optimization_log_head = read_file(OPTIMIZATION_LOG_PATH)[:3500]
    readme = read_file(README_PATH)
    current_status = read_file(CURRENT_STATUS_PATH)
    checks = [
        ("release_evidence_index_exists", bool(text), str(INDEX_PATH.relative_to(ROOT))),
        (
            "requirement_matrix_passes",
            command_passes(["python3", "shike/validation/validate_requirement_matrix.py"])
            and command_passes(["python3", "shike/validation/validate_user_research_evidence.py"])
            and command_passes(["python3", "shike/validation/validate_deliverables.py"]),
            "validate_requirement_matrix.py + validate_user_research_evidence.py + validate_deliverables.py",
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
                    "CLOUD_DEVICE_PACKAGE_METRIC 30/30",
                    "CLOUD_BACKEND_PREFLIGHT_METRIC",
                    "test_preflight_cloud_backend.py",
                    "APK_SECRET_HYGIENE_METRIC 8/8",
                    "NO_DEFAULT_IMAGE_UPLOAD_METRIC 12/12",
                    "validate_no_default_image_upload.py",
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
                    "USER_RESEARCH_EVIDENCE_METRIC 8/8",
                    "REQUIREMENT_MATRIX_METRIC 9/9",
                )
                )
            )
            and (
                all(
                token in current_status
                for token in (
                    "RELEASE_EVIDENCE_INDEX_METRIC 10/10",
                    "APK_SECRET_HYGIENE_METRIC 8/8",
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
                "materials/evidence/scoring-evidence-map.md",
                "docs/user-research-plan.md",
                "docs/user-interview-summary.md",
                "materials/evidence/desktop-guidance-source-status.md",
                "validation/fixtures/image_cases.json",
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
