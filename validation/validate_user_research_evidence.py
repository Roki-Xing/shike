#!/usr/bin/env python3
"""Validate Shike user-research evidence stays honest and traceable."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PLAN = ROOT / "docs/user-research-plan.md"
SUMMARY = ROOT / "docs/user-interview-summary.md"
SCORING_MAP = ROOT / "materials/evidence/scoring-evidence-map.md"
DELIVERY_SCORING = ROOT / "docs/delivery-boundary-and-scoring.md"
SUBMISSION = ROOT / "materials/submission-checklist.md"
TRACEABILITY = ROOT / "validation/traceability.md"


def read(path: Path) -> str:
    """Read a UTF-8 text file.

    Args:
        path: Absolute project file path.

    Returns:
        UTF-8 text, or empty text when absent.
    """

    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def has_all(text: str, tokens: tuple[str, ...]) -> bool:
    """Return whether every required token appears in text."""

    return all(token in text for token in tokens)


def main() -> int:
    """Run user-research evidence checks."""

    plan = read(PLAN)
    summary = read(SUMMARY)
    scoring_map = read(SCORING_MAP)
    delivery = read(DELIVERY_SCORING)
    submission = read(SUBMISSION)
    traceability = read(TRACEABILITY)
    combined = "\n".join([plan, summary, scoring_map, delivery, submission, traceability])

    checks = [
        (
            "research_files_exist",
            PLAN.is_file() and SUMMARY.is_file() and SCORING_MAP.is_file(),
            "docs/user-research-plan.md + docs/user-interview-summary.md + materials/evidence/scoring-evidence-map.md",
        ),
        (
            "plan_covers_target_segments",
            has_all(
                plan,
                (
                    "College students",
                    "Club or event organizers",
                    "Interns or young professionals",
                    "Frequent event or travel users",
                    "Total planned sample: 10 participants",
                ),
            ),
            "target segments",
        ),
        (
            "plan_tracks_required_metrics",
            has_all(
                plan,
                (
                    "Screenshot task count in last 7 days",
                    "Tasks manually converted to calendar/reminder/map",
                    "Missed or delayed actions caused by saved images",
                    "Willingness to try confirmable action cards",
                    "Privacy preference",
                    "Wrong-action concern",
                ),
            ),
            "survey metrics",
        ),
        (
            "summary_is_template_not_fake_results",
            has_all(summary, ("planned template", "待采集", "Do not fabricate interview data", "does not yet prove"))
            and "Real target users have validated" in summary
            and "planned" in summary,
            "summary boundary",
        ),
        (
            "scoring_map_links_value_gap",
            has_all(
                scoring_map,
                (
                    "Application value",
                    "30%",
                    "USER_RESEARCH_EVIDENCE_METRIC 8/8",
                    "LANDING_RELEASE_CANDIDATE_METRIC 63/63",
                    "Real interviews and survey metrics are 待采集",
                    "Do not fabricate interview data",
                    "materials/evidence/release-evidence-index.md",
                ),
            ),
            "scoring map",
        ),
        (
            "public_materials_reference_research_gate",
            has_all(
                delivery + "\n" + submission + "\n" + traceability,
                (
                    "docs/user-research-plan.md",
                    "docs/user-interview-summary.md",
                    "materials/evidence/scoring-evidence-map.md",
                    "USER_RESEARCH_EVIDENCE_METRIC 8/8",
                    "待采集",
                    "SHIKE-075",
                ),
            ),
            "delivery + submission + traceability",
        ),
        (
            "no_fake_completion_language",
            not any(
                phrase in combined
                for phrase in (
                    "已完成访谈",
                    "真实访谈已完成",
                    "用户已验证",
                    "validated by real users",
                    "fieldwork complete",
                )
            ),
            "no fabricated completion wording",
        ),
        (
            "does_not_embed_secret_like_value",
            re.search(r"\bsk-[A-Za-z0-9_\-]{12,}\b", combined) is None
            and "AppKEY" in combined
            and "backend tokens" in combined,
            "secret-safe text",
        ),
    ]

    passed = sum(1 for _, ok, _ in checks if ok)
    for name, ok, evidence in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}\t{evidence}")
    print(f"USER_RESEARCH_EVIDENCE_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
