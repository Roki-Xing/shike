#!/usr/bin/env python3
"""Tests for secret-safe public backend preflight helpers."""

from __future__ import annotations

import importlib.util
import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parent / "preflight_cloud_backend.py"


def load_module():
    """Load the preflight script as a module."""

    spec = importlib.util.spec_from_file_location("preflight_cloud_backend", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("preflight_cloud_backend.py is not importable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class PreflightCloudBackendTest(unittest.TestCase):
    def test_normalize_rejects_insecure_or_credential_urls(self) -> None:
        module = load_module()

        self.assertEqual("https://roky.chat", module.normalize_base_url("https://roky.chat/"))
        with self.assertRaises(ValueError):
            module.normalize_base_url("https://user:secret@roky.chat")
        with self.assertRaises(ValueError):
            module.normalize_base_url("http://roky.chat")
        self.assertEqual("http://127.0.0.1:8000", module.normalize_base_url("http://127.0.0.1:8000", allow_http=True))

    def test_payload_defaults_to_no_cloud_image_and_contains_no_secret(self) -> None:
        module = load_module()

        payload = module.build_payload(allow_cloud_image=False)
        serialized = str(payload)

        self.assertFalse(payload["allow_cloud_image"])
        self.assertIn("data:image/png;base64,", payload["image"]["data_url"])
        self.assertNotIn("sk-", serialized)
        self.assertNotIn("AppKEY", serialized)
        self.assertNotIn("Authorization", serialized)

    def test_run_preflight_prints_only_redacted_evidence(self) -> None:
        module = load_module()

        def fake_fetch_json(base_url: str, path: str, *, timeout_seconds: int):
            if path == "/health":
                return {"status": "ok"}
            if path == "/v2/schema":
                return {"title": "AnalyzeImageResponse"}
            raise AssertionError(path)

        def fake_post_json(base_url: str, path: str, body: dict, *, timeout_seconds: int):
            self.assertEqual("/v2/analyze-image", path)
            self.assertFalse(body["allow_cloud_image"])
            return {
                "title": "项目讨论",
                "suggested_actions": [{"type": "calendar", "disabled_reason": module.CONFIRMATION_DISABLED_REASON}],
                "ignored_regions": ["top_status_bar", "bottom_navigation_bar"],
            }

        module.fetch_json = fake_fetch_json
        module.post_json = fake_post_json
        output = io.StringIO()
        with redirect_stdout(output):
            ok = module.run_preflight(base_url="https://roky.chat", timeout_seconds=5, allow_cloud_image=False)

        text = output.getvalue()
        self.assertTrue(ok)
        self.assertIn("cloud_backend_preflight_base_url=https://HOST_REDACTED", text)
        self.assertIn("CLOUD_BACKEND_PREFLIGHT_METRIC=1/1", text)
        self.assertNotIn("sk-", text)
        self.assertNotIn("Authorization", text)
        self.assertNotIn("AppKEY", text)


if __name__ == "__main__":
    unittest.main()
