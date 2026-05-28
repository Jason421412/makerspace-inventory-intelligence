# Architecture

Makerspace Inventory Intelligence is a Python data tooling project organized around a small reusable package, a CLI, tests, and an optional Streamlit dashboard.

## Package Structure

```text
src/makerspace_inventory/
  models.py       Typed inventory record model
  loaders.py      CSV loading and row parsing
  analysis.py     Summary, issue ranking, and duplicate-support logic
  search.py       Weighted keyword search
  visualize.py    SVG/optional chart output
  cli.py          argparse command entry points
  __main__.py     python -m execution hook
```

## CLI Flow

```text
Command line args
  -> cli.py parses command and data path
  -> loaders.py reads CSV rows
  -> models.py normalizes records
  -> analysis/search/visualize runs selected operation
  -> text or chart output is returned
```

Current commands documented in the README include:

- `summary`
- `issues`
- `search`
- `duplicates`
- `visualize`

## Data Flow

The default public dataset is `data/sample_inventory.csv`. It is synthetic/sanitized and shaped like a spreadsheet export so the repository can demonstrate realistic data issues without publishing private operational records.

Typical flow:

1. CSV rows are loaded from disk.
2. Rows are converted into typed records.
3. Missing values and mixed quantity/status formats are handled defensively.
4. Analysis functions compute summaries, follow-up rankings, duplicate candidates, or search rankings.
5. Results are printed in the CLI or shown in the Streamlit dashboard.

## Dashboard

`app/streamlit_app.py` provides a lightweight review interface over the same analysis functions. It loads the sample dataset by default and can accept compatible uploaded CSV files.

## Tests

`tests/` uses Python `unittest` and covers the core analysis and search behavior. GitHub Actions runs the tests on push and pull request.

## Boundaries

- The project is a data toolkit, not an inventory database.
- It does not implement authentication, multi-user editing, or barcode scanning.
- Duplicate detection is heuristic, not a guaranteed entity-resolution system.
- The public dataset should remain synthetic or sanitized.
