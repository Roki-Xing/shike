#!/usr/bin/env python3
"""Validate risk and missing-field copy is user friendly."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    """Read a UTF-8 project file."""

    return (ROOT / relative).read_text(encoding="utf-8")


def main() -> int:
    """Run risk-copy checks.

    Returns:
        Process exit code.
    """

    evidence = read("android-mvp/app/src/main/java/cn/shike/app/domain/ActionCardEvidence.kt")
    model = read("android-mvp/app/src/main/java/cn/shike/app/ui/ActionCardUiModel.kt")
    structured = read("android-mvp/app/src/main/java/cn/shike/app/ui/StructuredActionCard.kt")
    risk_panel = read("android-mvp/app/src/main/java/cn/shike/app/ui/ReviewRiskChecklist.kt")
    test = read("android-mvp/app/src/test/java/cn/shike/app/FlexibleActionCardTest.kt")

    checks = [
        ("risk_tokens_are_mapped_in_domain_layer", all(token in evidence for token in ["relative_time", "location_low_confidence", "missing_location", "missing_exact_time", "provider_error", "manual_review", "schema_valid"])),
        ("risk_copy_uses_user_language", all(token in evidence for token in ["时间来自“明天/今晚”等相对表达，请确认日期", "地点识别不够确定，请确认", "还缺地点，暂不能打开地图", "还缺具体时间，暂不能加入日历", "AI 暂时不可用，已保留待确认卡", "待你确认"])),
        ("model_exposes_user_warnings", "val userWarnings: List<String>" in model and "userWarningsFrom(risks + missingFields)" in model),
        ("structured_card_uses_need_confirmation", "需要确认" in structured and "model.userWarnings" in structured and "风险" not in structured and "缺失项" not in structured),
        ("risk_panel_only_renders_when_needed", "if (warnings.isEmpty()) return" in risk_panel and "需要确认" in risk_panel and "风险与缺失字段" not in risk_panel),
        ("unit_test_blocks_engineering_warning_copy", "schema_valid" in test and "provider_error" in test and "manual_review" in test and "assertFalse(model.userWarnings.any" in test),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"RISK_COPY_USER_FRIENDLY_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
