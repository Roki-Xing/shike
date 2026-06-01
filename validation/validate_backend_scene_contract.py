#!/usr/bin/env python3
"""Validate `/v1/analyze` response contract stays in sync across repo layers.

This guard intentionally keeps the public response contract conservative:
- response `scene_type` only allows: course_notice / event_poster / unknown
- response `task.topic` only allows: course / event / unknown

Extended regression groups (assignment/meeting/interview/travel) are still
supported as *input hints* and evaluation categories, but must map to
`scene_type=unknown` in the current contract.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_SCENES = {
    "course_notice",
    "event_poster",
    "unknown",
}
EXPECTED_TOPICS = {"course", "event", "unknown"}

# Still allowed as request `scene_hint` values (and as regression case categories),
# but not allowed in the public response schema.
EXTENDED_HINTS = {"assignment_deadline", "meeting_notice", "interview_notice", "travel_ticket"}


def read(relative: str) -> str:
    """Read a UTF-8 file under the Shike repository.

    Args:
        relative: Repository-relative path.

    Returns:
        File content.
    """

    return (ROOT / relative).read_text(encoding="utf-8")


def read_json(relative: str) -> object:
    """Read a JSON file under the Shike repository."""

    return json.loads(read(relative))


def literal_values(class_name: str, field_name: str) -> set[str]:
    """Extract a field's Literal values from backend schemas.py.

    Args:
        class_name: Pydantic class name.
        field_name: Annotated field name.

    Returns:
        Literal values as strings.
    """

    module = ast.parse(read("backend/shike_backend/schemas.py"))
    for node in module.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for stmt in node.body:
                if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name) and stmt.target.id == field_name:
                    return annotation_literal_values(stmt.annotation)
    return set()


def annotation_literal_values(node: ast.AST) -> set[str]:
    """Return Literal string values from an annotation node."""

    if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) and node.value.id == "Literal":
        values_node = node.slice
        if isinstance(values_node, ast.Tuple):
            return {value.value for value in values_node.elts if isinstance(value, ast.Constant)}
        if isinstance(values_node, ast.Constant):
            return {str(values_node.value)}
    return set()


def response_scene(relative: str) -> str:
    """Read scene_type from a response sample."""

    return str(read_json(relative)["scene_type"])  # type: ignore[index]


def request_scene_hint(relative: str) -> str:
    """Read scene_hint from a request sample."""

    return str(read_json(relative)["scene_hint"])  # type: ignore[index]


def main() -> int:
    """Run scene contract checks."""

    schema = read_json("contracts/model-output.schema.json")
    schema_scenes = set(schema["properties"]["scene_type"]["enum"])  # type: ignore[index]
    schema_topics = set(schema["properties"]["task"]["properties"]["topic"]["enum"])  # type: ignore[index]
    mock_adapter = read("backend/shike_backend/adapters/mock_adapter.py")
    backend_smoke = read("backend/verify_backend.py")
    android_source = read("android-mvp/app/src/main/java/cn/shike/app/data/ModelApiClient.kt")
    android_test = read("android-mvp/app/src/test/java/cn/shike/app/ModelApiClientTest.kt")
    eval_cases = read("validation/regression-cases.json")
    eval_validator = read("validation/validate_model_eval_cases.py")
    adapter_doc = read("contracts/model-adapter.md")

    response_samples = {
        response_scene("contracts/sample-course-response.json"),
        response_scene("contracts/sample-event-response.json"),
        response_scene("contracts/sample-assignment-response.json"),
        response_scene("contracts/sample-meeting-response.json"),
        response_scene("contracts/sample-interview-response.json"),
        response_scene("contracts/sample-travel-ticket-response.json"),
    }
    request_samples = {
        request_scene_hint("contracts/sample-course-request.json"),
        request_scene_hint("contracts/sample-event-request.json"),
        request_scene_hint("contracts/sample-assignment-request.json"),
        request_scene_hint("contracts/sample-meeting-request.json"),
        request_scene_hint("contracts/sample-interview-request.json"),
        request_scene_hint("contracts/sample-travel-ticket-request.json"),
    }

    def has_unknown_assert_for(hint: str) -> bool:
        token = f'\"scene_hint\": \"{hint}\"'
        index = backend_smoke.find(token)
        if index == -1:
            return False
        # The smoke test should explicitly assert these map to unknown near the request.
        window = backend_smoke[index : index + 1200]
        return "== \"unknown\"" in window

    checks = [
        ("schema_scene_enum_complete", schema_scenes == EXPECTED_SCENES),
        ("schema_topic_enum_complete", schema_topics == EXPECTED_TOPICS),
        ("pydantic_scene_literal_matches_schema", literal_values("AnalyzeResponse", "scene_type") == EXPECTED_SCENES),
        ("pydantic_topic_literal_matches_schema", literal_values("TaskPayload", "topic") == EXPECTED_TOPICS),
        (
            "mock_adapter_handles_extended_hints",
            all(hint in mock_adapter for hint in EXTENDED_HINTS)
            and all(token not in mock_adapter for token in [f'scene_type=\"{hint}\"' for hint in EXTENDED_HINTS]),
        ),
        (
            "backend_smoke_covers_extended_hints_as_unknown",
            all(has_unknown_assert_for(hint) for hint in EXTENDED_HINTS),
        ),
        (
            "contract_samples_cover_extended_hints_as_unknown",
            EXTENDED_HINTS.issubset(request_samples) and response_samples == EXPECTED_SCENES,
        ),
        (
            "android_maps_extended_scene_hints",
            all(hint in android_source for hint in EXTENDED_HINTS),
        ),
        (
            "android_unit_tests_cover_extended_scene_hints",
            "buildAnalyzeRequestPayload_mapsExtendedSceneHints" in android_test and all(hint in android_test for hint in EXTENDED_HINTS),
        ),
        (
            "model_eval_cases_use_contract_scene_names",
            "travel_ticket" in eval_cases
            and "travel_plan" not in eval_cases
            and all(hint in eval_validator for hint in EXTENDED_HINTS),
        ),
        (
            "adapter_doc_notes_conservative_contract",
            "仅允许 `course_notice`、`event_poster`、`unknown`" in adapter_doc and "scene_type=unknown" in adapter_doc,
        ),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"BACKEND_SCENE_CONTRACT_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
