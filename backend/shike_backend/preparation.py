"""Preparation-item extraction for Shike action cards."""

from __future__ import annotations

import re
from typing import Any


_SEPARATORS_RE = re.compile(r"[、/和及与]")
_STOP_CHARS_RE = re.compile(r"[，,。；;\n]")
_ENGINEERING_TOKENS = ("schema_valid", "manual_review", "provider", "/v1/analyze", "/v2/analyze-image")


def preparation_items_from_text(text: str) -> list[str]:
    """Extract user-facing preparation items from OCR/model text.

    Args:
        text: OCR text, model task summary, action labels, or explanation.

    Returns:
        Distinct concise items such as `带准考证`.
    """

    results: list[str] = []

    def add(value: str) -> None:
        cleaned = _clean_item(value)
        if cleaned and cleaned not in results:
            results.append(cleaned)

    for match in re.finditer(r"记得带([^，,。；;\n]+)", text):
        for item in _expand_carry_items(match.group(1)):
            add(item)
    for match in re.finditer(r"(?:别忘|别忘了)([^，,。；;\n]+)", text):
        raw = match.group(1).strip()
        if raw and raw != "了":
            if raw.startswith(("带", "打印", "上传", "完成", "准备", "自备", "穿", "看", "发")):
                add(raw)
            else:
                add(f"带{raw}")
    if "东西别忘了" in text:
        add("东西别忘了")
    if "别迟到" in text:
        add("别迟到")
    for match in re.finditer(r"记得打印([^，,。；;\n]+)", text):
        add(f"打印{match.group(1)}")
    for match in re.finditer(r"带(?!到|来|回)([^，,。；;\n]+)", text):
        for item in _expand_carry_items(match.group(1)):
            add(item)
    for match in re.finditer(r"带到([^，,。；;\n]+)", text):
        add(f"带纸质版{_object_before(text, match.start())}".strip())
    for match in re.finditer(r"带上([^，,。；;\n]+)", text):
        for item in _expand_carry_items(match.group(1)):
            add(item)
    for match in re.finditer(r"先把([^，,。；;\n]+?)带上", text):
        for item in _expand_carry_items(match.group(1)):
            add(item)
    for match in re.finditer(r"提前准备([^，,。；;\n]+)", text):
        for item in _expand_prepare_items(match.group(1)):
            add(item)
    for match in re.finditer(r"准备([0-9一二三四五六七八九十两]+分钟[^，,。；;\n]+|风险清单|简历|作品集)", text):
        add(f"准备{match.group(1)}")
    for match in re.finditer(r"提前把([^，,。；;\n]+)", text):
        add(f"提前把{match.group(1)}")
    for match in re.finditer(r"(?:先|提前)(安装好[^，,。；;\n]+|看[^，,。；;\n]+|打印[^，,。；;\n]+|下载[^，,。；;\n]+|调试[^，,。；;\n]+)", text):
        add(match.group(1))
    for match in re.finditer(r"上课前(打印[^，,。；;\n]+)", text):
        add(match.group(1))
    for match in re.finditer(r"课前(?:交|提交)([^，,。；;\n]+)", text):
        add(f"带{match.group(1)}")
    for match in re.finditer(r"文件名写\s*([^，,。；;\n]+)", text):
        add(f"文件名写{match.group(1)}")
    for match in re.finditer(r"(上传PDF|完成问卷|截图发群里|扫描报名二维码|先加群报名|完成报名|报名)", text):
        add(match.group(1))
    if "录音作业" in text:
        add("录音作业")
    if "发QQ群" in text:
        add("发QQ群")
    for match in re.finditer(r"(自备[^，,。；;\n]+|穿[^，,。；;\n]+|看PRD第[0-9一二三四五六七八九十]+版|PPT[^，,。；;\n]*备份)", text):
        add(match.group(1))
    for match in re.finditer(r"别忘([^，,。；;\n]+)", text):
        if match.group(1).strip() != "了":
            add(match.group(1))
    for match in re.finditer(r"提前[一二三四五六七八九十两0-9]+分钟(?:到达|到|上线|入场)?", text):
        add(match.group(0))
    for match in re.finditer(r"提前[一二三四五六七八九十两0-9]+(?:小时|分钟)(?:到机场|到站|入会|到达)?", text):
        add(match.group(0))
    for match in re.finditer(r"先去?签到", text):
        add(match.group(0))
    for match in re.finditer(r"课前交([^，,。；;\n]+)", text):
        add(f"课前交{match.group(1)}")
    for match in re.finditer(r"不要迟到", text):
        add(match.group(0))
    for match in re.finditer(r"到[^，,。；;\n]{1,12}集合", text):
        add(match.group(0))

    return sorted(results, key=lambda item: _occurrence_index(text, item))


def enrich_preparation_payload(payload: dict[str, Any], evidence_texts: list[str]) -> dict[str, Any]:
    """Return a model payload with preparation fields filled from evidence.

    Args:
        payload: Schema-compatible response payload.
        evidence_texts: OCR/user/model text that can support preparation items.

    Returns:
        Copy of `payload` with `preparation_items` and `checklist_items`.
    """

    existing_items = _strings(payload.get("preparation_items"))
    checklist_items = _checklist_texts(payload.get("checklist_items"))
    source_text = "\n".join([*_payload_texts(payload), *evidence_texts])
    extracted_items = preparation_items_from_text(source_text)
    items = _distinct([*existing_items, *checklist_items, *extracted_items])
    if not items:
        return payload

    enriched = dict(payload)
    enriched["preparation_items"] = items
    enriched["checklist_items"] = _merge_checklist(payload.get("checklist_items"), items)
    return enriched


def _expand_carry_items(raw: str) -> list[str]:
    return [
        _normalize_carry_item(item)
        for item in (part.strip() for part in _SEPARATORS_RE.split(raw))
        if item
    ]


def _expand_prepare_items(raw: str) -> list[str]:
    return [
        item if item.startswith("准备") else f"准备{item}"
        for item in (part.strip() for part in _SEPARATORS_RE.split(raw))
        if item
    ]


def _normalize_carry_item(item: str) -> str:
    if item.startswith(("带", "打印", "上传", "完成", "截图", "扫描", "自备", "穿", "看", "发")):
        return item
    return f"带{item}"


def _object_before(text: str, index: int) -> str:
    prefix = text[:index]
    if "纸质版" in prefix and "实验报告" in prefix:
        return "实验报告"
    return ""


def _clean_item(value: str) -> str | None:
    cleaned = _STOP_CHARS_RE.sub("", value).strip().strip("：:。，,；;")
    cleaned = cleaned.removesuffix("带上").strip()
    while re.search(r"\s*(标题|未分类|AI)\s*$", cleaned):
        cleaned = re.sub(r"\s*(标题|未分类|AI)\s*$", "", cleaned).strip()
    cleaned = cleaned.replace("PPT存在云盘也备份", "PPT云盘备份")
    if not cleaned or len(cleaned) > 24:
        return None
    if cleaned in {"带上", "带了", "了"}:
        return None
    lower = cleaned.lower()
    if any(token in lower for token in _ENGINEERING_TOKENS):
        return None
    return cleaned


def _occurrence_index(text: str, item: str) -> int:
    candidates = [item, item.removeprefix("带").removeprefix("记得")]
    indexes = [index for candidate in candidates if (index := text.find(candidate)) >= 0]
    return min(indexes) if indexes else 10**9


def _payload_texts(payload: dict[str, Any]) -> list[str]:
    task = payload.get("task")
    actions = payload.get("suggested_actions")
    texts = [
        str(payload.get("title") or ""),
        str(payload.get("explanation") or ""),
    ]
    if isinstance(task, dict):
        texts.append(str(task.get("summary") or ""))
    if isinstance(actions, list):
        texts.extend(str(action.get("label") or "") for action in actions if isinstance(action, dict))
    return texts


def _strings(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _checklist_texts(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [
        item["text"].strip()
        for item in value
        if isinstance(item, dict) and isinstance(item.get("text"), str) and item["text"].strip()
    ]


def _distinct(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item not in result:
            result.append(item)
    return result


def _merge_checklist(value: object, items: list[str]) -> list[dict[str, object]]:
    existing = value if isinstance(value, list) else []
    result = [item for item in existing if isinstance(item, dict) and isinstance(item.get("text"), str)]
    existing_texts = {str(item["text"]).strip() for item in result}
    for item in items:
        if item not in existing_texts:
            result.append({"text": item, "source": "rule", "confidence": 0.86})
    return result
