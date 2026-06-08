#!/usr/bin/env python3
"""Validate the synthetic model evaluation case set."""

from __future__ import annotations

import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "validation/regression-cases.json"
WORKSPACE = ROOT.parent

REQUIRED_SCENES = {
    "course_notice",
    "event_poster",
    "meeting_notice",
    "assignment_deadline",
    "interview_notice",
    "travel_ticket",
    "low_quality_fragment",
    "negative_fragment",
}
REQUIRED_EDGE_KEYWORDS = ("低质量", "缺失", "相对", "反例")
VALID_ACTIONS = {"calendar", "reminder", "map"}


def command_passes(command: list[str]) -> bool:
    """Run a validation command from the workspace root."""

    result = subprocess.run(command, cwd=WORKSPACE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return result.returncode == 0


def load_cases() -> list[dict[str, object]]:
    """Load model evaluation cases.

    Returns:
        Parsed JSON case dictionaries.
    """

    data = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("regression-cases.json must contain a JSON list")
    return data


def has_required_shape(item: dict[str, object]) -> bool:
    """Check one case has the required public contract fields.

    Args:
        item: One model evaluation case.

    Returns:
        True when the case has the required shape.
    """

    required = ["id", "scene", "input", "expected_fields", "expected_actions", "edge"]
    return all(key in item for key in required) and isinstance(item.get("input"), str)


def main() -> int:
    """Run the model evaluation case-set checks.

    Returns:
        Process exit code.
    """

    cases = load_cases()
    ids = [str(item.get("id", "")) for item in cases]
    scenes = Counter(str(item.get("scene", "")) for item in cases)
    edges = " ".join(str(item.get("edge", "")) for item in cases)
    action_values = {
        action
        for item in cases
        for action in item.get("expected_actions", [])
        if isinstance(item.get("expected_actions"), list)
    }

    checks = [
        ("case_count_at_least_110", len(cases) >= 110, str(len(cases))),
        ("unique_case_ids", len(ids) == len(set(ids)), str(len(set(ids)))),
        ("required_scene_coverage", REQUIRED_SCENES.issubset(scenes), ",".join(sorted(scenes))),
        ("balanced_core_scenes", all(scenes[scene] >= 10 for scene in REQUIRED_SCENES), str(dict(scenes))),
        ("required_case_shape", all(has_required_shape(item) for item in cases), "shape"),
        ("low_quality_missing_relative_negative_edges", all(token in edges for token in REQUIRED_EDGE_KEYWORDS), edges),
        ("expected_actions_are_known", action_values.issubset(VALID_ACTIONS), ",".join(sorted(action_values))),
        (
            "negative_cases_have_no_actions",
            all(item.get("expected_actions") == [] for item in cases if item.get("scene") == "negative_fragment"),
            "negative_fragment",
        ),
        (
            "image_semantic_cases_pass",
            command_passes(["python3", "shike/validation/validate_image_semantic_cases.py"]),
            "IMAGE_SEMANTIC_CASES_METRIC 9/9",
        ),
    ]

    passed = sum(1 for _, ok, _ in checks if ok)
    for name, ok, evidence in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}\t{evidence}")
    print(f"MODEL_EVAL_CASES_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
