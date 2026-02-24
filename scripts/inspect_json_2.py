import json

with open('election66/th_election66_stats_cons.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("result_province items count:", len(data.get('result_province', [])))
if len(data.get('result_province', [])) > 0:
    first_prov = data['result_province'][0]
    print("first prov keys:", first_prov.keys())
    print("first prov name:", first_prov.get('province_thai'))
    if 'result_constituency' in first_prov:
        print("result_constituency count:", len(first_prov['result_constituency']))
        if len(first_prov['result_constituency']) > 0:
            first_cons = first_prov['result_constituency'][0]
            print("first_cons keys:", first_cons.keys())
            if 'result_vote' in first_cons:
                print("result_vote sample:")
                for v in first_cons['result_vote'][:3]:
                    print("  ", v)
