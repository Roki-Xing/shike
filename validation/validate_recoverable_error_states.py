#!/usr/bin/env python3
"""Validate user-recoverable error states for the Shike import and planning flow."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI_ROOT = ROOT / "android-mvp/app/src/main/java/cn/shike/app/ui"


def read(relative: str) -> str:
    """Read a UTF-8 UI source file.

    Args:
        relative: File path under the Android UI source root.

    Returns:
        File content.
    """

    return (UI_ROOT / relative).read_text(encoding="utf-8")


def main() -> int:
    """Run recoverable error-state checks.

    Returns:
        Process exit code.
    """

    frontend = read("FrontendStateComponents.kt")
    main_flow = read("MainFlowScreens.kt")
    planner = read("ActionPlannerPanel.kt")
    execution_gate = read("ExecutionActionGate.kt")
    recoverable_component = frontend[frontend.index("fun RecoverableErrorState("):frontend.index("@Composable\nfun ShikeLoadingSkeleton")]

    checks = [
        (
            "recoverable_error_component_exists",
            "fun RecoverableErrorState(" in frontend
            and "repairActions: List<RecoverableRepairAction>" in frontend
            and "data class RecoverableRepairAction" in frontend,
        ),
        (
            "import_failure_offers_repair_actions",
            "RecoverableErrorState(" in main_flow
            and all(token in main_flow for token in ["重新选择截图", "手动输入", "先存入待确认", "重新解析"]),
        ),
        (
            "import_failure_repairs_are_wired_to_real_handlers",
            "RecoverableRepairAction(\"先存入待确认\", onSavePendingReview)" in main_flow
            and "RecoverableRepairAction(\"重新解析\", onRetryAnalyze)" in main_flow
            and "RecoverableRepairAction(\"先存入待确认\") {}" not in main_flow
            and "RecoverableRepairAction(\"重新解析\") {}" not in main_flow,
        ),
        (
            "missing_time_and_location_have_direct_repairs",
            all(token in execution_gate for token in ["补充时间后可用", "补充地点后可用"])
            and all(token in planner for token in ["补时间", "补地点", "存入待确认"]),
        ),
        (
            "planner_reads_like_order_confirmation",
            all(token in planner for token in ["将执行以下动作", "加入日历", "设置提醒", "打开地图", "处理后清理截图", "完成安排"]),
        ),
        (
            "calendar_copy_stays_user_confirmed",
            "已打开系统日历新增页" in planner
            and "已写入日历" not in planner
            and "未确认前不会打开外部日历" in planner,
        ),
        (
            "error_state_has_multiple_buttons_not_single_cta",
            "repairActions.forEach" in recoverable_component
            and "OutlinedButton(" in recoverable_component
            and "ShikePrimaryButton(" not in recoverable_component,
        ),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"RECOVERABLE_ERROR_STATES_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
