from __future__ import annotations

from difflib import SequenceMatcher
import re
from typing import Iterable

from .analysis import effective_category
from .models import InventoryItem


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def score_item(item: InventoryItem, query: str) -> float:
    query_text = query.lower().strip()
    if not query_text:
        return 0.0

    searchable_parts = [
        item.asset_id,
        item.name,
        effective_category(item),
        item.location,
        item.container,
        item.tag_color,
        item.notes,
    ]
    searchable = " ".join(part for part in searchable_parts if part).lower()
    query_tokens = tokenize(query_text)
    item_tokens = tokenize(searchable)

    score = 0.0
    has_direct_signal = False
    if query_text == item.asset_id.lower():
        score += 6.0
        has_direct_signal = True
    elif item.asset_id.lower().startswith(query_text):
        score += 3.0
        has_direct_signal = True
    if query_text in item.name.lower():
        score += 4.0
        has_direct_signal = True
    if query_text in searchable:
        score += 1.5
        has_direct_signal = True
    if query_tokens:
        overlap = len(query_tokens & item_tokens) / len(query_tokens)
        score += 3.0 * overlap
        has_direct_signal = has_direct_signal or overlap > 0
    fuzzy_ratio = SequenceMatcher(None, query_text, item.name.lower()).ratio()
    if not has_direct_signal and fuzzy_ratio < 0.65:
        return 0.0
    score += 0.5 * fuzzy_ratio
    return round(score, 4)


def search_items(
    items: Iterable[InventoryItem],
    query: str,
    limit: int = 10,
) -> list[tuple[float, InventoryItem]]:
    scored = [(score_item(item, query), item) for item in items]
    scored = [pair for pair in scored if pair[0] > 0]
    scored.sort(key=lambda pair: (-pair[0], pair[1].name, pair[1].asset_id))
    return scored[:limit]
