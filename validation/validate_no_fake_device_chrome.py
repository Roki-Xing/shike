#!/usr/bin/env python3
"""Validate that production Android surfaces do not draw fake device chrome."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SCAN_ROOTS = [
    ROOT / "android-mvp/app/src/main",
    ROOT / "prototype",
]

FORBIDDEN_TOKENS = [
    "10:28",
    "100%",
    "5月24日",
    "星期五",
    "农历四月十七",
    "home-status",
    "fakeStatus",
    "deviceChrome",
]

TEXT_SUFFIXES = {".kt", ".java", ".xml", ".html", ".css", ".js", ".md"}

ALLOW_PATH_PARTS = {
    "archive",
    "problem-evidence",
    "docs",
}


def is_allowed(path: Path) -> bool:
    """Return whether a path is allowed to retain historical evidence text.

    Args:
        path: File path being scanned.

    Returns:
        True when the file is outside production/demo runtime surfaces.
    """

    normalized = str(path).replace("\\", "/")
    return any(f"/{part}/" in normalized for part in ALLOW_PATH_PARTS)


def iter_text_files(root: Path) -> list[Path]:
    """Collect text files under a scan root.

    Args:
        root: Directory to scan.

    Returns:
        Matching project files.
    """

    if not root.exists():
        return []
    return [
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix.lower() in TEXT_SUFFIXES
        and not is_allowed(path)
        and "build" not in path.parts
    ]


def main() -> int:
    """Run fake device chrome checks.

    Returns:
        Process exit code.
    """

    hits: list[tuple[Path, str]] = []
    date_strip = (ROOT / "android-mvp/app/src/main/java/cn/shike/app/ui/DateStrip.kt").read_text(encoding="utf-8", errors="replace")
    for root in SCAN_ROOTS:
        for path in iter_text_files(root):
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            for line in lines:
                stripped = line.strip()
                for token in FORBIDDEN_TOKENS:
                    if token not in line:
                        continue
                    if token == "100%" and (
                        stripped.startswith("height:")
                        or stripped.startswith("width:")
                        or "linear-gradient" in stripped
                        or "max-width:" in stripped
                        or "style=\"width:" in stripped
                    ):
                        continue
                    hits.append((path.relative_to(ROOT), token))

    date_copy_ok = (
        "formatTodayForHome(date: LocalDate)" in date_strip
        and "系统日期仅用于排序提示，不作为任务时间" in date_strip
        and "农历" not in date_strip
        and "5月24日" not in date_strip
        and "自动当作任务时间" not in date_strip
    )
    if not date_copy_ok:
        hits.append((Path("android-mvp/app/src/main/java/cn/shike/app/ui/DateStrip.kt"), "date-boundary-copy"))

    if hits:
        print("NO_FAKE_DEVICE_CHROME_FAILED")
        for path, token in hits:
            print(f"FAIL\t{path}\t{token}")
        print(f"NO_FAKE_DEVICE_CHROME_METRIC\t0/1")
        return 1

    print("PASS\tno_fake_device_chrome")
    print("NO_FAKE_DEVICE_CHROME_METRIC\t1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
