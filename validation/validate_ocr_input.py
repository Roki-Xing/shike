#!/usr/bin/env python3
"""Validate editable OCR text flow from capture to backend analysis."""

from __future__ import annotations

import subprocess
from pathlib import Path

from source_tree import read_android_source

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    """Read a UTF-8 text file under `shike`.

    Args:
        relative: File path under `shike`.

    Returns:
        File content.
    """

    return (ROOT / relative).read_text(encoding="utf-8")


def command_passes(command: list[str]) -> bool:
    """Run a command from the workspace root and return its pass status.

    Args:
        command: Command and arguments.

    Returns:
        True when the command exits with status code 0.
    """

    result = subprocess.run(command, cwd=ROOT.parent, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return result.returncode == 0


def main() -> int:
    android_source = read_android_source(ROOT)
    docs = "\n".join(
        read(path)
        for path in [
            "docs/android-mvp-implementation.md",
            "docs/device-runbook.md",
            "README.md",
        ]
    )

    checks = [
        ("model_bridge_checks_pass", command_passes(["python3", "shike/validation/validate_model_bridge.py"])),
        ("outlined_text_field_imported", "OutlinedTextField" in android_source),
        ("ocr_draft_state_present", "var ocrDraft by remember" in android_source),
        ("ocr_draft_label_visible", "OCR 文本草稿" in android_source),
        ("ocr_draft_edit_handler_present", "onOcrDraftChange" in android_source),
        ("backend_uses_ocr_draft", "textForAnalyze = backendAnalyzeText(ocrDraft, fallback)" in android_source and "fun backendAnalyzeText(" in android_source),
        ("call_analyze_uses_text_for_analyze", "callAnalyzeApi(endpoint, sourceType, textForAnalyze" in android_source),
        ("gallery_populates_ocr_draft", "相册 OCR 草稿" in android_source),
        ("camera_populates_ocr_draft", "相机 OCR 草稿" in android_source),
        (
            "fallback_preserves_edited_text",
            "fun backendFailureOutcome(" in android_source
            and "redactSensitiveLogText(textForAnalyze)" in android_source
            and "后端不可用，已回退本地 MockModelAdapter" in android_source,
        ),
        ("persist_selection_updates_draft", "ocrDraft = item.rawText" in android_source),
        ("ocr_input_documented", "OCR 文本草稿" in docs and "编辑" in docs and "/v1/analyze" in docs),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"OCR_INPUT_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
