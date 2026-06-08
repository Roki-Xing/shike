#!/usr/bin/env python3
"""Validate Android 16 real-implementation guide coverage.

This gate maps the desktop guide's P0/P1 task list to existing executable
validators and source-level evidence. It is intentionally an aggregate guard:
the detailed behavioral checks stay in the narrower validators it calls.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str


def read(relative: str) -> str:
    """Read a UTF-8 project file.

    Args:
        relative: File path under the Shike root.

    Returns:
        File content, or an empty string when absent.
    """

    path = ROOT / relative
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def command_passes(command: tuple[str, ...]) -> bool:
    """Run a child validator from the workspace root.

    Args:
        command: Command tuple to execute.

    Returns:
        True when the command exits successfully.
    """

    result = subprocess.run(
        command,
        cwd=WORKSPACE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return result.returncode == 0


def contains_all(text: str, tokens: tuple[str, ...]) -> bool:
    """Return whether every token appears in the text."""

    return all(token in text for token in tokens)


def main() -> int:
    """Run the Android 16 guide aggregate gate.

    Returns:
        Process exit code.
    """

    command_ok = {
        "no_fake_device_chrome": command_passes(("python3", "shike/validation/validate_no_fake_device_chrome.py")),
        "android16_screenshot_flow": command_passes(("python3", "shike/validation/validate_android16_screenshot_flow.py")),
        "no_default_image_upload": command_passes(("python3", "shike/validation/validate_no_default_image_upload.py")),
        "screenshot_cleanup": command_passes(("python3", "shike/validation/validate_screenshot_cleanup.py")),
        "vivo_multimodal_contract": command_passes(("python3", "shike/validation/validate_vivo_multimodal_contract.py")),
        "android_image_preprocess": command_passes(("python3", "shike/validation/validate_android_image_preprocess.py")),
        "action_execution": command_passes(("python3", "shike/validation/validate_action_execution.py")),
        "home_one_screen": command_passes(("python3", "shike/validation/validate_home_one_screen.py")),
        "screenshot_assist": command_passes(("python3", "shike/validation/validate_screenshot_assist.py")),
        "android_unit_tests": command_passes(("python3", "shike/validation/validate_android_unit_tests.py")),
    }

    capture_mapper = read("android-mvp/app/src/main/java/cn/shike/app/data/CaptureImportMapper.kt")
    ocr_engine = read("android-mvp/app/src/main/java/cn/shike/app/data/OcrEngine.kt")
    model_client = read("android-mvp/app/src/main/java/cn/shike/app/data/ModelApiClient.kt")
    backend_runner = read("android-mvp/app/src/main/java/cn/shike/app/data/BackendAnalysisRunner.kt")
    local_multimodal_runtime = read("android-mvp/app/src/main/java/cn/shike/app/data/LocalMultimodalRuntime.kt")
    local_multimodal_status = read("android-mvp/app/src/main/java/cn/shike/app/ui/LocalMultimodalStatus.kt")
    local_multimodal_test = read("android-mvp/app/src/test/java/cn/shike/app/data/LocalMultimodalRuntimeTest.kt")
    settings = read("android-mvp/app/src/main/java/cn/shike/app/ui/ReadinessSections.kt")
    docs = "\n".join(
        read(path)
        for path in (
            "README.md",
            "docs/current-validation-status.md",
            "docs/android-mvp-implementation.md",
            "materials/evidence/release-evidence-index.md",
        )
    )

    capture_draft_ok = (
        contains_all(
            capture_mapper + ocr_engine,
            (
                "data class CaptureDraft",
                "enum class CaptureSourceType",
                "ScreenshotCandidate",
                "Gallery",
                "Camera",
                "ShareText",
                "Manual",
                "sourceMediaStoreUri",
                "thumbnailUri",
                "deleteState",
                "ScreenshotDeleteState",
            ),
        )
        and command_ok["android_unit_tests"]
    )
    local_3b_ok = (
        contains_all(
            local_multimodal_status,
            (
                "端侧模型",
                "未安装",
                "可用",
                "初始化失败",
                "云端不可用时再启用",
            ),
        )
        and contains_all(
            local_multimodal_runtime,
            (
                "data class LocalMultimodalConfig",
                "val multimodal: Boolean = true",
                "interface LocalMultimodalEngine",
                "fun init(config: LocalMultimodalConfig): Int",
                "fun callVit(rgbBytes: ByteArray, width: Int, height: Int): Int",
                "fun generate(prompt: String): String",
                "looksSchemaValid",
                "用户确认前不可执行",
                "schema_valid",
            ),
        )
        and contains_all(
            local_multimodal_test,
            (
                "init(multimodal=true)",
                "callVit(width=1,height=2,bytes=6)",
                "generate(prompt_has_schema=true)",
                "local_schema_rejected",
                "B203",
                "18:30",
            ),
        )
        and command_ok["android_unit_tests"]
    )

    checks = [
        Check(
            "p0_001_no_fake_device_info",
            command_ok["no_fake_device_chrome"] and command_ok["android16_screenshot_flow"],
            "no fake time/battery/date, safeDrawing insets, no hand-drawn status row",
        ),
        Check(
            "p0_002_unified_capture_draft",
            capture_draft_ok,
            "ScreenshotShare/GalleryImage/CameraPhoto/ManualText share CaptureDraft with media uri, thumbnail, delete state",
        ),
        Check(
            "p0_003_image_share_import_no_auto_upload",
            command_ok["android16_screenshot_flow"]
            and command_ok["no_default_image_upload"]
            and contains_all(model_client + backend_runner, ("AnalyzeImageRequest", "allow_cloud_image", "imagePayload")),
            "image ACTION_SEND, Photo Picker, shared-image candidate, explicit analyze action before upload",
        ),
        Check(
            "p0_004_original_screenshot_delete",
            command_ok["screenshot_cleanup"],
            "MediaStore system confirmation, no silent delete, persisted cleanup status",
        ),
        Check(
            "p0_005_vivo_multimodal_backend_only",
            command_ok["vivo_multimodal_contract"]
            and "VIVO_MULTIMODAL_CONTRACT_METRIC 28/28" in docs
            and "Android still calls the Shike backend only" in docs,
            "/v2/analyze-image, image data URL, schema validation, backend-only provider secrets",
        ),
        Check(
            "p0_006_ocr_blocks_and_chrome_filtering",
            command_ok["vivo_multimodal_contract"] and command_ok["android_image_preprocess"],
            "vivo OCR blocks, ignored_regions, status/nav chrome filtering, screenshot crop policy",
        ),
        Check(
            "p0_007_real_calendar",
            command_ok["action_execution"],
            "confirmation gate, system calendar insert page, disabled without time",
        ),
        Check(
            "p0_008_real_notification_reminder",
            command_ok["action_execution"],
            "POST_NOTIFICATIONS fallback, AlarmManager scheduling, restore after restart/reboot",
        ),
        Check(
            "p0_009_real_map",
            command_ok["action_execution"],
            "confirmation gate, disabled without location, map fallback copies location",
        ),
        Check(
            "p0_010_home_slimming",
            command_ok["home_one_screen"],
            "single compact home import surface, no debug/backend controls on home, hidden developer entry",
        ),
        Check(
            "p1_011_recent_screenshot_assist",
            command_ok["screenshot_assist"]
            and command_ok["android16_screenshot_flow"]
            and contains_all(settings, ("最近截图助手", "不会自动上传")),
            "opt-in MediaStore assist, privacy copy, notification prompt, observer reset",
        ),
        Check(
            "p1_012_optional_local_3b_multimodal",
            local_3b_ok,
            "settings status plus init -> callVit -> generate -> schema-valid pending review boundary",
        ),
    ]

    passed = sum(1 for check in checks if check.ok)
    for check in checks:
        print(f"{'PASS' if check.ok else 'FAIL'}\t{check.name}\t{check.detail}")
    print(f"ANDROID16_REAL_IMPLEMENTATION_GUIDE_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
