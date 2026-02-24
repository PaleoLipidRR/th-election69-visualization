# Data Regeneration Guide

This document explains how to regenerate the three main JavaScript data files used by the visualization.

| Output File | Script | Source |
|---|---|---|
| `data/election66_data.js` | `scripts/build_election_data.py` | `data/election66/` JSONs + ECT website |
| `data/election69_ocr.js` | `scripts/build_election_data.py` | `election-69-OCR-result` repo |
| `data/election69_94pct.js` | `scripts/extract_94pct_data.py` | Excel file (94% unofficial) |

> **Quickstart:** run `bash scripts/regenerate_data.sh` to regenerate all three in one go.

---

## Prerequisites

```bash
pip install requests pandas openpyxl
```

- The [election-69-OCR-result](https://github.com/killernay/election-69-OCR-result) repository must be cloned at:  
  `~/Documents/GitHub/election-69-OCR-result/`

- The 94% unofficial Excel file must exist at:  
  `data/election69/ElectionData-Analysis-Public-Transfer-unofficial94percent.xlsx`

---

## Step 1 — Fetch latest 2566 data from ECT website

Fetches constituency and party-list stats from `https://ectreport66.ect.go.th`:

```bash
cd scripts
python fetch_ect_data.py
```

Outputs: `data/ect_mp_votes.csv`, `data/ect_mp_votes.json`

> Only needed when the ECT source data changes. Typically stable.

---

## Step 2 — Build `election66_data.js` and `election69_ocr.js`

Reads `data/election66/` JSONs and merges with OCR 2569 data:

```bash
cd scripts
python build_election_data.py
```

This creates:
- `data/election66_data.js` — 2566 baseline (constituency + party-list)
- `data/election69_ocr.js` — 2569 OCR latest (from the OCR repo)
- Updates `data/archives/manifest.json`

---

## Step 3 — Build `election69_94pct.js`

Reads the 94% unofficial Excel file and extracts the data:

```bash
cd scripts
python extract_94pct_data.py
```

> **Note:** Run from the `scripts/` directory. This script uses a relative path `../data/archives/`.

This creates:
- `data/archives/election_data_94pct.js`

---

## Step 4 — Verify

Open `http://localhost:8000` after running `python -m http.server` in the project root and confirm:
- Charts load for all three dataset options
- Tooltips show correct winner/runner-up data
- Header title dynamically updates on dataset switch

---

## Notes

- All output JS files embed a `// Generated: YYYY-MM-DD HH:MM:SS` timestamp at the top.
- The visualization reads this timestamp at runtime and displays it in the sidebar disclaimer section.
