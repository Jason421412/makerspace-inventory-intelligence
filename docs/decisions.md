# Design Decisions

## CLI First

The project is CLI-first because spreadsheet auditing tasks often start as quick checks:

- summarize the dataset
- find records needing follow-up
- search for a part
- detect likely duplicates
- generate a chart

A CLI keeps the workflow reproducible and easy to test. The Streamlit dashboard is optional and reuses the same analysis ideas for visual review.

## Synthetic/Sanitized Sample Data

Inventory spreadsheets may contain operational details, supplier notes, room labels, staff names, or other internal context. The public repository uses a synthetic/sanitized sample dataset so the project can demonstrate realistic data problems without exposing a real makerspace spreadsheet.

## Issue Detection

Issue ranking is intentionally rule-based. This makes the output explainable:

- missing or unknown status
- quantity gaps
- missing location/container fields
- notes that suggest follow-up

This is easier to audit than an ML model for a small dataset.

## Duplicate Detection

Duplicate detection uses text similarity ideas such as token overlap and trigram-like matching. This is enough to surface likely duplicate item names for review, but it should not automatically merge records.

## Visualization

SVG output keeps the chart workflow dependency-light and suitable for CI or simple command-line use. Optional plotting libraries can be added for richer visuals when needed.

## Limitations

- The project does not replace a real inventory management system.
- The heuristics are designed for small spreadsheet-style datasets.
- Search ranking and duplicate detection should be reviewed by a human.
- The sample data should remain sanitized before public commits.
