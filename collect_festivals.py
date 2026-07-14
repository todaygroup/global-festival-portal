import requests
import json
import time
import re
from collections import deque

# Constants
API_URL = 'https://ja.wikipedia.org/w/api.php'
HEADERS = {'User-Agent': 'HermesFestivalCollector/1.1 (contact: aiagent@example.com)'}
TARGET_COUNT = 3000
OUTPUT_PATH = '/home/aiagent/hyeongryeol_workspace/festa_global_db/JP/seed_list.json'

PREFECTURES = [
    "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
    "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
    "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
    "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
    "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
    "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
    "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
]

def get_category_members(category_name):
    members = []
    full_cat_name = category_name if category_name.startswith('Category:') else f'Category:{category_name}'
    params = {
        'action': 'query',
        'list': 'categorymembers',
        'cmtitle': full_cat_name,
        'cmlimit': '500',
        'format': 'json'
    }
    while True:
        try:
            response = requests.get(API_URL, params=params, headers=HEADERS, timeout=10)
            data = response.json()
            res_members = data.get('query', {}).get('categorymembers', [])
            members.extend(res_members)
            if 'continue' in data:
                params['cmcontinue'] = data['continue']['cmcontinue']
            else:
                break
        except Exception as e:
            print(f"Error fetching {full_cat_name}: {e}")
            break
    return members

def get_subcategories(category_name):
    full_cat_name = category_name if category_name.startswith('Category:') else f'Category:{category_name}'
    params = {
        'action': 'query',
        'list': 'categorymembers',
        'cmtitle': full_cat_name,
        'cmtype': 'subcat',
        'cmlimit': '500',
        'format': 'json'
    }
    try:
        response = requests.get(API_URL, params=params, headers=HEADERS, timeout=10)
        data = response.json()
        return [m['title'] for m in data.get('query', {}).get('categorymembers', [])]
    except Exception as e:
        print(f"Error fetching subcategories for {full_cat_name}: {e}")
        return []

def extract_city(text):
    """
    Attempt to find city/prefecture in the text.
    Looks for patterns like '[Prefecture][City]市' or '[Prefecture]'
    """
    if not text:
        return 'Unknown'
    
    # Search for prefecture + city/town/village
    # Example: 東京都新宿区, 大阪府大阪市
    match = re.search(r'([^\s]*?(?:県|府|都|道)[^\s]*?(?:市|区|町|村))', text)
    if match:
        return match.group(1)
    
    # Fallback to just prefecture
    for pref in PREFECTURES:
        if pref in text:
            return pref
            
    return 'Unknown'

def fetch_details_batched(festival_map):
    """
    Fetch extracts for all festivals in batches of 50.
    """
    page_ids = [f['pageid'] for f in festival_map.values()]
    batch_size = 50
    
    for i in range(0, len(page_ids), batch_size):
        batch = page_ids[i:i + batch_size]
        params = {
            'action': 'query',
            'prop': 'extracts',
            'exintro': True,
            'explaintext': True,
            'pageids': '|'.join(map(str, batch)),
            'format': 'json'
        }
        try:
            response = requests.get(API_URL, params=params, headers=HEADERS, timeout=10)
            data = response.json()
            pages = data.get('query', {}).get('pages', {})
            for pid, page in pages.items():
                extract = page.get('extract', '')
                city = extract_city(extract)
                if city != 'Unknown':
                    # Update the festival object in the map
                    for f in festival_map.values():
                        if f['pageid'] == int(pid):
                            f['city'] = city
                            break
        except Exception as e:
            print(f"Error fetching batch {i}: {e}")
        time.sleep(0.1)

def main():
    all_festivals = {} # name -> data
    visited_categories = set()
    queue = deque(['日本の祭り', '日本の祭礼'])
    
    for pref in PREFECTURES:
        queue.append(f'{pref}の祭り')
        queue.append(f'{pref}の祭礼')

    print(f"Starting acquisition. Target: {TARGET_COUNT}")
    
    while queue and len(all_festivals) < TARGET_COUNT:
        cat = queue.popleft()
        if cat in visited_categories:
            continue
        visited_categories.add(cat)
        
        subcats = get_subcategories(cat)
        for s in subcats:
            if s not in visited_categories:
                queue.append(s)
        
        members = get_category_members(cat)
        for m in members:
            if m['ns'] == 0:
                name = m['title']
                if name not in all_festivals:
                    all_festivals[name] = {
                        'name': name,
                        'city': 'Unknown', 
                        'source': f'https://ja.wikipedia.org/?curid={m["pageid"]}',
                        'pageid': m['pageid']
                    }
                    if len(all_festivals) >= TARGET_COUNT:
                        break
        if len(all_festivals) % 200 == 0:
            print(f"Collected {len(all_festivals)} seeds...")

    print(f"Seeds collected: {len(all_festivals)}. Now enriching cities...")
    fetch_details_batched(all_festivals)
    
    # Clean up pageid before saving
    final_list = []
    for f in all_festivals.values():
        final_list.append({
            'name': f['name'],
            'city': f['city'],
            'source': f['source']
        })
    
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(final_list)} festivals to {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
