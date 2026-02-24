import pandas as pd
import json
from datetime import datetime
from pathlib import Path

def extract_data():
    excel_path = '/home/ronnie-rattan/Documents/GitHub/th-election69-visualization/data/election69/ElectionData-Analysis-Public-Transfer-unofficial94percent.xlsx'
    
    # 1. CONSTITUENCY DATA
    df_const_full = pd.read_excel(excel_path, sheet_name='สสแบ่งเขต')
    
    # Group by province and constituency to get summaries
    # Assume ลำดับคะแนน 1 is the winner
    const_raw = []
    for (prov, cons), group in df_const_full.groupby(['จังหวัด', 'เขตเลือกตั้งที่']):
        winner_row = group[group['ลำดับคะแนน'] == 1].iloc[0] if not group[group['ลำดับคะแนน'] == 1].empty else None
        runnerup_row = group[group['ลำดับคะแนน'] == 2].iloc[0] if len(group) > 1 else None
        
        if winner_row is not None:
            voters = int(winner_row.get('ผู้มาใช้สิทธิ์', 0))
            valid = int(winner_row.get('บัตรดี', 0))
            invalid = int(winner_row.get('บัตรเสีย', 0))
            blank = int(winner_row.get('บัตรไม่เลือกผู้ใด', 0))
            margin = int(winner_row.get('คะแนนเสียง', 0)) - int(runnerup_row.get('คะแนนเสียง', 0)) if runnerup_row is not None else 0
            
            const_raw.append({
                "province_thai": str(prov),
                "cons_no": int(cons),
                "turn_out_2569": voters,
                "total_used_2569": voters,
                "valid_2569": valid,
                "invalid_2569": invalid,
                "blank_2569": blank,
                "percent_invalid_2569": (float(invalid) / float(voters) * 100) if voters > 0 else 0,
                "winner_party_2569": str(winner_row.get('พรรคที่สังกัด', 'Unknown')),
                "winner_votes_2569": int(winner_row.get('คะแนนเสียง', 0)),
                "runnerup_party_2569": str(runnerup_row.get('พรรคที่สังกัด', 'Unknown')) if runnerup_row is not None else "Unknown",
                "runnerup_votes_2569": int(runnerup_row.get('คะแนนเสียง', 0)) if runnerup_row is not None else 0,
                "margin_2569": int(margin)
            })

    # 2. PARTY LIST DATA (Simplified - assume voters/invalid same structure or similar)
    # The 'party list' sheet may have different columns, but let's try to load it
    try:
        df_pl_full = pd.read_excel(excel_path, sheet_name='party list')
        pl_raw = []
        for (prov, cons), group in df_pl_full.groupby(['จังหวัด', 'เขตเลือกตั้งที่']):
            # Logic similar to constituency
            winner_row = group[group['ลำดับคะแนน'] == 1].iloc[0] if not group[group['ลำดับคะแนน'] == 1].empty else None
            runnerup_row = group[group['ลำดับคะแนน'] == 2].iloc[0] if len(group) > 1 else None
            
            if winner_row is not None:
                voters = int(winner_row.get('ผู้มาใช้สิทธิ์', 0))
                valid = int(winner_row.get('บัตรดี', 0))
                invalid = int(winner_row.get('บัตรเสีย', 0))
                blank = int(winner_row.get('บัตรไม่เลือกผู้ใด', 0))
                margin = int(winner_row.get('คะแนนเสียง', 0)) - int(runnerup_row.get('คะแนนเสียง', 0)) if runnerup_row is not None else 0
                
                pl_raw.append({
                    "province_thai": str(prov),
                    "cons_no": int(cons),
                    "turn_out_2569": voters,
                    "total_used_2569": voters,
                    "valid_2569": valid,
                    "invalid_2569": invalid,
                    "blank_2569": blank,
                    "percent_invalid_2569": (float(invalid) / float(voters) * 100) if voters > 0 else 0,
                    "winner_party_2569": str(winner_row.get('พรรคการเมือง', 'Unknown')),
                    "winner_votes_2569": int(winner_row.get('คะแนนเสียง', 0)),
                    "runnerup_party_2569": str(runnerup_row.get('พรรคการเมือง', 'Unknown')) if runnerup_row is not None else "Unknown",
                    "runnerup_votes_2569": int(runnerup_row.get('คะแนนเสียง', 0)) if runnerup_row is not None else 0,
                    "margin_2569": int(margin)
                })
    except Exception as e:
        print(f"Party list extraction failed: {e}. Using empty/const fallback.")
        pl_raw = []

    # OUTPUT TO JS
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    const_json = json.dumps(const_raw, ensure_ascii=False, indent=2)
    pl_json = json.dumps(pl_raw, ensure_ascii=False, indent=2)

    js_content = f"""// Unofficial 94% Election Data for Thailand 2569
// Generated: {timestamp_str}

var CONST_RAW = {const_json};
var PARTYLIST_RAW = {pl_json};
"""
    
    # Write directly to data/ (no versioning needed for 94pct)
    out_path = Path('../data/election69_94pct.js')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"✓ Created {out_path}")

if __name__ == "__main__":
    extract_data()
