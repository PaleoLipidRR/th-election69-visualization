import json
import re

def extract_js_vars(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    const_idx = text.find('CONST_RAW = [')
    if const_idx == -1:
        const_idx = text.find('CONST_RAW= [')
        if const_idx == -1: return [], []
        
    const_start = text.find('[', const_idx)
    pl_idx = text.find('PARTYLIST_RAW = [', const_start)
    if pl_idx == -1: pl_idx = text.find('PARTYLIST_RAW= [', const_start)
    
    if pl_idx != -1:
        const_end = text.rfind(']', const_start, pl_idx) + 1
        const_str = text[const_start:const_end]
        
        pl_start = text.find('[', pl_idx)
        pl_end = text.rfind(']') + 1
        pl_str = text[pl_start:pl_end]
    else:
        const_end = text.rfind(']') + 1
        const_str = text[const_start:const_end]
        pl_str = '[]'
        
    try:
        const_data = json.loads(const_str) if const_str else []
        pl_data = json.loads(pl_str) if pl_str and pl_str != '[]' else []
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error in {filepath}: {e}")
        return [], []
        
    return const_data, pl_data

def process_66_enhanced(gen_const, gen_pl):
    try:
        with open('../data/election66/th_election66_info_party_overview.json', 'r', encoding='utf-8-sig') as f:
            parties = json.load(f)
        party_map = {int(p['id']): p['name'] for p in parties}
        
        with open('../data/election66/th_election66_stats_cons.json', 'r', encoding='utf-8-sig') as f:
            stats = json.load(f)
            
        enrich_map = {}
        for prov in stats.get('result_province', []):
            prov_id = prov.get('prov_id')
            if not prov_id: continue
            for cons in prov.get('constituencies', []):
                cons_str = cons.get('cons_id', '')
                try:
                    cons_no = int(cons_str.split('_')[1])
                except:
                    continue
                
                # Cons candidates
                cands = cons.get('candidates', [])
                if len(cands) >= 2:
                    cands.sort(key=lambda x: x.get('mp_app_vote', 0), reverse=True)
                    c_winner = cands[0]
                    c_runnerup = cands[1]
                    c_winner_party = party_map.get(c_winner.get('party_id'), 'Unknown')
                    c_winner_votes = int(c_winner.get('mp_app_vote', 0))
                    c_runner_party = party_map.get(c_runnerup.get('party_id'), 'Unknown')
                    c_runner_votes = int(c_runnerup.get('mp_app_vote', 0))
                elif len(cands) == 1:
                    c_winner = cands[0]
                    c_winner_party = party_map.get(c_winner.get('party_id'), 'Unknown')
                    c_winner_votes = int(c_winner.get('mp_app_vote', 0))
                    c_runner_party = 'None'
                    c_runner_votes = 0
                else:
                    c_winner_party = 'Unknown'
                    c_winner_votes = 0
                    c_runner_party = 'None'
                    c_runner_votes = 0
                
                # PL results
                pls = cons.get('result_party', [])
                if len(pls) >= 2:
                    pls.sort(key=lambda x: x.get('party_list_vote', 0), reverse=True)
                    p_winner = pls[0]
                    p_runnerup = pls[1]
                    p_winner_party = party_map.get(p_winner.get('party_id'), 'Unknown')
                    p_winner_votes = int(p_winner.get('party_list_vote', 0))
                    p_runner_party = party_map.get(p_runnerup.get('party_id'), 'Unknown')
                    p_runner_votes = int(p_runnerup.get('party_list_vote', 0))
                elif len(pls) == 1:
                    p_winner = pls[0]
                    p_winner_party = party_map.get(p_winner.get('party_id'), 'Unknown')
                    p_winner_votes = int(p_winner.get('party_list_vote', 0))
                    p_runner_party = 'None'
                    p_runner_votes = 0
                else:
                    p_winner_party = 'Unknown'
                    p_winner_votes = 0
                    p_runner_party = 'None'
                    p_runner_votes = 0
                
                valid = int(cons.get('valid_votes', 0))
                invalid = int(cons.get('invalid_votes', 0))
                blank = int(cons.get('blank_votes', 0))
                turn_out = int(cons.get('turn_out', 0))
                percent_invalid = float(cons.get('percent_invalid_votes', 0))
                
                pl_valid = int(cons.get('party_list_valid_votes', 0))
                pl_invalid = int(cons.get('party_list_invalid_votes', 0))
                pl_blank = int(cons.get('party_list_blank_votes', 0))
                pl_turn_out = int(cons.get('party_list_turn_out', 0))
                pl_percent_invalid = float(cons.get('party_list_percent_invalid_votes', 0))
                
                enrich_map[(prov_id, cons_no)] = {
                    'c_winner_party': c_winner_party,
                    'c_winner_votes': c_winner_votes,
                    'c_runner_party': c_runner_party,
                    'c_runner_votes': c_runner_votes,
                    'c_margin': c_winner_votes - c_runner_votes,
                    'c_valid': valid,
                    'c_invalid': invalid,
                    'c_blank': blank,
                    'c_turn_out': turn_out,
                    'c_percent_invalid': percent_invalid,
                    
                    'p_winner_party': p_winner_party,
                    'p_winner_votes': p_winner_votes,
                    'p_runner_party': p_runner_party,
                    'p_runner_votes': p_runner_votes,
                    'p_margin': p_winner_votes - p_runner_votes,
                    'p_valid': pl_valid,
                    'p_invalid': pl_invalid,
                    'p_blank': pl_blank,
                    'p_turn_out': pl_turn_out,
                    'p_percent_invalid': pl_percent_invalid,
                }
    except Exception as e:
        print(f"Error logic: {e}")
        enrich_map = {}
        
    out_c = []
    for d in gen_const:
        prov_id = d.get('prov_id', '')
        cons_no = d.get('cons_no', 0)
        info = enrich_map.get((prov_id, cons_no), {})
        
        rec = {
            "province_thai": d.get("province_thai", d.get("province", "Unknown")),
            "province_eng": d.get("province_eng", ""),
            "prov_id": prov_id,
            "cons_no": cons_no,
            "region": d.get("region", ""),
            "turn_out": info.get('c_turn_out', d.get("turn_out_2566", d.get("turn_out", 0))),
            "percent_invalid": info.get('c_percent_invalid', d.get("percent_invalid_2566", d.get("percent_invalid", 0))),
            
            "winner_party": info.get('c_winner_party', d.get("winner_party_2566", "Unknown")),
            "winner_votes": info.get('c_winner_votes', 0),
            "runnerup_party": info.get('c_runner_party', "Unknown"),
            "runnerup_votes": info.get('c_runner_votes', 0),
            "margin": info.get('c_margin', 0),
            
            "valid": info.get('c_valid', 0),
            "invalid": info.get('c_invalid', 0),
            "blank": info.get('c_blank', 0),
        }
        out_c.append(rec)
        
    out_p = []
    for d in gen_pl:
        prov_id = d.get('prov_id', '')
        cons_no = d.get('cons_no', 0)
        info = enrich_map.get((prov_id, cons_no), {})
        
        rec = {
            "province_thai": d.get("province_thai", d.get("province", "Unknown")),
            "province_eng": d.get("province_eng", ""),
            "prov_id": prov_id,
            "cons_no": cons_no,
            "region": d.get("region", ""),
            "turn_out": info.get('p_turn_out', d.get("turn_out_2566", d.get("turn_out", 0))),
            "percent_invalid": info.get('p_percent_invalid', d.get("percent_invalid_2566", d.get("percent_invalid", 0))),
            
            "winner_party": info.get('p_winner_party', "Unknown"),
            "winner_votes": info.get('p_winner_votes', 0),
            "runnerup_party": info.get('p_runner_party', "Unknown"),
            "runnerup_votes": info.get('p_runner_votes', 0),
            "margin": info.get('p_margin', 0),
            
            "valid": info.get('p_valid', 0),
            "invalid": info.get('p_invalid', 0),
            "blank": info.get('p_blank', 0),
        }
        out_p.append(rec)
        
    return out_c, out_p

def process_69(records):
    out = []
    for d in records:
        rec = {
            "province_thai": d.get("province_thai", d.get("province", "Unknown")),
            "province_eng": d.get("province_eng", ""),
            "prov_id": d.get("prov_id", ""),
            "cons_no": d.get("cons_no", 0),
            "region": d.get("region", ""),
            
            "turn_out": d.get("turn_out_2569", d.get("turn_out", 0)),
            "total_used": d.get("total_used_2569", d.get("total_used", 0)),
            "valid": d.get("valid_2569", d.get("valid", 0)),
            "invalid": d.get("invalid_2569", d.get("invalid", 0)),
            "blank": d.get("blank_2569", d.get("blank", 0)),
            "winner_party": d.get("winner_party_2569", d.get("winner_party", "Unknown")),
            "winner_votes": d.get("winner_votes_2569", d.get("winner_votes", 0)),
            "runnerup_party": d.get("runnerup_party_2569", d.get("runnerup_party", "Unknown")),
            "runnerup_votes": d.get("runnerup_votes_2569", d.get("runnerup_votes", 0)),
            "margin": d.get("margin_2569", d.get("margin", 0)),
            "percent_invalid": d.get("percent_invalid_2569", d.get("percent_invalid", 0))
        }
        out.append(rec)
    return out

def compute_surpluses(const_records, pl_records):
    pl_map = {f"{r.get('province_thai')}_{r.get('cons_no')}": r for r in pl_records}
    for c in const_records:
        k = f"{c.get('province_thai')}_{c.get('cons_no')}"
        p = pl_map.get(k)
        if p:
            if 'valid' in c and 'invalid' in c and 'blank' in c and \
               'valid' in p and 'invalid' in p and 'blank' in p:
                c_sum = c['valid'] + c['invalid'] + c['blank']
                p_sum = p['valid'] + p['invalid'] + p['blank']
                surplus = c_sum - p_sum
            else:
                surplus = 0
            
            c['ballot_surplus'] = surplus
            p['ballot_surplus'] = surplus
        else:
            c['ballot_surplus'] = 0

def write_js(filename, const_data, pl_data):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"const CONST_RAW = {json.dumps(const_data, ensure_ascii=False, indent=2)};\n\n")
        f.write(f"const PARTYLIST_RAW = {json.dumps(pl_data, ensure_ascii=False, indent=2)};\n")

# Main execution
gen_const, gen_pl = extract_js_vars("../data/election_data_generated.js")
pct94_const, pct94_pl = extract_js_vars("../data/election69_94pct.js")

# Map missing metadata in 94pct by using gen_const (which is complete)
meta_map = { f"{d.get('province_thai')}_{d.get('cons_no')}": d for d in gen_const }

for r in pct94_const:
    k = f"{r.get('province_thai')}_{r.get('cons_no')}"
    if k in meta_map:
        for fld in ['province_eng', 'prov_id', 'region']:
            if fld in meta_map[k]:
                r[fld] = meta_map[k][fld]

for r in pct94_pl:
    k = f"{r.get('province_thai')}_{r.get('cons_no')}"
    if k in meta_map:
        for fld in ['province_eng', 'prov_id', 'region']:
            if fld in meta_map[k]:
                r[fld] = meta_map[k][fld]

# Extract 66 data
const_66, pl_66 = process_66_enhanced(gen_const, gen_pl)
compute_surpluses(const_66, pl_66)
write_js("../data/election66_data.js", const_66, pl_66)
print("Created election66_data.js")

# Extract 69 OCR data
const_69ocr = process_69(gen_const)
pl_69ocr = process_69(gen_pl)
compute_surpluses(const_69ocr, pl_69ocr)
write_js("../data/election69_ocr.js", const_69ocr, pl_69ocr)
print("Created election69_ocr.js")

# Extract 69 94pct data
const_6994 = process_69(pct94_const)
pl_6994 = process_69(pct94_pl)
compute_surpluses(const_6994, pl_6994)
write_js("../data/election69_94pct.js", const_6994, pl_6994)
print("Created election69_94pct.js")
