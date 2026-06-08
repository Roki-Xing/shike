#!/usr/bin/env python3
"""Run Shike release handoff checks in dependency-safe order."""

from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent


@dataclass(frozen=True)
class HandoffCommand:
    name: str
    command: tuple[str, ...]
    expect_failure: bool = False


LOCAL_COMMANDS = (
    HandoffCommand(
        "prepare_cloud_device_evidence",
        ("python3", "shike/scripts/prepare_cloud_device_evidence.py"),
    ),
    HandoffCommand(
        "cloud_device_collection_script",
        ("python3", "shike/scripts/test_collect_cloud_device_evidence.py"),
    ),
    HandoffCommand(
        "cloud_backend_preflight_script",
        ("python3", "shike/scripts/test_preflight_cloud_backend.py"),
    ),
    HandoffCommand(
        "requirement_matrix",
        ("python3", "shike/validation/validate_requirement_matrix.py"),
    ),
    HandoffCommand(
        "release_blocking_report",
        ("python3", "shike/validation/validate_release_blocking_report.py"),
    ),
    HandoffCommand(
        "release_evidence_index",
        ("python3", "shike/validation/validate_release_evidence_index.py"),
    ),
    HandoffCommand(
        "live_smoke_evidence",
        ("python3", "shike/validation/validate_live_smoke_evidence.py"),
    ),
    HandoffCommand(
        "http_server_smoke",
        (
            "python3",
            "shike/backend/shike_backend/eval/http_server_smoke.py",
            "--timeout-seconds",
            "35",
            "--disable-cloud-image",
        ),
    ),
    HandoffCommand(
        "android16_screenshot_flow",
        ("python3", "shike/validation/validate_android16_screenshot_flow.py"),
    ),
    HandoffCommand(
        "android16_real_implementation_guide",
        ("python3", "shike/validation/validate_android16_real_implementation_guide.py"),
    ),
    HandoffCommand(
        "android16_definition_of_done",
        ("python3", "shike/validation/validate_android16_definition_of_done.py"),
    ),
    HandoffCommand(
        "no_fake_device_chrome",
        ("python3", "shike/validation/validate_no_fake_device_chrome.py"),
    ),
    HandoffCommand(
        "home_one_screen",
        ("python3", "shike/validation/validate_home_one_screen.py"),
    ),
    HandoffCommand(
        "screenshot_cleanup",
        ("python3", "shike/validation/validate_screenshot_cleanup.py"),
    ),
    HandoffCommand(
        "android_image_preprocess",
        ("python3", "shike/validation/validate_android_image_preprocess.py"),
    ),
    HandoffCommand(
        "cloud_device_package",
        ("python3", "shike/validation/validate_cloud_device_package.py"),
    ),
    HandoffCommand(
        "landing_release_candidate",
        ("python3", "shike/validation/validate_landing_release_candidate.py"),
    ),
    HandoffCommand(
        "secret_hygiene",
        ("python3", "shike/validation/validate_secret_hygiene.py"),
    ),
    HandoffCommand(
        "apk_secret_hygiene",
        ("python3", "shike/validation/validate_apk_secret_hygiene.py"),
    ),
    HandoffCommand(
        "no_default_image_upload",
        ("python3", "shike/validation/validate_no_default_image_upload.py"),
    ),
    HandoffCommand(
        "vivo_multimodal_contract",
        ("python3", "shike/validation/validate_vivo_multimodal_contract.py"),
    ),
    HandoffCommand(
        "image_semantic_cases",
        ("python3", "shike/validation/validate_image_semantic_cases.py"),
    ),
)

STRICT_COMMANDS = (
    HandoffCommand(
        "cloud_device_package_strict",
        ("python3", "shike/validation/validate_cloud_device_package.py", "--strict"),
        expect_failure=True,
    ),
    HandoffCommand(
        "landing_release_candidate_strict",
        ("python3", "shike/validation/validate_landing_release_candidate.py", "--strict"),
        expect_failure=True,
    ),
)


def run_command(item: HandoffCommand) -> bool:
    """Run one handoff command and print a compact status line.

    Args:
        item: Command metadata.

    Returns:
        True when the result matches the command expectation.
    """

    result = subprocess.run(
        item.command,
        cwd=WORKSPACE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    output = result.stdout.strip()
    if output:
        print(output)
    passed = result.returncode == 0
    if item.expect_failure:
        ok = not passed
        status = "EXPECTED_BLOCK" if ok else "UNEXPECTED_PASS"
    else:
        ok = passed
        status = "PASS" if ok else "FAIL"
    print(f"{status}\t{item.name}\t{' '.join(item.command)}")
    return ok


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments.

    Returns:
        Parsed command-line arguments.
    """

    parser = argparse.ArgumentParser(description="Run Shike release handoff checks.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Also run strict external-evidence gates after local handoff checks.",
    )
    parser.add_argument(
        "--strict-ready",
        action="store_true",
        help="Require strict external-evidence gates to pass instead of treating them as expected blockers.",
    )
    return parser.parse_args()


def main() -> int:
    """Run release handoff checks.

    Returns:
        0 when all required checks match their expected status.
    """

    args = parse_args()
    commands = list(LOCAL_COMMANDS)
    if args.strict or args.strict_ready:
        strict_commands = [
            HandoffCommand(item.name, item.command, expect_failure=not args.strict_ready)
            for item in STRICT_COMMANDS
        ]
        commands.extend(strict_commands)

    results = [run_command(item) for item in commands]
    passed = sum(1 for ok in results if ok)
    print(f"RELEASE_HANDOFF_CHECKS_METRIC\t{passed}/{len(results)}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
