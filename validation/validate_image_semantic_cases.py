#!/usr/bin/env python3
"""Validate synthetic image-semantic cases for Android 16 multimodal parsing."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "validation/fixtures/image_cases.json"

REQUIRED_COUNTS = {
    "course_notice": 8,
    "assignment_deadline": 6,
    "event_poster": 6,
    "meeting_notice": 5,
    "interview_notice": 4,
    "travel_ticket": 4,
    "low_quality_fragment": 4,
    "negative_fragment": 3,
}
VALID_ACTIONS = {"calendar", "reminder", "map"}
VALID_SOURCES = {"screenshot_share", "photo_picker", "camera", "recent_screenshot_assist"}
REQUIRED_NEGATIVE_IDS = {"img-negative-001", "img-negative-002", "img-negative-003"}
REQUIRED_EXPECTED_KEYS = {
    "must_not_extract_status_bar_time",
    "title_contains",
    "time_required",
    "location_required",
    "actions",
}
FORBIDDEN_TOKENS = {"10:28", "100%", "09:50", "AppKEY", "sk-"}
NEGATIVE_REQUIRED_MISSING_FIELDS = {"task", "time", "location"}


def load_cases() -> list[dict[str, object]]:
    """Load image semantic cases.

    Returns:
        Parsed case dictionaries.
    """

    data = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("image_cases.json must contain a JSON list")
    return data


def has_required_shape(case: dict[str, object]) -> bool:
    """Return whether one image case has the public manifest shape."""

    expected = case.get("expected")
    return (
        all(key in case for key in ("id", "scene", "source_type", "image_fixture", "ocr_text_hint", "expected"))
        and isinstance(case.get("id"), str)
        and isinstance(case.get("scene"), str)
        and case.get("source_type") in VALID_SOURCES
        and isinstance(case.get("image_fixture"), str)
        and str(case.get("image_fixture", "")).startswith("validation/fixtures/images/")
        and isinstance(case.get("ocr_text_hint"), str)
        and isinstance(expected, dict)
        and REQUIRED_EXPECTED_KEYS.issubset(expected)
        and isinstance(expected.get("actions"), list)
    )


def negative_case_has_ui_boundary(case: dict[str, object]) -> bool:
    """Return whether a negative screenshot case guards UI chrome extraction.

    Args:
        case: One image semantic case.

    Returns:
        True when the negative case explicitly prevents app/navigation/status
        UI from becoming an action card.
    """

    expected = case.get("expected")
    if not isinstance(expected, dict):
        return False
    missing_fields = expected.get("missing_fields", [])
    title_terms = expected.get("forbidden_title_terms", [])
    location_terms = expected.get("forbidden_location_terms", [])
    evidence_regions = expected.get("forbidden_evidence_regions", [])
    return (
        case.get("scene") == "negative_fragment"
        and expected.get("actions") == []
        and expected.get("output_scene") == "unknown"
        and isinstance(missing_fields, list)
        and NEGATIVE_REQUIRED_MISSING_FIELDS.issubset(set(missing_fields))
        and isinstance(title_terms, list)
        and len(title_terms) >= 1
        and isinstance(location_terms, list)
        and len(location_terms) >= 1
        and isinstance(evidence_regions, list)
        and "top_status_bar" in evidence_regions
        and "bottom_navigation_bar" in evidence_regions
    )


def synthetic_descriptor_matches_case(case: dict[str, object]) -> bool:
    """Return whether the referenced synthetic descriptor exists and matches.

    Args:
        case: One image semantic case.

    Returns:
        True when the descriptor file is present and contains the case's
        identifying fields plus the OCR hint.
    """

    relative = case.get("image_fixture")
    if not isinstance(relative, str):
        return False
    path = ROOT / relative
    if not path.is_file() or path.stat().st_size == 0:
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(
        token in text
        for token in (
            f"id: {case.get('id')}",
            f"scene: {case.get('scene')}",
            f"source_type: {case.get('source_type')}",
            "fixture_type: synthetic_descriptor",
            str(case.get("ocr_text_hint")),
        )
    )


def main() -> int:
    """Run image semantic case checks."""

    if not CASES_PATH.is_file():
        print("FAIL\timage_cases_manifest_exists\tvalidation/fixtures/image_cases.json")
        print("IMAGE_SEMANTIC_CASES_METRIC\t0/9")
        return 1

    cases = load_cases()
    ids = [str(case.get("id", "")) for case in cases]
    scenes = Counter(str(case.get("scene", "")) for case in cases)
    action_values = {
        action
        for case in cases
        for action in case.get("expected", {}).get("actions", [])  # type: ignore[union-attr]
        if isinstance(case.get("expected"), dict)
    }
    all_text = json.dumps(cases, ensure_ascii=False)

    checks = [
        ("case_count_at_least_40", len(cases) >= 40, str(len(cases))),
        ("unique_case_ids", len(ids) == len(set(ids)), str(len(set(ids)))),
        ("required_scene_distribution", all(scenes[scene] >= count for scene, count in REQUIRED_COUNTS.items()), str(dict(scenes))),
        ("required_case_shape", all(isinstance(case, dict) and has_required_shape(case) for case in cases), "shape"),
        ("expected_actions_are_known", action_values.issubset(VALID_ACTIONS), ",".join(sorted(action_values))),
        (
            "negative_cases_have_no_actions",
            REQUIRED_NEGATIVE_IDS.issubset(set(ids))
            and all(
                negative_case_has_ui_boundary(case)
                for case in cases
                if case.get("scene") == "negative_fragment"
            ),
            "negative_fragment + own-ui/navigation/status guards",
        ),
        (
            "status_bar_guard_present",
            all(case.get("expected", {}).get("must_not_extract_status_bar_time") is True for case in cases),  # type: ignore[union-attr]
            "must_not_extract_status_bar_time",
        ),
        (
            "synthetic_fixture_paths_only",
            all(
                str(case.get("image_fixture", "")).endswith(".synthetic.txt")
                and synthetic_descriptor_matches_case(case)
                for case in cases
            ),
            "synthetic descriptors present and aligned",
        ),
        (
            "no_secret_or_fake_chrome_literal",
            not any(token in all_text for token in FORBIDDEN_TOKENS),
            "redaction",
        ),
    ]

    passed = sum(1 for _, ok, _ in checks if ok)
    for name, ok, evidence in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}\t{evidence}")
    print(f"IMAGE_SEMANTIC_CASES_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
