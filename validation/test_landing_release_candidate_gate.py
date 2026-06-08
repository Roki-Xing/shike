#!/usr/bin/env python3
"""Tests for the landing release-candidate gate composition."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "validation/validate_landing_release_candidate.py"


class LandingReleaseCandidateGateTest(unittest.TestCase):
    def test_local_gate_runs_live_smoke_evidence_validator(self) -> None:
        text = VALIDATOR_PATH.read_text(encoding="utf-8")

        self.assertIn("live_smoke_evidence_passes", text)
        self.assertIn("validate_live_smoke_evidence.py", text)

    def test_local_gate_runs_backend_audit_log_validator(self) -> None:
        text = VALIDATOR_PATH.read_text(encoding="utf-8")

        self.assertIn("backend_audit_log_passes", text)
        self.assertIn("validate_backend_audit_log.py", text)


if __name__ == "__main__":
    unittest.main()
