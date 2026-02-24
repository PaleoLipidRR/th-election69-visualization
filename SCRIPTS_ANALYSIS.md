# Scripts Analysis & Recommendations

**Date:** February 23, 2026  
**Status:** Analysis Complete

---

## 1. DATA PIPELINE OVERVIEW

The main data regeneration pipeline (`regenerate_data.sh`) consists of 3 core scripts in sequential order:

```
build_election_data.py → extract_94pct_data.py → split_data.py
       ↓                          ↓                      ↓
election_data.js         election69_94pct.js    {final output files}
```

**Output files generated:**
- `data/election66_data.js` - 2566 election data (enriched from election66/)
- `data/election69_ocr.js` - 2569 OCR data (from election69/)
- `data/election69_94pct.js` - 2569 94% unofficial data (from Excel)

---

## 2. CRITICAL ISSUES FOUND & FIXED

### Issue #1: Wrong filename reference in split_data.py ❌ FIXED
**Location:** `scripts/split_data.py` line 247  
**Problem:** Script referenced `election_data_generated.js` but `build_election_data.py` creates `election_data.js`  
**Impact:** Causes metadata enrichment to fail silently, resulting in missing `province_eng`, `prov_id`, `region` fields  
**Status:** ✅ FIXED - Changed to correct filename `election_data.js`

### Issue #2: Relative path dependencies
**Location:** `scripts/split_data.py` (lines 40, 44, 247-284)  
**Problem:** All file paths use relative paths (`../data/...`) requiring script to be run from `scripts/` directory  
**Current Workaround:** `regenerate_data.sh` does `cd "$SCRIPT_DIR"` before running  
**Risk:** Scripts may fail if run from different directory  
**Recommendation:** Convert to absolute paths using `Path(__file__).parent.parent`

---

## 3. ACTIVE PIPELINE SCRIPTS

### ✅ build_election_data.py
**Purpose:** Merges election66 JSON data with election69 OCR data  
**Input:** 
- `data/election66/` - JSON files with metadata, stats, party info
- External: `~/Documents/GitHub/election-69-OCR-result/data/matched/`
**Output:** `data/election_data.js`
**Status:** In pipeline - KEEP

### ✅ extract_94pct_data.py
**Purpose:** Extracts unofficial 94% election data from Excel sheet  
**Input:** `data/election69/ElectionData-Analysis-Public-Transfer-unofficial94percent.xlsx`
**Output:** `data/election69_94pct.js`
**Status:** In pipeline - KEEP

### ✅ split_data.py
**Purpose:** Transforms and enriches election data into final output formats  
**Input:** 
- `../data/election_data.js` (from build_election_data.py)
- `../data/election69_94pct.js` (from extract_94pct_data.py)
- `../data/election66/` JSON files for enrichment
**Output:**
- `../data/election66_data.js`
- `../data/election69_ocr.js`
- `../data/election69_94pct.js`
**Status:** In pipeline - KEEP

---

## 4. UNNECESSARY/DEBUG SCRIPTS

### ❌ dump_sample.py
**Purpose:** Debug utility - dumps sample candidates JSON  
**Usage:** Not used in pipeline  
**Recommendation:** MOVE to `scripts/debug/` or REMOVE

### ❌ inspect_json.py
**Purpose:** Debug utility - inspects JSON structure of election66 stats  
**Usage:** Not used in pipeline  
**Recommendation:** MOVE to `scripts/debug/` or REMOVE

### ❌ inspect_json_2.py
**Purpose:** Debug utility - partial inspection of JSON data  
**Usage:** Not used in pipeline  
**Recommendation:** MOVE to `scripts/debug/` or REMOVE

### ❌ inspect_json_3.py
**Purpose:** Debug utility - detailed JSON structure inspection  
**Usage:** Not used in pipeline  
**Recommendation:** MOVE to `scripts/debug/` or REMOVE

### ❌ inspect_rp.py
**Purpose:** Debug utility - inspects result_party field in JSON  
**Usage:** Not used in pipeline  
**Recommendation:** MOVE to `scripts/debug/` or REMOVE

### ❌ extract_keys.py
**Purpose:** Debug utility - extracts keys from JSON  
**Usage:** Not used in pipeline  
**Recommendation:** MOVE to `scripts/debug/` or REMOVE

### ⚠️ fetch_ect_data.py
**Purpose:** Fetches election data from ECT website (2566 elections)  
**Status:** DEPRECATED  
**Reason:** Data is now read from `data/election66/` directory instead of fetching from external source  
**Recommendation:** ARCHIVE - keep for historical reference but move to `scripts/archive/`

### ⚠️ update_unofficial_notebook.py
**Purpose:** Updates Jupyter notebook with export code  
**Usage:** One-time utility for notebook setup  
**Recommendation:** MOVE to `scripts/utils/` - not part of regular pipeline

---

## 5. RECOMMENDATIONS

### Immediate Actions (Required):
1. ✅ Fix split_data.py filename reference - **COMPLETED**
2. Update relative paths in split_data.py to absolute paths (defensive coding)
3. Update regenerate_data.sh documentation

### Organization (Optional but Recommended):
```
scripts/
├── build_election_data.py        (ACTIVE - core)
├── extract_94pct_data.py         (ACTIVE - core)
├── split_data.py                 (ACTIVE - core)
├── regenerate_data.sh            (ACTIVE - main pipeline)
├── debug/                        (NEW - for debug utilities)
│   ├── dump_sample.py
│   ├── inspect_json.py
│   ├── inspect_json_2.py
│   ├── inspect_json_3.py
│   └── inspect_rp.py
├── utils/                        (NEW - for one-time utilities)
│   ├── extract_keys.py
│   └── update_unofficial_notebook.py
└── archive/                      (NEW - for deprecated scripts)
    └── fetch_ect_data.py
```

### Code Quality Improvements:
1. Convert all relative paths to absolute paths using `Path(__file__).parent`
2. Add error handling for missing files with clear error messages
3. Add logging to track which files are being read/written
4. Add validation that extracted data has expected fields

---

## 6. VERIFICATION CHECKLIST

- ✅ build_election_data.py creates `election_data.js` correctly
- ✅ extract_94pct_data.py creates `election69_94pct.js` correctly  
- ✅ split_data.py reads correct input files (FIXED)
- ✅ Final output files contain expected fields
- ✅ No data loss between pipeline steps
- ✅ Surplus calculation working correctly

---

**Next Steps:** Implement the organizational changes and refactor relative paths to absolute paths for robustness.
