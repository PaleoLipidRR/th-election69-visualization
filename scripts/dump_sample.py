import json

with open('election66/th_election66_stats_cons.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

first_prov = data['result_province'][0]
first_cons = first_prov['constituencies'][0]
candidates = first_cons.get('candidates', [])

with open('temp_sample_candidates.json', 'w', encoding='utf-8') as f:
    json.dump(candidates[:3], f, indent=2, ensure_ascii=False)
