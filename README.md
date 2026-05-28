# Makerspace Inventory Intelligence

## Overview

Makerspace Inventory Intelligence is a Python toolkit for analyzing spreadsheet-style inventory data in small labs, makerspaces, and hardware rooms.

The project uses a synthetic sample dataset inspired by common inventory management problems: inconsistent item names, missing quantities, unclear locations, duplicate records, and follow-up items that are easy to lose inside a spreadsheet.

It demonstrates data cleaning, search, duplicate detection, CLI design, visualization, and testing in a compact portfolio-friendly package.

## Problem Statement

Small hardware rooms often track parts and equipment with spreadsheets. Over time, those sheets become hard to trust because item names drift, quantities are incomplete, labels are inconsistent, and priority issues are mixed with normal records.

This project answers practical questions such as:

- Which items need attention first?
- Where is a part stored?
- Are two rows likely describing the same item?
- What categories dominate the inventory?
- Can the dataset be shared safely as a reproducible example?

## Features

- Load inventory CSV data into typed Python objects.
- Infer equipment categories from item names.
- Summarize status and category distributions.
- Rank follow-up items using a priority score.
- Search by item ID, name, category, location, container, color, or notes.
- Detect likely duplicate item names using token and trigram similarity.
- Generate a status distribution chart.
- Build a synthetic sample dataset for demos.
- Test core analysis and search behavior with `unittest`.

## Algorithms / Techniques Used

- Rule-based text normalization for spreadsheet-style values.
- Keyword-based category inference for robotics, sensors, fabrication, power, displays, and communication equipment.
- Priority scoring based on missing/unknown status, notes, quantity gaps, and missing locations.
- Token-overlap and trigram-similarity matching for duplicate detection.
- Weighted search ranking using exact ID matches, substring matches, token overlap, and sequence similarity.

## Tech Stack

- Python 3.10+
- Standard library: `csv`, `argparse`, `dataclasses`, `collections`, `difflib`, `unittest`
- Optional imports:
  - `matplotlib` only if PNG chart export is preferred over the default SVG output

## Folder Structure

```text
makerspace-inventory-intelligence/
|-- README.md
|-- pyproject.toml
|-- requirements.txt
|-- data/
|   |-- README.md
|   `-- sample_inventory.csv
|-- src/
|   `-- makerspace_inventory/
|       |-- analysis.py
|       |-- cli.py
|       |-- loaders.py
|       |-- models.py
|       |-- search.py
|       `-- visualize.py
|-- scripts/
|   `-- build_sample_data.py
|-- notebooks/
|   `-- inventory_exploration.ipynb
|-- docs/
|   |-- project_ideas.md
|   `-- source_audit.md
|-- assets/
|   `-- inventory_status_summary.svg
`-- tests/
    |-- test_analysis.py
    `-- test_search.py
```

## How To Run

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install optional dependencies:

```bash
pip install -r requirements.txt
```

Run the CLI from the project root:

```bash
$env:PYTHONPATH="src"
python -m makerspace_inventory.cli summary
python -m makerspace_inventory.cli issues
python -m makerspace_inventory.cli search arduino
python -m makerspace_inventory.cli duplicates
python -m makerspace_inventory.cli visualize --output assets/inventory_status_summary.svg
```

Run tests:

```bash
$env:PYTHONPATH="src"
python -m unittest discover
```

Regenerate the synthetic sample data:

```bash
$env:PYTHONPATH="src"
python scripts/build_sample_data.py
```

## Example Output

```text
Inventory Summary
  Total assets        36
  Follow-up items     9
  Quantity gaps       8

Status Counts
  recorded           17
  complete           10
  unknown             4
  missing             2
  no_label            2
  mixed               1
```

```text
Search Results: arduino
 8.83  MC-001       Arduino Uno R3 | Cabinet A / Shelf 1
```

## What I Learned

- Spreadsheet-like operations data needs defensive parsing because blank cells, mixed quantity formats, and inconsistent labels are common.
- Simple ranking and search algorithms can make inventory data more usable without requiring a heavy ML model.
- A strong portfolio repository should be reproducible, safe to publish, and easy to run in a few minutes.
- Synthetic data is useful when demonstrating realistic workflows without exposing sensitive operational records.

## Future Improvements

- Add a Streamlit or FastAPI dashboard for interactive search and audit views.
- Add configurable category rules in YAML.
- Add barcode or QR-code label generation for assets.
- Add an anonymized checkout and return simulator.
- Add import templates for common spreadsheet layouts.

## Portfolio Value

This project shows practical engineering judgment: define a clean data model, implement useful algorithms, write tests, build a CLI, and provide a reproducible demo dataset. It is positioned as a polished public portfolio project rather than a dump of unrelated files.
