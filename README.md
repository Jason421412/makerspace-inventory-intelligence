# Makerspace Inventory Intelligence

[![Tests](https://github.com/Jason421412/makerspace-inventory-intelligence/actions/workflows/tests.yml/badge.svg)](https://github.com/Jason421412/makerspace-inventory-intelligence/actions/workflows/tests.yml)

## Overview

Makerspace Inventory Intelligence is a Python toolkit for analyzing spreadsheet-style inventory data for small labs, makerspaces, and hardware rooms.

The project uses a synthetic sample dataset inspired by common inventory management problems: inconsistent item names, missing quantities, unclear locations, duplicate records, and follow-up items that are easy to lose inside a spreadsheet.

It demonstrates data cleaning, search, duplicate detection, CLI design, visualization, dashboard design, automated tests, and continuous integration in a compact portfolio-friendly package.

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
- Explore the data in a Streamlit dashboard.
- Test core analysis and search behavior with `unittest`.
- Run tests automatically with GitHub Actions.

## Dashboard

The Streamlit dashboard loads the included synthetic dataset by default and can also accept a custom CSV with the same columns.

Dashboard views include:

- summary metrics
- inventory status visualization
- category counts
- priority follow-ups
- low-stock records
- keyword search
- likely duplicate names

Run it from the project root:

```bash
pip install -r requirements.txt
$env:PYTHONPATH="src"
streamlit run app/streamlit_app.py
```

## Screenshot Placeholder

Add a dashboard screenshot here after launching the Streamlit app.

```text
assets/dashboard_screenshot.png
```

## CLI Examples

Run the CLI from the project root:

```bash
$env:PYTHONPATH="src"
python -m makerspace_inventory.cli summary
python -m makerspace_inventory.cli issues
python -m makerspace_inventory.cli search arduino
python -m makerspace_inventory.cli duplicates
python -m makerspace_inventory.cli visualize --output assets/inventory_status_summary.svg
```

Example summary:

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

Example search:

```text
Search Results: arduino
 8.83  MC-001       Arduino Uno R3 | Cabinet A / Shelf 1
```

## Algorithms / Techniques Used

- Rule-based text normalization for spreadsheet-style values.
- Keyword-based category inference for robotics, sensors, fabrication, power, displays, and communication equipment.
- Priority scoring based on missing/unknown status, notes, quantity gaps, and missing locations.
- Token-overlap and trigram-similarity matching for duplicate detection.
- Weighted search ranking using exact ID matches, substring matches, token overlap, and sequence similarity.
- SVG chart rendering for dependency-light visualization.

## Tech Stack

- Python 3.10+
- Streamlit
- Standard library: `csv`, `argparse`, `dataclasses`, `collections`, `difflib`, `unittest`
- GitHub Actions for automated test runs
- Optional: `matplotlib` for PNG chart export

## Folder Structure

```text
makerspace-inventory-intelligence/
|-- .github/
|   `-- workflows/
|       `-- tests.yml
|-- app/
|   `-- streamlit_app.py
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

## How To Run Tests

```bash
$env:PYTHONPATH="src"
python -m unittest discover
```

## Regenerate Demo Data

```bash
$env:PYTHONPATH="src"
python scripts/build_sample_data.py
```

## What I Learned

- Spreadsheet-like operations data needs defensive parsing because blank cells, mixed quantity formats, and inconsistent labels are common.
- Simple ranking and search algorithms can make inventory data more usable without requiring a heavy ML model.
- A strong portfolio repository should be reproducible, safe to publish, and easy to run in a few minutes.
- Synthetic data is useful when demonstrating realistic workflows without exposing sensitive operational records.
- A dashboard makes the same analysis easier to review for non-CLI users.

## Future Improvements

- Add configurable category rules in YAML.
- Add barcode or QR-code label generation for assets.
- Add an anonymized checkout and return simulator.
- Add import templates for common spreadsheet layouts.
- Add benchmark queries for search relevance.

## Portfolio Value

This project shows practical engineering judgment: define a clean data model, implement useful algorithms, write tests, build a CLI, add an interactive dashboard, and automate verification with CI. It is positioned as a polished public portfolio project for data tooling and applied Python work.
