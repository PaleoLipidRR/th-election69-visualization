import json

with open('election66/th_election66_stats_cons.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

first_prov = data['result_province'][0]
print("first_prov['prov_id']:", first_prov['prov_id'])
if 'constituencies' in first_prov:
    print("constituencies count:", len(first_prov['constituencies']))
    if len(first_prov['constituencies']) > 0:
        first_cons = first_prov['constituencies'][0]
        print("first_cons keys:", first_cons.keys())
        if 'result_vote' in first_cons:
            print("result_vote count:", len(first_cons['result_vote']))
            print("result_vote sample:")
            for v in first_cons['result_vote'][:3]:
                print("  ", v)
