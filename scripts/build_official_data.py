#!/usr/bin/env python3
"""
Build official election 2569 data from กกต. Form สส.6/1 (OCR-extracted)

Source: killernay/election-69-OCR-result (matched JSON files)
These files are OCR-extracted from the official Form สส.6/1 PDF documents
published by the Election Commission of Thailand (กกต.) on ect.go.th

Output: data/election69_official.js
        data/election69/election69_official_raw.json (archive)
"""

import json
import glob
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# ══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"

# Source: election-69-OCR-result matched JSON files
OCR_RESULT_DIR = Path.home() / "Documents/GitHub/election-69-OCR-result/data/matched"
CONSTITUENCY_DIR = OCR_RESULT_DIR / "constituency"
PARTY_LIST_DIR = OCR_RESULT_DIR / "party_list"

# Output
OUTPUT_JS = DATA_DIR / "election69_official.js"
OUTPUT_JSON = DATA_DIR / "election69" / "election69_official_raw.json"

# Province name → prov_id mapping (from election66 data for consistency)
ELECTION66_DIR = DATA_DIR / "election66"


def load_province_mapping() -> Dict[str, str]:
    """Load mapping from Thai province names to prov_id codes"""
    prov_mapping = {}
    
    prov_file = ELECTION66_DIR / "th_election66_info_province.json"
    if prov_file.exists():
        with open(prov_file, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
            for prov in data.get('province', []):
                thai_name = prov.get('province')
                prov_id = prov.get('prov_id')
                if thai_name and prov_id:
                    prov_mapping[thai_name] = prov_id
    
    return prov_mapping


def load_province_eng_mapping() -> Dict[str, str]:
    """Load mapping from prov_id to province English name"""
    prov_eng_map = {}
    
    prov_file = ELECTION66_DIR / "th_election66_info_province.json"
    if prov_file.exists():
        with open(prov_file, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
            for prov in data.get('province', []):
                prov_id = prov.get('prov_id')
                province_eng = prov.get('eng')
                if prov_id and province_eng:
                    prov_eng_map[prov_id] = province_eng
    
    return prov_eng_map


# Region mapping (standard 6-region classification)
REGION_MAP = {
    "BKK": "Central", "NBI": "Central", "PTE": "Central", "SPK": "Central", "AYA": "Central",
    "LRI": "Central", "SBR": "Central", "CNT": "Central", "SRI": "Central", "NPT": "Central",
    "SKN": "Central", "SKM": "Central", "PBI": "Central", "RYB": "Central", "KRI": "Central",
    "SPB": "Central", "ATG": "Central", "NYK": "Central", "CCO": "Central", "PRI": "Central",
    "SKW": "Central", "TRT": "Central", "RYG": "Central", "CTI": "Central", "CBI": "Central",
    
    "CMI": "North", "CRI": "North", "MSN": "North", "PYO": "North", "NAN": "North",
    "PRE": "North", "LPG": "North", "LPN": "North", "UTT": "North", "STI": "North",
    "PLK": "North", "TAK": "North", "KPT": "North", "PCT": "North", "PNB": "North",
    "NSN": "North", "UTI": "North",
    
    "KKN": "Northeast", "UDN": "Northeast", "NKI": "Northeast", "LEI": "Northeast", "NBP": "Northeast",
    "BKN": "Northeast", "SNK": "Northeast", "NPM": "Northeast", "MDH": "Northeast", "KSN": "Northeast",
    "RET": "Northeast", "MKM": "Northeast", "CPM": "Northeast", "NMA": "Northeast", "BRM": "Northeast",
    "SRN": "Northeast", "SSK": "Northeast", "UBN": "Northeast", "YST": "Northeast", "ACR": "Northeast",
    
    "NST": "South", "SKA": "South", "SNI": "South", "TRG": "South", "PKN": "South",
    "CPN": "South", "RNG": "South", "PNA": "South", "PKT": "South", "KBI": "South",
    "PLG": "South", "STN": "South", "PTN": "South", "YLA": "South", "NWT": "South"
}


def process_json_folder(folder_path: Path, data_type: str,
                        prov_mapping: Dict[str, str],
                        prov_eng_mapping: Dict[str, str]) -> List[Dict[str, Any]]:
    """Process matched JSON files from OCR result into standardized records"""
    records = []
    
    if not folder_path.exists():
        print(f"⚠️  Folder not found: {folder_path}")
        return records
    
    json_files = sorted(glob.glob(os.path.join(folder_path, "*.json")))
    # Filter out non-data files
    json_files = [f for f in json_files if os.path.basename(f) not in 
                  ('issues.json', 'validation_report.json')]
    
    print(f"  Found {len(json_files)} {data_type} files")
    
    for fpath in json_files:
        with open(fpath, encoding="utf-8") as f:
            d = json.load(f)
        
        province = d.get("province_name_normalized", d.get("province_name", "Unknown"))
        cons_no = d.get("constituency_number", 0)
        summary = d.get("summary", {})
        results = d.get("results", [])
        
        # Sort by votes descending to get winner / runner-up
        sorted_results = sorted(results, key=lambda x: x.get("votes", 0), reverse=True)
        winner = sorted_results[0] if len(sorted_results) > 0 else {"party": None, "votes": 0}
        runnerup = sorted_results[1] if len(sorted_results) > 1 else {"party": None, "votes": 0}
        
        total_valid = summary.get("good_votes", 0)
        invalid = summary.get("invalid_votes", 0)
        no_votes = summary.get("no_votes", 0)
        voters_came = summary.get("voters_came", 0)
        eligible = summary.get("eligible_voters", 0)
        
        winner_votes = winner.get("votes", 0)
        runnerup_votes = runnerup.get("votes", 0)
        margin = winner_votes - runnerup_votes
        
        # Get prov_id and province_eng
        prov_id = prov_mapping.get(province, "")
        province_eng = prov_eng_mapping.get(prov_id, "")
        region = REGION_MAP.get(prov_id, "")
        
        invalid_pct = (invalid / voters_came * 100) if voters_came > 0 else 0
        
        record = {
            "province_thai": province,
            "province_eng": province_eng,
            "prov_id": prov_id,
            "cons_no": cons_no,
            "region": region,
            "turn_out_2569": voters_came,
            "total_used_2569": voters_came,
            "eligible_voters_2569": eligible,
            "valid_2569": total_valid,
            "invalid_2569": invalid,
            "blank_2569": no_votes,
            "percent_invalid_2569": round(invalid_pct, 4),
            "winner_party_2569": winner.get("party"),
            "winner_votes_2569": winner_votes,
            "runnerup_party_2569": runnerup.get("party"),
            "runnerup_votes_2569": runnerup_votes,
            "margin_2569": margin,
        }
        records.append(record)
    
    return records


def compute_surpluses(const_records: List[Dict], pl_records: List[Dict]):
    """Compute ballot surplus (constituency ballots - party list ballots)"""
    pl_map = {f"{r.get('province_thai')}_{r.get('cons_no')}": r for r in pl_records}
    for c in const_records:
        k = f"{c.get('province_thai')}_{c.get('cons_no')}"
        p = pl_map.get(k)
        if p:
            c_sum = c.get('valid_2569', 0) + c.get('invalid_2569', 0) + c.get('blank_2569', 0)
            p_sum = p.get('valid_2569', 0) + p.get('invalid_2569', 0) + p.get('blank_2569', 0)
            surplus = c_sum - p_sum
            c['ballot_surplus'] = surplus
            p['ballot_surplus'] = surplus
        else:
            c['ballot_surplus'] = 0


def main():
    print("🔍 Building Official Election 2569 Data")
    print("   Source: กกต. Form สส.6/1 (OCR-extracted)")
    print("═" * 55)
    
    # Load mappings
    prov_mapping = load_province_mapping()
    prov_eng_mapping = load_province_eng_mapping()
    print(f"✓ Loaded {len(prov_mapping)} province mappings")
    
    # Process constituency data
    print("\n📥 Processing constituency data...")
    const_raw = process_json_folder(CONSTITUENCY_DIR, "constituency", prov_mapping, prov_eng_mapping)
    print(f"✓ Created {len(const_raw)} constituency records")
    
    # Process party list data
    print("\n📥 Processing party list data...")
    pl_raw = process_json_folder(PARTY_LIST_DIR, "party_list", prov_mapping, prov_eng_mapping)
    print(f"✓ Created {len(pl_raw)} party list records")
    
    # Compute surpluses
    compute_surpluses(const_raw, pl_raw)
    
    # Sort by prov_id and cons_no for consistency
    const_raw.sort(key=lambda x: (x.get('prov_id', ''), x.get('cons_no', 0)))
    pl_raw.sort(key=lambda x: (x.get('prov_id', ''), x.get('cons_no', 0)))
    
    # ── Summary Statistics ────────────────────────────────────────────────
    print("\n📊 Summary:")
    parties_const = {}
    for r in const_raw:
        p = r.get('winner_party_2569', 'Unknown')
        parties_const[p] = parties_const.get(p, 0) + 1
    
    print("  Constituency winners (top 5):")
    for party, count in sorted(parties_const.items(), key=lambda x: -x[1])[:5]:
        print(f"    {party}: {count} seats")
    
    total_voters = sum(r.get('turn_out_2569', 0) for r in const_raw)
    total_valid = sum(r.get('valid_2569', 0) for r in const_raw)
    total_invalid = sum(r.get('invalid_2569', 0) for r in const_raw)
    print(f"\n  Total voters (const): {total_voters:,}")
    print(f"  Total valid votes: {total_valid:,}")
    print(f"  Total invalid votes: {total_invalid:,}")
    
    # ── Export as JavaScript ──────────────────────────────────────────────
    now = datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
    
    const_json = json.dumps(const_raw, ensure_ascii=False, indent=2)
    pl_json = json.dumps(pl_raw, ensure_ascii=False, indent=2)
    
    js_content = f"""// Official Election 2569 Data (กกต. Form สส.6/1)
// Source: killernay/election-69-OCR-result (OCR-extracted from official ECT documents)
// Coverage: {len(const_raw)}/400 constituencies, {len(pl_raw)}/400 party list areas
// Generated: {timestamp_str}

const CONST_RAW = {const_json};

const PARTYLIST_RAW = {pl_json};
"""
    
    with open(OUTPUT_JS, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"\n✓ JavaScript file saved to: {OUTPUT_JS}")
    
    # ── Also save raw JSON for archiving ──────────────────────────────────
    os.makedirs(OUTPUT_JSON.parent, exist_ok=True)
    raw_archive = {
        "metadata": {
            "source": "killernay/election-69-OCR-result (OCR from กกต. Form สส.6/1)",
            "generated": timestamp_str,
            "coverage": {
                "constituency": len(const_raw),
                "party_list": len(pl_raw),
                "total_possible": 400,
            },
        },
        "constituency": const_raw,
        "party_list": pl_raw,
    }
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(raw_archive, f, ensure_ascii=False, indent=2)
    print(f"✓ Raw JSON archive saved to: {OUTPUT_JSON}")
    
    print(f"\n✅ Complete! ({len(const_raw)} const + {len(pl_raw)} party list records)")


if __name__ == "__main__":
    main()
