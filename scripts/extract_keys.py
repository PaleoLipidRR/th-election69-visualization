import json

print("Reading cons...")
try:
    with open('election66/th_election66_stats_cons.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open('temp_cons_0.json', 'w', encoding='utf-8') as f:
        json.dump(data[0:2], f, indent=2, ensure_ascii=False)
    print("Cons done.")
    
    with open('election66/th_election66_stats_party.json', 'r', encoding='utf-8') as f:
        data2 = json.load(f)
    with open('temp_party_0.json', 'w', encoding='utf-8') as f:
        json.dump(data2[0:2], f, indent=2, ensure_ascii=False)
    print("Party done.")
except Exception as e:
    print(f"Error: {e}")
