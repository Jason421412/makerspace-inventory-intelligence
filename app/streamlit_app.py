from __future__ import annotations

import csv
import io
from pathlib import Path
import sys
import tempfile


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from makerspace_inventory.analysis import (  # noqa: E402
    detect_duplicate_names,
    effective_category,
    has_quantity_gap,
    normalized_status,
    priority_score,
    rank_followups,
    summarize,
)
from makerspace_inventory.loaders import FIELDNAMES, load_inventory_csv  # noqa: E402
from makerspace_inventory.models import InventoryItem  # noqa: E402
from makerspace_inventory.search import search_items  # noqa: E402
from makerspace_inventory.visualize import create_status_chart  # noqa: E402


DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "sample_inventory.csv"


def load_uploaded_inventory(uploaded_file) -> list[InventoryItem]:
    content = uploaded_file.getvalue().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(content))
    missing = set(FIELDNAMES) - set(reader.fieldnames or [])
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    return [InventoryItem.from_row(row) for row in reader if row.get("name") or row.get("asset_id")]


def item_rows(items: list[InventoryItem]) -> list[dict[str, object]]:
    return [
        {
            "asset_id": item.asset_id,
            "name": item.name,
            "category": effective_category(item),
            "location": item.location,
            "expected_qty": item.expected_qty,
            "actual_qty": item.actual_qty,
            "status": normalized_status(item),
            "priority": priority_score(item),
            "notes": item.notes,
        }
        for item in items
    ]


def followup_rows(items: list[InventoryItem]) -> list[dict[str, object]]:
    return [
        {
            "priority": score,
            "asset_id": item.asset_id,
            "name": item.name,
            "status": normalized_status(item),
            "expected_qty": item.expected_qty,
            "actual_qty": item.actual_qty,
            "notes": item.notes,
        }
        for score, item in rank_followups(items, limit=50)
    ]


def low_stock_rows(items: list[InventoryItem]) -> list[dict[str, object]]:
    rows = []
    for item in items:
        if has_quantity_gap(item) and item.quantity_delta is not None and item.quantity_delta < 0:
            rows.append(
                {
                    "asset_id": item.asset_id,
                    "name": item.name,
                    "expected_qty": item.expected_qty,
                    "actual_qty": item.actual_qty,
                    "gap": item.quantity_delta,
                    "location": item.location,
                }
            )
    return sorted(rows, key=lambda row: (row["gap"], row["asset_id"]))


def duplicate_rows(items: list[InventoryItem]) -> list[dict[str, object]]:
    return [
        {
            "score": candidate.score,
            "asset_id_a": candidate.left.asset_id,
            "name_a": candidate.left.name,
            "asset_id_b": candidate.right.asset_id,
            "name_b": candidate.right.name,
        }
        for candidate in detect_duplicate_names(items, limit=25)
    ]


def render_status_visualization(st, items: list[InventoryItem]) -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        chart_path = create_status_chart(items, Path(tmp_dir) / "inventory_status.svg")
        st.markdown(chart_path.read_text(encoding="utf-8"), unsafe_allow_html=True)


def main() -> None:
    try:
        import streamlit as st
    except ImportError as exc:
        raise RuntimeError("Install dashboard dependencies with: pip install -r requirements.txt") from exc

    st.set_page_config(page_title="Makerspace Inventory Intelligence", page_icon=":bar_chart:", layout="wide")
    st.title("Makerspace Inventory Intelligence")
    st.caption("Analyze spreadsheet-style inventory data for small labs, makerspaces, and hardware rooms.")

    uploaded_file = st.sidebar.file_uploader("Upload inventory CSV", type=["csv"])
    try:
        items = load_uploaded_inventory(uploaded_file) if uploaded_file else load_inventory_csv(DEFAULT_DATA_PATH)
    except Exception as exc:
        st.error(f"Could not load inventory data: {exc}")
        st.stop()

    summary = summarize(items)
    status_counts = summary["status_counts"]
    category_counts = summary["category_counts"]

    metric_cols = st.columns(4)
    metric_cols[0].metric("Total assets", summary["total_assets"])
    metric_cols[1].metric("Follow-up items", summary["follow_up_count"])
    metric_cols[2].metric("Quantity gaps", summary["quantity_gap_count"])
    metric_cols[3].metric("Categories", len(category_counts))

    left, right = st.columns([1.1, 1])
    with left:
        st.subheader("Inventory status")
        render_status_visualization(st, items)
    with right:
        st.subheader("Category mix")
        st.dataframe(
            [{"category": key, "count": value} for key, value in category_counts.items()],
            hide_index=True,
            use_container_width=True,
        )

    tab_overview, tab_issues, tab_search, tab_duplicates = st.tabs(
        ["Inventory", "Issues", "Search", "Duplicates"]
    )

    with tab_overview:
        st.dataframe(item_rows(items), hide_index=True, use_container_width=True)

    with tab_issues:
        st.subheader("Priority follow-ups")
        st.dataframe(followup_rows(items), hide_index=True, use_container_width=True)
        st.subheader("Low-stock records")
        st.dataframe(low_stock_rows(items), hide_index=True, use_container_width=True)

    with tab_search:
        query = st.text_input("Keyword search", value="arduino")
        if query.strip():
            results = [
                {
                    "score": score,
                    "asset_id": item.asset_id,
                    "name": item.name,
                    "category": effective_category(item),
                    "location": item.location,
                    "status": normalized_status(item),
                }
                for score, item in search_items(items, query, limit=25)
            ]
            st.dataframe(results, hide_index=True, use_container_width=True)
        else:
            st.info("Enter a keyword to search by asset ID, name, category, location, or notes.")

    with tab_duplicates:
        st.dataframe(duplicate_rows(items), hide_index=True, use_container_width=True)


if __name__ == "__main__":
    main()
