#!/usr/bin/env python3
"""Verify the 20-file Shike submission package.

Args:
    package_dir: Path to the core 20-file package directory.

Returns:
    Process exit code 0 when the package contains exactly the expected files.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path


EXPECTED_FILES = [
    "README.md",
    "android-mvp/app/build/outputs/apk/debug/app-debug.apk",
    "android-mvp/app/src/main/AndroidManifest.xml",
    "android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt",
    "android-mvp/app/src/main/res/values/styles.xml",
    "backend/requirements.txt",
    "backend/shike_backend/main.py",
    "contracts/model-output.schema.json",
    "contracts/sample-course-request.json",
    "contracts/sample-course-response.json",
    "docs/android-mvp-implementation.md",
    "docs/device-runbook.md",
    "docs/product-spec.md",
    "materials/demo-script.md",
    "materials/device-demo-checklist.md",
    "materials/submission-checklist.md",
    "prototype/index.html",
    "validation/validate_action_execution.py",
    "validation/validate_demo_acceptance.py",
    "validation/validate_real_world_ready.py",
]

STRUCTURE_GUARD_REFERENCES = {
    "README.md": ("validate_android_structure.py", "ANDROID_STRUCTURE_METRIC 31/31"),
    "materials/device-demo-checklist.md": ("validate_android_structure.py", "ANDROID_STRUCTURE_METRIC 31/31"),
    "validation/validate_demo_acceptance.py": ("android_structure_guard_listed", "validate_android_structure.py"),
}

ACTION_EXECUTION_GUARD_REFERENCES = {
    "README.md": ("validate_action_execution.py", "ACTION_EXECUTION_METRIC 17/17"),
    "materials/device-demo-checklist.md": ("validate_action_execution.py", "ACTION_EXECUTION_METRIC 17/17"),
    "validation/validate_demo_acceptance.py": ("validate_action_execution.py", "workspace_command_style_consistent"),
}

UNIT_TEST_GUARD_REFERENCES = {
    "README.md": ("validate_android_unit_tests.py", "ANDROID_UNIT_TEST_METRIC 82/82"),
    "materials/device-demo-checklist.md": ("validate_android_unit_tests.py", "ANDROID_UNIT_TEST_METRIC 82/82"),
    "validation/validate_demo_acceptance.py": ("validate_android_unit_tests.py", "workspace_command_style_consistent"),
}


def sha256(path: Path) -> str:
    """Hash a file for stable APK/source comparison.

    Args:
        path: File path to hash.

    Returns:
        Hex SHA-256 digest.
    """

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_contains(path: Path, tokens: tuple[str, ...]) -> bool:
    """Check whether a package text file contains required tokens.

    Args:
        path: Text file path.
        tokens: Required text snippets.

    Returns:
        True when the file exists and contains every token.
    """

    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    return all(token in text for token in tokens)


def main(argv: list[str]) -> int:
    """Run package verification.

    Args:
        argv: CLI arguments.

    Returns:
        0 when verification passes, 1 otherwise.
    """

    package_dir = Path(argv[1]).resolve() if len(argv) > 1 else Path.cwd()
    expected = set(EXPECTED_FILES)
    actual = {str(path.relative_to(package_dir)) for path in package_dir.rglob("*") if path.is_file()}
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)

    for path in EXPECTED_FILES:
        file_path = package_dir / path
        ok = file_path.is_file() and file_path.stat().st_size > 0
        print(f"{'PASS' if ok else 'FAIL'}\t{path}")

    print(f"CORE20_FILE_COUNT\t{len(actual)}/20")
    if missing:
        print("MISSING\t" + ",".join(missing))
    if extra:
        print("EXTRA\t" + ",".join(extra))

    apk = package_dir / "android-mvp/app/build/outputs/apk/debug/app-debug.apk"
    if apk.is_file():
        print(f"APK_SHA256\t{sha256(apk)}")

    structure_guard_passes = True
    for relative, tokens in STRUCTURE_GUARD_REFERENCES.items():
        ok = text_contains(package_dir / relative, tokens)
        structure_guard_passes = structure_guard_passes and ok
        print(f"{'PASS' if ok else 'FAIL'}\tSTRUCTURE_GUARD\t{relative}")

    action_execution_guard_passes = True
    for relative, tokens in ACTION_EXECUTION_GUARD_REFERENCES.items():
        ok = text_contains(package_dir / relative, tokens)
        action_execution_guard_passes = action_execution_guard_passes and ok
        print(f"{'PASS' if ok else 'FAIL'}\tACTION_EXECUTION_GUARD\t{relative}")

    unit_test_guard_passes = True
    for relative, tokens in UNIT_TEST_GUARD_REFERENCES.items():
        ok = text_contains(package_dir / relative, tokens)
        unit_test_guard_passes = unit_test_guard_passes and ok
        print(f"{'PASS' if ok else 'FAIL'}\tUNIT_TEST_GUARD\t{relative}")

    return (
        0
        if len(actual) == 20
        and not missing
        and not extra
        and structure_guard_passes
        and action_execution_guard_passes
        and unit_test_guard_passes
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
