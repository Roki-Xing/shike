"""Helpers for validation checks that inspect Android source files."""

from __future__ import annotations

from pathlib import Path


def read_android_source(root: Path) -> str:
    """Read all Kotlin source files under the Shike Android app package.

    Args:
        root: The `shike` project root.

    Returns:
        Concatenated UTF-8 source text.
    """

    source_root = root / "android-mvp/app/src/main/java/cn/shike/app"
    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(source_root.rglob("*.kt"))
        if path.is_file()
    )

