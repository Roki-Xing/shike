"""Workflow and persistence spike for Shike."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .model_adapter import MockModelAdapter, ModelInput


class ActionPlanner:
    """Converts model output into confirmed action plans."""

    def build_plan(self, output: dict[str, Any], permissions: dict[str, bool]) -> dict[str, Any]:
        """Build an executable or downgraded action plan.

        Args:
            output: Model output following the Shike schema.
            permissions: Permission availability for calendar, reminder, and map.

        Returns:
            Action plan with execution mode per suggested action.
        """

        actions = []
        for action in output["suggested_actions"]:
            action_type = action["type"]
            permitted = permissions.get(action_type, True)
            mode = "native" if permitted else self._fallback_mode(action_type)
            actions.append({
                "type": action_type,
                "label": action["label"],
                "mode": mode,
                "requires_user_confirmation": True,
            })
        needs_confirmation = bool(output["missing_fields"]) or output.get("confidence", 0) < 0.65
        return {
            "title": output["title"],
            "scene_type": output["scene_type"],
            "status": "pending_confirmation" if needs_confirmation else "ready_to_execute",
            "actions": actions,
            "missing_fields": output["missing_fields"],
        }

    @staticmethod
    def _fallback_mode(action_type: str) -> str:
        if action_type == "calendar":
            return "local_inbox_card"
        if action_type == "reminder":
            return "in_app_countdown"
        if action_type == "map":
            return "copy_location"
        return "manual"


class InboxStore:
    """SQLite-backed local state store for the spike."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def initialize(self) -> None:
        """Create the inbox table.

        Args:
            None.

        Returns:
            None.
        """

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS inbox_items (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    scene_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    payload TEXT NOT NULL
                )
                """
            )

    def upsert_item(self, item_id: str, plan: dict[str, Any]) -> None:
        """Insert or update one inbox item.

        Args:
            item_id: Stable item identifier.
            plan: Action plan payload.

        Returns:
            None.
        """

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO inbox_items (id, title, scene_type, status, payload)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    title = excluded.title,
                    scene_type = excluded.scene_type,
                    status = excluded.status,
                    payload = excluded.payload
                """,
                (
                    item_id,
                    plan["title"],
                    plan["scene_type"],
                    plan["status"],
                    json.dumps(plan, ensure_ascii=False),
                ),
            )

    def list_items(self) -> list[dict[str, Any]]:
        """Read all inbox items.

        Args:
            None.

        Returns:
            List of persisted inbox rows with decoded payload.
        """

        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT id, title, scene_type, status, payload FROM inbox_items ORDER BY id"
            ).fetchall()
        return [
            {
                "id": row[0],
                "title": row[1],
                "scene_type": row[2],
                "status": row[3],
                "payload": json.loads(row[4]),
            }
            for row in rows
        ]


def run_sample(sample: dict[str, Any], permissions: dict[str, bool], store: InboxStore) -> dict[str, Any]:
    """Run one sample through adapter, planner, and store.

    Args:
        sample: Sample request data.
        permissions: Permission availability map.
        store: Local inbox store.

    Returns:
        Combined spike result.
    """

    adapter = MockModelAdapter()
    planner = ActionPlanner()
    output = adapter.analyze(ModelInput(
        input_id=sample["input_id"],
        source_type=sample["source_type"],
        ocr_text=sample["ocr_text"],
        scene_hint=sample.get("scene_hint"),
    ))
    plan = planner.build_plan(output, permissions)
    store.upsert_item(sample["input_id"], plan)
    return {"input_id": sample["input_id"], "model_output": output, "plan": plan}
