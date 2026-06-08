#!/usr/bin/env python3
"""Validate Shike's landing release-candidate readiness.

Default mode is a local, reproducible gate. It proves the repository has a
coherent release-candidate package without requiring live BlueLM credentials or
cloud-device access.

Strict mode keeps the same local checks and adds external-evidence blockers:
real BlueLM success evidence and real cloud-device recordings. When strict
evidence is missing, the script writes ``materials/evidence/blocking-report.md``.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
BLOCKING_REPORT = ROOT / "materials/evidence/blocking-report.md"
CLOUD_EVIDENCE = ROOT / "materials/evidence/cloud-device"
REQUIRED_CLOUD_VIDEOS = [
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


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    evidence: str


_COMMAND_CACHE: dict[tuple[str, ...], bool] = {}


def read(relative: str) -> str:
    """Read a UTF-8 file under the Shike root.

    Args:
        relative: Repository-relative file path.

    Returns:
        File content, or an empty string when the file is absent.
    """

    path = ROOT / relative
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def file_nonempty(relative: str) -> bool:
    """Check that a repository file exists and is non-empty.

    Args:
        relative: Repository-relative file path.

    Returns:
        True when the path is a non-empty file.
    """

    path = ROOT / relative
    return path.is_file() and path.stat().st_size > 0


def command_passes(command: list[str]) -> bool:
    """Run and cache a local validation command.

    Args:
        command: Command list executed from the workspace root.

    Returns:
        True when the command exits with code 0.
    """

    key = tuple(command)
    if key not in _COMMAND_CACHE:
        result = subprocess.run(
            command,
            cwd=WORKSPACE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        _COMMAND_CACHE[key] = result.returncode == 0
    return _COMMAND_CACHE[key]


def contains_all(text: str, tokens: list[str] | tuple[str, ...]) -> bool:
    """Check whether all tokens are present in text."""

    return all(token in text for token in tokens)


def regression_case_count() -> int:
    """Return the number of model regression cases."""

    cases_path = ROOT / "validation/regression-cases.json"
    if not cases_path.is_file():
        return 0
    data = json.loads(cases_path.read_text(encoding="utf-8"))
    return len(data) if isinstance(data, list) else 0


def build_local_checks() -> list[Check]:
    """Build the 63 local release-candidate checks.

    Returns:
        Check objects grouped by release surface.
    """

    readme = read("README.md")
    status = read("docs/current-validation-status.md")
    landing_guide = read("docs/SHIKE_LANDING_APP_OPTIMIZATION_GUIDE.md")
    goal_mode_guide = read("docs/CODEX_GOAL_MODE_OPTIMIZATION_GUIDE.md")
    runbook = read("docs/device-runbook.md")
    android_doc = read("docs/android-mvp-implementation.md")
    bluelm_doc = read("docs/bluelm-integration-runbook.md")
    scoring = read("docs/delivery-boundary-and-scoring.md")
    model_report = read("docs/model-eval-report.md")
    contract = read("contracts/model-output.schema.json")
    requirements = read("backend/requirements.txt")
    settings = read("backend/shike_backend/settings.py")
    backend_main = read("backend/shike_backend/main.py")
    adapter = read("backend/shike_backend/adapters/bluelm_adapter.py")
    ocr_engine = read("android-mvp/app/src/main/java/cn/shike/app/data/OcrEngine.kt")
    capture_mapper = read("android-mvp/app/src/main/java/cn/shike/app/data/CaptureImportMapper.kt")
    share_mapper = read("android-mvp/app/src/main/java/cn/shike/app/data/ShareImportMapper.kt")
    main_flow = read("android-mvp/app/src/main/java/cn/shike/app/ui/MainFlowScreens.kt")
    debug_screen = read("android-mvp/app/src/main/java/cn/shike/app/ui/DebugDemoScreen.kt")
    inbox_database = read("android-mvp/app/src/main/java/cn/shike/app/data/InboxDatabase.kt")
    inbox_entities = read("android-mvp/app/src/main/java/cn/shike/app/data/InboxEntities.kt")
    cloud_report = read("materials/evidence/cloud-device/cloud-device-test-report.md")
    cloud_log = read("materials/evidence/cloud-device/backend-redacted-access-log.txt")
    cloud_package_readme = read("materials/evidence/cloud-device/README.md")
    demo_checklist = read("materials/device-demo-checklist.md")
    submission = read("materials/submission-checklist.md")
    demo_script = read("materials/demo-script.md")
    deck = read("materials/preliminary-deck.md")
    prototype = read("prototype/demo.html")
    delivery_tree = landing_guide.split("## 13. 最终交付包建议", 1)[-1].split("## 14.", 1)[0]
    landing_guide_current = (
        "当前本地门禁总分 63 项" in landing_guide
        and "LANDING_RELEASE_CANDIDATE_METRIC 63/63" in landing_guide
        and "validate_backend_audit_log.py" in landing_guide
        and "BACKEND_AUDIT_LOG_METRIC 8/8" in landing_guide
        and "validate_live_smoke_evidence.py" in landing_guide
        and "LIVE_SMOKE_EVIDENCE_METRIC 7/7" in landing_guide
        and "validate_android_image_preprocess.py" in landing_guide
        and "ANDROID_IMAGE_PREPROCESS_METRIC 15/15" in landing_guide
        and "validate_no_default_image_upload.py" in landing_guide
        and "LANDING_RELEASE_CANDIDATE_METRIC 50/50" not in landing_guide
        and "validate_capture_ocr_pipeline.py" not in landing_guide
        and "validate_landing_materials.py" not in landing_guide
        and "validate_ocr_engine_layer.py" in landing_guide
        and "validate_ocr_input.py" in landing_guide
        and "validate_deliverables.py" in landing_guide
        and "validate_release_evidence_index.py" in landing_guide
        and "RELEASE_EVIDENCE_INDEX_METRIC 10/10" in landing_guide
        and "docs/optimization-log.md" in landing_guide
        and "README 公开入口" in landing_guide
        and "validation/traceability.md" in landing_guide
        and "SHIKE-070" in landing_guide
        and "prepare_cloud_device_evidence.py" in landing_guide
        and "CLOUD_DEVICE_PREP_METRIC 5/5" in landing_guide
        and "CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9" in landing_guide
        and "CLOUD_DEVICE_PACKAGE_METRIC 30/30" in landing_guide
        and "LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7" in landing_guide
        and "validate_cloud_device_package.py --strict" in landing_guide
        and "validate_release_blocking_report.py" in landing_guide
        and "materials/evidence/blocking-report.md" in landing_guide
        and "materials/evidence/release-evidence-index.md" in landing_guide
        and "/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md" in landing_guide
        and "materials/evidence/requirement-matrix.md" in landing_guide
        and "REQUIREMENT_MATRIX_METRIC 9/9" in landing_guide
        and "Pre-recording Evidence Gate" in landing_guide
        and "all 9 real cloud-device MP4 files" in landing_guide
        and "no placeholder fields remain after capture" in landing_guide
        and "validate_demo_acceptance.py" in delivery_tree
        and "validate_real_world_ready.py" in delivery_tree
        and "validate_release_blocking_report.py" in delivery_tree
        and "validate_release_evidence_index.py" in delivery_tree
        and "validate_deliverables.py" in delivery_tree
        and "docs/blocking-report.md" not in landing_guide
        and "docs/delivery-boundary-and-scoring.md" in landing_guide
        and "materials/demo-script.md" in landing_guide
        and "materials/preliminary-deck.md" in landing_guide
        and "materials/submission-checklist.md" in landing_guide
        and "cloud-device-test-report.md" in delivery_tree
        and "backend-redacted-access-log.txt" in delivery_tree
        and "apk-sha256.txt" in delivery_tree
        and "shike_backend/main.py" in delivery_tree
        and "shike_backend/adapters/" in delivery_tree
        and "shike_backend/prompts/" in delivery_tree
        and "scoring-evidence-map.md" not in landing_guide
        and "final-demo-script.md" not in landing_guide
        and "landing-deck-outline.md" not in landing_guide
        and "docs/cloud-device-test-report.md" not in landing_guide
        and "docs/privacy-and-security.md" not in landing_guide
        and "\n    main.py" not in delivery_tree
        and "env.example" not in delivery_tree
    )
    goal_mode_guide_current = (
        "android-mvp/app/src/androidTest/" not in goal_mode_guide
        and "docs/device-runbook.md" in goal_mode_guide
        and "materials/device-demo-checklist.md" in goal_mode_guide
    )

    command_checks = [
        Check("secret_hygiene_passes", command_passes(["python3", "shike/validation/validate_secret_hygiene.py"]), "validate_secret_hygiene.py"),
        Check("bluelm_adapter_passes", command_passes(["python3", "shike/validation/validate_bluelm_adapter.py"]), "validate_bluelm_adapter.py"),
        Check("vivo_ocr_adapter_passes", command_passes(["python3", "shike/validation/validate_vivo_ocr_adapter.py"]), "validate_vivo_ocr_adapter.py"),
        Check("vivo_multimodal_contract_passes", command_passes(["python3", "shike/validation/validate_vivo_multimodal_contract.py"]), "validate_vivo_multimodal_contract.py"),
        Check("cloud_backend_ready_passes", command_passes(["python3", "shike/validation/validate_cloud_backend_ready.py"]), "validate_cloud_backend_ready.py"),
        Check("backend_audit_log_passes", command_passes(["python3", "shike/validation/validate_backend_audit_log.py"]), "validate_backend_audit_log.py"),
        Check("model_contract_strict_passes", command_passes(["python3", "shike/validation/validate_model_contract_strict.py"]), "validate_model_contract_strict.py"),
        Check("backend_smoke_passes", command_passes(["python3", "shike/backend/verify_backend.py"]), "verify_backend.py"),
        Check("no_sample_contamination_passes", command_passes(["python3", "shike/validation/validate_no_sample_contamination.py"]), "validate_no_sample_contamination.py"),
        Check("no_default_image_upload_passes", command_passes(["python3", "shike/validation/validate_no_default_image_upload.py"]), "validate_no_default_image_upload.py"),
        Check("android_image_preprocess_passes", command_passes(["python3", "shike/validation/validate_android_image_preprocess.py"]), "validate_android_image_preprocess.py"),
        Check("screenshot_assist_passes", command_passes(["python3", "shike/validation/validate_screenshot_assist.py"]), "validate_screenshot_assist.py"),
        Check("screenshot_cleanup_passes", command_passes(["python3", "shike/validation/validate_screenshot_cleanup.py"]), "validate_screenshot_cleanup.py"),
        Check("user_facing_copy_passes", command_passes(["python3", "shike/validation/validate_user_facing_copy.py"]), "validate_user_facing_copy.py"),
        Check("home_one_screen_passes", command_passes(["python3", "shike/validation/validate_home_one_screen.py"]), "validate_home_one_screen.py"),
        Check("model_eval_cases_pass", command_passes(["python3", "shike/validation/validate_model_eval_cases.py"]), "validate_model_eval_cases.py"),
        Check("android_structure_passes", command_passes(["python3", "shike/validation/validate_android_structure.py"]), "validate_android_structure.py"),
        Check("android_unit_tests_pass", command_passes(["python3", "shike/validation/validate_android_unit_tests.py"]), "validate_android_unit_tests.py"),
        Check("frontend_polish_passes", command_passes(["python3", "shike/validation/validate_frontend_polish.py"]), "validate_frontend_polish.py"),
        Check("ocr_engine_layer_passes", command_passes(["python3", "shike/validation/validate_ocr_engine_layer.py"]), "validate_ocr_engine_layer.py"),
        Check("ocr_input_passes", command_passes(["python3", "shike/validation/validate_ocr_input.py"]), "validate_ocr_input.py"),
        Check("inbox_workbench_landing_passes", command_passes(["python3", "shike/validation/validate_inbox_workbench_landing.py"]), "validate_inbox_workbench_landing.py"),
        Check("action_execution_passes", command_passes(["python3", "shike/validation/validate_action_execution.py"]), "validate_action_execution.py"),
        Check("today_ranking_passes", command_passes(["python3", "shike/validation/validate_today_ranking.py"]), "validate_today_ranking.py"),
        Check("product_beta_strict_passes", command_passes(["python3", "shike/validation/validate_advanced_product_beta.py", "--strict"]), "validate_advanced_product_beta.py --strict"),
        Check("real_world_ready_passes", command_passes(["python3", "shike/validation/validate_real_world_ready.py"]), "validate_real_world_ready.py"),
        Check("landable_passes", command_passes(["python3", "shike/validation/validate_landable.py"]), "validate_landable.py"),
        Check("demo_acceptance_passes", command_passes(["python3", "shike/validation/validate_demo_acceptance.py"]), "validate_demo_acceptance.py"),
        Check("cloud_device_package_passes", command_passes(["python3", "shike/validation/validate_cloud_device_package.py"]), "validate_cloud_device_package.py"),
        Check("release_blocking_report_passes", command_passes(["python3", "shike/validation/validate_release_blocking_report.py"]), "validate_release_blocking_report.py"),
        Check("release_evidence_index_passes", command_passes(["python3", "shike/validation/validate_release_evidence_index.py"]), "validate_release_evidence_index.py"),
        Check("live_smoke_evidence_passes", command_passes(["python3", "shike/validation/validate_live_smoke_evidence.py"]), "validate_live_smoke_evidence.py"),
        Check("manual_review_passes", command_passes(["python3", "shike/validation/validate_manual_review.py"]), "validate_manual_review.py"),
        Check("backend_config_passes", command_passes(["python3", "shike/validation/validate_backend_config.py"]), "validate_backend_config.py"),
        Check("model_bridge_passes", command_passes(["python3", "shike/validation/validate_model_bridge.py"]), "validate_model_bridge.py"),
        Check("persistence_passes", command_passes(["python3", "shike/validation/validate_persistence.py"]), "validate_persistence.py"),
        Check("deliverables_pass", command_passes(["python3", "shike/validation/validate_deliverables.py"]), "validate_deliverables.py"),
        Check("spike_passes", command_passes(["python3", "shike/spike/run_spike.py", "--all"]), "run_spike.py --all"),
    ]

    local_checks = [
        Check("requirements_include_model_dependencies", "requests" in requirements and "jsonschema" in requirements, "backend/requirements.txt"),
        Check("bluelm_runbook_exists", file_nonempty("docs/bluelm-integration-runbook.md"), "docs/bluelm-integration-runbook.md"),
        Check("bluelm_runbook_secret_safe", contains_all(bluelm_doc, ("BLUELM_APP_ID", "BLUELM_APP_KEY", "Android", "不得")), "BlueLM env + Android boundary"),
        Check("adapter_supports_provider_switch", "SHIKE_MODEL_PROVIDER" in settings and "BlueLMModelAdapter" in backend_main, "provider switch"),
        Check("adapter_has_safe_fallback", "SHIKE_ALLOW_MOCK_FALLBACK" in settings and "MockModelAdapter" in backend_main, "mock fallback"),
        Check("adapter_uses_structured_prompt", "analyze_system_prompt.txt" in adapter and "analyze_user_template.txt" in adapter, "prompt files"),
        Check("schema_rejects_extra_fields", '"additionalProperties": false' in contract, "model-output.schema.json"),
        Check("regression_cases_at_least_110", regression_case_count() >= 110, f"{regression_case_count()} cases"),
        Check("model_eval_report_exists", file_nonempty("docs/model-eval-report.md") and "Model Eval Report" in model_report, "docs/model-eval-report.md"),
        Check("android_doc_has_ocr_layer", contains_all(android_doc, ("OCR 分层", "ManualOcrEngine", "MockOcrEngine", "CaptureDraft")), "docs/android-mvp-implementation.md"),
        Check("ocr_contracts_present", contains_all(ocr_engine, ("interface OcrEngine", "data class CaptureInput", "data class OcrResult")), "OcrEngine.kt"),
        Check("capture_draft_records_ocr_metadata", contains_all(capture_mapper, ("ocrText", "ocrConfidence", "ocrEngineName", "privacyLevel", "cloudAllowed", "imageCleared")), "CaptureDraft"),
        Check("share_text_disables_cloud_by_default", "ManualOcrEngine()" in share_mapper and "allowCloudEnhancement = false" in share_mapper, "ShareImportMapper.kt"),
        Check("frontend_has_real_screen_shells", contains_all(main_flow + debug_screen, ("HomeActionScreen", "CaptureHubScreen", "ParseConfirmScreen", "ActionPlanScreen", "InboxScreen", "PrivacySettingsScreen", "DebugDemoScreen")), "screen shells"),
        Check("debug_tools_not_on_home", "BackendEndpointControls" not in main_flow.split("fun CaptureHubScreen")[0] and "DebugDemoScreen" in debug_screen, "debug separation"),
        Check("inbox_sqlite_database_present", "SQLiteOpenHelper" in inbox_database and "inbox_items" in inbox_database, "InboxDatabase.kt"),
        Check("inbox_entities_present", contains_all(inbox_entities, ("InboxItemEntity", "CaptureDraftEntity", "ActionDraftEntity", "ExecutionResultEntity")), "InboxEntities.kt"),
        Check("cloud_runbook_separates_network_modes", contains_all(runbook, ("模拟器", "USB 真机", "云真机", "https://your-domain.example.com")), "docs/device-runbook.md"),
        Check("cloud_package_skeleton_exists", file_nonempty("materials/evidence/cloud-device/cloud-device-manifest.md") and file_nonempty("materials/evidence/cloud-device/cloud-device-test-report.md"), "cloud evidence skeleton"),
        Check("demo_checklist_has_recording_names", contains_all(demo_checklist, ("01-install-and-open.mp4", "06-delivery-readiness.mp4", "validate_real_world_ready.py")), "materials/device-demo-checklist.md"),
        Check("submission_checklist_exists", file_nonempty("materials/submission-checklist.md") and "device-demo-checklist.md" in submission, "materials/submission-checklist.md"),
        Check("scoring_map_exists", file_nonempty("docs/delivery-boundary-and-scoring.md") and contains_all(scoring, ("创新性", "应用价值", "大模型应用能力")), "docs/delivery-boundary-and-scoring.md"),
        Check("prototype_demo_console_lists_guards", "validate_landing_release_candidate.py" in prototype or "validate_real_world_ready.py" in prototype, "prototype/demo.html"),
        Check("readme_lists_release_candidate_gate", "validate_landing_release_candidate.py" in readme and "LANDING_RELEASE_CANDIDATE_METRIC 63/63" in readme, "README.md"),
        Check(
            "public_docs_list_release_candidate_gate",
            "validate_landing_release_candidate.py" in status
            and "LANDING_RELEASE_CANDIDATE_METRIC 63/63" in status
            and landing_guide_current
            and goal_mode_guide_current,
            "docs/current-validation-status.md + docs/SHIKE_LANDING_APP_OPTIMIZATION_GUIDE.md",
        ),
    ]

    checks = command_checks + local_checks
    if len(checks) != 63:
        raise AssertionError(f"release-candidate check count must stay 63, got {len(checks)}")
    return checks


def build_strict_blockers() -> list[Check]:
    """Build strict external-evidence checks.

    Returns:
        Checks that require credentials, hosted backend evidence, and real videos.
    """

    access_log = read("materials/evidence/cloud-device/backend-redacted-access-log.txt")
    logcat = read("materials/evidence/cloud-device/cloud-device-logcat.txt")
    report = read("materials/evidence/cloud-device/cloud-device-test-report.md")
    apk_sha = read("materials/evidence/cloud-device/apk-sha256.txt")
    return [
        Check("strict_cloud_device_package_passes", command_passes(["python3", "shike/validation/validate_cloud_device_package.py", "--strict"]), "validate_cloud_device_package.py --strict"),
        Check("strict_cloud_videos_present", all((CLOUD_EVIDENCE / name).is_file() and (CLOUD_EVIDENCE / name).stat().st_size > 0 for name in REQUIRED_CLOUD_VIDEOS), "9 cloud mp4 files"),
        Check("strict_report_has_no_tbd", not any(marker in report for marker in ("TBD", "待补录", "待采集", "TODO")), "cloud-device-test-report.md"),
        Check("strict_report_lists_video_evidence", "## Video Evidence" in report and all(name in report for name in REQUIRED_CLOUD_VIDEOS), "cloud-device-test-report.md video evidence"),
        Check("strict_logcat_not_placeholder", "placeholder" not in logcat.lower(), "cloud-device-logcat.txt"),
        Check("strict_apk_sha_valid", re.search(r"\b[a-fA-F0-9]{64}\b", apk_sha) is not None, "apk-sha256.txt"),
        Check("strict_bluelm_online_log_present", "provider=bluelm" in access_log and "result_schema_valid=true" in access_log, "backend-redacted-access-log.txt"),
    ]


def missing_cloud_videos() -> list[str]:
    """List required strict-mode cloud-device videos still missing."""

    return [
        name
        for name in REQUIRED_CLOUD_VIDEOS
        if not (CLOUD_EVIDENCE / name).is_file() or (CLOUD_EVIDENCE / name).stat().st_size == 0
    ]


def report_placeholder_lines(report: str) -> list[str]:
    """Return report lines that still contain placeholder markers."""

    markers = ("TBD", "待补录", "待采集", "TODO")
    return [line.strip() for line in report.splitlines() if any(marker in line for marker in markers)]


def write_blocking_report(blockers: list[Check]) -> None:
    """Write a strict-mode blocking report for missing external evidence."""

    missing = [check for check in blockers if not check.ok]
    missing_names = {check.name for check in missing}
    report = read("materials/evidence/cloud-device/cloud-device-test-report.md")
    missing_videos = missing_cloud_videos()
    placeholder_lines = report_placeholder_lines(report)
    lines = [
        "# Shike Release-Candidate Blocking Report",
        "",
        "Strict release mode is blocked by external evidence gaps. No secret values are required in this file.",
        "",
        "## Missing Evidence",
    ]
    for check in missing:
        lines.append(f"- `{check.name}`: {check.evidence}")

    if missing_videos:
        lines.extend(["", "## Missing Cloud Videos", ""])
        for name in missing_videos:
            lines.append(f"- [ ] `materials/evidence/cloud-device/{name}`")

    if placeholder_lines:
        lines.extend(["", "## Report Fields Still Placeholder", ""])
        for line in placeholder_lines:
            lines.append(f"- `{line}`")

    actions: list[str] = []
    if "strict_bluelm_online_log_present" in missing_names:
        actions.extend(
            [
                "Run the backend with real BlueLM credentials from local environment variables only.",
                "Capture a redacted backend log containing `provider=bluelm` and `result_schema_valid=true`.",
            ]
        )
    if "strict_cloud_videos_present" in missing_names or "strict_cloud_device_package_passes" in missing_names:
        actions.append("Record every missing MP4 listed above on a cloud device using a HTTPS backend URL.")
    if "strict_report_has_no_tbd" in missing_names or "strict_apk_sha_valid" in missing_names:
        actions.append("Fill every placeholder line in `cloud-device-test-report.md` with redacted real device evidence.")
    if "strict_report_lists_video_evidence" in missing_names:
        actions.append("Add a `## Video Evidence` section to `cloud-device-test-report.md` and list all 9 required MP4 filenames with redacted notes.")
    if "strict_logcat_not_placeholder" in missing_names:
        actions.append("Replace `cloud-device-logcat.txt` placeholder text with redacted session-level diagnostics from the actual cloud-device run.")
    if "strict_report_has_no_tbd" in missing_names or "strict_apk_sha_valid" in missing_names or "strict_report_lists_video_evidence" in missing_names:
        actions.append(
            "In the report's `Pre-recording Evidence Gate`, confirm the desktop guidance source, requirement matrix file, "
            "`REQUIREMENT_MATRIX_METRIC 9/9`, `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7`, all 9 real cloud-device MP4 files, and no placeholder fields remain after capture."
        )
        actions.append(
            "Refresh `apk-sha256.txt` and `cloud-device-capture-todo.md` with `python3 shike/scripts/prepare_cloud_device_evidence.py`, "
            "then confirm `CLOUD_DEVICE_PREP_METRIC 5/5` and the expected pre-capture state `CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9`."
        )
        actions.append("Rerun `python3 shike/validation/validate_cloud_device_package.py` so the non-strict package handoff remains at `CLOUD_DEVICE_PACKAGE_METRIC 30/30` before strict validation.")
        actions.append("Rerun `python3 shike/validation/validate_release_evidence_index.py` so the release evidence index still matches the refreshed cloud-device package.")
        actions.append("Rerun `python3 shike/validation/validate_requirement_matrix.py` so the desktop guidance stages A-E still map to refreshed cloud-device blockers.")
        actions.append(
            "Before recording, confirm `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md` is still the desktop guidance source and "
            "`materials/evidence/requirement-matrix.md` still passes `REQUIREMENT_MATRIX_METRIC 9/9`."
        )
    actions.append("Keep AppKEY, backend tokens, full OCR text, phone numbers, emails, and student IDs out of videos, logs, and filenames.")
    actions.append("Rerun `python3 shike/validation/validate_landing_release_candidate.py --strict`.")

    lines.extend(["", "## Required Next Actions", ""])
    for index, action in enumerate(actions, start=1):
        lines.append(f"{index}. {action}")
    BLOCKING_REPORT.parent.mkdir(parents=True, exist_ok=True)
    BLOCKING_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """Run the release-candidate validator."""

    parser = argparse.ArgumentParser(description="Validate Shike landing release-candidate readiness.")
    parser.add_argument("--strict", action="store_true", help="Require real BlueLM online evidence and cloud-device recordings.")
    args = parser.parse_args()

    checks = build_local_checks()
    passed = sum(1 for check in checks if check.ok)
    for check in checks:
        print(f"{'PASS' if check.ok else 'FAIL'}\t{check.name}\t{check.evidence}")
    print(f"LANDING_RELEASE_CANDIDATE_METRIC\t{passed}/{len(checks)}")

    if passed != len(checks):
        return 1

    if args.strict:
        strict_checks = build_strict_blockers()
        strict_passed = sum(1 for check in strict_checks if check.ok)
        for check in strict_checks:
            print(f"{'PASS' if check.ok else 'FAIL'}\t{check.name}\t{check.evidence}")
        print(f"LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE\t{strict_passed}/{len(strict_checks)}")
        if strict_passed != len(strict_checks):
            write_blocking_report(strict_checks)
            print(f"BLOCKING_REPORT\t{BLOCKING_REPORT.relative_to(ROOT)}")
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
