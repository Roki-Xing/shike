#!/usr/bin/env python3
"""Validate flexible preparation item extraction for action cards."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    """Read a UTF-8 project file.

    Args:
        relative: File path under the Shike root.

    Returns:
        File content.
    """

    return (ROOT / relative).read_text(encoding="utf-8")


def main() -> int:
    """Run preparation-item source checks.

    Returns:
        Process exit code.
    """

    evidence = read("android-mvp/app/src/main/java/cn/shike/app/domain/ActionCardEvidence.kt")
    model = read("android-mvp/app/src/main/java/cn/shike/app/ui/ActionCardUiModel.kt")
    api = read("android-mvp/app/src/main/java/cn/shike/app/data/ModelApiClient.kt")
    mock = read("backend/shike_backend/adapters/mock_adapter.py")
    prompt = read("backend/shike_backend/prompts/analyze_system_prompt.txt")
    image_prompt = read("backend/shike_backend/prompts/analyze_image_system_prompt.txt")
    test = read("android-mvp/app/src/test/java/cn/shike/app/FlexibleActionCardTest.kt")

    sample_inputs = [
        "明天早上九点上英语口语教室E520，记得带书",
        "今晚七点组会腾讯会议，提前准备周报",
        "明天下午三点实验课，带实验报告和学生证",
        "周五十点面试，提前十分钟上线",
    ]
    sample_outputs = ["带书", "提前准备周报", "带实验报告", "带学生证", "提前十分钟上线"]

    checks = [
        ("domain_preparation_parser_present", "fun preparationItemsFromText(text: String)" in evidence),
        ("domain_covers_common_extra_actions", all(token in evidence for token in ["记得带", "提前准备", "先去?签到", "课前交", "不要迟到", "集合"])),
        ("parser_splits_multiple_carry_items", "prepSeparators" in evidence and "带$it" in evidence),
        ("action_card_has_preparation_items_field", "val preparationItems: List<String>" in model and "preparationItemsFrom(item)" in model),
        ("title_cleanup_keeps_extra_action_out", "stripPreparationFromTitle" in model and "courseTitleFromEvidence" in model),
        ("api_accepts_future_preparation_fields", all(token in api for token in ["preparation_items", "checklist_items", "准备："])),
        ("mock_title_extracts_course_subject", "上([\\u4e00-\\u9fa5A-Za-z0-9]{1,16}?)" in mock and "subject}课" in mock),
        ("prompts_preserve_extra_actions", all(token in prompt + image_prompt for token in ["记得带书", "提前准备周报", "不要塞进 title"])),
        ("unit_test_covers_required_inputs", all(token in test for token in sample_inputs)),
        ("unit_test_covers_required_outputs", all(token in test for token in sample_outputs)),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"FLEXIBLE_ACTION_ITEM_EXTRACTION_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
