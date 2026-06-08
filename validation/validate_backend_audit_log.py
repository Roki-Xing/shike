#!/usr/bin/env python3
"""Validate backend audit logs are metadata-only and secret-safe."""

from __future__ import annotations

import subprocess
import os
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "shike"


def read(relative: str) -> str:
    """Read a project file.

    Args:
        relative: Path under the Shike project root.

    Returns:
        UTF-8 file text.
    """

    return (ROOT / relative).read_text(encoding="utf-8")


def command_passes(command: list[str]) -> bool:
    """Run a command from the Shike root.

    Args:
        command: Command argv.

    Returns:
        True when the command exits successfully.
    """

    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "backend")
    result = subprocess.run(command, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if result.stdout.strip():
        print(result.stdout.strip())
    return result.returncode == 0


def main() -> int:
    """Run backend audit log checks."""

    audit_log = read("backend/shike_backend/audit_log.py")
    main_py = read("backend/shike_backend/main.py")
    test_file = read("backend/tests/test_audit_log_redaction.py")
    runbook = read("docs/server-deployment-runbook.md")

    forbidden_copies = ["data_url", "image_base64", "Authorization", "AppKEY", "app_key", "ocr_text_hint"]
    metadata_tokens = [
        "input_id_hash",
        "image_present",
        "image_sha256_prefix",
        "ocr_block_count",
        "source_type",
        "key_present",
        "duration_ms",
        "status",
        "ocr_hint_length",
        "ocr_has_course_signal",
        "ocr_has_time_signal",
        "ocr_has_location_signal",
        "ocr_repair_applied",
        "ocr_repair_reasons",
    ]

    checks = [
        (
            "audit_log_module_exists",
            "def build_analyze_image_audit_event" in audit_log and "def redact_log_text" in audit_log,
        ),
        (
            "audit_event_uses_metadata_only",
            all(token in audit_log for token in metadata_tokens)
            and all(f"\"{token}\":" not in audit_log and f"'{token}':" not in audit_log for token in forbidden_copies),
        ),
        (
            "audit_event_hashes_user_controlled_input_id",
            "def _stable_hash_prefix" in audit_log
            and "hashlib.sha256" in audit_log
            and '"input_id_hash": _stable_hash_prefix(request.input_id)' in audit_log
            and '"input_id": request.input_id' not in audit_log
            and "test@example.com" in test_file
            and "assertNotIn(request.input_id" in test_file,
        ),
        (
            "audit_event_redacts_pii_patterns",
            all(token in audit_log for token in ["手机号***", "学号/编号***", "邮箱***", "_PHONE_RE", "_NUMERIC_ID_RE"]),
        ),
        (
            "analyze_image_route_logs_audit_event",
            "build_analyze_image_audit_event" in main_py
            and "analyze_image_audit" in main_py
            and "logger.info" in main_py,
        ),
        (
            "audit_logger_emits_info",
            'logging.getLogger("shike_backend.audit")' in main_py
            and "logger.setLevel(logging.INFO)" in main_py
            and "logger.addHandler(logging.StreamHandler())" in main_py
            and "repair_risks=repair_risks" in main_py,
        ),
        (
            "redaction_unit_test_exists",
            "test_analyze_image_audit_event_uses_redacted_metadata_only" in test_file
            and "assertNotIn" in test_file
            and "13800138000" in test_file
            and "abcdefghijklmnopqrstuvwxyz123456" in test_file,
        ),
        (
            "redaction_unit_test_passes",
            command_passes(["python3", "-m", "unittest", "backend.tests.test_audit_log_redaction"]),
        ),
        (
            "runbook_documents_no_raw_logs",
            all(token in runbook for token in ["Never log", "Authorization", "full OCR text", "base64 image payload"]),
        ),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"BACKEND_AUDIT_LOG_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
