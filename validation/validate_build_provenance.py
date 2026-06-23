#!/usr/bin/env python3
"""Validate Android APK build provenance is injected and visible."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_GRADLE = ROOT / "android-mvp/app/build.gradle.kts"
PROVENANCE = ROOT / "android-mvp/app/src/main/java/cn/shike/app/BuildProvenance.kt"
SETTINGS = ROOT / "android-mvp/app/src/main/java/cn/shike/app/ui/MainFlowScreens.kt"
APK_HASH = ROOT / "materials/evidence/cloud-device/apk-sha256.txt"
LOCAL_APK = ROOT / "android-mvp/app/build/outputs/apk/debug/app-debug.apk"
DESKTOP_APK = Path("/mnt/c/Users/Xing/Desktop/Shike-app-debug.apk")
ANDROID_MAIN = ROOT / "android-mvp/app/src/main"


def require(path: Path, token: str) -> bool:
    return path.is_file() and token in path.read_text(encoding="utf-8")


def declared_apk_hash() -> str | None:
    if not APK_HASH.is_file():
        return None
    match = re.search(r"APK SHA-256:\s*([a-fA-F0-9]{64})", APK_HASH.read_text(encoding="utf-8"))
    return match.group(1).lower() if match else None


def sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def latest_android_input_mtime() -> float | None:
    inputs = [BUILD_GRADLE]
    if ANDROID_MAIN.is_dir():
        inputs.extend(path for path in ANDROID_MAIN.rglob("*") if path.is_file())
    existing = [path.stat().st_mtime for path in inputs if path.is_file()]
    return max(existing) if existing else None


def local_apk_is_fresh() -> bool:
    input_mtime = latest_android_input_mtime()
    return LOCAL_APK.is_file() and input_mtime is not None and LOCAL_APK.stat().st_mtime >= input_mtime


def main() -> int:
    declared_hash = declared_apk_hash()
    local_hash = sha256(LOCAL_APK)
    desktop_hash = sha256(DESKTOP_APK)
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
        declared_hash is not None,
        local_hash is not None and local_hash == declared_hash,
        desktop_hash is None or desktop_hash == declared_hash,
        local_apk_is_fresh(),
    ]
    passed = sum(1 for ok in checks if ok)
    total = len(checks)
    print(f"BUILD_PROVENANCE_METRIC {passed}/{total}")
    if passed != total:
        print(f"DECLARED_APK_SHA256 {declared_hash or 'MISSING'}")
        print(f"LOCAL_APK_SHA256 {local_hash or 'MISSING'}")
        print(f"DESKTOP_APK_SHA256 {desktop_hash or 'MISSING'}")
        return 1
    print("PASS build_provenance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
