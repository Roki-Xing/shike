#!/usr/bin/env python3
"""Validate ordinary user UI hides backend/debug copy."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI_ROOT = ROOT / "android-mvp/app/src/main/java/cn/shike/app/ui"

USER_SCREEN_FILES = [
    "ShikeMainScreen.kt",
    "MainFlowScreens.kt",
    "MainScreenRoutes.kt",
    "HomeActionScreen.kt",
    "HomePendingReviewPanel.kt",
    "AnalyzeProgressPanel.kt",
    "StructuredActionCard.kt",
    "BottomNavigation.kt",
    "CaptureEntryPanel.kt",
    "OcrDraftEditor.kt",
    "HomeAgendaList.kt",
    "ParseConfirmPanel.kt",
    "ActionPlannerPanel.kt",
    "InboxPanel.kt",
    "ReviewRiskChecklist.kt",
]

FORBIDDEN_COPY = [
    "后端 /v2",
    "/v2/analyze-image",
    "/v1/analyze",
    "后端模型编排",
    "MockModelAdapter",
    "schema_valid",
    "manual_review",
    "provider_error",
    "risk code",
    "validate_",
]


def read(path: Path) -> str:
    """Read a UTF-8 source file."""

    return path.read_text(encoding="utf-8")


def main() -> int:
    """Run user-facing copy checks.

    Returns:
        Process exit code.
    """

    user_ui = "\n".join(read(UI_ROOT / path) for path in USER_SCREEN_FILES if (UI_ROOT / path).is_file())
    debug_ui = read(UI_ROOT / "DebugDemoScreen.kt")
    ocr_editor = read(UI_ROOT / "OcrDraftEditor.kt")
    evidence = read(ROOT / "android-mvp/app/src/main/java/cn/shike/app/domain/ActionCardEvidence.kt")

    checks = [
        ("ordinary_ui_hides_backend_and_provider_copy", all(token not in user_ui for token in FORBIDDEN_COPY)),
        ("debug_screen_can_keep_engineering_tools", "BackendEndpointControls" in debug_ui and "OfflineSampleActions" in debug_ui),
        ("ocr_editor_filters_debug_lines", "userVisibleOcrDraftText" in ocr_editor and "userVisibleEvidenceText(text)" in ocr_editor),
        ("evidence_filter_removes_backend_lines", all(token in evidence for token in ["startsWith(\"云端 ai 解析\")", "startsWith(\"后端\")", "manual_review", "provider"])),
        ("ordinary_ui_uses_product_copy", all(token in user_ui for token in ["识别到的文字", "准备事项", "需要确认", "生成行动卡"])),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"NO_BACKEND_COPY_IN_USER_UI_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
