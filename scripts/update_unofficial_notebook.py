import nbformat as nbf
import os
import json
from pathlib import Path

def update_notebook():
    notebook_path = '/home/ronnie-rattan/Documents/GitHub/th-election69-visualization/notebooks/Thailand_Election_2569_unofficial94percent.ipynb'
    if not os.path.exists(notebook_path):
        print(f"Error: {notebook_path} not found")
        return

    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    # Check if export cell already exists
    for cell in nb.cells:
        if 'EXPORT FOR VISUALIZATION' in cell.source:
            print("Export cell already exists.")
            return

    export_cell_code = """# EXPORT FOR VISUALIZATION
import json
import os
from datetime import datetime
from pathlib import Path

def export_to_javascript_94pct(const_df, party_df):
    output_js = '../data/election_data_94pct.js'
    
    # 1. Process Constituency Data
    const_raw = []
    for _, r in const_df.iterrows():
        total_voters = r.get('const_voters', 0)
        invalid = r.get('const_invalid_ballots', 0)
        pct_invalid = (invalid / total_voters * 100) if total_voters > 0 else 0
        
        const_raw.append({
            "province_thai": str(r.get('province', 'Unknown')),
            "cons_no": int(r.get('constituency_number', 0)),
            "region": str(r.get('region', 'Unknown')),
            "invalid_2569": int(invalid),
            "percent_invalid_2569": float(pct_invalid),
            "winner_party_2569": str(r.get('const_winning_party', 'Unknown')),
            "winner_votes_2569": int(r.get('const_winning_score', 0)),
            "runnerup_party_2569": str(r.get('const_runnerUp_party', 'Unknown')),
            "runnerup_votes_2569": int(r.get('const_runnerUp_score', 0)),
            "margin_2569": int(r.get('const_winning_score_diff', 0))
        })

    # 2. Process Party List Data
    pl_raw = []
    for _, r in party_df.iterrows():
        total_voters = r.get('party_voters', 0)
        invalid = r.get('party_invalid_ballots', 0)
        pct_invalid = (invalid / total_voters * 100) if total_voters > 0 else 0
        
        pl_raw.append({
            "province_thai": str(r.get('province', 'Unknown')),
            "cons_no": int(r.get('constituency_number', 0)),
            "region": str(r.get('region', 'Unknown')),
            "invalid_2569": int(invalid),
            "percent_invalid_2569": float(pct_invalid),
            "winner_party_2569": str(r.get('party_winning_party', 'Unknown')),
            "winner_votes_2569": int(r.get('party_winning_score', 0)),
            "runnerup_party_2569": str(r.get('party_runnerUp_party', 'Unknown')),
            "runnerup_votes_2569": int(r.get('party_runnerUp_score', 0)),
            "margin_2569": int(r.get('party_winning_score_diff', 0))
        })

    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    const_json = json.dumps(const_raw, ensure_ascii=False, indent=2)
    pl_json = json.dumps(pl_raw, ensure_ascii=False, indent=2)

    js_content = f\"\"\"// Unofficial 94% Election Data for Thailand 2569
// Generated: {timestamp_str}

var CONST_RAW = {const_json};
var PARTYLIST_RAW = {pl_json};
\"\"\"
    with open(output_js, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"✓ Exported {output_js}")

    # ARCHIVING
    archives_dir = Path('../data/archives')
    archives_dir.mkdir(exist_ok=True, parents=True)
    
    timestamp_file = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_filename = f"election_data_94pct_{timestamp_file}.js"
    archive_path = archives_dir / archive_filename
    
    with open(archive_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"✓ Archived to {archive_path}")

    # UPDATE MANIFEST
    manifest_file = archives_dir / 'manifest.json'
    if manifest_file.exists():
        with open(manifest_file, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    else:
        manifest = []
    
    archive_id = f"94pct_{timestamp_file}"
    manifest.append({
        "id": archive_id,
        "name": f"Unofficial 94%: {timestamp_str}",
        "file": f"data/archives/{archive_filename}"
    })
    
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print("✓ Manifest updated.")

# Execution call
# Assumes 'voters' dataframe is available from the previous cells
if 'voters' in globals():
    export_to_javascript_94pct(voters, voters) # Both currently derived from 'voters' in this notebook
else:
    print("Error: 'voters' dataframe not found. Please run previous cells first.")
"""
    nb.cells.append(nbf.v4.new_code_cell(export_cell_code))

    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Successfully added export cell to {notebook_path}")

if __name__ == "__main__":
    update_notebook()
