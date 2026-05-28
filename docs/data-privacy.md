# Data Privacy

This repository should not contain real private inventory exports unless they have been reviewed and sanitized.

## Safe Public Data

The included `data/sample_inventory.csv` is intended to be synthetic or sanitized. It should demonstrate realistic inventory issues without exposing:

- staff or student names
- emails or phone numbers
- internal room access details
- supplier account details
- purchase records with sensitive pricing context
- private notes copied directly from an operational spreadsheet

## Files to Avoid Committing

Avoid committing:

- raw `.xlsx` or `.xls` spreadsheets
- exported PDFs or reports
- private photos of rooms, labels, or asset tags
- zip files of operational data
- source files from real admin systems
- documents containing names, contact info, IDs, addresses, or financial details

The `.gitignore` blocks common raw/private folders and document formats, but manual review is still required before publishing data.

## Sanitization Checklist

Before adding or updating sample data:

1. Replace real item IDs if they map to a private asset system.
2. Remove people names and contact details.
3. Generalize exact rooms or restricted locations.
4. Remove purchase/vendor/account details.
5. Keep enough variety to test search, duplicate detection, quantity gaps, and status summaries.
6. Run the test suite after changing sample data.

## Why This Matters

The point of the project is to show data tooling and analysis skills, not to publish real operational data. A small, realistic sample is enough for portfolio review and safer for long-term public maintenance.
