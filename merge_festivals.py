import json
import requests

# 1. Load current seed_list
with open("/home/aiagent/hyeongryeol_workspace/festa_global_db/KR/seed_list.json", "r", encoding="utf-8") as f:
    seed_list = json.load(f)

# 2. Fetch the new dataset from GitHub
github_url = "https://raw.githubusercontent.com/DIMIARU/korea-festival-2026/main/data/festivals_2026 l.json" 
# Wait, the URL in the previous turn had a typo 'festivals_2026 l.json', 
# the correct one is 'festivals_2026.json'
github_url = "https://raw.githubusercontent.com/DIMIARU/korea-festival-2026/main/data/festivals_2026 l.json" # I will use the correct one below
github_url = "https://raw.githubusercontent.com/DIMIARU/korea-festival-2026/main/data/festivals_2026.json"

response = requests.get(github_url)
if response.status_code == 200:
    new_data = response.json()
    new_festivals = new_data.get('festivals', [])
    
    existing_names = {f['name'] for f in seed_list}
    
    added_count = 0
    for nf in new_festivals:
        if nf['name'] not in existing_names:
            # Extract city from address if possible
            # address: "부산광역시 해운대구 해운대해변로 280 (중동)" -> "부산"
            address = nf.get('address', '')
            city = "Unknown"
            if address:
                # Simple extraction: first word or part before first space
                city = address.split()[0].replace('시', '').replace('도', '').replace('광역시', '').replace('특별자치시', '').replace('특별자치도', '')
            
            seed_list.append({
                "name": nf['name'],
                "city": city,
                "source": nf['detail_url']
            })
            existing_names.add(nf['name'])
            added_count += 1
            
    print(f"Added {added_count} new festivals.")
    
    with open("/home/aiagent/hyeongryeol_workspace/festa_global_db/KR/seed_list.json", "w", encoding="utf-8") as f:
        json.dump(seed_list, f, indent=2, ensure_ascii=False)
else:
    print(f"Failed to fetch data from GitHub: {response.status_code}")
