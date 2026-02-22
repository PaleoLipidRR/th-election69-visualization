# 📊 Data Building Guide: Thailand Election Visualization

## Overview

This guide explains how to build the `CONST_RAW` (constituency MP) and `PARTYLIST_RAW` (party list MP) datasets for the election visualization.

## Data Structure

### Current Data (Election 2569 - Constituency MP)

Your current `index.html` contains:
```javascript
const RAW = [
  {
    "cons_id": "NWT_3",
    "province_thai": "นราธิวาส",
    "cons_no": 3,
    "invalid_votes": 6778,          // 2566 data
    "percent_invalid": 8.42909,      // 2566 data
    "invalid_2026": 2416,            // 2569 data
    "invalid_pct_2026": 2.914,       // 2569 data
    "invalid_pct_change": -5.515,    // 2566 → 2569 change
    // ... other fields
  },
  // ... 400 constituencies
]
```

### What You Have

✅ **Election 2566 (2023)** data in JSON folder: `election66/`
- `th_election66_info_constituency.json` - Constituency info
- `th_election66_stats_cons.json` - Constituency stats  
- `th_election66_stats_party.json` - Party list stats
- Other reference data

✅ **Election 2569 (2026)** from OCR:
- Constituency results: `~/Documents/GitHub/election-69-OCR-result/data/matched/constituency/`
- Party list results: `~/Documents/GitHub/election-69-OCR-result/data/matched/party_list/`

## Building Process

### Method 1: Using the Jupyter Notebook (Recommended)

Run the notebook at: `election_data_processing.ipynb`

```bash
jupyter notebook election_data_processing.ipynb
```

**Steps:**
1. Install pandas if needed: `pip install pandas`
2. Run each cell in order
3. The notebook will:
   - Load election 2566 and 2569 data
   - Merge constituency + party_list for 2569
   - Calculate invalid ballot percentages and changes
   - Export as JavaScript arrays

**Output:** `election_data_generated.js` with `CONST_RAW` and `PARTYLIST_RAW`

### Method 2: Using Python Script

Run: `build_election_data.py`

```bash
python build_election_data.py
```

This will:
- Load all data files
- Process into correct format
- Export as JavaScript
- Save to `election_data.js`

### Method 3: Manual Processing

Follow the data transformation logic shown in your original Jupyter notebook:

```python
# ──────────────────────────────────────────────────────────────
# 2566 DATA (Constituency - from JSON files)
# ──────────────────────────────────────────────────────────────

cons_info = {}
cons_stats = {}

# Load from election66/th_election66_info_constituency.json
with open('election66/th_election66_info_constituency.json') as f:
    for item in json.load(f):
        cons_key = f"{item['prov_id']}_{item['cons_no']}"
        cons_info[cons_key] = item

# Load from election66/th_election66_stats_cons.json  
with open('election66/th_election66_stats_cons.json') as f:
    for item in json.load(f):
        cons_key = f"{item['prov_id']}_{item['cons_no']}"
        cons_stats[cons_key] = item


# ──────────────────────────────────────────────────────────────
# 2569 DATA (from OCR JSON files)
# ──────────────────────────────────────────────────────────────

def load_json_folder(folder_path):
    """Load election results from folder of JSON files"""
    rows = []
    
    for json_file in sorted(glob.glob(os.path.join(folder_path, "*.json"))):
        with open(json_file, encoding="utf-8") as f:
            d = json.load(f)
        
        province = d["province_name_normalized"]
        cons_no = d["constituency_number"]
        summary = d["summary"]
        results = d["results"]
        
        # Find winner and runner-up
        sorted_results = sorted(results, key=lambda x: x["votes"], reverse=True)
        winner = sorted_results[0] if len(sorted_results) > 0 else {"party": None, "votes": 0}
        runnerup = sorted_results[1] if len(sorted_results) > 1 else {"party": None, "votes": 0}
        
        rows.append({
            "province": province,
            "cons_no": cons_no,
            "invalid_ballots": summary["invalid_votes"],
            "voters": summary["voters_came"],
            "winning_party": winner["party"],
            "winning_score": winner["votes"],
            "runnerUp_party": runnerup["party"],
            "runnerUp_score": runnerup["votes"],
        })
    
    return rows

# Load both ballot types
const_data = load_json_folder("~/Documents/GitHub/election-69-OCR-result/data/matched/constituency")
pl_data = load_json_folder("~/Documents/GitHub/election-69-OCR-result/data/matched/party_list")

# Merge on province + constituency
merged = merge_data(const_data, pl_data)

# Calculate metrics
for record in merged:
    # Invalid ballot percentage 2569
    const_invalid_pct = (record['const_invalid'] / record['const_voters'] * 100)
    pl_invalid_pct = (record['pl_invalid'] / record['pl_voters'] * 100)
    
    # For CONST_RAW
    CONST_RAW.append({
        "province_thai": record['province'],
        "cons_no": record['cons_no'],
        "invalid_votes": record['2566_invalid'],      # from cons_stats
        "percent_invalid": record['2566_invalid_pct'],
        "invalid_2026": record['const_invalid'],
        "invalid_pct_2026": const_invalid_pct,
        "invalid_pct_change": const_invalid_pct - record['2566_invalid_pct'],
        # ... other fields
    })
    
    # For PARTYLIST_RAW
    PARTYLIST_RAW.append({
        "province_thai": record['province'],
        "cons_no": record['cons_no'],
        "invalid_votes": record['2566_invalid_pl'],  # from stats_party
        "percent_invalid": record['2566_invalid_pct_pl'],
        "invalid_2026": record['pl_invalid'],
        "invalid_pct_2026": pl_invalid_pct,
        "invalid_pct_change": pl_invalid_pct - record['2566_invalid_pct_pl'],
        # ... other fields
    })
```

## Data Fields Required

Each record in `CONST_RAW` and `PARTYLIST_RAW` should have:

```javascript
{
  // Identification
  "prov_id": "NWT",                  // 3-letter province code
  "province_thai": "นราธิวาส",        // Thai province name
  "province_eng": "NARATHIWAT",      // English province name
  "cons_no": 3,                      // Constituency number
  
  // 2566 (2023) Data - Constituency
  "invalid_votes": 6778,             // Invalid ballots
  "percent_invalid": 8.42909,        // Percentage
  "turn_out": 80412,                 // Voter turnout
  "winner_party": "พลังประชารัฐ",     // Winning party
  "margin_votes": 4460,              // Winner - runner-up margin
  "runnerup_votes": 29951,           // Runner-up votes
  "winner_votes": 34411,             // Winner votes
  
  // 2569 (2026) Data
  "invalid_2026": 2416,              // Invalid ballots
  "invalid_pct_2026": 2.914,         // Percentage
  "invalid_pct_change": -5.515,      // % change from 2566
  "invalid_change": -4362,           // Absolute change
  "turnout_2026": 82910,             // Voter turnout
  "pct_turnout_2026": 73.14708,      // Turnout percentage
  
  // 2569 Winners
  "winner_party_2569": "กล้าธรรม",    // Winning party
  "winner_votes_2569": 36053,        // Winner votes
  "margin_2569": 1640,               // Winner margin
  "runnerUp_votes": 34413,           // Runner-up votes
  "runnerUp_party": "ประชาชน"        // Runner-up party
}
```

## Key Differences: CONST_RAW vs PARTYLIST_RAW

The two datasets differ primarily in:

| Field | CONST_RAW | PARTYLIST_RAW |
|-------|-----------|---------------|
| **2566 Source** | Constituency ballots (green) | Party list ballots (pink) |
| **2569 Source** | Constituency elections | Party list elections |
| **invalid_ballots** | Brown ballot invalid count | Pink ballot invalid count |
| **winner_party** | Constituency winner | Party list winner |
| **margin_2569** | Constituency margin | Party list margin |

## Updating Your Visualization

### Step 1: Generate Data

Run the Jupyter notebook or Python script to generate the datasets.

### Step 2: Replace in HTML

Option A - Single file approach:
```html
<!-- At top of <script> section in index.html -->
<script src="election_data_generated.js"></script>
```

Option B - Replace const RAW:
```javascript
// Replace the large const RAW = [...] with your generated data
const CONST_RAW = [...];  // Generated from notebook
const PARTYLIST_RAW = [...];  // Generated from notebook
```

### Step 3: Update Toggle Logic

Your toggle is already set up! The `switchDataset()` function at lines ~596-632 handles switching between:
- `CONST_RAW` (ส.ส. เขต)
- `PARTYLIST_RAW` (บส. รายชื่อ)

## Data Validation Checklist

After building your datasets, verify:

- [ ] Both datasets have exactly 400 or same number of records
- [ ] All `cons_no` values between 1-15 (Thailand constituencies per province)
- [ ] Province names match exactly (Thai spelling matters!)
- [ ] Invalid ballot percentages reasonable (typically 5-15%)
- [ ] Percentage changes make sense (usually -10% to +10%)
- [ ] No missing required fields (no `null` values for critical fields)
- [ ] Party names match your `PARTY_COLOR` mapping

## Testing Your Data

In browser console, verify:
```javascript
// Check data loaded
CONST_RAW.length  // Should be ~400
PARTYLIST_RAW.length  // Should be ~400

// Toggle between datasets
switchDataset('constituency')
switchDataset('partylist')

// Verify data appears correctly
data.length  // Should equal RAW.length for selected dataset
```

## Updating When Election 2569 Data Changes

The notebook is designed to be reusable:

1. **When new 2569 data arrives** (constituency or party list):
   - Place new JSON files in the appropriate directory
   - Re-run the notebook
   - It will automatically detect and process new files

2. **When adding 2566 data**:
   - Add or update files in `election66/` folder
   - Modify the data loading section in the notebook
   - Re-run to regenerate with 2566 comparisons

3. **When adding multiple elections for trend analysis**:
   - Add data loading sections for election 60, 62, etc.
   - Add trend calculation fields
   - Update visualization to show multi-election trends

## Troubleshooting

### Data column mismatch errors
**Problem:** "KeyError: 'province_name_normalized'"
**Solution:** Check that election69 JSON files have correct structure. Run the first cell of notebook to verify file format.

### Missing constituencies
**Problem:** Only 350 records instead of 400
**Solution:** Check if some constituencies have missing data. Verify all JSON files loaded. Look for errors in JSON processing.

### Invalid percentages > 100%
**Problem:** Invalid ballot percentages showing > 100%
**Solution:** Check calculation - should be `(invalid_ballots / total_voters) * 100`. Verify the summary fields in source JSON.

### Negative percentage changes seem wrong  
**Problem:** Changes don't look realistic
**Solution:** Verify you're using same ballot type (constituency vs party list) for both 2566 and 2569.

## Questions?

Refer to your original Jupyter notebook at line references for the data processing logic that inspired this structure.
