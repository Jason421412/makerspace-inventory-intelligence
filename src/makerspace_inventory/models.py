from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Mapping


_EMPTY_VALUES = {"", "-", "?", "n/a", "na", "none", "null"}


def clean_text(value: object) -> str:
    """Normalize spreadsheet-style cell values into stable strings."""
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def parse_simple_quantity(value: object) -> float | None:
    """Parse simple numeric quantities and ignore labels such as ``2*9``."""
    text = clean_text(value).lower()
    if text in _EMPTY_VALUES:
        return None
    if re.fullmatch(r"-?\d+(?:\.\d+)?", text):
        number = float(text)
        return int(number) if number.is_integer() else number
    return None


@dataclass(frozen=True)
class InventoryItem:
    asset_id: str
    name: str
    category: str = ""
    location: str = ""
    container: str = ""
    tag_color: str = ""
    expected_qty: str = ""
    actual_qty: str = ""
    status: str = ""
    notes: str = ""
    source: str = ""

    @classmethod
    def from_row(cls, row: Mapping[str, object]) -> "InventoryItem":
        return cls(
            asset_id=clean_text(row.get("asset_id")),
            name=clean_text(row.get("name")),
            category=clean_text(row.get("category")),
            location=clean_text(row.get("location")),
            container=clean_text(row.get("container")),
            tag_color=clean_text(row.get("tag_color")),
            expected_qty=clean_text(row.get("expected_qty")),
            actual_qty=clean_text(row.get("actual_qty")),
            status=clean_text(row.get("status")),
            notes=clean_text(row.get("notes")),
            source=clean_text(row.get("source")),
        )

    @property
    def expected_number(self) -> float | None:
        return parse_simple_quantity(self.expected_qty)

    @property
    def actual_number(self) -> float | None:
        return parse_simple_quantity(self.actual_qty)

    @property
    def quantity_delta(self) -> float | None:
        if self.expected_number is None or self.actual_number is None:
            return None
        return self.actual_number - self.expected_number

    def to_row(self) -> dict[str, str]:
        return {
            "asset_id": self.asset_id,
            "name": self.name,
            "category": self.category,
            "location": self.location,
            "container": self.container,
            "tag_color": self.tag_color,
            "expected_qty": self.expected_qty,
            "actual_qty": self.actual_qty,
            "status": self.status,
            "notes": self.notes,
            "source": self.source,
        }
