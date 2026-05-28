from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import re
from typing import Iterable

from .models import InventoryItem


CATEGORY_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("microcontroller", ("arduino", "raspberry", "esp32", "grovepi", "microcontroller")),
    ("sensor", ("sensor", "rfid", "pir", "ldr", "moisture", "humidity", "ultrasonic", "camera")),
    ("power", ("battery", "power supply", "adapter", "charger", "solar", "relay")),
    ("fabrication", ("3d printer", "filament", "laser", "cutter", "perspex", "acrylic")),
    ("robotics", ("robot", "servo", "motor", "wheel", "chassis", "arm", "actuator")),
    ("communication", ("lora", "gateway", "wifi", "bluetooth", "rf", "antenna")),
    ("display", ("lcd", "display", "led", "light", "screen")),
    ("tooling", ("tool", "screw", "marker", "glove", "tape", "cabinet", "connector", "wire")),
    ("smart_garden", ("garden", "plant", "pump", "soil", "grow")),
]


STATUS_ALIASES = {
    "": "recorded",
    "inventory_record": "recorded",
    "ok": "complete",
    "available": "complete",
    "complete": "complete",
    "unknown": "unknown",
    "need checking": "unknown",
    "missing": "missing",
    "no label": "no_label",
    "no_label": "no_label",
    "mixed": "mixed",
}


@dataclass(frozen=True)
class DuplicateCandidate:
    left: InventoryItem
    right: InventoryItem
    score: float


def infer_category(name: str) -> str:
    lowered = name.lower()
    for category, keywords in CATEGORY_RULES:
        if any(keyword in lowered for keyword in keywords):
            return category
    return "general"


def normalized_status(item: InventoryItem) -> str:
    raw = item.status.strip().lower().replace("-", "_")
    if raw in STATUS_ALIASES:
        return STATUS_ALIASES[raw]
    if "missing" in raw:
        return "missing"
    if "unknown" in raw or "check" in raw:
        return "unknown"
    if "label" in raw:
        return "no_label"
    if "mixed" in raw:
        return "mixed"
    return raw or "recorded"


def effective_category(item: InventoryItem) -> str:
    return item.category or infer_category(item.name)


def has_quantity_gap(item: InventoryItem) -> bool:
    delta = item.quantity_delta
    return delta is not None and abs(delta) > 0


def priority_score(item: InventoryItem) -> int:
    status_score = {
        "missing": 100,
        "unknown": 85,
        "no_label": 70,
        "mixed": 65,
        "recorded": 20,
        "complete": 0,
    }.get(normalized_status(item), 45)
    score = status_score
    if item.notes:
        score += 10
    if has_quantity_gap(item):
        score += min(30, int(abs(item.quantity_delta or 0) * 3))
    if not item.location:
        score += 5
    return score


def summarize(items: Iterable[InventoryItem]) -> dict[str, object]:
    item_list = list(items)
    status_counts = Counter(normalized_status(item) for item in item_list)
    category_counts = Counter(effective_category(item) for item in item_list)
    return {
        "total_assets": len(item_list),
        "status_counts": dict(status_counts.most_common()),
        "category_counts": dict(category_counts.most_common()),
        "follow_up_count": sum(priority_score(item) >= 70 for item in item_list),
        "quantity_gap_count": sum(has_quantity_gap(item) for item in item_list),
    }


def rank_followups(items: Iterable[InventoryItem], limit: int = 10) -> list[tuple[int, InventoryItem]]:
    ranked = [(priority_score(item), item) for item in items]
    ranked.sort(key=lambda pair: (-pair[0], pair[1].asset_id, pair[1].name))
    return [pair for pair in ranked if pair[0] >= 45][:limit]


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def _trigrams(text: str) -> set[str]:
    compact = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
    if len(compact) < 3:
        return {compact} if compact else set()
    return {compact[i : i + 3] for i in range(len(compact) - 2)}


def _similarity(left: str, right: str) -> float:
    left_tokens = _tokens(left)
    right_tokens = _tokens(right)
    token_score = len(left_tokens & right_tokens) / max(1, len(left_tokens | right_tokens))
    left_trigrams = _trigrams(left)
    right_trigrams = _trigrams(right)
    trigram_score = len(left_trigrams & right_trigrams) / max(1, len(left_trigrams | right_trigrams))
    return (token_score * 0.6) + (trigram_score * 0.4)


def _is_generic_component_name(name: str) -> bool:
    return bool(re.search(r"\bcomponent\s+\d", name.lower()))


def detect_duplicate_names(
    items: Iterable[InventoryItem],
    threshold: float = 0.74,
    limit: int = 20,
) -> list[DuplicateCandidate]:
    item_list = [item for item in items if len(item.name) >= 4]
    candidates: list[DuplicateCandidate] = []
    for idx, left in enumerate(item_list):
        for right in item_list[idx + 1 :]:
            if left.asset_id == right.asset_id and left.source == right.source:
                continue
            if _is_generic_component_name(left.name) and _is_generic_component_name(right.name):
                continue
            score = _similarity(left.name, right.name)
            if score >= threshold:
                candidates.append(DuplicateCandidate(left=left, right=right, score=round(score, 3)))
    candidates.sort(key=lambda candidate: (-candidate.score, candidate.left.name, candidate.right.name))
    return candidates[:limit]
