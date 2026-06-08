#!/usr/bin/env python3
"""Validate Shike secret hygiene (no real credentials committed).

This validator is intentionally conservative and filesystem-only:

- It scans plaintext project files under the Shike module for secret-like patterns.
- It delegates APK artifact scanning to validate_apk_secret_hygiene.py.
- It never prints full matched values (to avoid leaking secrets via logs).
- It does NOT require any real BlueLM credentials to exist.

Scope is based on `docs/SHIKE_LANDING_APP_OPTIMIZATION_GUIDE.md` (secret hygiene section):
android-mvp/, backend/, contracts/, docs/, materials/, prototype/, validation/, AGENTS.md, .agents/, README.md.
"""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "shike"


TEXT_EXTENSIONS = {
    ".kt",
    ".kts",
    ".java",
    ".xml",
    ".json",
    ".md",
    ".html",
    ".css",
    ".js",
    ".ts",
    ".py",
    ".txt",
    ".toml",
    ".yaml",
    ".yml",
    ".properties",
    ".gradle",
}

# Skip generated/binary-heavy folders to reduce noise and accidental leakage in outputs.
SKIP_DIR_NAMES = {
    ".gradle",
    ".idea",
    ".pytest_cache",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
}

SKIP_FILE_SUFFIXES = {
    ".apk",
    ".aab",
    ".jar",
    ".keystore",
    ".jks",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".mp4",
    ".mov",
    ".pdf",
    ".sqlite3",
    ".db",
}


SCAN_TARGETS: list[Path] = [
    ROOT / "android-mvp",
    ROOT / "backend",
    ROOT / "contracts",
    ROOT / "docs",
    ROOT / "materials",
    ROOT / "prototype",
    ROOT / "validation",
    ROOT / ".agents",
    ROOT / "AGENTS.md",
    ROOT / "README.md",
]


def _is_text_candidate(path: Path) -> bool:
    if path.suffix.lower() in SKIP_FILE_SUFFIXES:
        return False
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    # Also treat common extension-less files as text.
    if path.name in {".gitignore", "Dockerfile"}:
        return True
    return False


def _iter_text_files(root: Path) -> list[Path]:
    files: list[Path] = []
    if root.is_file():
        return [root] if _is_text_candidate(root) else []
    if not root.exists():
        return []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIR_NAMES for part in p.parts):
            continue
        if _is_text_candidate(p):
            files.append(p)
    return files


def _mask(value: str) -> str:
    # Never print full secrets; show only a safe prefix/suffix.
    if len(value) <= 8:
        return "***"
    return f"{value[:4]}***{value[-4:]}"


@dataclass(frozen=True)
class Finding:
    path: Path
    line_no: int
    rule: str
    preview: str


def _find_in_text(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = text.splitlines()

    # Rule 1: OpenAI-style "sk-" tokens are never allowed unless clearly redacted/placeholder.
    # - We require some length after "sk-" to avoid matching "sk-" mention in docs.
    # - We allow masked patterns (contain "*" or "redacted") and obvious placeholders ("your", "...").
    sk_re = re.compile(r"\bsk-[A-Za-z0-9_\-]{12,}\b")

    # Rule 2: AppKEY assignment with a non-placeholder value.
    #
    # We intentionally anchor to beginning-of-line to avoid false positives in:
    # - documentation mentions like "`AppKEY=`"
    # - grep/rg command examples that separately mention env keys and sk-style prefixes
    #
    # This remains a "guardrail" not a full secret scanner.
    appkey_assign_re = re.compile(r"^\s*(?:export\s+)?AppKEY\s*=\s*([^\s#]+)")

    # Rule 3: BlueLM env assignment with a non-placeholder value.
    bluelm_key_assign_re = re.compile(r"^\s*(?:export\s+)?BLUELM_APP_KEY\s*=\s*([^\s#]+)")

    # Rule 4: AI gateway signature header with a suspicious value.
    # (Exact format is provider-specific; this is a minimal guardrail.)
    signature_re = re.compile(r"^\s*X-AI-GATEWAY-SIGNATURE\b\s*[:=]\s*([^\s#]+)")

    for idx, line in enumerate(lines, start=1):
        # Skip very long lines to avoid accidental large prints; but still detect patterns.
        lowered = line.lower()

        for m in sk_re.finditer(line):
            token = m.group(0)
            if "*" in token or "redacted" in lowered or "your" in lowered or "example" in lowered:
                continue
            findings.append(Finding(path=path, line_no=idx, rule="sk_token", preview=_mask(token)))

        for m in appkey_assign_re.finditer(line):
            value = m.group(1).strip("`\"'")
            if value in {"***", "...", "your-app-key", "yourkey", "your_app_key", "real-looking-secret"}:
                continue
            if "*" in value or "redacted" in lowered:
                continue
            if "|" in value:
                continue
            findings.append(Finding(path=path, line_no=idx, rule="appkey_assignment", preview=_mask(value)))

        for m in bluelm_key_assign_re.finditer(line):
            value = m.group(1).strip("`\"'")
            if value in {"***", "...", "your-app-key", "your_app_key", "real-looking-secret"}:
                continue
            if "*" in value or "redacted" in lowered:
                continue
            if "|" in value:
                continue
            findings.append(Finding(path=path, line_no=idx, rule="bluelm_app_key_assignment", preview=_mask(value)))

        for m in signature_re.finditer(line):
            value = m.group(1).strip("`\"'")
            if value in {"***", "...", "your-signature", "your_signature", "placeholder"}:
                continue
            if "*" in value or "redacted" in lowered:
                continue
            if "|" in value:
                continue
            findings.append(Finding(path=path, line_no=idx, rule="gateway_signature", preview=_mask(value)))

    return findings


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        # As a fallback, try a binary read and decode best-effort.
        return path.read_bytes().decode("utf-8", errors="replace")


def _check_android_must_not_mention_tokens() -> list[Finding]:
    # Android should never contain BlueLM secret names or "sk-" patterns.
    android_root = ROOT / "android-mvp"
    if not android_root.exists():
        return []
    findings: list[Finding] = []
    for p in _iter_text_files(android_root):
        text = _read_text(p)
        # These strings should not appear in Android code/resources.
        for token in ["BLUELM_APP_KEY", "BLUELM_APP_ID"]:
            if token in text:
                findings.append(Finding(path=p, line_no=1, rule="android_contains_bluelm_token", preview=token))
        # Even "sk-" mention in Android is suspicious; allow only if clearly part of documentation (Android should not have docs).
        if "sk-" in text:
            findings.append(Finding(path=p, line_no=1, rule="android_contains_sk_prefix", preview="sk-"))
    return findings


def _check_gitignore_env_rules() -> list[str]:
    # Prefer repo/workspace root .gitignore (Shike is a module under WORKSPACE).
    gitignore = WORKSPACE / ".gitignore"
    if not gitignore.is_file():
        return ["missing WORKSPACE .gitignore (expected to ignore .env files)"]
    content = gitignore.read_text(encoding="utf-8", errors="replace")
    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.strip().startswith("#")]

    # Accept either explicit entries or a wildcard that covers them.
    def has(pattern: str) -> bool:
        return any(line == pattern for line in lines)

    has_env = has(".env")
    has_env_local = has(".env.local") or has(".env.*") or any(line.startswith(".env") and "*" in line for line in lines)
    has_env_prod = has(".env.production") or has(".env.*") or any(line.startswith(".env") and "*" in line for line in lines)

    problems: list[str] = []
    if not has_env:
        problems.append("WORKSPACE .gitignore missing '.env' rule")
    if not has_env_local:
        problems.append("WORKSPACE .gitignore missing rule covering '.env.local'")
    if not has_env_prod:
        problems.append("WORKSPACE .gitignore missing rule covering '.env.production'")
    return problems


def _check_apk_secret_hygiene() -> list[str]:
    """Run the APK artifact secret hygiene validator.

    Returns:
        Empty list when the APK validator passes; safe redacted output lines otherwise.
    """

    result = subprocess.run(
        [sys.executable, str(ROOT / "validation/validate_apk_secret_hygiene.py")],
        cwd=WORKSPACE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if result.returncode == 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def main() -> int:
    missing_targets = [str(p.relative_to(WORKSPACE)) for p in SCAN_TARGETS if not p.exists()]
    if missing_targets:
        # Missing paths are not fatal; structure may evolve. We still scan what exists.
        for rel in missing_targets:
            print(f"WARN\tmissing_scan_target\t{rel}")

    findings: list[Finding] = []
    for target in SCAN_TARGETS:
        for p in _iter_text_files(target):
            text = _read_text(p)
            findings.extend(_find_in_text(p, text))

    findings.extend(_check_android_must_not_mention_tokens())

    gitignore_problems = _check_gitignore_env_rules()
    apk_secret_problems = _check_apk_secret_hygiene()

    passed = True
    if gitignore_problems:
        passed = False
        for msg in gitignore_problems:
            print(f"FAIL\tgitignore\t{msg}")

    if findings:
        passed = False
        for f in findings:
            rel = f.path.relative_to(WORKSPACE)
            print(f"FAIL\t{f.rule}\t{rel}:{f.line_no}\t{f.preview}")

    if apk_secret_problems:
        passed = False
        print("FAIL\tapk_secret_hygiene\tvalidation/validate_apk_secret_hygiene.py")
        for line in apk_secret_problems:
            print(line)

    if passed:
        print("PASS\tsecret_hygiene")
        return 0
    print(f"SECRET_HYGIENE_FINDINGS\t{len(findings)}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
