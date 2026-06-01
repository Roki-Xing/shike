#!/usr/bin/env python3
"""Validate the landing-oriented multi-record inbox layer."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def command_passes(command: list[str]) -> bool:
    result = subprocess.run(command, cwd=WORKSPACE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return result.returncode == 0


def main() -> int:
    entities = read("android-mvp/app/src/main/java/cn/shike/app/data/InboxEntities.kt")
    database = read("android-mvp/app/src/main/java/cn/shike/app/data/InboxDatabase.kt")
    store = read("android-mvp/app/src/main/java/cn/shike/app/data/LocalInboxStore.kt")
    shike_app = read("android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt")
    inbox_panel = read("android-mvp/app/src/main/java/cn/shike/app/ui/InboxPanel.kt")
    inbox_workbench = read("android-mvp/app/src/main/java/cn/shike/app/ui/InboxWorkbench.kt")
    seed = read("android-mvp/app/src/main/java/cn/shike/app/data/InboxSeedFactory.kt")
    tests = read("android-mvp/app/src/test/java/cn/shike/app/data/InboxEntitiesTest.kt")
    current_status = read("docs/current-validation-status.md")
    goal_guide = read("docs/CODEX_GOAL_MODE_OPTIMIZATION_GUIDE.md")
    readme = read("README.md")

    checks = [
        (
            "entity_types_present",
            all(name in entities for name in ["InboxItemEntity", "CaptureDraftEntity", "ActionDraftEntity", "ExecutionResultEntity"]),
            "entities",
        ),
        (
            "sqlite_store_present",
            "SQLiteOpenHelper" in database and "CREATE TABLE IF NOT EXISTS $TABLE_INBOX_ITEMS" in database and "upsertInboxItem" in database,
            "SQLiteOpenHelper",
        ),
        (
            "shared_preferences_kept_for_legacy_snapshot",
            "SharedPreferences" in store and "legacyInboxItemFromPreferences" in store,
            "legacy snapshot",
        ),
        (
            "save_snapshot_writes_sqlite_history",
            "upsertInboxItem" in store and "inboxItemEntityFrom" in store,
            "saveSnapshot",
        ),
        (
            "ui_uses_multi_record_history",
            "initialInboxHistory" in shike_app and "historyEntries" in inbox_panel and "allEntries" in inbox_panel,
            "historyEntries",
        ),
        (
            "workbench_maps_entity_entries",
            "inboxWorkbenchEntryFromEntity" in inbox_workbench and "InboxItemEntity" in inbox_workbench,
            "entity mapper",
        ),
        (
            "seed_covers_50_records",
            "syntheticInboxSeed(count: Int = 50" in seed and "0 until count" in seed,
            "50 records",
        ),
        (
            "status_filter_search_archive_still_present",
            all(token in inbox_workbench for token in ["inboxStatusFilters", "visibleInboxEntries", "matches(query", "inboxArchiveActionStateFor"]),
            "inbox workbench",
        ),
        (
            "unit_tests_cover_entities",
            all(token in tests for token in ["syntheticInboxSeed", "inboxItemEntityFrom", "shikeItemFromInboxEntity"]),
            "InboxEntitiesTest",
        ),
        (
            "android_unit_guard_passes",
            command_passes(["python3", "shike/validation/validate_android_unit_tests.py"]),
            "validate_android_unit_tests.py",
        ),
        (
            "current_status_documents_sqlite_inbox",
            all(
                token in current_status
                for token in [
                    "InboxDatabase",
                    "SQLite history",
                    "InboxItemEntity",
                    "50-record synthetic seed",
                    "legacy `SharedPreferences` snapshot migration",
                ]
            )
            and "does not yet satisfy the guide's Room/SQLite inbox target" not in current_status
            and "至少 50 条历史行动卡合成种子可持久化" in goal_guide
            and "INBOX_WORKBENCH_LANDING_METRIC 12/12" in goal_guide
            and "至少 10 条历史行动卡" not in goal_guide,
            "docs/current-validation-status.md + docs/CODEX_GOAL_MODE_OPTIMIZATION_GUIDE.md",
        ),
        (
            "readme_lists_current_inbox_gate",
            "validate_inbox_workbench_landing.py" in readme
            and "INBOX_WORKBENCH_LANDING_METRIC 12/12" in readme
            and "状态文档同步" in readme,
            "README.md",
        ),
    ]

    passed = sum(1 for _, ok, _ in checks if ok)
    for name, ok, evidence in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}\t{evidence}")
    print(f"INBOX_WORKBENCH_LANDING_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
