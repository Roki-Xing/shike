#!/usr/bin/env python3
"""Validate field-level repair affordances in the action-card review flow."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI_ROOT = ROOT / "android-mvp/app/src/main/java/cn/shike/app/ui"


def read(relative: str) -> str:
    """Read a UTF-8 UI source file.

    Args:
        relative: File path under the Android UI source root.

    Returns:
        File content.
    """

    return (UI_ROOT / relative).read_text(encoding="utf-8")


def main() -> int:
    """Run field-level editing checks.

    Returns:
        Process exit code.
    """

    parse_confirm = read("ParseConfirmPanel.kt")
    structured_card = read("StructuredActionCard.kt")
    review_edit = read("ReviewEditSheet.kt")

    checks = [
        (
            "action_card_exposes_field_edit_callbacks",
            all(token in structured_card for token in [
                "onEditTime",
                "onEditLocation",
                "onEditPreparation",
                "onEditSourceText",
            ]),
        ),
        (
            "action_card_has_field_level_buttons",
            all(token in structured_card for token in ["改时间", "改地点", "改准备", "改原文"])
            and "FieldEditRow(" in structured_card,
        ),
        (
            "parse_confirm_tracks_edit_target",
            "enum class ReviewEditTarget" in parse_confirm
            and "var editTarget" in parse_confirm
            and all(token in parse_confirm for token in [
                "ReviewEditTarget.Time",
                "ReviewEditTarget.Location",
                "ReviewEditTarget.Preparation",
                "ReviewEditTarget.SourceText",
            ]),
        ),
        (
            "parse_confirm_default_form_collapsed",
            "ReviewEditSheet(" in parse_confirm
            and "editTarget != ReviewEditTarget.None" in parse_confirm
            and "OutlinedTextField(" not in parse_confirm,
        ),
        (
            "review_edit_sheet_is_targeted",
            "target: ReviewEditTarget" in review_edit
            and "when (target)" in review_edit
            and all(token in review_edit for token in ["只改时间", "只改地点", "只改准备事项", "修改原文并重新生成"]),
        ),
        (
            "source_text_edit_can_regenerate",
            "draftSourceText" in parse_confirm
            and "onRegenerateFromSource" in review_edit
            and "重新生成行动卡" in review_edit,
        ),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"FIELD_LEVEL_EDITING_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
