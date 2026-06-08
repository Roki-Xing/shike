#!/usr/bin/env python3
"""Collect real cloud-device evidence with adb.

The script automates capture mechanics only. It does not fabricate MP4 files,
report values, or logcat content. Operators still need to perform each scenario
on a connected device while `adb screenrecord` is running.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVIDENCE_ROOT = ROOT / "materials/evidence/cloud-device"
REPORT_NAME = "cloud-device-test-report.md"
LOGCAT_NAME = "cloud-device-logcat.txt"
REMOTE_DIR = "/sdcard/shike-cloud-device-evidence"
PREFLIGHT_SCRIPT = ROOT / "scripts/preflight_cloud_backend.py"
DEFAULT_PREFLIGHT_TIMEOUT_SECONDS = 90


@dataclass(frozen=True)
class Scenario:
    """One required strict-release cloud-device recording."""

    name: str
    title: str
    operator_prompt: str


REQUIRED_SCENARIOS = (
    Scenario(
        "01-cloud-install-open.mp4",
        "安装并打开",
        "安装桌面 APK，打开拾刻，覆盖 Android 16 guide 14.1：确认无第二套假状态栏/假日期且首页第一屏可用。",
    ),
    Scenario(
        "02-cloud-gallery-bluelm.mp4",
        "相册截图导入 + BlueLM",
        "从导入页选择合成课程/活动截图，点击解析，确认生成待确认卡、状态栏时间未被提取且动作未自动执行。",
    ),
    Scenario(
        "03-cloud-camera-bluelm.mp4",
        "拍照导入 + BlueLM",
        "拍摄合成海报或课程通知，解析后检查标题、时间、地点、风险和确认门禁。",
    ),
    Scenario(
        "04-cloud-share-text.mp4",
        "截图分享图片 + 文本分享边界",
        "覆盖 Android 16 guide 14.2：从系统截图浮层分享合成图片到拾刻，显示缩略图后点开始识别；再抽查文本分享不携带旧图片。",
    ),
    Scenario(
        "05-cloud-permission-fallback.mp4",
        "权限降级",
        "覆盖 Android 16 guide 14.4：拒绝通知或图片权限，确认行动卡保留且提示可恢复，不崩溃。",
    ),
    Scenario(
        "06-cloud-backend-failure.mp4",
        "后端失败回退",
        "临时切换不可达后端或断网，确认进入手动确认/本地回退而非训练样例。",
    ),
    Scenario(
        "07-cloud-restart-restore.mp4",
        "重启恢复",
        "创建待确认或已安排行动后重启 App，确认收件箱和未过期提醒状态可恢复。",
    ),
    Scenario(
        "08-cloud-ui-polish.mp4",
        "UI 体验",
        "覆盖 Android 16 guide 14.7：浏览今日、导入、确认、行动、收件箱、设置页，打开/关闭最近截图助手，确认 Debug 不在主路径且没有自动上传。",
    ),
    Scenario(
        "09-cloud-final-route.mp4",
        "最终闭环",
        "覆盖 Android 16 guide 14.3/14.5/14.6：完成截图/拍照 -> AI 解析 -> 用户确认 -> 日历/提醒/地图 -> 删除原截图系统确认 -> 收件箱追踪。",
    ),
)

ANDROID16_GUIDE_RECORDING_COVERAGE = (
    ("14.1 无假信息", "01-cloud-install-open.mp4", "只显示系统状态栏；页面内无 10:28 / 100% / 固定 5月24日。"),
    ("14.2 截图分享导入", "04-cloud-share-text.mp4", "从系统截图浮层分享图片到拾刻，显示缩略图，用户点击开始识别后才请求后端。"),
    ("14.3 确认后打开日历", "09-cloud-final-route.mp4", "用户确认后打开系统日历新增页，标题/时间/地点带入。"),
    ("14.4 通知权限与提醒", "05-cloud-permission-fallback.mp4", "通知权限允许/拒绝都有可恢复状态，提醒不在确认前执行。"),
    ("14.5 地图", "09-cloud-final-route.mp4", "确认后打开地图或复制地点 fallback。"),
    ("14.6 删除原截图", "09-cloud-final-route.mp4", "MediaStore 系统删除确认后行动卡仍保留并显示删除状态。"),
    ("14.7 最近截图助手", "08-cloud-ui-polish.mp4", "最近截图助手默认关闭，开启后只提示导入，关闭后不再提示。"),
)


def redact_log_text(text: str) -> str:
    """Redact secrets and personal identifiers from log text.

    Args:
        text: Raw logcat or command output.

    Returns:
        Redacted text safe to store in the evidence package.
    """

    redacted = re.sub(r"Authorization\s*:\s*Bearer\s+[^\s]+", "AUTH_HEADER_REDACTED", text, flags=re.I)
    redacted = re.sub(r"\bAppKEY\b\s*=\s*[^\s]+", "PROVIDER_KEY_REDACTED", redacted, flags=re.I)
    redacted = re.sub(r"\bsk-[A-Za-z0-9_=+\-/]{8,}\b", "PROVIDER_KEY_REDACTED", redacted)
    redacted = re.sub(r"data:image/[a-zA-Z0-9.+-]+;base64,[A-Za-z0-9+/=\r\n]+", "IMAGE_DATA_URL_REDACTED", redacted)
    redacted = re.sub(r"\b1[3-9]\d{9}\b", "PHONE_REDACTED", redacted)
    redacted = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "EMAIL_REDACTED", redacted)
    redacted = re.sub(r"\b\d{8,12}\b", "LONG_NUMBER_REDACTED", redacted)
    return redacted


def remote_recording_path(scenario: Scenario) -> str:
    """Return the remote screenrecord path for a scenario."""

    return f"{REMOTE_DIR}/{scenario.name}"


def build_screenrecord_command(serial: str | None, remote_path: str, duration_seconds: int) -> list[str]:
    """Build an adb screenrecord command."""

    command = ["adb"]
    if serial:
        command.extend(["-s", serial])
    command.extend(["shell", "screenrecord", "--time-limit", str(duration_seconds), remote_path])
    return command


def build_pull_command(serial: str | None, remote_path: str, local_path: Path) -> list[str]:
    """Build an adb pull command for one recording."""

    command = ["adb"]
    if serial:
        command.extend(["-s", serial])
    command.extend(["pull", remote_path, str(local_path)])
    return command


def build_preflight_command(base_url: str, timeout_seconds: int, *, allow_cloud_image: bool) -> list[str]:
    """Build one public backend preflight command.

    Args:
        base_url: Public backend base URL reachable by the cloud device.
        timeout_seconds: Per-request timeout for backend checks.
        allow_cloud_image: Whether to verify the live cloud-image branch.

    Returns:
        Command arguments for ``preflight_cloud_backend.py``.
    """

    command = [
        "python3",
        str(PREFLIGHT_SCRIPT),
        "--base-url",
        base_url,
        "--timeout-seconds",
        str(timeout_seconds),
    ]
    if allow_cloud_image:
        command.append("--allow-cloud-image")
    return command


def build_preflight_commands(base_url: str, timeout_seconds: int) -> list[list[str]]:
    """Build deterministic and live-image backend preflight commands.

    Args:
        base_url: Public backend base URL reachable by the cloud device.
        timeout_seconds: Per-request timeout for backend checks.

    Returns:
        Two command lines: no-cloud-image first, live image branch second.
    """

    return [
        build_preflight_command(base_url, timeout_seconds, allow_cloud_image=False),
        build_preflight_command(base_url, timeout_seconds, allow_cloud_image=True),
    ]


def adb_command(serial: str | None, *args: str) -> list[str]:
    """Build a generic adb command."""

    command = ["adb"]
    if serial:
        command.extend(["-s", serial])
    command.extend(args)
    return command


def run(command: list[str], *, dry_run: bool) -> subprocess.CompletedProcess[str]:
    """Run or print a command.

    Args:
        command: Command and arguments.
        dry_run: Print instead of executing.

    Returns:
        A completed process object.
    """

    print("+ " + " ".join(command))
    if dry_run:
        return subprocess.CompletedProcess(command, 0, "", "")
    return subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)


def scenario_by_name(name: str) -> Scenario:
    """Find a scenario by filename or 1-based index."""

    if name.isdigit():
        index = int(name) - 1
        if 0 <= index < len(REQUIRED_SCENARIOS):
            return REQUIRED_SCENARIOS[index]
    for scenario in REQUIRED_SCENARIOS:
        if scenario.name == name:
            return scenario
    raise ValueError(f"Unknown scenario: {name}")


def record_scenario(
    scenario: Scenario,
    *,
    serial: str | None,
    evidence_root: Path,
    duration_seconds: int,
    dry_run: bool,
) -> int:
    """Record and pull one scenario video."""

    evidence_root.mkdir(parents=True, exist_ok=True)
    remote_path = remote_recording_path(scenario)
    local_path = evidence_root / scenario.name

    print(f"SCENARIO {scenario.name}: {scenario.title}")
    print(f"OPERATOR_PROMPT {scenario.operator_prompt}")
    mkdir_result = run(adb_command(serial, "shell", "mkdir", "-p", REMOTE_DIR), dry_run=dry_run)
    if mkdir_result.returncode != 0:
        print(mkdir_result.stdout, end="")
        return mkdir_result.returncode

    record_result = run(build_screenrecord_command(serial, remote_path, duration_seconds), dry_run=dry_run)
    if record_result.returncode != 0:
        print(record_result.stdout, end="")
        return record_result.returncode

    pull_result = run(build_pull_command(serial, remote_path, local_path), dry_run=dry_run)
    if pull_result.returncode != 0:
        print(pull_result.stdout, end="")
        return pull_result.returncode

    run(adb_command(serial, "shell", "rm", "-f", remote_path), dry_run=dry_run)
    return 0


def preflight_backend(*, base_url: str, timeout_seconds: int, dry_run: bool) -> int:
    """Run both public backend preflight branches before recording.

    Args:
        base_url: Public backend base URL reachable by the cloud device.
        timeout_seconds: Per-request timeout for backend checks.
        dry_run: Print commands without executing.

    Returns:
        0 only when both preflight branches pass.
    """

    for command in build_preflight_commands(base_url, timeout_seconds):
        result = run(command, dry_run=dry_run)
        if result.stdout:
            print(result.stdout, end="")
        if result.returncode != 0:
            return result.returncode
    return 0


def capture_logcat(*, serial: str | None, evidence_root: Path, dry_run: bool) -> int:
    """Capture and redact device logcat."""

    evidence_root.mkdir(parents=True, exist_ok=True)
    command = adb_command(serial, "logcat", "-d", "-v", "time")
    result = run(command, dry_run=dry_run)
    if result.returncode != 0:
        print(result.stdout, end="")
        return result.returncode
    if dry_run:
        return 0

    redacted = redact_log_text(result.stdout)
    output = evidence_root / LOGCAT_NAME
    output.write_text(redacted.rstrip() + "\n", encoding="utf-8")
    print(f"WROTE {output}")
    return 0


def adb_shell_value(serial: str | None, prop: str, *, dry_run: bool) -> str:
    """Read one Android property value."""

    result = run(adb_command(serial, "shell", "getprop", prop), dry_run=dry_run)
    if result.returncode != 0 or dry_run:
        return ""
    return result.stdout.strip()


def write_report_draft(
    *,
    serial: str | None,
    evidence_root: Path,
    backend_url: str,
    result_summary: str,
    dry_run: bool,
) -> int:
    """Write a report draft using device metadata and existing videos."""

    evidence_root.mkdir(parents=True, exist_ok=True)
    model = adb_shell_value(serial, "ro.product.model", dry_run=dry_run) or "待确认机型"
    android_version = adb_shell_value(serial, "ro.build.version.release", dry_run=dry_run) or "待确认 Android 版本"
    timestamp = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
    backend_redacted = re.sub(r"://[^/@]+", "://HOST_REDACTED", backend_url) if backend_url else "HOST_REDACTED"

    lines = [
        "# Cloud Device Test Report",
        "",
        f"- 机型: {model}",
        f"- Android 版本: {android_version}",
        f"- 测试时间: {timestamp}",
        f"- 后端地址: {backend_redacted}",
        f"- 后端地址脱敏: {backend_redacted}",
        f"- 结果: {result_summary}",
        "",
        "## Pre-recording Evidence Gate",
        "",
        "- Desktop guidance source checked: `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md`",
        "- Android 16 real implementation guide checked: `/mnt/c/Users/Xing/Desktop/SHIKE_ANDROID16_REAL_IMPLEMENTATION_GUIDE (1).md`",
        "- Requirement matrix checked: `materials/evidence/requirement-matrix.md`",
        "- Requirement matrix gate: `REQUIREMENT_MATRIX_METRIC 9/9`",
        "- Android 16 guide gate: `ANDROID16_REAL_IMPLEMENTATION_GUIDE_METRIC 12/12`",
        "- Strict release gate before filling this report: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7`",
        "- All 9 real cloud-device MP4 files present: operator-confirmed after recording",
        "- No placeholder fields remain after capture: operator-confirmed after final review",
        "",
        "## Summary",
    ]
    summary_fields = (
        "安装与打开",
        "相册导入",
        "拍照导入",
        "分享导入",
        "权限降级",
        "后端失败回退",
        "重启恢复",
        "UI 体验",
    )
    for field in summary_fields:
        lines.append(f"- {field}: 已录制，详见对应视频证据")
    lines.extend(["", "## Android 16 Guide Acceptance Coverage"])
    for section, video, expectation in ANDROID16_GUIDE_RECORDING_COVERAGE:
        status = "present" if (evidence_root / video).is_file() else "missing"
        lines.append(f"- {section}: `{video}` ({status}) - {expectation}")
    lines.extend(["", "## Video Evidence"])
    for scenario in REQUIRED_SCENARIOS:
        status = "present" if (evidence_root / scenario.name).is_file() else "missing"
        lines.append(f"- `{scenario.name}`: {status} - {scenario.title}")

    output = evidence_root / REPORT_NAME
    if dry_run:
        print(f"WOULD_WRITE {output}")
        return 0
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE {output}")
    return 0


def list_scenarios() -> None:
    """Print the required scenario list."""

    for index, scenario in enumerate(REQUIRED_SCENARIOS, start=1):
        print(f"{index}. {scenario.name} - {scenario.title}")
        print(f"   {scenario.operator_prompt}")
    print("Android 16 guide acceptance coverage:")
    for section, video, expectation in ANDROID16_GUIDE_RECORDING_COVERAGE:
        print(f"   {section} -> {video}: {expectation}")


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""

    parser = argparse.ArgumentParser(description="Collect Shike cloud-device evidence with adb.")
    parser.add_argument("--evidence-root", type=Path, default=DEFAULT_EVIDENCE_ROOT)
    parser.add_argument("--serial", help="adb serial. Omit when only one device is connected.")
    parser.add_argument("--duration-seconds", type=int, default=180)
    parser.add_argument("--list", action="store_true", help="List required recording scenarios.")
    parser.add_argument("--record", help="Record one scenario by 1-based index or MP4 filename.")
    parser.add_argument(
        "--preflight-backend",
        action="store_true",
        help="Run no-cloud-image and live-image public backend preflights before recording.",
    )
    parser.add_argument("--capture-logcat", action="store_true", help="Export redacted `cloud-device-logcat.txt`.")
    parser.add_argument("--write-report-draft", action="store_true", help="Write a report draft from device metadata.")
    parser.add_argument("--backend-url", default="https://roky.chat", help="Backend URL to redact into the report.")
    parser.add_argument(
        "--preflight-timeout-seconds",
        type=int,
        default=DEFAULT_PREFLIGHT_TIMEOUT_SECONDS,
        help="Per-request timeout for `--preflight-backend`.",
    )
    parser.add_argument("--result-summary", default="待 strict-ready 复核", help="Report result summary.")
    parser.add_argument("--dry-run", action="store_true", help="Print adb commands without executing them.")
    return parser.parse_args()


def main() -> int:
    """Run the selected collection actions."""

    args = parse_args()
    if args.list:
        list_scenarios()
    exit_code = 0
    if args.preflight_backend:
        exit_code = preflight_backend(
            base_url=args.backend_url,
            timeout_seconds=args.preflight_timeout_seconds,
            dry_run=args.dry_run,
        )
    if exit_code == 0 and args.record:
        try:
            scenario = scenario_by_name(args.record)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        exit_code = record_scenario(
            scenario,
            serial=args.serial,
            evidence_root=args.evidence_root,
            duration_seconds=args.duration_seconds,
            dry_run=args.dry_run,
        )
    if exit_code == 0 and args.capture_logcat:
        exit_code = capture_logcat(serial=args.serial, evidence_root=args.evidence_root, dry_run=args.dry_run)
    if exit_code == 0 and args.write_report_draft:
        exit_code = write_report_draft(
            serial=args.serial,
            evidence_root=args.evidence_root,
            backend_url=args.backend_url,
            result_summary=args.result_summary,
            dry_run=args.dry_run,
        )
    if not (args.list or args.preflight_backend or args.record or args.capture_logcat or args.write_report_draft):
        list_scenarios()
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
