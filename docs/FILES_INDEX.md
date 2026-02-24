# 🇹🇭 Thailand Election Data Visualization - Data Building Index

## 📑 Documentation Files & How to Use Them

This folder contains everything you need to build and maintain the election visualization with both Constituency MP (ส.ส.) and Party List MP (บส.) datasets.

---

## 🚀 Start Here

### For First-Time Setup:
👉 **[QUICK_START.md](QUICK_START.md)** - 3-step guide to get started (5 min read)

### For Detailed Reference:
📚 **[DATA_BUILDING_GUIDE.md](DATA_BUILDING_GUIDE.md)** - Complete documentation (20 min read)

---

## 🛠️ Data Processing Tools

### Interactive Processing:
**[election_data_processing.ipynb](election_data_processing.ipynb)**
- Jupyter notebook with cell-by-cell processing
- Load election 2566 & 2569 data
- Calculate metrics and changes
- Export as JavaScript
- ✅ Best for understanding the process
- ✅ Best for debugging and validation

**How to run:**
```bash
jupyter notebook election_data_processing.ipynb
```

### Automated Processing:
**[build_election_data.py](build_election_data.py)**
- Python script for batch processing
- Single command execution
- ✅ Best for repeated updates
- ✅ Faster for large datasets

**How to run:**
```bash
python build_election_data.py
```

---

## 📋 Reference Documentation

### Data Structure Reference:
**[example_data_structure.js](example_data_structure.js)**
- Shows exact format of CONST_RAW and PARTYLIST_RAW
- Field explanations
- Validation checklist
- Key differences between datasets

### Main Implementation:
**[index.html](index.html)**
- Lines ~450-465: Toggle button UI (ส.ส. / บส.)
- Lines ~596-632: `switchDataset()` function
- Lines ~542 onwards: Data definitions (replace with your data)

---

## 📊 Data Flow Diagram

```
┌─────────────────────────────────────┐
│  Your Data Sources                   │
│  ├─ election66/ (JSON files)         │
│  ├─ OCR results constituency/        │
│  └─ OCR results party_list/          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Processing Tools                    │
│  ├─ election_data_processing.ipynb   │
│  └─ build_election_data.py          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Generated JavaScript                │
│  ├─ CONST_RAW (400 constituencies)   │
│  └─ PARTYLIST_RAW (77 regions)      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Updated index.html                  │
│  └─ Toggle between datasets ✓        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Live Visualization                  │
│  ├─ ส.ส. (Constituency view)         │
│  └─ บส. (Party List view)           │
└─────────────────────────────────────┘
```

---

## 📁 File Organization

```
th-election69-visualization/
│
├── README files (you are here)
│   ├── QUICK_START.md               ← Start with this
│   ├── DATA_BUILDING_GUIDE.md        ← Detailed reference
│   └── FILES_INDEX.md               (this file)
│
├── Data Processing Tools
│   ├── election_data_processing.ipynb ← Jupyter notebook
│   ├── build_election_data.py        ← Python script
│   └── example_data_structure.js     ← Reference format
│
├── Visualization
│   ├── index.html                   ← Main visualization
│   └── all dependencies (CSS, SVG, etc.) included in index.html
│
├── Source Data
│   └── election66/                  ← Your 2566 JSON data
│       ├── th_election66_info_constituency.json
│       ├── th_election66_stats_cons.json
│       ├── th_election66_stats_party.json
│       └── ...other files
│
└── Generated Output (after running notebook/script)
    └── election_data_generated.js   ← Copy this to index.html
```

---

## 🔄 Typical Workflow

### Initial Setup (First Time)
1. Read [QUICK_START.md](QUICK_START.md)
2. Open [election_data_processing.ipynb](election_data_processing.ipynb)
3. Run cells in order
4. Copy generated data to index.html
5. Test in browser

### Updates (When New Data Arrives)
1. Check if data structure changed → Read [DATA_BUILDING_GUIDE.md](DATA_BUILDING_GUIDE.md) if needed
2. Run notebook with new data
3. Copy output to index.html
4. Done!

### Debugging
1. Reference [example_data_structure.js](example_data_structure.js)
2. Check validation checklist in [DATA_BUILDING_GUIDE.md](DATA_BUILDING_GUIDE.md)
3. Review browser console for errors

---

## 📌 Key Concepts

### CONST_RAW (ส.ส. - Constituency MPs)
- **Count:** ~400 constituencies
- **Data source:** Green ballots (เลือกตั้งแบบปกติ)  
- **Comparison:** Invalid ballots % between 2566 → 2569
- **Key metric:** `invalid_pct_change` (negative = improvement)

### PARTYLIST_RAW (บส. - Party List MPs)
- **Count:** 77 regions (one per province)
- **Data source:** Pink ballots (เลือกตั้งแบบสัดส่วน)
- **Comparison:** Same metrics as CONST_RAW, different ballot type
- **Key difference:** Fewer records, regional level data

### Main Metric: Invalid Ballots
Shows how many voters spoiled their ballots (marking invalid choices)
- Higher % = more confusion or dissatisfaction
- Comparing 2566 vs 2569 shows trends
- Visualization highlights areas where invalid ballots exceed winner margin

---

## 🔍 Quick Reference: What Each File Does

| File | Purpose | When to Use |
|------|---------|------------|
| QUICK_START.md | 3-step quick guide | First time setup |
| DATA_BUILDING_GUIDE.md | Detailed step-by-step | Reference & learning |
| election_data_processing.ipynb | Interactive notebook | Development & debugging |
| build_election_data.py | Automated script | Batch processing |
| example_data_structure.js | Data format reference | Validation & verification |
| index.html | Main visualization | The final result |

---

## ❓ FAQ

**Q: Which file should I start with?**
A: Start with [QUICK_START.md](QUICK_START.md) for the fast track.

**Q: I don't know Python/Jupyter - what do I do?**
A: Follow the notebook step-by-step. It's designed for both technical and non-technical users. Each cell has explanations.

**Q: How often do I need to update data?**
A: Whenever new election data becomes available. The notebook can be rerun for any data source.

**Q: Can I use this with just one dataset (only ส.ส. or only บส.)?**
A: Yes! Leave PARTYLIST_RAW empty and the toggle will show "data coming soon" message.

**Q: What if my data has different structure?**
A: Adjust the data loading section in the notebook to match your file format. See [DATA_BUILDING_GUIDE.md](DATA_BUILDING_GUIDE.md) for details.

---

## 🔗 Related Resources

- **Thailand Election Data**: election66/ folder with 2566 results
- **OCR Results**: ~/Documents/GitHub/election-69-OCR-result/
- **Visualization**: Open index.html in any modern browser

---

## 📝 Notes for Future Maintainers

### When Adding New Features:
1. The toggle is already implemented in index.html
2. Add feature to BOTH display paths if needed
3. Test with both CONST_RAW and PARTYLIST_RAW datasets

### When Updating Data:
1. Documentation auto-explains expected fields
2. Use example_data_structure.js as validation template
3. Always run notebook's validation checklist

### When Collaborating:
1. Use the notebook for code clarity
2. Document any custom transformations
3. Update this index when adding new tools/docs

---

## 🎯 Success Criteria

You'll know you're successful when:
- ✅ Toggle buttons work in the visualization
- ✅ Switching between ส.ส. and บส. shows different data
- ✅ All 400 constituencies + 77 regions display correctly
- ✅ Invalid ballot percentages make sense (2-15%)
- ✅ Percentage changes show realistic trends
- ✅ No console errors in browser

---

## 📞 Support

For issues or questions:
1. Check the relevant .md file (see table above)
2. Review example_data_structure.js for format questions
3. Check browser console for data validation errors
4. Review the notebook for data processing questions

---

**Last Updated:** February 2026
**Version:** 1.0 - Initial release with toggle feature & data processing tools
