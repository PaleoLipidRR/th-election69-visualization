#!/usr/bin/env python3
"""
Build election data for Thailand election visualization
Processes election66 JSON data and merges with election69 data
Exports as JavaScript arrays for use in index.html
"""

import json
import os
import glob
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# ══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════

# Paths
ELECTION66_JSON_DIR = Path(__file__).parent.parent / "data" / "election66"
ELECTION69_CONST_DIR = Path.home() / "Documents/GitHub/election-69-OCR-result/data/matched/constituency"
ELECTION69_PL_DIR = Path.home() / "Documents/GitHub/election-69-OCR-result/data/matched/party_list"
OUTPUT_FILE = Path(__file__).parent.parent / "data" / "election_data.js"
ARCHIVE_DIR = Path(__file__).parent.parent / "data" / "archives"
MANIFEST_FILE = ARCHIVE_DIR / "manifest.json"

# ══════════════════════════════════════════════════════════════════════════
# REGION MAPPING
# ══════════════════════════════════════════════════════════════════════════

# Mapping province IDs to regions (standard 6-region classification)
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


def load_election66_constituency_data() -> Dict[str, Any]:
    """Load election66 constituency election results"""
    print("📥 Loading election66 data...")
    
    if not ELECTION66_JSON_DIR.exists():
        print(f"⚠️  election66 directory not found: {ELECTION66_JSON_DIR}")
        return {}
    
    # Load constituency info and stats
    cons_info = {}
    
    cons_info_file = ELECTION66_JSON_DIR / "th_election66_info_constituency.json"
    if cons_info_file.exists():
        with open(cons_info_file, 'r', encoding='utf-8') as f:
            cons_list = json.load(f)
            for item in cons_list:
                cons_key = f"{item['prov_id']}_{item['cons_no']}"
                cons_info[cons_key] = item
    
    cons_stats_file = ELECTION66_JSON_DIR / "th_election66_stats_cons.json"
    if cons_stats_file.exists():
        with open(cons_stats_file, 'r', encoding='utf-8') as f:
            stats_data = json.load(f)
            # Traverse nested structure: result_province -> constituencies
            for prov in stats_data.get('result_province', []):
                prov_id = prov.get('prov_id')
                for cons in prov.get('constituencies', []):
                    cons_id = cons.get('cons_id', '')
                    if '_' in cons_id:
                        try:
                            # Extract cons_no from cons_id (e.g., "ACR_1" -> 1)
                            cons_no = int(cons_id.split('_')[-1])
                            cons_key = f"{prov_id}_{cons_no}"
                            if cons_key in cons_info:
                                cons_info[cons_key].update(cons)
                            else:
                                cons_info[cons_key] = cons
                        except (ValueError, IndexError):
                            continue
    
    print(f"✓ Loaded {len(cons_info)} constituencies with stats")
    return cons_info


def load_province_mapping() -> Dict[str, str]:
    """Load mapping from Thai province names to prov_id codes"""
    prov_mapping = {}
    
    prov_file = ELECTION66_JSON_DIR / "th_election66_info_province.json"
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
    
    prov_file = ELECTION66_JSON_DIR / "th_election66_info_province.json"
    if prov_file.exists():
        with open(prov_file, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
            for prov in data.get('province', []):
                prov_id = prov.get('prov_id')
                province_eng = prov.get('eng')
                if prov_id and province_eng:
                    prov_eng_map[prov_id] = province_eng
    
    return prov_eng_map


# ══════════════════════════════════════════════════════════════════════════
# LOAD ELECTION69 DATA
# ══════════════════════════════════════════════════════════════════════════

def load_json_folder(folder_path: Path, ballot_type: str = "constituency") -> List[Dict[str, Any]]:
    """Load election results from JSON folder"""
    rows = []
    
    if not folder_path.exists():
        print(f"⚠️  Folder not found: {folder_path}")
        return rows
    
    json_files = sorted(glob.glob(os.path.join(folder_path, "*.json")))
    print(f"  Found {len(json_files)} {ballot_type} files")
    
    for fpath in json_files:
        with open(fpath, encoding="utf-8") as f:
            d = json.load(f)

        province    = d.get("province_name_normalized", "Unknown")
        cons_no     = d.get("constituency_number", 0)
        summary     = d.get("summary", {})
        results     = d.get("results", [])

        # Sort by votes descending to get winner / runner-up
        sorted_results = sorted(results, key=lambda x: x.get("votes", 0), reverse=True)
        winner   = sorted_results[0]  if len(sorted_results) > 0 else {"party": None, "votes": 0}
        runnerup = sorted_results[1]  if len(sorted_results) > 1 else {"party": None, "votes": 0}

        total_valid = summary.get("good_votes", 0)
        invalid = summary.get("invalid_votes", 0)
        no_votes = summary.get("no_votes", 0)
        voters_came = summary.get("voters_came", 0)
        
        others = total_valid - winner.get("votes", 0) - runnerup.get("votes", 0)

        rows.append({
            "province_thai": province,
            "cons_no": cons_no,
            "total_valid": total_valid,
            "invalid_ballots": invalid,
            "no_votes": no_votes,
            "voters_came": voters_came,
            "winning_score": winner.get("votes", 0),
            "winning_party": winner.get("party"),
            "runnerUp_score": runnerup.get("votes", 0),
            "runnerUp_party": runnerup.get("party"),
            "others_score": max(others, 0),
        })
    
    return rows


def load_election69_data() -> tuple:
    """Load election 2569 (2026) data"""
    print("\n📥 Loading election69 data...")
    
    const_data = load_json_folder(ELECTION69_CONST_DIR, "constituency")
    print(f"✓ Loaded {len(const_data)} constituency results")
    
    pl_data = load_json_folder(ELECTION69_PL_DIR, "party_list")
    print(f"✓ Loaded {len(pl_data)} party_list results")
    
    return const_data, pl_data


# ══════════════════════════════════════════════════════════════════════════
# PROCESS AND MERGE DATA
# ══════════════════════════════════════════════════════════════════════════

def process_election66_to_const_raw(election66_data: Dict) -> List[Dict[str, Any]]:
    """
    Transform election66 data into CONST_RAW format matching election69 structure
    For now, we'll create a minimal dataset to show the structure
    """
    print("\n🔄 Processing election66 into CONST_RAW...")
    
    # This would require more detailed election66 data
    # For now returning empty - you'll populate this with actual data
    return []


def process_election69_to_datasets(const_data: List[Dict], pl_data: List[Dict], prov_mapping: Dict[str, str], prov_eng_mapping: Dict[str, str]) -> tuple:
    """
    Transform election69 data into CONST_RAW and PARTYLIST_RAW
    Calculate differences between election66 and election69
    """
    print("\n🔄 Processing election69 data...")
    
    const_raw = []
    pl_raw = []
    
    # Build lookup by province + cons_no
    pl_lookup = {
        f"{d['province_thai']}_{d['cons_no']}": d 
        for d in pl_data
    }
    
    for c_data in const_data:
        prov_thai = c_data['province_thai']
        cons_no = c_data['cons_no']
        key = f"{prov_thai}_{cons_no}"
        
        # Find matching party list data
        pl_match = pl_lookup.get(key)
        if not pl_match:
            continue
        
        # Get prov_id and province_eng from mappings
        prov_id = prov_mapping.get(prov_thai, prov_thai[:3].upper())
        province_eng = prov_eng_mapping.get(prov_id, "")
        region = REGION_MAP.get(prov_id, "")
        
        # Extract vote counts
        const_valid = c_data['total_valid']
        const_invalid = c_data['invalid_ballots']
        const_blank = c_data['no_votes']
        const_total_used = c_data['voters_came']
        
        const_invalid_pct = (const_invalid / const_total_used * 100) if const_total_used > 0 else 0
        const_margin = c_data['winning_score'] - c_data['runnerUp_score']
        
        # Create constituency MP record
        const_record = {
            "prov_id": prov_id,
            "province_thai": prov_thai,
            "province_eng": province_eng,
            "region": region,
            "cons_no": cons_no,
            "valid_2569": const_valid,
            "invalid_2569": const_invalid,
            "blank_2569": const_blank,
            "total_used_2569": const_total_used,
            "turn_out_2569": const_total_used,
            "percent_invalid_2569": const_invalid_pct,
            "winner_party_2569": c_data['winning_party'],
            "winner_votes_2569": c_data['winning_score'],
            "runnerup_party_2569": c_data['runnerUp_party'],
            "runnerup_votes_2569": c_data['runnerUp_score'],
            "margin_2569": const_margin,
        }
        const_raw.append(const_record)
        
        # Create party list MP record
        pl_valid = pl_match['total_valid']
        pl_invalid = pl_match['invalid_ballots']
        pl_blank = pl_match['no_votes']
        pl_total_used = pl_match['voters_came']
        pl_invalid_pct = (pl_invalid / pl_total_used * 100) if pl_total_used > 0 else 0
        pl_margin = pl_match['winning_score'] - pl_match['runnerUp_score']
        
        pl_record = {
            "prov_id": prov_id,
            "province_thai": prov_thai,
            "province_eng": province_eng,
            "region": region,
            "cons_no": cons_no,
            "valid_2569": pl_valid,
            "invalid_2569": pl_invalid,
            "blank_2569": pl_blank,
            "total_used_2569": pl_total_used,
            "turn_out_2569": pl_total_used,
            "percent_invalid_2569": pl_invalid_pct,
            "winner_party_2569": pl_match['winning_party'],
            "winner_votes_2569": pl_match['winning_score'],
            "runnerup_party_2569": pl_match['runnerUp_party'],
            "runnerup_votes_2569": pl_match['runnerUp_score'],
            "margin_2569": pl_margin,
        }
        pl_raw.append(pl_record)
    
    print(f"✓ Created {len(const_raw)} constituency records")
    print(f"✓ Created {len(pl_raw)} party list records")
    
    return const_raw, pl_raw


# ══════════════════════════════════════════════════════════════════════════
# ARCHIVING & EXPORT
# ══════════════════════════════════════════════════════════════════════════

def update_manifest(archive_filename: str, timestamp_str: str):
    """Update manifest.json with new archive info"""
    if not MANIFEST_FILE.exists():
        manifest = []
    else:
        try:
            with open(MANIFEST_FILE, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
        except:
            manifest = []
    
    # Check if latest entry exists, if not add it
    has_latest = any(item['id'] == 'latest' for item in manifest)
    if not has_latest:
        manifest.insert(0, {
            "id": "latest",
            "name": "Latest (Active)",
            "file": "election_data_generated.js"
        })

    # Add new archive
    archive_id = timestamp_str.replace(" ", "_").replace(":", "").replace("-", "")
    manifest.append({
        "id": archive_id,
        "name": f"Archive: {timestamp_str}",
        "file": f"archives/{archive_filename}"
    })
    
    with open(MANIFEST_FILE, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"✓ Updated manifest: {MANIFEST_FILE}")


def export_to_javascript(const_raw: List[Dict], pl_raw: List[Dict], archive: bool = False):
    """Export data as JavaScript arrays"""
    now = datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # Convert lists to JSON strings
    const_json = json.dumps(const_raw, ensure_ascii=False, indent=2)
    pl_json = json.dumps(pl_raw, ensure_ascii=False, indent=2)
    
    js_content = f"""// Generated election data for Thailand election visualization
// Generated: {timestamp_str}

// Constituency MP (ส.ส. เขต) - {len(const_raw)} constituencies
var CONST_RAW = {const_json};

// Party List MP (บส. รายชื่อ) - {len(pl_raw)} records
var PARTYLIST_RAW = {pl_json};
"""
    
    # Always write to main output file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"✓ JavaScript file saved to: {OUTPUT_FILE}")
    
    # Optionally save to archive
    if archive:
        if not ARCHIVE_DIR.exists():
            ARCHIVE_DIR.mkdir(parents=True)
            
        archive_filename = f"election_data_{now.strftime('%Y%md_%H%M')}.js"
        archive_path = ARCHIVE_DIR / archive_filename
        
        with open(archive_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
        print(f"  📦 Archived as: {archive_path}")
        
        update_manifest(archive_filename, timestamp_str)



# ══════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Build election data for Thailand election visualization")
    parser.add_argument("--archive", action="store_true", help="Save a copy of the data to the archives folder")
    args = parser.parse_args()

    print("🔍 Thailand Election Data Builder")
    print("═" * 50)
    
    # Load data
    election66_data = load_election66_constituency_data()
    prov_mapping = load_province_mapping()
    prov_eng_mapping = load_province_eng_mapping()
    const_data, pl_data = load_election69_data()
    
    # Process and merge
    const_raw = []
    pl_raw = []
    
    if const_data or pl_data:
        const_raw, pl_raw = process_election69_to_datasets(const_data, pl_data, prov_mapping, prov_eng_mapping)
    
    # Export
    export_to_javascript(const_raw, pl_raw, archive=args.archive)
    
    print("\n✅ Complete!")
    print(f"\nNext steps:")
    print(f"1. Verification:")
    print(f"   Check your generated data in: {OUTPUT_FILE}")
    if args.archive:
        print(f"   Check manifest updated in: {MANIFEST_FILE}")



if __name__ == "__main__":
    main()
