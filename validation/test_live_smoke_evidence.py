#!/usr/bin/env python3
"""Tests for the redacted backend live-smoke evidence validator."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parent / "validate_live_smoke_evidence.py"


def load_module():
    """Load the validator script as a module."""

    spec = importlib.util.spec_from_file_location("validate_live_smoke_evidence", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("validate_live_smoke_evidence.py is not importable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class LiveSmokeEvidenceTest(unittest.TestCase):
    def test_accepts_current_secret_safe_combined_live_smoke_log(self) -> None:
        module = load_module()

        checks = module.build_checks(module.ACCESS_LOG_PATH)
        by_name = {check.name: check.ok for check in checks}

        for name in (
            "access_log_exists",
            "no_secret_like_tokens",
            "bluelm_text_schema_valid",
            "vivo_ocr_passed_and_image_cleared",
            "multimodal_fallback_then_pass",
            "route_v2_schema_valid_and_actions_disabled",
            "live_smoke_metric_4_of_4",
        ):
            self.assertTrue(by_name[name], name)

    def test_rejects_secret_like_or_unconfirmed_action_log(self) -> None:
        module = load_module()
        synthetic_key = "sk" + "-example-secret"

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "backend-redacted-access-log.txt"
            path.write_text(
                "\n".join(
                    [
                        "POST /v1/analyze 200 provider=bluelm result_schema_valid=true",
                        "POST /v1/ocr 200 provider=vivo_general_ocr ocr_status=pass image_cleared=true",
                        "POST /v2/analyze-image 200 multimodal_status=pass selected_model=Doubao-Seed-2.0-mini",
                        "POST /v2/analyze-image 200 route_v2_status=pass route_v2_schema_valid=true route_v2_actions_disabled=false",
                        "live_smoke_metric=4/4",
                        f"AppKEY={synthetic_key}",
                    ]
                ),
                encoding="utf-8",
            )

            checks = module.build_checks(path)
            by_name = {check.name: check.ok for check in checks}

            self.assertFalse(by_name["no_secret_like_tokens"])
            self.assertFalse(by_name["route_v2_schema_valid_and_actions_disabled"])


if __name__ == "__main__":
    unittest.main()
