#!/usr/bin/env python3
"""Validate that `/v1/analyze` source_type matches all product entry points."""

from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


EXPECTED_SOURCE_TYPES = {"screenshot", "camera", "share_text", "manual"}


def read(relative: str) -> str:
    """Read a UTF-8 file under the Shike repository.

    Args:
        relative: Repository-relative path.

    Returns:
        File content.
    """

    return (ROOT / relative).read_text(encoding="utf-8")


def request_source_type(relative: str) -> str:
    """Read a contract sample request source_type.

    Args:
        relative: Repository-relative JSON path.

    Returns:
        The sample request `source_type`.
    """

    return str(json.loads(read(relative))["source_type"])


def analyze_request_source_type_values() -> set[str]:
    """Extract the Pydantic AnalyzeRequest source_type Literal values.

    Returns:
        The literal values accepted by `AnalyzeRequest.source_type`.
    """

    module = ast.parse(read("backend/shike_backend/schemas.py"))
    for node in module.body:
        if isinstance(node, ast.ClassDef) and node.name == "AnalyzeRequest":
            for stmt in node.body:
                if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name) and stmt.target.id == "source_type":
                    annotation = stmt.annotation
                    if isinstance(annotation, ast.Subscript) and isinstance(annotation.value, ast.Name) and annotation.value.id == "Literal":
                        values_node = annotation.slice
                        if isinstance(values_node, ast.Tuple):
                            return {value.value for value in values_node.elts if isinstance(value, ast.Constant)}
                        if isinstance(values_node, ast.Constant):
                            return {str(values_node.value)}
    return set()


def main() -> int:
    """Run source_type contract checks.

    Returns:
        Process exit code.
    """

    schemas = read("backend/shike_backend/schemas.py")
    backend_smoke = read("backend/verify_backend.py")
    capture_mapper = read("android-mvp/app/src/main/java/cn/shike/app/data/CaptureImportMapper.kt")
    backend_runner = read("android-mvp/app/src/main/java/cn/shike/app/data/BackendAnalysisRunner.kt")
    shike_app = read("android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt")
    model_api_test = read("android-mvp/app/src/test/java/cn/shike/app/ModelApiClientTest.kt")
    capture_test = read("android-mvp/app/src/test/java/cn/shike/app/data/CaptureImportMapperTest.kt")
    backend_runner_test = read("android-mvp/app/src/test/java/cn/shike/app/BackendAnalysisRunnerTest.kt")
    adapter_doc = read("contracts/model-adapter.md")
    android_doc = read("docs/android-mvp-implementation.md")
    device_runbook = read("docs/device-runbook.md")
    bluelm_runbook = read("docs/bluelm-integration-runbook.md")

    sample_sources = {
        request_source_type("contracts/sample-course-request.json"),
        request_source_type("contracts/sample-event-request.json"),
        request_source_type("contracts/sample-share-text-request.json"),
        request_source_type("contracts/sample-manual-request.json"),
    }

    checks = [
        ("analyze_request_accepts_all_source_types", analyze_request_source_type_values() == EXPECTED_SOURCE_TYPES),
        ("analyze_request_forbids_extra_fields", 'model_config = ConfigDict(extra="forbid")' in schemas),
        ("backend_smoke_covers_share_text", '"source_type": "share_text"' in backend_smoke and "sample-share-001" in backend_smoke),
        ("backend_smoke_covers_manual", '"source_type": "manual"' in backend_smoke and "sample-manual-001" in backend_smoke),
        ("contract_samples_cover_all_source_types", sample_sources == EXPECTED_SOURCE_TYPES),
        (
            "android_capture_source_mapping_present",
            "fun backendSourceTypeFromCaptureSource" in capture_mapper
            and '"share_text"' in capture_mapper
            and '"manual"' in capture_mapper
            and '"camera"' in capture_mapper
            and '"screenshot"' in capture_mapper,
        ),
        (
            "android_backend_uses_current_draft_source",
            "backendAnalysisInputForCurrentDraft(" in shike_app
            and "captureSource = captureSource" in shike_app
            and "fallback = selected" in shike_app
            and "imageUri = imageUri" in shike_app
            and "allowCloudImage = allowCloudImageForPreference(localMultimodalPreference)" in shike_app
            and "fun backendAnalysisInputForCurrentDraft" in backend_runner
            and "backendSourceTypeFromCaptureSource(captureSource)" in backend_runner,
        ),
        (
            "android_unit_tests_cover_new_sources",
            "buildAnalyzeRequestPayload_acceptsShareTextAndManualSourceTypes" in model_api_test
            and "backendSourceTypeFromCaptureSource_mapsAllProductEntrypoints" in capture_test
            and "backendAnalysisInputForCurrentDraft_usesCaptureSourceSpecificBackendType" in backend_runner_test,
        ),
        (
            "docs_list_source_type_contract",
            all(source in adapter_doc for source in EXPECTED_SOURCE_TYPES)
            and all(source in android_doc for source in EXPECTED_SOURCE_TYPES)
            and all(source in device_runbook for source in EXPECTED_SOURCE_TYPES)
            and all(source in bluelm_runbook for source in EXPECTED_SOURCE_TYPES),
        ),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"BACKEND_SOURCE_TYPE_CONTRACT_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
