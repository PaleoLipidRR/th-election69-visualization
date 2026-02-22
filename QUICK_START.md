# 📱 Summary: Building CONST_RAW and PARTYLIST_RAW Datasets

## What You Now Have

✅ **Added Toggle Feature** - Switch between Constituency MP (ส.ส.) and Party List MP (บส.)

✅ **Data Building Tools**:
1. **Jupyter Notebook** - `election_data_processing.ipynb` (interactive, cell-by-cell)
2. **Python Script** - `build_election_data.py` (automated)
3. **Comprehensive Guide** - `DATA_BUILDING_GUIDE.md` (detailed documentation)
4. **Example Structure** - `example_data_structure.js` (reference format)

---

## Quick Start: 3 Steps to Populate Party List Data

### 1️⃣ **Open & Run the Jupyter Notebook**

```bash
cd ~/Documents/GitHub/th-election69-visualization
jupyter notebook election_data_processing.ipynb
```

**Inside the notebook, you'll find:**
- Load election66 JSON data from your `election66/` folder
- Load election69 JSON data from the OCR results directory
- Merge both ballot types (constituency + party list)
- Calculate invalid ballot metrics and changes
- Export as JavaScript

### 2️⃣ **Copy Generated Data**

After running, the notebook outputs JavaScript in this format:
```javascript
const CONST_RAW = [...];
const PARTYLIST_RAW = [...];
```

### 3️⃣ **Update index.html**

Replace the current data definitions with your generated data.

---

## Data Sources & Processing Logic

### From Your Jupyter Notebook Notes

**Your notes show the structure:**

```python
# Election 66 data structure
voters66 = pd.DataFrame({
    "province": province_thai,
    "constituency_number": cons_no,
    # For each ballot type:
    "const_voters": turnout,
    "const_winning_score": winner_votes,
    "const_invalid_ballots": invalid + blank,
    "party_voters": pl_turnout,
    "party_winning_score": pl_winner_votes,
    "party_invalid_ballots": pl_invalid + pl_blank,
})

# Election 69 merged data
voters69 = merge_on_province_and_cons_no(
    constituency_json_folder,
    party_list_json_folder
)

# Calculate ballot difference
voters69["voters_diff_const_PL"] = (
    (const_total_valid + const_invalid) -
    (partylist_total_valid + partylist_invalid)
)
```

### Raw → Processed Data Transformation

**Input:** JSON files from OCR
```json
{
  "province_name_normalized": "นราธิวาส",
  "constituency_number": 3,
  "summary": {
    "good_votes": 93000,
    "invalid_votes": 2416,
    "voters_came": 82910
  },
  "results": [
    {"party": "กล้าธรรม", "votes": 36053},
    {"party": "ประชาชน", "votes": 34413}
  ]
}
```

**Output:** JavaScript record for visualization
```javascript
{
  "province_thai": "นราธิวาส",
  "cons_no": 3,
  "invalid_2026": 2416,
  "invalid_pct_2026": 2.914,
  "winner_party_2569": "กล้าธรรม",
  "margin_2569": 1640,
  // ... plus 2566 data for comparison
}
```

---

## Key Metrics Explained

| Metric | Description | Calculation |
|--------|-------------|-------------|
| `invalid_pct_2026` | Invalid ballot % in 2569 | `(invalid_2026 / turnout_2026) * 100` |
| `invalid_pct_change` | Change from 2566 to 2569 | `invalid_pct_2026 - percent_invalid` |
| `margin_2569` | Winner margin in 2569 | `winning_score - runnerUp_score` |
| `pct_turnout_2026` | Voter turnout % | `(turnout_2026 / registered_voters) * 100` |

---

## File Descriptions

### 📄 Core Files Created

| File | Purpose |
|------|---------|
| `election_data_processing.ipynb` | Interactive notebook - load, process, export data |
| `build_election_data.py` | Automated Python script version |
| `DATA_BUILDING_GUIDE.md` | Detailed step-by-step guide |
| `example_data_structure.js` | Reference format for CONST_RAW & PARTYLIST_RAW |

### 🔄 How They Connect

```
Your Election 2566/2569 JSON Data
    ↓
election_data_processing.ipynb  ←─ or ─→  build_election_data.py
    ↓
election_data_generated.js
    ↓
Update index.html with new CONST_RAW + PARTYLIST_RAW
    ↓
Visualization shows both datasets with toggle
```

---

## What Happens When You Switch Datasets

### Current Toggle Button State

```html
<button class="btn-sort btn-dataset active" onclick="switchDataset('constituency')">
  ส.ส. (เขต)
</button>
<button class="btn-sort btn-dataset" onclick="switchDataset('partylist')">
  บส. (รายชื่อ)
</button>
```

### When User Clicks "บส. (รายชื่อ)"

```javascript
switchDataset('partylist') // Line ~596

1. Update button states
2. Check if PARTYLIST_RAW is empty
   - If empty: Show "data coming soon" message
   - If full: Load PARTYLIST_RAW into `data` array
3. Reset filters and sorts to defaults
4. Update header subtitle to show "Party List MP"
5. Rebuild visualization with new data
```

---

## Future Updates: When Election 2569 Data Changes

The system is designed to be updatable:

```python
# When you have new OC R results:
1. Place new JSON files in:
   ~/Documents/GitHub/election-69-OCR-result/data/matched/constituency/
   ~/Documents/GitHub/election-69-OCR-result/data/matched/party_list/

2. Run notebook again:
   jupyter notebook election_data_processing.ipynb

3. Copy new election_data_generated.js output

4. Update index.html CONST_RAW and PARTYLIST_RAW arrays

5. Visualization automatically reflects changes
```

---

## Data Validation

Before using generated data, verify in browser console:

```javascript
// Check data structure
CONST_RAW.length                    // Should be ~400
PARTYLIST_RAW.length                // Should be ~77
CONST_RAW[0].invalid_pct_2026       // Should be number 0-100
CONST_RAW[0].province_thai          // Should be Thai text

// Test toggle
switchDataset('constituency')       // Switches to CONST_RAW
switchDataset('partylist')          // Switches to PARTYLIST_RAW

// Verify no errors in console
```

---

## Files in Your Project Now

```
th-election69-visualization/
├── index.html                          (your main visualization - already updated with toggle)
├── election66/                         (your election 2566 JSON data)
│   ├── th_election66_info_constituency.json
│   ├── th_election66_stats_cons.json
│   └── ...
├── election_data_processing.ipynb      (💡 START HERE - Jupyter notebook)
├── build_election_data.py              (automated Python script)
├── DATA_BUILDING_GUIDE.md              (comprehensive guide)
├── example_data_structure.js           (reference format)
└── election_data_generated.js          (output - generated after running notebook)
```

---

## Next: Run the Notebook

1. **Install pandas** (if needed):
   ```bash
   pip install pandas
   ```

2. **Open & run the notebook**:
   ```bash
   cd ~/Documents/GitHub/th-election69-visualization
   jupyter notebook election_data_processing.ipynb
   ```

3. **Execute cells in order** - Follow the markdown sections

4. **Copy the output** - Will generate `election_data_generated.js`

5. **Update index.html** - Replace RAW data with generated data

6. **Test** - Toggle between ส.ส. and บส. in visualization

---

## Questions or Issues?

### Common Issues & Solutions

**Q: "pandas is not installed"**
- A: Run `pip install pandas`

**Q: "election69 directories not found"**
- A: Update paths in notebook to match your system (check line 1 of notebook)

**Q: "JSON files have different structure"**
- A: Check file format matches expected structure (see example_data_structure.js)

**Q: "Generated data looks wrong"**
- A: Verify calculations match DATA_BUILDING_GUIDE.md section "Data Fields Required"

**Q: "Visualization doesn't change when I toggle"**
- A: Check browser console for errors. Verify data is valid JavaScript array.

---

## Summary

✅ **What was added:**
- Toggle button for ส.ส. / บส. datasets  
- Switchable data structure (CONST_RAW / PARTYLIST_RAW)
- Full data processing toolkit with documentation

✅ **What you need to do:**
- Run the Jupyter notebook with your data
- Generate the JavaScript output
- Update index.html with the new data

✅ **Result:**
- Interactive visualization showing both Constituency & Party List invalid ballot comparisons
- Ability to switch between datasets with one click
- Scalable system for future data updates

---

**Ready to build? Start with:** `jupyter notebook election_data_processing.ipynb`
