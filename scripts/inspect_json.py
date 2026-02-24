import json

try:
    with open('election66/th_election66_stats_cons.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print("Cons Data Type:", type(data))
    if isinstance(data, dict):
        print("Cons Data Keys:", list(data.keys()))
        for k in list(data.keys())[:3]:
            print(f"  {k} type:", type(data[k]))
            if isinstance(data[k], list) and len(data[k]) > 0:
                print(f"  {k} first item keys:", list(data[k][0].keys()))
            elif isinstance(data[k], dict) and len(data[k]) > 0:
                first_key = list(data[k].keys())[0]
                print(f"  {k}[{first_key}] type:", type(data[k][first_key]))
    elif isinstance(data, list) and len(data) > 0:
        print("Cons Data first item keys:", list(data[0].keys()))

    print("\n---")
    with open('election66/th_election66_stats_party.json', 'r', encoding='utf-8') as f:
        data_party = json.load(f)
    print("Party Data Type:", type(data_party))
    if isinstance(data_party, dict):
        print("Party Data Keys:", list(data_party.keys()))
        for k in list(data_party.keys())[:3]:
            if isinstance(data_party[k], list) and len(data_party[k]) > 0:
                print(f"  {k} first item keys:", list(data_party[k][0].keys()))
except Exception as e:
    print(f"Error: {e}")
