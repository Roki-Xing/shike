#!/usr/bin/env python3
"""Validate Shike deliverables against the issue acceptance criteria."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Check:
    """One deliverable validation check.

    Args:
        issue_id: Issue identifier.
        description: Human-readable check description.
        files: Files that must exist.
        keywords: Keywords that must appear in the combined file text.
        min_count: Minimum number for optional numeric checks.

    Returns:
        The dataclass is used by the validation runner.
    """

    issue_id: str
    description: str
    files: tuple[str, ...]
    keywords: tuple[str, ...]
    min_count: int | None = None


CHECKS = (
    Check(
        "SHIKE-000",
        "交付边界与评分映射覆盖初赛、复赛、决赛和评分项",
        ("docs/delivery-boundary-and-scoring.md",),
        ("初赛", "复赛", "决赛增强", "创新性", "应用价值", "完成度", "大模型应用能力", "P0", "P1", "P2"),
    ),
    Check(
        "SHIKE-010",
        "MVP 范围锁定两个入口、两个场景、三个动作和排除项",
        ("docs/mvp-scope.md",),
        ("截图导入", "相机拍照", "课程通知", "活动海报", "日历", "提醒", "地图", "排除项"),
        min_count=4,
    ),
    Check(
        "SHIKE-020",
        "产品规格包含定位、画像、痛点、差异、链路、页面和非目标",
        ("docs/product-spec.md",),
        ("产品定位", "用户画像", "核心痛点", "差异", "核心链路", "页面清单", "非目标", "执行代理", "执行编排", "主动"),
    ),
    Check(
        "SHIKE-030",
        "高保真原型至少覆盖 7 个页面和两条链路",
        ("prototype/high-fidelity-prototype.md", "prototype/index.html", "prototype/demo-storyboard.md"),
        ("今日行动台", "截图悬浮动作卡", "相机导办页", "AI 解析确认页", "行动编排页", "收件箱页", "隐私与端云设置页"),
        min_count=7,
    ),
    Check(
        "SHIKE-040",
        "技术 Spike 覆盖五类关键风险点",
        ("spike/run_spike.py", "spike/shike_spike/model_adapter.py", "spike/shike_spike/workflow.py"),
        ("OCR/图片导入", "结构化字段抽取", "日历或提醒写入", "地图 deeplink", "SQLite 状态存储"),
    ),
    Check(
        "SHIKE-050",
        "模型适配器与 JSON Schema 字段完整",
        ("contracts/model-adapter.md", "contracts/model-output.schema.json", "contracts/sample-course-response.json", "contracts/sample-event-response.json"),
        ("ModelAdapter", "scene_type", "confidence", "time", "location", "task", "suggested_actions", "missing_fields", "BlueLM", "OpenAI"),
    ),
    Check(
        "SHIKE-060",
        "复赛 Android MVP 主链路方案覆盖导入、解析、确认、执行和状态管理",
        (
            "docs/android-mvp-implementation.md",
            "android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt",
            "android-mvp/app/build/outputs/apk/debug/app-debug.apk",
            "android-mvp/build-report.md",
            "backend/shike_backend/main.py",
            "backend/verify_backend.py",
        ),
        ("Android", "Kotlin", "Jetpack Compose", "FastAPI", "导入", "解析", "确认", "动作编排", "收件箱状态", "ShikeApp"),
    ),
    Check(
        "SHIKE-070",
        "初赛材料包包含 PPT、海报、演示脚本和录屏分镜",
        ("materials/preliminary-deck.md", "materials/poster-copy.md", "materials/demo-script.md", "prototype/demo-storyboard.md", "materials/submission-checklist.md"),
        ("PPT", "海报", "演示脚本", "录屏", "作品简介", "用户洞察", "创新点", "架构", "大模型应用"),
    ),
    Check(
        "SHIKE-080",
        "复赛样例回归包含课程和活动各 5 条并覆盖边界情况",
        ("validation/sample-regression.md", "validation/regression-cases.json"),
        ("课程通知", "活动海报", "清晰文本", "模糊时间", "地点缺失", "多个截止时间", "低质量图片"),
        min_count=10,
    ),
    Check(
        "SHIKE-090",
        "降级矩阵覆盖五类风险且决赛增强说明价值、依赖和排除原因",
        ("docs/fallback-and-finals-roadmap.md",),
        ("模型失败", "权限拒绝", "网络不可用", "字段缺失", "官方 API 变化", "端侧轻分类", "隐私脱敏", "桌面组件", "智能体兼容层", "校园模板市场"),
    ),
)


def read_text(relative: str) -> str:
    """Read one project file.

    Args:
        relative: Repo-relative path under `shike`.

    Returns:
        File content.
    """

    path = ROOT / relative
    if path.suffix in {".apk", ".sqlite3", ".bin", ".lock"}:
        return ""
    return path.read_text(encoding="utf-8")


def count_exclusions(text: str) -> int:
    return len(re.findall(r"^\| .* \| .* \| .* \|$", text, re.MULTILINE))


def count_prototype_pages(text: str) -> int:
    return len(re.findall(r"\| .* \| .* \| .* \| .* \|", text)) - 2


def count_regression_cases() -> int:
    data = json.loads((ROOT / "validation/regression-cases.json").read_text(encoding="utf-8"))
    scenes = {item["scene"] for item in data}
    if not {"course_notice", "event_poster"}.issubset(scenes):
        return 0
    course_count = sum(1 for item in data if item["scene"] == "course_notice")
    event_count = sum(1 for item in data if item["scene"] == "event_poster")
    return min(len(data), course_count * 2, event_count * 2)


def numeric_metric(check: Check, combined: str) -> bool:
    if check.min_count is None:
        return True
    if check.issue_id == "SHIKE-010":
        return combined.count("|") >= check.min_count and combined.count("不进入") >= 1
    if check.issue_id == "SHIKE-030":
        return count_prototype_pages(combined) >= check.min_count
    if check.issue_id == "SHIKE-080":
        return count_regression_cases() >= check.min_count
    return count_exclusions(combined) >= check.min_count


def validate_check(check: Check) -> tuple[bool, str]:
    missing_files = [path for path in check.files if not (ROOT / path).is_file()]
    if missing_files:
        return False, f"{check.issue_id}: 缺少文件 {missing_files}"

    combined = "\n".join(read_text(path) for path in check.files)
    missing_keywords = [keyword for keyword in check.keywords if keyword not in combined]
    if missing_keywords:
        return False, f"{check.issue_id}: 缺少关键词 {missing_keywords}"

    if not numeric_metric(check, combined):
        return False, f"{check.issue_id}: 数量型验收未达标"

    return True, f"{check.issue_id}: {check.description}"


def main() -> int:
    passed = 0
    messages = []
    for check in CHECKS:
        ok, message = validate_check(check)
        messages.append(("PASS" if ok else "FAIL", message))
        passed += int(ok)

    for status, message in messages:
        print(f"{status}\t{message}")

    print(f"METRIC\t{passed}/{len(CHECKS)}")
    return 0 if passed == len(CHECKS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
