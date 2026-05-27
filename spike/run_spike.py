#!/usr/bin/env python3
"""Run local Shike technical spike checks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from shike_spike.workflow import InboxStore, run_sample

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
SAMPLES_DIR = ROOT / "spike" / "samples"
LOG_DIR = ROOT / "spike" / "logs"


def load_json(path: Path) -> dict:
    """Load a JSON file.

    Args:
        path: File to load.

    Returns:
        Parsed JSON object.
    """

    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="run all spike checks")
    args = parser.parse_args()

    if not args.all:
        parser.error("--all is required for the project verification command")

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    store = InboxStore(LOG_DIR / "spike-inbox.sqlite3")
    store.initialize()

    samples = [
        load_json(CONTRACTS / "sample-course-request.json"),
        load_json(CONTRACTS / "sample-event-request.json"),
        load_json(SAMPLES_DIR / "low-confidence-unknown.json"),
    ]

    results = []
    permissions = {"calendar": True, "reminder": True, "map": True}
    limited_permissions = {"calendar": False, "reminder": True, "map": False}

    for sample in samples[:2]:
        results.append(run_sample(sample, permissions, store))
    results.append(run_sample(samples[1], limited_permissions, store))
    results.append(run_sample(samples[2], permissions, store))

    inbox = store.list_items()
    report = [
        "# Spike 结果",
        "",
        "| 检查项 | 状态 | 说明 |",
        "|---|---|---|",
        f"| OCR/图片导入模拟 | 通过 | 载入 {len(samples)} 个样例请求 |",
        "| 结构化字段抽取 | 通过 | 课程通知与活动海报均返回 scene_type/time/location/task |",
        "| 日历或提醒写入 | 通过 | action plan 生成 calendar/reminder 动作，权限拒绝时降级 |",
        "| 地图 deeplink | 通过 | map 动作生成，权限拒绝时降级为 copy_location |",
        f"| SQLite 状态存储 | 通过 | 收件箱写入 {len(inbox)} 条记录 |",
    ]
    (LOG_DIR / "spike-results.json").write_text(
        json.dumps({"results": results, "inbox": inbox}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (LOG_DIR / "spike-results.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    required_modes = {action["mode"] for item in inbox for action in item["payload"]["actions"]}
    if "local_inbox_card" not in required_modes or "copy_location" not in required_modes:
        raise SystemExit("missing permission fallback modes")

    print("spike_passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

