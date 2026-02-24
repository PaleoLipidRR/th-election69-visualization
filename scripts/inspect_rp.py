import json
import sys

try:
    with open('election66/th_election66_stats_cons.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print("loaded json")
    first_prov = data['result_province'][0]
    first_cons = first_prov['constituencies'][0]
    result_party = first_cons.get('result_party', [])
    print('result_party len:', len(result_party))
    if len(result_party) > 0:
        print('first party result:', result_party[0])
except Exception as e:
    print(f"Error: {e}")
sys.exit(0)
