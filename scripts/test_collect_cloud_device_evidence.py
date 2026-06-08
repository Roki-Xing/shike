#!/usr/bin/env python3
"""Tests for cloud-device evidence collection helpers."""

from __future__ import annotations

import importlib.util
import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parent / "collect_cloud_device_evidence.py"


def load_module():
    """Load the collection script as a module."""

    spec = importlib.util.spec_from_file_location("collect_cloud_device_evidence", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("collect_cloud_device_evidence.py is not importable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class CollectCloudDeviceEvidenceTest(unittest.TestCase):
    def test_required_scenarios_match_strict_video_set(self) -> None:
        module = load_module()

        names = [scenario.name for scenario in module.REQUIRED_SCENARIOS]

        self.assertEqual(
            [
                "01-cloud-install-open.mp4",
                "02-cloud-gallery-bluelm.mp4",
                "03-cloud-camera-bluelm.mp4",
                "04-cloud-share-text.mp4",
                "05-cloud-permission-fallback.mp4",
                "06-cloud-backend-failure.mp4",
                "07-cloud-restart-restore.mp4",
                "08-cloud-ui-polish.mp4",
                "09-cloud-final-route.mp4",
            ],
            names,
        )

    def test_android16_manual_acceptance_scripts_are_mapped(self) -> None:
        module = load_module()

        joined_prompts = "\n".join(
            f"{scenario.title}\n{scenario.operator_prompt}" for scenario in module.REQUIRED_SCENARIOS
        )
        coverage = "\n".join(
            f"{section} {video} {expectation}"
            for section, video, expectation in module.ANDROID16_GUIDE_RECORDING_COVERAGE
        )

        for token in (
            "14.1 无假信息",
            "14.2 截图分享导入",
            "14.3 确认后打开日历",
            "14.4 通知权限与提醒",
            "14.5 地图",
            "14.6 删除原截图",
            "14.7 最近截图助手",
            "系统截图浮层分享",
            "删除原截图系统确认",
            "没有自动上传",
        ):
            self.assertIn(token, joined_prompts + "\n" + coverage)

        self.assertIn("04-cloud-share-text.mp4", coverage)
        self.assertIn("09-cloud-final-route.mp4", coverage)

    def test_builds_predictable_screenrecord_commands(self) -> None:
        module = load_module()
        scenario = module.REQUIRED_SCENARIOS[1]

        remote_path = module.remote_recording_path(scenario)
        command = module.build_screenrecord_command("device-123", remote_path, 90)
        pull = module.build_pull_command("device-123", remote_path, Path("/tmp/out.mp4"))

        self.assertEqual(
            ["adb", "-s", "device-123", "shell", "screenrecord", "--time-limit", "90", remote_path],
            command,
        )
        self.assertEqual(["adb", "-s", "device-123", "pull", remote_path, "/tmp/out.mp4"], pull)

    def test_builds_two_backend_preflight_commands(self) -> None:
        module = load_module()

        commands = module.build_preflight_commands("https://roky.chat", 90)

        self.assertEqual(2, len(commands))
        self.assertEqual("python3", commands[0][0])
        self.assertTrue(commands[0][1].endswith("preflight_cloud_backend.py"))
        self.assertIn("--base-url", commands[0])
        self.assertIn("https://roky.chat", commands[0])
        self.assertIn("--timeout-seconds", commands[0])
        self.assertIn("90", commands[0])
        self.assertNotIn("--allow-cloud-image", commands[0])
        self.assertIn("--allow-cloud-image", commands[1])

    def test_preflight_backend_dry_run_prints_both_commands(self) -> None:
        module = load_module()

        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = module.preflight_backend(
                base_url="https://roky.chat",
                timeout_seconds=90,
                dry_run=True,
            )

        text = output.getvalue()
        self.assertEqual(0, exit_code)
        self.assertEqual(2, text.count("preflight_cloud_backend.py"))
        self.assertIn("--base-url https://roky.chat", text)
        self.assertIn("--allow-cloud-image", text)

    def test_parse_args_accepts_preflight_backend(self) -> None:
        module = load_module()

        with patch.object(
            sys,
            "argv",
            [
                "collect_cloud_device_evidence.py",
                "--preflight-backend",
                "--backend-url",
                "https://roky.chat",
                "--preflight-timeout-seconds",
                "90",
            ],
        ):
            args = module.parse_args()

        self.assertTrue(args.preflight_backend)
        self.assertEqual("https://roky.chat", args.backend_url)
        self.assertEqual(90, args.preflight_timeout_seconds)

    def test_redacts_logcat_sensitive_values(self) -> None:
        module = load_module()
        synthetic_key = "sk" + "-xuanji-example-secret"
        auth_header = "Authorization" + ": Bearer"

        raw = (
            f"{auth_header} {synthetic_key}\n"
            f"AppKEY={synthetic_key}\n"
            "phone 13800138000 email test@example.com student 2026468887\n"
            "data:image/png;base64,abcdefghijklmnopqrstuvwxyz0123456789+/=\n"
        )
        redacted = module.redact_log_text(raw)

        self.assertNotIn(synthetic_key, redacted)
        self.assertNotIn("Authorization", redacted)
        self.assertNotIn("AppKEY", redacted)
        self.assertNotIn("13800138000", redacted)
        self.assertNotIn("test@example.com", redacted)
        self.assertNotIn("abcdefghijklmnopqrstuvwxyz0123456789", redacted)
        self.assertIn("PROVIDER_KEY_REDACTED", redacted)
        self.assertIn("PHONE_REDACTED", redacted)
        self.assertIn("EMAIL_REDACTED", redacted)


if __name__ == "__main__":
    unittest.main()
