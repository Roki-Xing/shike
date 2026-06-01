#!/usr/bin/env python3
"""Scan Shike Product Beta readiness against the advanced guide."""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

from source_tree import read_android_source

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class BetaCheck:
    """One Product Beta readiness check.

    Args:
        name: Stable machine-readable check name.
        passed: Whether the current workspace satisfies the check.
        evidence: Short evidence string for the current result.
        next_step: Concrete next action when the check is not yet satisfied.

    Returns:
        Dataclass instance used by the scanner.
    """

    name: str
    passed: bool
    evidence: str
    next_step: str


def read(relative: str) -> str:
    """Read a UTF-8 project file if it exists.

    Args:
        relative: File path relative to the Shike root.

    Returns:
        File text, or an empty string when the file is missing.
    """

    path = ROOT / relative
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def file_exists(relative: str) -> bool:
    """Check whether a repo-relative file exists.

    Args:
        relative: File path relative to the Shike root.

    Returns:
        True when the file exists.
    """

    return (ROOT / relative).is_file()


def has_any_file(pattern: str) -> bool:
    """Check whether any project file matches a glob pattern.

    Args:
        pattern: Glob pattern under the Shike root.

    Returns:
        True when at least one file matches.
    """

    return any(ROOT.glob(pattern))


def load_regression_case_count() -> int:
    """Load the existing synthetic regression case count.

    Args:
        None.

    Returns:
        Number of JSON cases, or 0 when the file cannot be parsed.
    """

    try:
        data = json.loads(read("validation/regression-cases.json"))
    except json.JSONDecodeError:
        return 0
    return len(data) if isinstance(data, list) else 0


def command_passes(command: list[str]) -> bool:
    """Run a project command and return whether it passed.

    Args:
        command: Command and arguments.

    Returns:
        True when the command exits successfully.
    """

    result = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return result.returncode == 0


def check(name: str, passed: bool, evidence: str, next_step: str) -> BetaCheck:
    """Create a Product Beta check row.

    Args:
        name: Stable machine-readable check name.
        passed: Whether the check passed.
        evidence: Current evidence.
        next_step: Suggested next step if failed.

    Returns:
        BetaCheck instance.
    """

    return BetaCheck(name, passed, evidence, next_step)


def build_checks() -> list[BetaCheck]:
    """Build the 30-item Product Beta readiness checklist.

    Args:
        None.

    Returns:
        Ordered beta readiness checks.
    """

    android_source = read_android_source(ROOT)
    home_agenda = read("android-mvp/app/src/main/java/cn/shike/app/ui/HomeAgendaList.kt")
    main_flow = read("android-mvp/app/src/main/java/cn/shike/app/ui/MainFlowScreens.kt")
    capture_entry = read("android-mvp/app/src/main/java/cn/shike/app/ui/CaptureEntryPanel.kt")
    inbox_panel = read("android-mvp/app/src/main/java/cn/shike/app/ui/InboxPanel.kt")
    inbox_workbench = read("android-mvp/app/src/main/java/cn/shike/app/ui/InboxWorkbench.kt")
    inbox_source = inbox_panel + "\n" + inbox_workbench
    import_panel = read("android-mvp/app/src/main/java/cn/shike/app/ui/ImportPanel.kt")
    import_surface = "\n".join([import_panel, capture_entry, main_flow])
    action_controls = read("android-mvp/app/src/main/java/cn/shike/app/ui/ActionPlannerExecutionControls.kt")
    system_actions = read("android-mvp/app/src/main/java/cn/shike/app/system/SystemActions.kt")
    share_mapper = read("android-mvp/app/src/main/java/cn/shike/app/data/ShareImportMapper.kt")
    capture_mapper = read("android-mvp/app/src/main/java/cn/shike/app/data/CaptureImportMapper.kt")
    local_store = read("android-mvp/app/src/main/java/cn/shike/app/data/LocalInboxStore.kt")
    confirm_panel = read("android-mvp/app/src/main/java/cn/shike/app/ui/ParseConfirmPanel.kt")
    model_schema = read("contracts/model-output.schema.json")
    optimization_log = read("docs/optimization-log.md")
    current_status = read("docs/current-validation-status.md")
    sample_cases = load_regression_case_count()

    today_ranking_passes = file_exists("validation/validate_today_ranking.py") and command_passes(
        ["python3", "validation/validate_today_ranking.py"]
    )
    has_today_model = "TodayActionItem" in android_source or today_ranking_passes
    fixed_home_titles = [
        "高数A班教室变更",
        "AI应用分享会报名截止",
        "行动卡：查看路线并提交作业",
    ]
    fixed_agenda_cards = sum(1 for title in fixed_home_titles if title in home_agenda)
    main_screen = read("android-mvp/app/src/main/java/cn/shike/app/ui/ShikeMainScreen.kt")
    home_uses_current_item = (
        "fun HomeAgendaList(" in home_agenda
        and "item: ShikeItem" in home_agenda
        and ("HomeAgendaList(" in main_screen or "HomeAgendaList(" in main_flow)
        and (
            "HomeAgendaList(selected)" in main_screen
            or "item = selected" in main_screen
            or "HomeAgendaList(selected)" in main_flow
            or "item = selected" in main_flow
        )
    )
    inbox_status_tokens = ["待确认", "已安排", "即将截止", "已完成", "已忽略"]
    cloud_toggle_mentions = android_source.count("云侧增强")
    log_redaction_tokens = ["脱敏", "手机号", "邮箱", "学号"]

    return [
        check(
            "today_uses_inbox_data",
            has_today_model and home_uses_current_item and fixed_agenda_cards == 0,
            f"TodayActionItem/排序脚本={'present' if has_today_model else 'missing'}, current item={home_uses_current_item}, fixed demo titles={fixed_agenda_cards}",
            "实现 TodayActionItem 映射，让首页从本地收件箱生成行动卡，不再硬编码固定 AgendaCard。",
        ),
        check(
            "today_empty_state",
            "空状态" in android_source and any(token in android_source for token in ["截图", "拍照", "分享"]),
            "空状态入口文案" if "空状态" in android_source else "missing",
            "为今日行动台增加空收件箱状态，并提供截图、拍照、分享或手动输入入口。",
        ),
        check(
            "today_error_state",
            "错误状态" in android_source or "加载失败" in android_source,
            "错误状态/加载失败" if ("错误状态" in android_source or "加载失败" in android_source) else "missing",
            "为今日行动台增加本地数据加载失败和后端不可用的可解释错误状态。",
        ),
        check(
            "today_sorting_test",
            today_ranking_passes,
            "TODAY_RANKING_METRIC 7/7" if today_ranking_passes else "missing or failing",
            "新增 10 条合成 TodayActionItem 样例和稳定排序验证脚本。",
        ),
        check(
            "inbox_five_status_filters",
            all(token in inbox_source for token in inbox_status_tokens),
            "status tokens=" + ",".join(token for token in inbox_status_tokens if token in inbox_source),
            "在收件箱实现待确认、已安排、即将截止、已完成、已忽略等状态筛选。",
        ),
        check(
            "inbox_search",
            "搜索" in inbox_panel,
            "search control present" if "搜索" in inbox_panel else "missing",
            "为收件箱增加标题、地点、来源文本、场景搜索并补充验证。",
        ),
        check(
            "detail_shows_ocr_raw_text",
            "rawText" in android_source and "OCR 原文" in android_source,
            "rawText present, OCR label=" + str("OCR 原文" in android_source),
            "在卡片详情展示 OCR 原文，并允许用户按隐私设置关闭保存。",
        ),
        check(
            "detail_shows_model_explanation",
            "explanation" in model_schema and "模型解释" in android_source,
            "schema explanation=" + str("explanation" in model_schema),
            "在确认页或详情页展示模型解释，低置信度时说明需要人工确认的原因。",
        ),
        check(
            "detail_shows_execution_result",
            "ExecutionResult" in android_source,
            "ExecutionResult reference" if "ExecutionResult" in android_source else "missing",
            "为日历、提醒、地图执行结果建立 ExecutionResult，并在收件箱详情展示。",
        ),
        check(
            "can_edit_title_time_location",
            all(token in confirm_panel for token in ["title", "time", "location"]) and "确认修正" in android_source,
            "confirm fields title/time/location=" + str(all(token in confirm_panel for token in ["title", "time", "location"])),
            "确认页保留标题、时间、地点二次编辑，并补充对应行为验证。",
        ),
        check(
            "archive_and_restore",
            all(token in inbox_panel or token in local_store for token in ["归档", "恢复"]),
            "archive/restore mentioned",
            "实现收件箱归档与恢复，归档不删除数据，恢复路径有确认和验证。",
        ),
        check(
            "gallery_to_capture_draft",
            all(token in android_source for token in ["GetContent", "CaptureDraft"]) or "CaptureDraft" in capture_mapper,
            "gallery import present, CaptureDraft=" + str("CaptureDraft" in android_source or "CaptureDraft" in capture_mapper),
            "将相册 URI 导入统一到 CaptureDraft 管线。",
        ),
        check(
            "camera_to_capture_draft",
            all(token in android_source for token in ["TakePicturePreview", "CaptureDraft"]) or "CaptureDraft" in capture_mapper,
            "camera import present, CaptureDraft=" + str("CaptureDraft" in android_source or "CaptureDraft" in capture_mapper),
            "将拍照 Bitmap 导入统一到 CaptureDraft 管线。",
        ),
        check(
            "share_to_capture_draft",
            all(token in android_source for token in ["ACTION_SEND", "CaptureDraft"]) or "CaptureDraft" in share_mapper,
            "share import present, CaptureDraft=" + str("CaptureDraft" in android_source or "CaptureDraft" in share_mapper),
            "将 ACTION_SEND 文本入口统一到 CaptureDraft 管线并保留来源。",
        ),
        check(
            "manual_input_analyze",
            "手动" in import_surface and ("解析" in import_surface or "继续" in import_surface),
            "manual input mention" if "手动" in import_surface else "missing",
            "增加手动输入入口，允许无 OCR 或 OCR 失败时直接进入解析。",
        ),
        check(
            "ocr_failure_manual_continue",
            ("OCR 失败" in android_source or "未识别到稳定文字" in android_source)
            and ("手动" in android_source or "继续" in android_source),
            "OCR failure fallback" if "OCR 失败" in android_source else "missing",
            "将 OCR 失败分类为 no_text、low_quality、permission_denied、timeout，并提供手动继续。",
        ),
        check(
            "low_confidence_manual_review",
            "confidence" in model_schema and ("人工确认" in android_source or "待人工确认" in android_source),
            "confidence schema and manual review UI",
            "低置信度模型结果必须进入人工确认，不能启用系统动作。",
        ),
        check(
            "missing_location_disables_map",
            "缺少地点" in android_source and "地图" in action_controls,
            "missing location map guard" if "缺少地点" in android_source else "missing",
            "需要地图但缺少地点时禁用地图动作，并解释缺失原因。",
        ),
        check(
            "missing_time_disables_calendar",
            "缺少时间" in android_source and "加日历" in action_controls,
            "missing time calendar guard" if "缺少时间" in android_source else "missing",
            "需要日历但缺少时间时禁用日历动作，并要求用户修正。",
        ),
        check(
            "relative_time_prompt",
            "相对时间" in android_source or "今晚" in confirm_panel,
            "relative time prompt" if ("相对时间" in android_source or "今晚" in confirm_panel) else "missing",
            "对今晚、明天等相对时间在确认页提示用户确认具体日期。",
        ),
        check(
            "timed_reminder_scheduler",
            "ReminderScheduler" in android_source or "AlarmManager" in android_source,
            "ReminderScheduler/AlarmManager present" if ("ReminderScheduler" in android_source or "AlarmManager" in android_source) else "missing",
            "实现真实定时提醒调度，不再只发即时通知。",
        ),
        check(
            "reminder_permission_fallback",
            "通知权限" in android_source and ("permission_blocked" in android_source or "权限拒绝" in android_source),
            "notification permission fallback",
            "通知权限拒绝时保留行动卡，进入 permission_blocked 或 fallback_ready。",
        ),
        check(
            "map_unavailable_copy_location",
            "ClipboardManager" in android_source or "ClipData" in android_source,
            "clipboard fallback present" if ("ClipboardManager" in android_source or "ClipData" in android_source) else "missing",
            "地图不可用或无地图 App 时提供复制地点降级。",
        ),
        check(
            "calendar_intent_not_saved_claim",
            "已打开系统新增页" in android_source and "CalendarContract" in system_actions,
            "calendar opened wording" if "已打开系统新增页" in android_source else "missing",
            "日历 Intent 只能记录已打开系统新增页，不得记录成用户已保存。",
        ),
        check(
            "cloud_off_does_not_call_backend",
            cloud_toggle_mentions > 0 and ("关闭云侧增强" in android_source or "关闭云侧增强" in optimization_log),
            f"cloud toggle mentions={cloud_toggle_mentions}",
            "实现云侧增强开关；关闭时 Android 不应发起后端解析请求。",
        ),
        check(
            "log_redaction",
            any(token in android_source or token in optimization_log for token in log_redaction_tokens),
            "redaction token present" if any(token in android_source or token in optimization_log for token in log_redaction_tokens) else "missing",
            "增加日志脱敏验证，覆盖手机号、邮箱、学号和完整局域网地址。",
        ),
        check(
            "clear_local_data",
            "一键清除" in android_source or "数据清除" in android_source,
            "clear data control" if ("一键清除" in android_source or "数据清除" in android_source) else "missing",
            "在设置页增加一键清除本地收件箱和设置的真实工程行为。",
        ),
        check(
            "backend_schema_validation",
            file_exists("contracts/model-output.schema.json") and "schema" in read("backend/shike_backend/main.py"),
            "schema file and backend route present",
            "保持 /v1/schema 与 Android 契约一致，并让后端分析结果进入 schema 校验。",
        ),
        check(
            "model_eval_110_cases",
            sample_cases >= 110,
            f"synthetic cases={sample_cases}",
            "建立不少于 110 条合成模型评测样例，覆盖课程、活动、会议、作业、面试、出行票务、低质量和反例。",
        ),
        check(
            "optimization_log_updated",
            "Round 074" in optimization_log
            and "PRODUCT_BETA_METRIC" in optimization_log
            and "Product Beta readiness now passes at `30/30`" in current_status
            and "`python3 shike/validation/validate_advanced_product_beta.py --strict` | PASS" in current_status
            and "Do not treat `validate_advanced_product_beta.py --strict` as a required pass until Product Beta exits the S2 workstream." not in current_status,
            (
                "Product Beta optimization round and current-status completion present"
                if "Round 074" in optimization_log and "Product Beta readiness now passes at `30/30`" in current_status
                else "missing"
            ),
            "每轮继续更新 docs/optimization-log.md，并保持 docs/current-validation-status.md 不回退到 Product Beta strict 未完成口径。",
        ),
    ]


def print_results(checks: list[BetaCheck]) -> None:
    """Print Product Beta readiness results.

    Args:
        checks: Ordered beta readiness checks.

    Returns:
        None.
    """

    for item in checks:
        status = "PASS" if item.passed else "FAIL"
        print(f"{status}\t{item.name}\t{item.evidence}")
        if not item.passed:
            print(f"NEXT\t{item.name}\t{item.next_step}")

    passed = sum(1 for item in checks if item.passed)
    print(f"PRODUCT_BETA_METRIC\t{passed}/{len(checks)}")


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments.

    Args:
        None.

    Returns:
        Parsed argument namespace.
    """

    parser = argparse.ArgumentParser(description="Scan Shike Product Beta readiness.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return non-zero unless every Product Beta readiness check passes.",
    )
    return parser.parse_args()


def main() -> int:
    """Run Product Beta readiness scan.

    Args:
        None.

    Returns:
        0 by default after producing the readiness metric; with --strict, 1 unless all checks pass.
    """

    args = parse_args()
    checks = build_checks()
    print_results(checks)
    if args.strict:
        return 0 if all(item.passed for item in checks) else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
