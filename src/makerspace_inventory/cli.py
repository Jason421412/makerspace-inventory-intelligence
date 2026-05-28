from __future__ import annotations

import argparse
from pathlib import Path

from .analysis import detect_duplicate_names, rank_followups, summarize
from .loaders import load_inventory_csv
from .search import search_items
from .visualize import create_status_chart


def default_data_path() -> Path:
    return Path(__file__).resolve().parents[2] / "data" / "sample_inventory.csv"


def _load(path: str | Path):
    return load_inventory_csv(Path(path))


def _print_counts(title: str, counts: dict[str, int]) -> None:
    print(title)
    for label, value in counts.items():
        print(f"  {label:<18} {value}")


def cmd_summary(args: argparse.Namespace) -> int:
    summary = summarize(_load(args.data))
    print("Inventory Summary")
    print(f"  Total assets        {summary['total_assets']}")
    print(f"  Follow-up items     {summary['follow_up_count']}")
    print(f"  Quantity gaps       {summary['quantity_gap_count']}")
    _print_counts("\nStatus Counts", summary["status_counts"])
    _print_counts("\nCategory Counts", summary["category_counts"])
    return 0


def cmd_issues(args: argparse.Namespace) -> int:
    print("Highest Priority Follow-ups")
    for score, item in rank_followups(_load(args.data), limit=args.limit):
        label = item.status or "recorded"
        note = f" - {item.notes}" if item.notes else ""
        print(f"{score:>3}  {item.asset_id:<12} {label:<12} {item.name}{note}")
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    query = " ".join(args.query)
    print(f"Search Results: {query}")
    for score, item in search_items(_load(args.data), query, limit=args.limit):
        place = f" | {item.location}" if item.location else ""
        print(f"{score:>5.2f}  {item.asset_id:<12} {item.name}{place}")
    return 0


def cmd_duplicates(args: argparse.Namespace) -> int:
    print("Potential Duplicate Item Names")
    for candidate in detect_duplicate_names(_load(args.data), threshold=args.threshold, limit=args.limit):
        print(
            f"{candidate.score:>4.2f}  "
            f"{candidate.left.asset_id:<12} {candidate.left.name}  <->  "
            f"{candidate.right.asset_id:<12} {candidate.right.name}"
        )
    return 0


def cmd_visualize(args: argparse.Namespace) -> int:
    output = create_status_chart(_load(args.data), args.output)
    print(f"Wrote {output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="makerspace-inventory",
        description="Analyze messy makerspace and robotics lab inventory records.",
    )
    parser.add_argument("--data", default=str(default_data_path()), help="Path to inventory CSV data.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    summary = subparsers.add_parser("summary", help="Print status and category summaries.")
    summary.set_defaults(func=cmd_summary)

    issues = subparsers.add_parser("issues", help="Rank inventory records that need follow-up.")
    issues.add_argument("--limit", type=int, default=10)
    issues.set_defaults(func=cmd_issues)

    search = subparsers.add_parser("search", help="Search assets by ID, name, category, or location.")
    search.add_argument("query", nargs="+")
    search.add_argument("--limit", type=int, default=10)
    search.set_defaults(func=cmd_search)

    duplicates = subparsers.add_parser("duplicates", help="Find likely duplicate item names.")
    duplicates.add_argument("--threshold", type=float, default=0.74)
    duplicates.add_argument("--limit", type=int, default=20)
    duplicates.set_defaults(func=cmd_duplicates)

    visualize = subparsers.add_parser("visualize", help="Generate a status distribution chart.")
    visualize.add_argument("--output", default=str(Path("assets") / "inventory_status_summary.svg"))
    visualize.set_defaults(func=cmd_visualize)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
