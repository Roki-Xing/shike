#!/usr/bin/env python3
"""Validate redacted live-smoke evidence for backend private-env model tests."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACCESS_LOG_PATH = ROOT / "materials/evidence/cloud-device/backend-redacted-access-log.txt"

SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9]{8,}\b"),
    re.compile(r"Authorization\s*[:=]", re.IGNORECASE),
    re.compile(r"Bearer\s+[A-Za-z0-9._=-]+", re.IGNORECASE),
    re.compile(r"data:image/[A-Za-z0-9.+-]+;base64,", re.IGNORECASE),
    re.compile(r"\b1[3-9]\d{9}\b"),
    re.compile(r"[\w.\-]+@[\w.\-]+\.\w+"),
)

SECRET_TOKENS = (
    "AppKEY",
    "BLUELM_APP_KEY",
    "VIVO_AIGC_APP_KEY",
    "VIVO_OCR_APP_KEY",
    "VIVO_MULTIMODAL_APP_KEY",
    "api_key",
    "credential",
    "password",
    "secret=",
    "token=",
)


@dataclass(frozen=True)
class Check:
    """One validator check result."""

    name: str
    ok: bool
    evidence: str


def read(path: Path) -> str:
    """Read a UTF-8 evidence file.

    Args:
        path: Evidence file path.

    Returns:
        File text, or an empty string when absent.
    """

    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def contains_all(text: str, tokens: tuple[str, ...]) -> bool:
    """Return whether all required tokens appear in text.

    Args:
        text: Evidence text.
        tokens: Required substrings.

    Returns:
        True when every token is present.
    """

    return all(token in text for token in tokens)


def contains_secret_like_value(text: str) -> bool:
    """Detect raw credentials, personal data, or image payloads in evidence text.

    Args:
        text: Evidence text.

    Returns:
        True when the evidence includes unsafe data.
    """

    lowered = text.lower()
    if any(token.lower() in lowered for token in SECRET_TOKENS):
        return True
    return any(pattern.search(text) is not None for pattern in SECRET_PATTERNS)


def build_checks(path: Path = ACCESS_LOG_PATH) -> list[Check]:
    """Build redacted live-smoke evidence checks.

    Args:
        path: Backend redacted access log path.

    Returns:
        Ordered check results.
    """

    text = read(path)
    return [
        Check("access_log_exists", bool(text), str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)),
        Check("no_secret_like_tokens", bool(text) and not contains_secret_like_value(text), "no AppKEY/token/base64/PII"),
        Check(
            "bluelm_text_schema_valid",
            contains_all(text, ("provider=bluelm", "result_schema_valid=true", "scene_type=course_notice")),
            "BlueLM text route schema-valid course notice",
        ),
        Check(
            "vivo_ocr_passed_and_image_cleared",
            contains_all(
                text,
                (
                    "provider=vivo_general_ocr",
                    "ocr_status=pass",
                    "image_persisted=false",
                    "image_cleared=true",
                    "ocr_text_length=",
                ),
            ),
            "vivo OCR pass with non-persistent image handling",
        ),
        Check(
            "multimodal_fallback_then_pass",
            contains_all(
                text,
                (
                    "multimodal_status=fail",
                    "provider_model_does_not_support_image",
                    "selected_model=Volc-DeepSeek-V3.2",
                    "multimodal_status=pass",
                    "selected_model=Doubao-Seed-2.0-mini",
                    "multimodal_schema_valid=true",
                ),
            ),
            "image model fallback then schema-valid candidate",
        ),
        Check(
            "route_v2_schema_valid_and_actions_disabled",
            contains_all(
                text,
                (
                    "route_v2_status=pass",
                    "route_v2_schema_valid=true",
                    "route_v2_actions_disabled=true",
                    "route_v2_ignored_regions_allowed=true",
                    "ignored_regions=top_status_bar,bottom_navigation_bar",
                    "scene_type=course_notice",
                ),
            )
            and "route_v2_actions_disabled=false" not in text,
            "route-v2 schema valid with user-confirmation action gate",
        ),
        Check("live_smoke_metric_4_of_4", "live_smoke_metric=4/4" in text, "combined live smoke 4/4"),
    ]


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments.

    Returns:
        Parsed command-line arguments.
    """

    parser = argparse.ArgumentParser(description="Validate redacted Shike live-smoke evidence.")
    parser.add_argument(
        "--access-log",
        type=Path,
        default=ACCESS_LOG_PATH,
        help="Path to backend-redacted-access-log.txt.",
    )
    return parser.parse_args()


def main() -> int:
    """Run live-smoke evidence validation.

    Returns:
        0 when every check passes.
    """

    args = parse_args()
    checks = build_checks(args.access_log)
    passed = sum(1 for check in checks if check.ok)
    for check in checks:
        print(f"{'PASS' if check.ok else 'FAIL'}\t{check.name}\t{check.evidence}")
    print(f"LIVE_SMOKE_EVIDENCE_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
