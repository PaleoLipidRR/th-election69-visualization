# Thailand Election 2566–2569 Data Visualization

An open-source, browser-based platform for exploring and comparing Thai general election results between 2566 B.E. (2023 C.E.) and 2569 B.E. (2026 C.E.). The project focuses on three key metrics: **invalid ballots (บัตรเสีย)**, **no-vote / blank ballots (บัตรไม่เลือกผู้ใด)**, and **ballot surplus (ส่วนต่างบัตร)** — the numerical discrepancy between constituency and party-list ballot counts within the same polling station.

---

## 📊 Pages

### 1. Landing Page (`index.html`)
Entry point with links to all three analysis tools.

### 2. Invalid Ballot Analysis (`invalid_analysis.html`)
Slope chart comparing invalid ballot rates per constituency between two user-selected datasets.
- **Danger zone** flags: constituencies where invalid ballots exceed the winner's margin
- **Dataset comparison**: select any two of the three available datasets as Left (baseline) and Right (comparison)
- **Group by**: region, winning party (L or R)
- **Sort by**: % change, absolute change, province, winning party
- **Filter**: all constituencies / danger zone only / safe only

### 3. No-Vote (Blank Ballot) Analysis (`blank_analysis.html`)
Same slope-chart format as the invalid ballot page, but tracks blank (no-vote) ballots instead.
- Danger zone: constituencies where blank ballots exceed the winner's margin
- Same controls as invalid analysis (dataset comparison, groupby, sort, filter)

### 4. Ballot Surplus Analysis (`surplus_analysis_v2.html`)
Bar chart showing the per-constituency difference between constituency ballot usage and party-list ballot usage.
- A positive surplus means more ballots were used in the constituency count than in the party-list count for the same polling station
- Grouped by region or winning party; filterable by surplus direction

---

## 🗄️ Datasets

Three JavaScript data files are loaded dynamically in the browser:

| File | Description |
|------|-------------|
| `data/election66_data.js` | Official 2566 results from ECT (กกต.) |
| `data/election69_ocr.js` | 2569 unofficial results — OCR-extracted from official ส.ส.6/1 report PDFs |
| `data/election69_94pct.js` | 2569 unofficial results at ~94% count — sourced from Excel data |

The pages display dataset names clearly in the header title (e.g. **"2566 → 2569 (OCR)"** vs **"2566 → 2569 (94%)"**) so the source is always visible.

---

## ⚙️ Data Pipeline

To regenerate all three data files from source:

```bash
cd scripts
bash regenerate_data.sh
```

This runs three steps:
1. `build_election_data.py` — merges 2566 ECT data with 2569 OCR results → `data/election66_data.js` + `data/election69_ocr.js`
2. `extract_94pct_data.py` — extracts the 94% Excel data → `data/election69_94pct.js`
3. `split_data.py` — post-processes and adds ballot surplus computation to all three files

Source data lives in:
- `data/election66/` — raw JSON from ECT 2566
- `data/election69/` — Excel source for the 94% dataset
- OCR results are fetched externally by `build_election_data.py`

---

## 🚀 Running Locally

No build step or dependencies required. All visualizations run entirely in the browser.

1. Clone the repository
2. Start a local HTTP server from the project root:
   ```bash
   python -m http.server 8000
   # or: npx serve .
   ```
3. Open `http://localhost:8000` in your browser

> **Note:** A local server is required because the pages fetch data files via `fetch()`. Opening `index.html` directly as a `file://` URL will fail due to browser CORS restrictions.

---

## 📁 Project Structure

```
.
├── index.html                    # Landing page
├── invalid_analysis.html         # Invalid ballot comparison tool
├── blank_analysis.html           # No-vote ballot comparison tool
├── surplus_analysis_v2.html      # Ballot surplus analysis tool
├── data/
│   ├── election66_data.js        # 2566 processed data
│   ├── election69_ocr.js         # 2569 OCR data
│   ├── election69_94pct.js       # 2569 unofficial 94% data
│   ├── election66/               # Source JSON from ECT 2566
│   ├── election69/               # Source Excel for 2569 94%
│   └── archives/                 # Historical OCR snapshots
├── scripts/
│   ├── regenerate_data.sh        # Master rebuild script
│   ├── build_election_data.py    # 2566+2569 OCR merger
│   ├── extract_94pct_data.py     # 94% Excel extractor
│   └── split_data.py             # Post-processor & surplus calculator
└── notebooks/                    # Exploratory analysis notebooks
```

---

## ⚠️ Disclaimers

**Data accuracy:** The 2569 election data presented here is **unofficial and unverified**. It was extracted from PDF documents using OCR (Optical Character Recognition) and from an unofficial Excel dataset. OCR extraction is inherently error-prone. The constituency-level vote counts have been spot-checked against source PDF documents for approximately 42 constituencies where the margin between the top two candidates was smaller than the reported invalid ballot count, but **no comprehensive accuracy guarantee is provided**.

**Source data:**
- **2566 data** is sourced from the official ECT website: [ectreport66.ect.go.th](https://ectreport66.ect.go.th/)
- **2569 OCR data** was extracted from official ส.ส.6/1 report PDFs published by กกต. (ECT), processed by Chanon Ngernthongdee. Source repository: [killernay/election-69-OCR-result](https://github.com/killernay/election-69-OCR-result)
- **2569 94% data** is from an unofficial Excel dataset compiled during vote counting

**No endorsement:** This project is an independent, non-partisan data visualization effort. It does not represent the views of any political party, candidate, or government body. The identification of "danger zone" constituencies (where invalid or blank ballots exceed the winner's margin) is a mathematical observation only — it does not constitute an allegation of electoral fraud, irregularity, or wrongdoing.

**No legal advice:** Nothing in this project constitutes legal, electoral, or political advice. Users are responsible for verifying any data before relying on it for any purpose.

**Copyright of source data:** Raw election results are public records published by the Election Commission of Thailand (กกต. / ECT). This project does not claim copyright over the underlying data.

**Use for educational purposes only.** The authors accept no liability for decisions made based on information presented in this visualization.

---

## 👤 Credits

Data visualization and tooling by **Ronnakrit Rattanasriampaipong** · © 2026

OCR source data by **Chanon Ngernthongdee** ([killernay/election-69-OCR-result](https://github.com/killernay/election-69-OCR-result))
