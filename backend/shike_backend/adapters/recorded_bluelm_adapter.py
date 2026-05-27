"""Recorded BlueLM adapter.

Purpose:
- Avoid repeated paid/unstable online calls during demos and regression tests.
- Keep the upper layer contract stable: returns AnalyzeResponse.

Security note:
Recordings must be generated only from synthetic/demo-safe inputs (no PII).
This module does not attempt to detect PII; enforce via process + validators.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from shike_backend.adapters.base import AdapterError, ModelAdapter
from shike_backend.schemas import AnalyzeRequest, AnalyzeResponse


@dataclass(frozen=True)
class RecordedBlueLMAdapter:
    recording_dir: Path
    base: ModelAdapter | None = None

    def _path_for(self, input_id: str) -> Path:
        safe = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in input_id)[:80]
        return self.recording_dir / f"{safe}.json"

    def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        path = self._path_for(request.input_id)
        if path.is_file():
            data = json.loads(path.read_text(encoding="utf-8"))
            return AnalyzeResponse.model_validate(data)

        if self.base is None:
            raise AdapterError("recording_missing_and_no_base")

        result = self.base.analyze(request)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result.model_dump(), ensure_ascii=False, indent=2), encoding="utf-8")
        return result

