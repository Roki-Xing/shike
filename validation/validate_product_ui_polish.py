#!/usr/bin/env python3
"""Validate user-facing Shike UI is product-like rather than debug-like."""

from __future__ import annotations

import subprocess
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    """Read a UTF-8 project file.

    Args:
        relative: Path under the Shike root.

    Returns:
        File content.
    """

    return (ROOT / relative).read_text(encoding="utf-8")


def command_passes(command: list[str]) -> bool:
    """Run a command from the Android project root.

    Args:
        command: Gradle command argv.

    Returns:
        True when the command exits successfully.
    """

    result = subprocess.run(
        command,
        cwd=ROOT / "android-mvp",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=180,
    )
    if result.stdout.strip():
        print(result.stdout.strip())
    return result.returncode == 0


def target_unit_tests_pass() -> bool:
    """Run or read target Android unit-test results."""

    gradle = shutil.which("gradle")
    if gradle:
        return command_passes(
            [
                gradle,
                "--no-daemon",
                "testDebugUnitTest",
                "--tests",
                "cn.shike.app.ActionCardUiModelTest",
                "--tests",
                "cn.shike.app.PreparationCalendarReminderTest",
                "--tests",
                "cn.shike.app.data.InitialSelectionMapperTest",
            ]
        )
    required = [
        "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.ActionCardUiModelTest.xml",
        "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.PreparationCalendarReminderTest.xml",
        "android-mvp/app/build/test-results/testDebugUnitTest/TEST-cn.shike.app.data.InitialSelectionMapperTest.xml",
    ]
    for relative in required:
        path = ROOT / relative
        if not path.is_file():
            return False
        suite = ET.fromstring(path.read_text(encoding="utf-8"))
        if int(suite.attrib.get("failures", "0")) or int(suite.attrib.get("errors", "0")):
            return False
    return True


def main() -> int:
    """Run product UI polish checks."""

    main_sources = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "android-mvp/app/src/main/java/cn/shike/app").rglob("*.kt")
        if path.name
        not in {
            "DebugDemoScreen.kt",
            "ReadinessSections.kt",
            "LocalMultimodalRuntime.kt",
            "BackendEndpointControls.kt",
        }
    )
    home_agenda = read("android-mvp/app/src/main/java/cn/shike/app/ui/HomeAgendaList.kt")
    initial_mapper = read("android-mvp/app/src/main/java/cn/shike/app/data/InitialSelectionMapper.kt")
    structured_card = read("android-mvp/app/src/main/java/cn/shike/app/ui/StructuredActionCard.kt")
    parse_confirm = read("android-mvp/app/src/main/java/cn/shike/app/ui/ParseConfirmPanel.kt")
    model_client = read("android-mvp/app/src/main/java/cn/shike/app/data/ModelApiClient.kt")
    risk_panel = read("android-mvp/app/src/main/java/cn/shike/app/ui/ReviewRiskChecklist.kt")
    notification = read("android-mvp/app/src/main/java/cn/shike/app/system/ScreenshotNotification.kt")
    tests = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "android-mvp/app/src/test/java/cn/shike/app").rglob("*.kt")
    )

    forbidden_user_copy = [
        "今日行动台空状态",
        "今日行动台错误状态",
        "空状态",
        "错误状态",
        "ocr_evidence_repair",
        "schema_valid",
        "manual_review",
        "/v2/analyze-image",
        "MockModelAdapter",
        "validate_",
    ]
    checks = [
        (
            "home_empty_and_error_copy_user_friendly",
            "今天还没有待处理事项" in home_agenda
            and "把截图交给拾刻，生成第一张行动卡" in home_agenda
            and "AI 暂时没识别成功" in home_agenda
            and "截图已保存为待确认" in home_agenda
            and "今天还没有待处理事项" in initial_mapper
            and all(token not in home_agenda + initial_mapper for token in ["今日行动台空状态", "今日行动台错误状态"]),
        ),
        (
            "ordinary_user_sources_hide_engineering_terms",
            all(token not in main_sources for token in forbidden_user_copy),
        ),
        (
            "structured_card_has_product_sections",
            all(token in structured_card for token in ["事项", "时间", "地点", "准备事项", "建议动作", "需要确认"]),
        ),
        (
            "risk_panel_uses_need_confirmation_only",
            "需要确认" in risk_panel and "风险" not in risk_panel and "缺失字段" not in risk_panel,
        ),
        (
            "ocr_and_explanation_are_collapsible",
            "查看识别原文" in parse_confirm and "为什么这样判断" in parse_confirm and "rememberSaveable" in parse_confirm,
        ),
        (
            "model_client_does_not_store_risk_prefix_for_ui",
            '"风险：$it"' not in model_client and "需要确认：" in model_client,
        ),
        (
            "screenshot_notification_is_main_entry_copy",
            "检测到截图，是否交给拾刻？" in notification and "交给拾刻" in notification and "忽略" in notification,
        ),
        (
            "unit_tests_cover_product_copy_and_preparation",
            all(
                token in tests
                for token in [
                    "actionCardUiModelFrom_surfacesPreparationAsPrimarySectionAndMapsWarnings",
                    "calendarDraft_includesPreparationItemsInDescription",
                    "scheduledReminder_includesPreparationItemsInDetail",
                    "initialSelectionMapper_usesUserFacingHomeCopy",
                ]
            ),
        ),
        (
            "gradle_target_tests_pass",
            target_unit_tests_pass(),
        ),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"PRODUCT_UI_POLISH_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
