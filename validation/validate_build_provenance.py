#!/usr/bin/env python3
"""Validate Android APK build provenance is injected and visible."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_GRADLE = ROOT / "android-mvp/app/build.gradle.kts"
PROVENANCE = ROOT / "android-mvp/app/src/main/java/cn/shike/app/BuildProvenance.kt"
SETTINGS = ROOT / "android-mvp/app/src/main/java/cn/shike/app/ui/MainFlowScreens.kt"
APK_HASH = ROOT / "materials/evidence/cloud-device/apk-sha256.txt"


def require(path: Path, token: str) -> bool:
    return path.is_file() and token in path.read_text(encoding="utf-8")


def main() -> int:
    checks = [
        require(BUILD_GRADLE, "gitOutput(\"rev-parse\", \"--short=7\", \"HEAD\")"),
        require(BUILD_GRADLE, "buildConfigField(\"String\", \"SHORT_GIT_SHA\""),
        require(BUILD_GRADLE, "buildConfigField(\"String\", \"BUILD_TIME_UTC\""),
        require(BUILD_GRADLE, "buildConfig = true"),
        require(PROVENANCE, "BuildConfig.SHORT_GIT_SHA"),
        require(PROVENANCE, "BuildConfig.BUILD_TIME_UTC"),
        require(PROVENANCE, "版本 $versionLabel · 构建 $shortGitSha"),
        require(SETTINGS, "currentBuildProvenance()"),
        require(SETTINGS, "构建时间"),
        require(APK_HASH, "APK SHA-256:"),
    ]
    passed = sum(1 for ok in checks if ok)
    total = len(checks)
    print(f"BUILD_PROVENANCE_METRIC {passed}/{total}")
    if passed != total:
        return 1
    print("PASS build_provenance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
