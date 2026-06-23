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
    header = read_ui("ParseConfirmHeader.kt")
    evidence = read("android-mvp/app/src/main/java/cn/shike/app/domain/ActionCardEvidence.kt")
    preparation_parser = read("android-mvp/app/src/main/java/cn/shike/app/domain/PreparationItemParser.kt")
    api_client = read("android-mvp/app/src/main/java/cn/shike/app/data/ModelApiClient.kt")
    model_test = read("android-mvp/app/src/test/java/cn/shike/app/ActionCardUiModelTest.kt")
    flexible_test = read("android-mvp/app/src/test/java/cn/shike/app/FlexibleActionCardTest.kt")
    image_test = read("android-mvp/app/src/test/java/cn/shike/app/data/AnalyzeImageApiClientTest.kt")

    checks = [
        ("action_card_model_present", "data class ActionCardUiModel" in model and "actionCardUiModelFrom" in model),
        ("model_extracts_structured_evidence", all(token in model + evidence for token in ["任务：", "需要确认："])),
        ("model_cleans_null_copy", "equals(\"null\", ignoreCase = true)" in model and "split(\" / \")" in model),
        ("model_has_preparation_and_user_warnings", "preparationItems" in model and "userWarnings" in model and "sourceTextPreview" in model),
        (
            "structured_card_fields_present",
            all(token in structured for token in [
                "ActionCardHero(",
                "PreparationSection(",
                "SuggestedPlanSection(",
                "ConfirmationSection(",
                "事项",
                "准备事项",
                "建议动作",
                "需要确认",
            ]),
        ),
        ("structured_card_hides_raw_risk_labels", "风险" not in structured and "缺失项" not in structured),
        ("confirm_panel_uses_structured_card", "StructuredActionCard(" in confirm and "model = actionCard" in confirm and "来源文本" not in confirm),
        ("api_maps_task_preparation_risk_missing", all(token in api_client for token in ["任务：$it", "准备：", "需要确认："])),
        ("unit_tests_cover_null_and_evidence", "ActionCardUiModelTest" in model_test and "contains(\"null\"" in model_test),
        (
            "ui_uses_confidence_status_not_fixed_decimal",
            "confidenceStatus" in model
            and "confidenceStatus" in header
            and "字段状态" in header
            and "置信度 ${if" not in header
            and "0.91" not in model + header + structured + confirm
            and "0.94" not in model + header + structured + confirm,
        ),
        (
            "flexible_tests_cover_preparation_noise_and_confidence",
            flexible_test.count("@Test") >= 3
            and "actionCardUiModel_rejectsPreparationNoiseFromScreenshotChrome" in flexible_test
            and "带6 标题 2026 23:04 0.20 KB" in flexible_test
            and "带准考证" in flexible_test
            and "confidenceStatus" in model_test
            and "0.91" in model_test
            and "0.94" in model_test,
        ),
        (
            "preparation_parser_rejects_screenshot_chrome_noise",
            all(
                token in preparation_parser
                for token in [
                    "isScreenshotChromeNoise",
                    "hasFileMetadata",
                    "hasClockLikeText",
                    "hasLongNumericRun",
                ]
            )
            and all(token in preparation_parser for token in ["准考证", "学生证"])
            and "preparationItemsFromText(item.rawText)" in evidence
            and "item.title" not in evidence.split("fun preparationItemsFrom(item: ShikeItem): List<String> =", 1)[1].split("/**", 1)[0],
        ),
        ("image_mapping_test_covers_deadline_null", "JSONObject.NULL" in image_test and "assertFalse(item.time.contains(\"null\"))" in image_test),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"STRUCTURED_ACTION_CARD_UI_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
