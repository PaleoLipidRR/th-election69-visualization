#!/usr/bin/env python3
"""
Build election data for Thailand election visualization
Processes election66 JSON data and merges with election69 data
Exports as JavaScript arrays for use in index.html
"""

import json
import os
import glob
from pathlib import Path
from typing import Dict, List, Any

# ══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════

# Paths
ELECTION66_JSON_DIR = Path(__file__).parent / "election66"
ELECTION69_CONST_DIR = Path.home() / "Documents/GitHub/election-69-OCR-result/data/matched/constituency"
ELECTION69_PL_DIR = Path.home() / "Documents/GitHub/election-69-OCR-result/data/matched/party_list"
OUTPUT_FILE = Path(__file__).parent / "election_data.js"

# ══════════════════════════════════════════════════════════════════════════
# REGION MAPPING
# ══════════════════════════════════════════════════════════════════════════

NE_region = ["อำนาจเจริญ","บึงกาฬ","บุรีรัมย์","ชัยภูมิ","กาฬสินธุ์","ขอนแก่น","เลย",
             "มหาสารคาม","มุกดาหาร","นครพนม","นครราชสีมา","หนองบัวลำภู","หนองคาย",
             "ร้อยเอ็ด","สกลนคร","ศรีสะเกษ","สุรินทร์","อุบลราชธานี","อุดรธานี","ยโสธร"]
N_region  = ["เชียงใหม่","เชียงราย","ลำปาง","ลำพูน","แม่ฮ่องสอน","น่าน","พะเยา","แพร่","อุตรดิตถ์"]
W_region  = ["ตาก","กาญจนบุรี","ราชบุรี","เพชรบุรี","ประจวบคีรีขันธ์"]
E_region  = ["ฉะเชิงเทรา","จันทบุรี","ชลบุรี","ปราจีนบุรี","ระยอง","สระแก้ว","ตราด"]
C_region  = ["อุทัยธานี","อ่างทอง","ชัยนาท","พระนครศรีอยุธยา","ลพบุรี","นครปฐม","นนทบุรี",
             "ปทุมธานี","นครนายก","นครสวรรค์","สมุทรปราการ","สมุทรสาคร","สมุทรสงคราม",
             "สระบุรี","สิงห์บุรี","สุพรรณบุรี","สุโขทัย","พิษณุโลก","พิจิตร","กำแพงเพชร","เพชรบูรณ์"]
BKK       = ["กรุงเทพมหานคร"]
S_region  = ["ชุมพร","นครศรีธรรมราช","นราธิวาส","ปัตตานี","พัทลุง","สงขลา","สุราษฎร์ธานี",
             "ยะลา","กระบี่","พังงา","ภูเก็ต","ระนอง","สตูล","ตรัง"]

REGION_DICT = {
    **{p: "02 ภาคอีสาน"        for p in NE_region},
    **{p: "01 ภาคเหนือ"        for p in N_region},
    **{p: "06 ภาคตะวันตก"      for p in W_region},
    **{p: "03 ภาคตะวันออก"     for p in E_region},
    **{p: "04 ภาคกลาง"         for p in C_region},
    **{p: "05 กรุงเทพมหานคร"   for p in BKK},
    **{p: "07 ภาคใต้"          for p in S_region},
}

# ══════════════════════════════════════════════════════════════════════════
# PROVINCE MAPPING (prov_id to Thai name from election66 data)
# ══════════════════════════════════════════════════════════════════════════

def build_province_id_to_name_map() -> Dict[str, str]:
    """Extract province ID to Thai name mapping from election66 constituency data"""
    if not ELECTION66_JSON_DIR.exists():
        return {}
    
    mapping = {}
    for json_file in ELECTION66_JSON_DIR.glob("*.json"):
        if "constituency" in json_file.name:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    prov_id = item.get('prov_id')
                    # Try to get province name - we'll need to map this
                    if prov_id:
                        # This will be populated during processing
                        pass
    return mapping


# ══════════════════════════════════════════════════════════════════════════
# LOAD ELECTION66 DATA
# ══════════════════════════════════════════════════════════════════════════

def load_election66_constituency_data() -> Dict[str, Any]:
    """Load election66 constituency election results"""
    print("📥 Loading election66 data...")
    
    if not ELECTION66_JSON_DIR.exists():
        print(f"⚠️  election66 directory not found: {ELECTION66_JSON_DIR}")
        return {}
    
    # Load constituency info and stats
    cons_info = {}
    cons_stats = {}
    
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
            stats_list = json.load(f)
            for item in stats_list:
                cons_key = f"{item['prov_id']}_{item['cons_no']}"
                cons_stats[cons_key] = item
    
    print(f"✓ Loaded {len(cons_info)} constituencies info")
    print(f"✓ Loaded {len(cons_stats)} constituencies stats")
    
    return {"info": cons_info, "stats": cons_stats}


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


def process_election69_to_datasets(const_data: List[Dict], pl_data: List[Dict]) -> tuple:
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
        
        # Calculate metrics
        const_voters = c_data['voters_came']
        const_invalid = c_data['invalid_ballots']
        const_invalid_pct = (const_invalid / const_voters * 100) if const_voters > 0 else 0
        
        const_margin = c_data['winning_score'] - c_data['runnerUp_score']
        
        # Create constituency MP record
        const_record = {
            "prov_id": prov_thai[:3].upper(),  # Simplified
            "province_thai": prov_thai,
            "cons_no": cons_no,
            "invalid_votes": const_invalid,
            "percent_invalid": const_invalid_pct,
            "turn_out": const_voters,
            "invalid_2026": const_invalid,
            "turnout_2026": const_voters,
            "pct_turnout_2026": (const_voters / (const_voters + c_data['no_votes']) * 100) if (const_voters + c_data['no_votes']) > 0 else 0,
            "invalid_change": 0,  # Will be calculated with election66 data
            "invalid_pct_2026": const_invalid_pct,
            "invalid_pct_change": 0,  # Will be calculated with election66 data
            "winner_party": c_data['winning_party'],
            "margin_votes": const_margin,
            "margin_2569": const_margin,
            "runnerup_votes": c_data['runnerUp_score'],
            "winner_votes": c_data['winning_score'],
            "winner_party_2569": c_data['winning_party'],
            "winner_votes_2569": c_data['winning_score'],
        }
        const_raw.append(const_record)
        
        # Create party list MP record (same structure)
        pl_record = const_record.copy()
        pl_record.update({
            "invalid_2026": pl_match['invalid_ballots'],
            "invalid_pct_2026": (pl_match['invalid_ballots'] / pl_match['voters_came'] * 100) if pl_match['voters_came'] > 0 else 0,
            "margin_2569": pl_match['winning_score'] - pl_match['runnerUp_score'],
            "winner_party_2569": pl_match['winning_party'],
        })
        pl_raw.append(pl_record)
    
    print(f"✓ Created {len(const_raw)} constituency records")
    print(f"✓ Created {len(pl_raw)} party list records")
    
    return const_raw, pl_raw


# ══════════════════════════════════════════════════════════════════════════
# EXPORT TO JAVASCRIPT
# ══════════════════════════════════════════════════════════════════════════

def export_to_javascript(const_raw: List[Dict], pl_raw: List[Dict]):
    """Export data as JavaScript arrays"""
    print(f"\n💾 Exporting to {OUTPUT_FILE}...")
    
    # Convert lists to JSON strings
    const_json = json.dumps(const_raw, ensure_ascii=False, indent=2)
    pl_json = json.dumps(pl_raw, ensure_ascii=False, indent=2)
    
    js_content = f"""// Generated election data for Thailand election visualization
// Generated by build_election_data.py

// Constituency MP (ส.ส. เขต) - 400 constituencies
const CONST_RAW = {const_json};

// Party List MP (บส. รายชื่อ)
const PARTYLIST_RAW = {pl_json};
"""
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"✓ Exported {len(const_raw)} constituency records")
    print(f"✓ Exported {len(pl_raw)} party list records")
    print(f"✓ JavaScript file saved to: {OUTPUT_FILE}")


# ══════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════

def main():
    print("🔍 Thailand Election Data Builder")
    print("═" * 50)
    
    # Load data
    election66_data = load_election66_constituency_data()
    const_data, pl_data = load_election69_data()
    
    # Process and merge
    const_raw = []
    pl_raw = []
    
    if const_data or pl_data:
        const_raw, pl_raw = process_election69_to_datasets(const_data, pl_data)
    
    # Export
    export_to_javascript(const_raw, pl_raw)
    
    print("\n✅ Complete!")
    print(f"\nNext steps:")
    print(f"1. Add the generated data to your index.html:")
    print(f"   <script src='election_data.js'></script>")
    print(f"\n2. Or copy the contents of {OUTPUT_FILE}")
    print(f"   into the <script> section of index.html")


if __name__ == "__main__":
    main()
