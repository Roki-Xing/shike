#!/usr/bin/env python3
"""Validate structured action-card UI fields and null-safe display."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI_ROOT = ROOT / "android-mvp/app/src/main/java/cn/shike/app/ui"


def read_ui(relative: str) -> str:
    return (UI_ROOT / relative).read_text(encoding="utf-8")


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def main() -> int:
    model = read_ui("ActionCardUiModel.kt")
    structured = read_ui("StructuredActionCard.kt")
    confirm = read_ui("ParseConfirmPanel.kt")
    api_client = read("android-mvp/app/src/main/java/cn/shike/app/data/ModelApiClient.kt")
    model_test = read("android-mvp/app/src/test/java/cn/shike/app/ActionCardUiModelTest.kt")
    image_test = read("android-mvp/app/src/test/java/cn/shike/app/data/AnalyzeImageApiClientTest.kt")

    checks = [
        ("action_card_model_present", "data class ActionCardUiModel" in model and "actionCardUiModelFrom" in model),
        ("model_extracts_structured_evidence", all(token in model for token in ["任务：", "风险：", "待补："])),
        ("model_cleans_null_copy", "equals(\"null\", ignoreCase = true)" in model and "split(\" / \")" in model),
        ("structured_card_fields_present", all(token in structured for token in ["课程/事项", "时间", "地点", "任务", "风险", "缺失项"])),
        ("confirm_panel_uses_structured_card", "StructuredActionCard(actionCard)" in confirm and "来源文本" not in confirm),
        ("api_maps_task_risk_missing", all(token in api_client for token in ["任务：$it", "风险：$it", "待补：$it"])),
        ("unit_tests_cover_null_and_evidence", "ActionCardUiModelTest" in model_test and "contains(\"null\"" in model_test),
        ("image_mapping_test_covers_deadline_null", "JSONObject.NULL" in image_test and "assertFalse(item.time.contains(\"null\"))" in image_test),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"STRUCTURED_ACTION_CARD_UI_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
