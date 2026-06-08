#!/usr/bin/env python3
"""Validate the desktop-guidance requirement matrix stays auditable."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "materials/evidence/requirement-matrix.md"
SOURCE_STATUS_PATH = ROOT / "materials/evidence/desktop-guidance-source-status.md"

STAGE_TOKENS = {
    "stage_a_bluelm": (
        "Stage A - BlueLM Credible Evidence",
        "BLUELM_ADAPTER_METRIC 8/8",
        "MODEL_CONTRACT_STRICT_METRIC 10/10",
        "MODEL_EVAL_METRIC 110/110",
        "PASS secret_hygiene",
        "provider=bluelm",
        "result_schema_valid=true",
        "thinking.type",
        "enable_thinking",
        "requestId",
        "request_id",
    ),
    "stage_b_cloud_device": (
        "Stage B - Cloud-Device And HTTPS Backend",
        "scripts/prepare_cloud_device_evidence.py",
        "scripts/test_preflight_cloud_backend.py",
        "CLOUD_BACKEND_PREFLIGHT_METRIC",
        "CLOUD_DEVICE_PREP_METRIC 5/5",
        "CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9",
        "docs/server-deployment-runbook.md",
        "CLOUD_BACKEND_READY_METRIC 9/9",
        "http_server_smoke_metric=1/1",
        "https://roky.chat",
        "https://api.roky.chat",
        "/etc/shike/shike-backend.env",
        "/opt/shike/backend",
        "CLOUD_DEVICE_PACKAGE_METRIC 30/30",
        "ANDROID16_REAL_IMPLEMENTATION_GUIDE_METRIC 12/12",
        "ANDROID16_DOD_COVERAGE_METRIC 28/28",
        "RELEASE_HANDOFF_CHECKS_METRIC 24/24",
        "LIVE_SMOKE_EVIDENCE_METRIC 7/7",
        "RELEASE_BLOCKING_REPORT_METRIC 8/8",
        "LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7",
        "01-cloud-install-open.mp4",
        "09-cloud-final-route.mp4",
        "TBD",
    ),
    "stage_c_frontend": (
        "Stage C - Frontend Productization",
        "HomeActionScreen",
        "CaptureHubScreen",
        "ParseConfirmScreen",
        "ActionPlanScreen",
        "InboxScreen",
        "PrivacySettingsScreen",
        "DebugDemoScreen",
        "LocalMultimodalStatus",
        "ShikeDesignTokens",
        "FrontendStateComponents",
        "FRONTEND_POLISH_METRIC 12/12",
        "ANDROID_STRUCTURE_METRIC 31/31",
        "ANDROID_UNIT_TEST_METRIC 86/86",
    ),
    "stage_d_inbox": (
        "Stage D - Long-Lived Inbox Workbench",
        "InboxDatabase.kt",
        "InboxEntities.kt",
        "InboxItemEntity",
        "CaptureDraftEntity",
        "ActionDraftEntity",
        "ExecutionResultEntity",
        "InboxSeedFactory.kt",
        "LegacyInboxSnapshot.kt",
        "INBOX_WORKBENCH_LANDING_METRIC 12/12",
        "REAL_WORLD_READY_METRIC 22/22",
    ),
    "stage_e_materials": (
        "Stage E - Materials Upgraded To Release Evidence",
        "materials/evidence/release-evidence-index.md",
        "materials/evidence/desktop-guidance-source-status.md",
        "materials/evidence/blocking-report.md",
        "materials/submission-checklist.md",
        "materials/device-demo-checklist.md",
        "docs/delivery-boundary-and-scoring.md",
        "docs/current-validation-status.md",
        "Guide header is anchored to `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md`",
        "DELIVERABLES_METRIC 10/10",
        "RELEASE_EVIDENCE_INDEX_METRIC 10/10",
        "REQUIREMENT_MATRIX_METRIC 9/9",
        "LANDING_RELEASE_CANDIDATE_METRIC 63/63",
    ),
}

REQUIRED_COMMANDS = (
    "python3 shike/validation/validate_secret_hygiene.py",
    "python3 shike/validation/validate_bluelm_adapter.py",
    "python3 shike/validation/validate_model_contract_strict.py",
    "python3 shike/backend/verify_backend.py",
    "python3 shike/backend/shike_backend/eval/run_model_eval.py --progress-every 25",
    "python3 shike/scripts/prepare_cloud_device_evidence.py",
    "python3 shike/scripts/test_collect_cloud_device_evidence.py",
    "python3 shike/validation/validate_live_smoke_evidence.py",
    "python3 shike/scripts/run_release_handoff_checks.py --strict",
    "python3 shike/validation/validate_android16_real_implementation_guide.py",
    "python3 shike/validation/validate_android16_definition_of_done.py",
    "python3 shike/validation/validate_cloud_backend_ready.py",
    "python3 shike/validation/validate_cloud_device_package.py",
    "python3 shike/validation/validate_release_blocking_report.py",
    "python3 shike/validation/validate_landing_release_candidate.py --strict",
    "python3 shike/validation/validate_frontend_polish.py",
    "python3 shike/validation/validate_android_structure.py",
    "python3 shike/validation/validate_android_unit_tests.py",
    "python3 shike/validation/validate_demo_acceptance.py",
    "python3 shike/validation/validate_inbox_workbench_landing.py",
    "python3 shike/validation/validate_real_world_ready.py",
    "python3 shike/validation/validate_deliverables.py",
    "python3 shike/validation/validate_release_evidence_index.py",
    "python3 shike/validation/validate_landing_release_candidate.py",
)

BLOCKER_TOKENS = (
    "strict cloud-device release evidence is still blocked",
    "Strict blockers that must remain explicit",
    "Missing 9 real cloud-device MP4 recordings",
    "cloud-device-test-report.md",
    "TBD",
    "Pre-recording Evidence Gate",
    "All 9 real cloud-device MP4 files",
    "no placeholder fields remain after capture",
    "Do not mark strict release complete",
    "desktop guidance source",
    "restored",
    "AppKEY",
    "backend token",
    "full OCR text",
)

REQUIRED_FILES = (
    "README.md",
    "backend/requirements.txt",
    "backend/shike_backend/adapters/bluelm_adapter.py",
    "docs/bluelm-integration-runbook.md",
    "docs/device-runbook.md",
    "materials/evidence/cloud-device/backend-redacted-access-log.txt",
    "materials/evidence/cloud-device/cloud-device-test-report.md",
    "materials/evidence/blocking-report.md",
    "materials/evidence/release-evidence-index.md",
    "materials/evidence/desktop-guidance-source-status.md",
    "android-mvp/app/src/main/java/cn/shike/app/ui/MainFlowScreens.kt",
    "android-mvp/app/src/main/java/cn/shike/app/ui/DebugDemoScreen.kt",
    "android-mvp/app/src/main/java/cn/shike/app/data/InboxDatabase.kt",
    "android-mvp/app/src/main/java/cn/shike/app/data/InboxEntities.kt",
    "docs/delivery-boundary-and-scoring.md",
    "docs/current-validation-status.md",
)

ENTRYPOINT_TOKENS = (
    "python3 shike/validation/validate_requirement_matrix.py",
    "REQUIREMENT_MATRIX_METRIC 9/9",
)

CURRENT_STATUS_TOKENS = (
    "Guide: `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md`",
    "materials/evidence/desktop-guidance-source-status.md",
    "currently readable",
    "Desktop guidance stages A-E",
    "materials/evidence/requirement-matrix.md",
    "REQUIREMENT_MATRIX_METRIC 9/9",
)


def read_matrix() -> str:
    """Read the matrix text.

    Returns:
        UTF-8 matrix text, or an empty string when absent.
    """

    if not MATRIX_PATH.is_file():
        return ""
    return MATRIX_PATH.read_text(encoding="utf-8")


def read(relative: str) -> str:
    """Read a repository file.

    Args:
        relative: Repository-relative file path.

    Returns:
        UTF-8 text, or an empty string when absent.
    """

    path = ROOT / relative
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def source_status_is_current() -> bool:
    """Check that the desktop source file is readable and explicitly documented.

    Returns:
        True when the status note exists and records the current source-file availability.
    """

    source_path = Path("/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md")
    text = read("materials/evidence/desktop-guidance-source-status.md")
    source_text = source_path.read_text(encoding="utf-8", errors="replace") if source_path.is_file() else ""
    return source_path.is_file() and all(
        token in text
        for token in (
            "/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md",
            "restored and readable",
            "20,950-byte",
            "$RUY975C.md",
            "Default local release gates prove",
        )
    ) and all(
        token in source_text
        for token in (
            "现在的拾刻已经不是“原型阶段”",
            "BlueLM 接入仍需实测闭环",
            "云真机还缺 HTTPS 后端和录屏证据",
            "HomeActionScreen",
            "Room / SQLite",
            "interface OcrEngine",
            "source_type",
        )
    )


def main() -> int:
    """Run matrix checks.

    Returns:
        0 when every desktop guidance stage is traceable to evidence and blockers.
    """

    text = read_matrix()
    checks: list[tuple[str, bool, str]] = [
        ("requirement_matrix_exists", bool(text), str(MATRIX_PATH.relative_to(ROOT))),
        (
            "lists_all_guidance_stages",
            all(f"Stage {letter}" in text for letter in ("A", "B", "C", "D", "E")),
            "Stage A-E",
        ),
        (
            "lists_stage_evidence_tokens",
            all(all(token in text for token in tokens) for tokens in STAGE_TOKENS.values()),
            "stage evidence tokens",
        ),
        ("lists_required_commands", all(command in text for command in REQUIRED_COMMANDS), "validation commands"),
        ("keeps_strict_blockers_explicit", all(token in text for token in BLOCKER_TOKENS), "strict blockers"),
        (
            "references_existing_files",
            all((ROOT / relative).is_file() for relative in REQUIRED_FILES),
            "referenced evidence files",
        ),
        (
            "lists_public_entrypoints",
            all(token in read("README.md") for token in ENTRYPOINT_TOKENS)
            and all(token in read("docs/current-validation-status.md") for token in ENTRYPOINT_TOKENS),
            "README.md + docs/current-validation-status.md",
        ),
        (
            "current_status_names_desktop_guidance",
            all(token in read("docs/current-validation-status.md") for token in CURRENT_STATUS_TOKENS)
            and SOURCE_STATUS_PATH.is_file()
            and source_status_is_current()
            and "SHIKE_ADVANCED_DEVELOPMENT_OPTIMIZATION_GUIDE.md" not in read("docs/current-validation-status.md").split("## Repository Structure Baseline", 1)[0],
            "docs/current-validation-status.md guide + source status",
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
    print(f"REQUIREMENT_MATRIX_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
