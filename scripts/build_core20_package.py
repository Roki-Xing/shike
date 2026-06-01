#!/usr/bin/env python3
"""Build a 20-file Shike submission package from the current repository state.

This script is intentionally simple and deterministic:
- It copies exactly the 20 files expected by `scripts/verify_core20_package.py`.
- Optional: compare an existing package directory and write a drift report.

The generated package directory is meant for offline submission handoff (outside git).
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from shutil import copy2


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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _default_out_dir() -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return Path("/mnt/c/Users/Xing/Desktop") / f"shike-core20-{stamp}"


def _run_verify(package_dir: Path) -> tuple[int, str]:
    repo_root = _repo_root()
    verify_script = repo_root / "scripts" / "verify_core20_package.py"
    if not verify_script.is_file():
        raise RuntimeError("missing_verify_script")
    proc = subprocess.run(
        [sys.executable, "-X", "utf8", str(verify_script), str(package_dir)],
        cwd=str(repo_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
    )
    return proc.returncode, proc.stdout


def _git_head() -> str:
    repo_root = _repo_root()
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(repo_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            check=True,
        )
        return proc.stdout.strip()
    except Exception:
        return "unknown"


def build_package(*, out_dir: Path) -> None:
    repo_root = _repo_root()
    out_dir.mkdir(parents=True, exist_ok=False)
    for rel in EXPECTED_FILES:
        src = repo_root / rel
        if not src.is_file():
            raise FileNotFoundError(f"missing_expected_file:{rel}")
        dest = out_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        copy2(src, dest)


def _hash_map(root: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for rel in EXPECTED_FILES:
        path = root / rel
        mapping[rel] = sha256(path) if path.is_file() else ""
    return mapping


def _verify_fail_lines(output: str) -> list[str]:
    lines = []
    for raw in output.splitlines():
        line = raw.strip()
        if line.startswith("FAIL\t"):
            lines.append(line)
    return lines


def write_drift_report(*, report_path: Path, old_dir: Path, new_dir: Path) -> None:
    old_hashes = _hash_map(old_dir)
    new_hashes = _hash_map(new_dir)

    changed = [rel for rel in EXPECTED_FILES if old_hashes.get(rel, "") != new_hashes.get(rel, "")]
    unchanged = [rel for rel in EXPECTED_FILES if rel not in changed]

    old_rc, old_out = _run_verify(old_dir)
    new_rc, new_out = _run_verify(new_dir)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        "\n".join(
            [
                "# Core 20 Version Sync Report",
                "",
                f"- generated_at: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`",
                f"- repo_head: `{_git_head()}`",
                f"- old_package: `{old_dir}`",
                f"- new_package: `{new_dir}`",
                "",
                "## Verify Summary",
                "",
                f"- old_verify_exit_code: `{old_rc}`",
                f"- new_verify_exit_code: `{new_rc}`",
                "",
                "Old verify FAIL lines:",
                "",
                "```text",
                *(_verify_fail_lines(old_out) or ["(none)"]),
                "```",
                "",
                "New verify FAIL lines:",
                "",
                "```text",
                *(_verify_fail_lines(new_out) or ["(none)"]),
                "```",
                "",
                "## Drift Summary",
                "",
                f"- unchanged_files: `{len(unchanged)}/{len(EXPECTED_FILES)}`",
                f"- changed_files: `{len(changed)}/{len(EXPECTED_FILES)}`",
                "",
                "## Changed Files",
                "",
                "```text",
                *(
                    [
                        f"{rel}\told_sha256={old_hashes[rel]}\tnew_sha256={new_hashes[rel]}"
                        for rel in changed
                    ]
                    or ["(none)"]
                ),
                "```",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=None, help="Output directory for the generated core20 package.")
    parser.add_argument(
        "--compare-old",
        type=Path,
        default=None,
        help="Optional existing core20 package directory to compare against.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="Optional drift report path (markdown). Defaults to <out-dir>/core20-version-sync-report.md when comparing.",
    )
    args = parser.parse_args(argv)

    out_dir = args.out_dir or _default_out_dir()
    build_package(out_dir=out_dir)

    rc, out = _run_verify(out_dir)
    print(out, end="")
    if rc != 0:
        print("ERROR\tnew_package_verify_failed", file=sys.stderr)
        return 1

    if args.compare_old is not None:
        old_dir = args.compare_old
        if not old_dir.is_dir():
            print("ERROR\tcompare_old_not_a_dir", file=sys.stderr)
            return 1
        report_path = args.report or (out_dir / "core20-version-sync-report.md")
        write_drift_report(report_path=report_path, old_dir=old_dir, new_dir=out_dir)
        print(f"drift_report_written\t{report_path}")

    print(f"core20_package_written\t{out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

