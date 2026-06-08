#!/usr/bin/env python3
"""Validate that Shike APK artifacts do not embed provider credentials.

The check scans decompressed APK entries rather than raw compressed zip bytes to
avoid random binary false positives. It never prints configured secret values.
"""

from __future__ import annotations

import os
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

APK_PATHS = [
    ROOT / "android-mvp/app/build/outputs/apk/debug/app-debug.apk",
    Path("/mnt/c/Users/Xing/Desktop/Shike-app-debug.apk"),
]

PROVIDER_SECRET_NAMES = (
    b"BLUELM_APP_KEY",
    b"VIVO_AIGC_APP_KEY",
    b"VIVO_OCR_APP_KEY",
    b"VIVO_MULTIMODAL_APP_KEY",
    b"VIVO_APP_KEY",
    b"AppKEY",
)

PROVIDER_DIRECT_ENDPOINTS = (
    b"api-ai.vivo.com.cn",
    b"aigc.vivo.com.cn",
    b"/v1/chat/completions",
    b"/ocr/general_recognition",
)

PRIVATE_ENV_NAMES = (
    "BLUELM_APP_KEY",
    "VIVO_AIGC_APP_KEY",
    "VIVO_OCR_APP_KEY",
    "VIVO_MULTIMODAL_APP_KEY",
    "VIVO_APP_KEY",
    "AppKEY",
    "APPKEY",
    "BLUELM_APP_ID",
    "VIVO_AIGC_APP_ID",
    "VIVO_OCR_APP_ID",
    "VIVO_MULTIMODAL_APP_ID",
    "VIVO_APP_ID",
    "VIVO_OCR_BUSINESS_ID",
)

SECRET_LIKE_RE = re.compile(rb"\bsk-[A-Za-z0-9_\-=]{12,}\b")


@dataclass(frozen=True)
class Finding:
    """One APK hygiene finding."""

    apk: Path
    entry: str
    rule: str
    preview: str


def _is_placeholder(value: str) -> bool:
    """Return whether an env value is placeholder/redacted text."""

    stripped = value.strip().strip("\"'")
    if not stripped:
        return True
    lowered = stripped.lower()
    return (
        stripped in {"***", "...", "your-app-key", "your_app_key", "your-app-id", "your_app_id"}
        or "*" in stripped
        or "redacted" in lowered
        or "placeholder" in lowered
    )


def _parse_env_file(path: Path) -> dict[str, str]:
    """Parse simple KEY=value or export KEY=value env files.

    Args:
        path: Private environment file path.

    Returns:
        Parsed key/value pairs, or an empty mapping when unavailable.
    """

    if not path.is_file():
        return {}
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("\"'")
    return values


def _private_env_values() -> dict[str, bytes]:
    """Collect configured provider values for exact APK byte matching.

    Returns:
        Mapping from env name to UTF-8 bytes. Values are never printed.
    """

    env_paths = [
        Path(os.environ["SHIKE_BACKEND_ENV_FILE"]).expanduser()
        if os.environ.get("SHIKE_BACKEND_ENV_FILE")
        else None,
        Path.home() / ".config/shike/bluelm.env",
        Path("/etc/shike/shike-backend.env"),
    ]
    merged: dict[str, str] = {}
    for path in env_paths:
        if path is not None:
            merged.update(_parse_env_file(path))
    for name in PRIVATE_ENV_NAMES:
        if os.environ.get(name):
            merged[name] = os.environ[name]

    candidates: dict[str, bytes] = {}
    for name in PRIVATE_ENV_NAMES:
        value = merged.get(name, "")
        if _is_placeholder(value) or len(value) < 6:
            continue
        candidates[name] = value.encode("utf-8")
    return candidates


def _scan_entry(apk: Path, entry: str, data: bytes, private_values: dict[str, bytes]) -> list[Finding]:
    """Scan one decompressed APK entry.

    Args:
        apk: APK file path.
        entry: Zip entry name.
        data: Decompressed entry bytes.
        private_values: Backend-only configured values to match exactly.

    Returns:
        Findings for this entry.
    """

    findings: list[Finding] = []
    for match in SECRET_LIKE_RE.finditer(data):
        findings.append(Finding(apk=apk, entry=entry, rule="secret_like_token", preview="sk-***"))
        # One finding per entry is enough and avoids noisy binary output.
        break

    for token in PROVIDER_SECRET_NAMES:
        if token in data:
            findings.append(
                Finding(apk=apk, entry=entry, rule="provider_secret_env_name", preview=token.decode("ascii"))
            )

    for token in PROVIDER_DIRECT_ENDPOINTS:
        if token in data:
            findings.append(
                Finding(apk=apk, entry=entry, rule="provider_direct_endpoint", preview=token.decode("ascii"))
            )

    for name, value in private_values.items():
        if value in data:
            findings.append(Finding(apk=apk, entry=entry, rule="private_env_value_embedded", preview=name))

    return findings


def _scan_apk(apk: Path, private_values: dict[str, bytes]) -> tuple[bool, list[Finding]]:
    """Scan an APK file.

    Args:
        apk: APK path.
        private_values: Private backend values to match exactly.

    Returns:
        Tuple of zip-readable flag and findings.
    """

    findings: list[Finding] = []
    try:
        with zipfile.ZipFile(apk) as archive:
            for info in archive.infolist():
                if info.is_dir():
                    continue
                data = archive.read(info)
                findings.extend(_scan_entry(apk, info.filename, data, private_values))
    except zipfile.BadZipFile:
        return False, findings
    return True, findings


def main() -> int:
    """Run APK secret hygiene checks.

    Returns:
        0 when all APK artifacts are clean.
    """

    private_values = _private_env_values()
    existing_apks = [path for path in APK_PATHS if path.is_file()]
    checks: list[tuple[str, bool, str]] = [
        ("local_debug_apk_exists", APK_PATHS[0].is_file() and APK_PATHS[0].stat().st_size > 0, str(APK_PATHS[0])),
        (
            "desktop_apk_absent_or_exists",
            (not APK_PATHS[1].exists()) or (APK_PATHS[1].is_file() and APK_PATHS[1].stat().st_size > 0),
            str(APK_PATHS[1]),
        ),
        ("private_env_values_loaded_or_optional", True, f"{len(private_values)} configured values checked"),
    ]

    all_findings: list[Finding] = []
    all_zip_readable = True
    for apk in existing_apks:
        zip_readable, findings = _scan_apk(apk, private_values)
        all_zip_readable = all_zip_readable and zip_readable
        all_findings.extend(findings)

    checks.extend(
        [
            ("apk_zip_entries_readable", all_zip_readable and bool(existing_apks), f"{len(existing_apks)} APK artifact(s)"),
            (
                "no_secret_like_tokens_in_apk",
                not any(f.rule == "secret_like_token" for f in all_findings),
                "sk-* pattern scan",
            ),
            (
                "no_provider_secret_names_in_apk",
                not any(f.rule == "provider_secret_env_name" for f in all_findings),
                "provider env names",
            ),
            (
                "no_provider_direct_endpoints_in_apk",
                not any(f.rule == "provider_direct_endpoint" for f in all_findings),
                "vivo direct endpoints",
            ),
            (
                "no_private_env_values_in_apk",
                not any(f.rule == "private_env_value_embedded" for f in all_findings),
                "exact private env byte match",
            ),
        ]
    )

    passed = sum(1 for _, ok, _ in checks if ok)
    for name, ok, evidence in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}\t{evidence}")
    for finding in all_findings:
        try:
            apk_label = str(finding.apk.relative_to(ROOT))
        except ValueError:
            apk_label = str(finding.apk)
        print(f"FAIL\t{finding.rule}\t{apk_label}:{finding.entry}\t{finding.preview}")
    print(f"APK_SECRET_HYGIENE_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) and not all_findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
