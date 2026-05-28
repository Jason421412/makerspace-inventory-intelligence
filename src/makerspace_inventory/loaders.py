from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from .models import InventoryItem


FIELDNAMES = [
    "asset_id",
    "name",
    "category",
    "location",
    "container",
    "tag_color",
    "expected_qty",
    "actual_qty",
    "status",
    "notes",
    "source",
]


def load_inventory_csv(path: str | Path) -> list[InventoryItem]:
    with Path(path).open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        missing = set(FIELDNAMES) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")
        return [InventoryItem.from_row(row) for row in reader if row.get("name") or row.get("asset_id")]


def save_inventory_csv(items: Iterable[InventoryItem], path: str | Path) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        for item in items:
            writer.writerow(item.to_row())
