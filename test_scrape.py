
import os
import json
import hashlib
from datetime import datetime
import requests
from bs4 import BeautifulSoup

BASE_DIR = "/home/aiagent/hyeongryeol_workspace/festa_global_db"

def generate_festival_id(country_code, name):
    hash_obj = hashlib.md5(name.encode())
    return f"{country_code}-{hash_obj.hexdigest()[:8]}"

def create_sds_record(festival, country_code):
    name_en = festival.get('name', 'Unknown Festival')
    fest_id = generate_festival_id(country_code, name_en)
    return {
        "identity": {
            "festival_id": fest_id,
            "name_en": name_en,
            "name_local": festival.get('local_name', name_en),
            "country": festival.get('country', 'Unknown'),
            "city": festival.get('city', 'Unknown City'),
            "category": festival.get('category', 'Cultural')
        },
        "schedule": {
            "start_date": festival.get('start', 'TBD'),
            "end_date": festival.get('end', 'TBD'),
            "frequency": "Annual",
            "season": festival.get('season', 'Unknown')
        },
        "logistics": {
            "location": {
                "address": f"Main venue, {festival.get('city', 'Unknown City')}",
                "coordinates": festival.get('coords', {"lat": 0.0, "lon": 0.0})
            },
            "access": "Public transport and local services."
        },
        "multimedia": {
            "official_url": festival.get('url', ''),
            "images": [],
            "videos": []
        },
        "resources": {
            "tickets": "Check official website",
            "guide_url": festival.get('url', '') + "/guide" if festival.get('url') else ""
        },
        "verification": {
            "source": "Web Discovery",
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "status": "discovered"
        }
    }

def get_category_members(category_name):
    """Fetch all pages in a Wikipedia category."""
    members = []
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{category_name}",
        "cmlimit": "500",
        "format": "json"
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            for item in data.get("query", {}).get("categorymembers", []):
                members.append(item["title"])
    except Exception as e:
        print(f"⚠️ Category Error {category_name}: {e}")
    return members

def scrape_page_for_festivals(page_title, country_name):
    """Scrape a specific Wikipedia page for festival names."""
    festivals = []
    url = f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            # Table extraction
            for table in soup.find_all('table', class_='wikitable'):
                for row in table.find_all('tr')[1:]:
                    cols = row.find_all('td')
                    if cols:
                        name = cols[0].text.strip()
                        if name and len(name) < 100:
                            festivals.append({"name": name, "country": country_name, "url": url})
            # List extraction
            for li in soup.find_all('li'):
                text = li.text.strip()
                if 5 < len(text) < 150 and any(w in text.lower() for w in ["festival", "carnival", "holiday"]):
                    name = text.split('(')[0].strip()
                    festivals.append({"name": name, "country": country_name, "url": url})
    except Exception as e:
        pass
    return festivals

def process_country(cc, country_name):
    print(f"🚀 Processing {country_name} ({cc})...")
    country_dir = os.path.join(BASE_DIR, cc)
    os.makedirs(country_dir, exist_ok=True)
    
    # Try a few categories
    categories = [
        f"Festivals of {country_name}",
        f"Festivals in {country_name}",
        f"Culture of {country_name}",
        f"Holidays of {country_name}"
    ]
    
    all_fests = []
    for cat in categories:
        members = get_category_members(cat)
        for member in members:
            all_fests.extend(scrape_page_for_festivals(member, country_name))
    
    # Unique
    seen = set()
    count = 0
    for f in all_fests:
        if f['name'] not in seen:
            record = create_sds_record(f, cc)
            fname = f"{record['identity']['festival_id']}_sds.json"
            with open(os.path.join(country_dir, fname), 'w', encoding='utf-8') as fout:
                json.dump(record, fout, indent=2, ensure_ascii=False)
            seen.add(f['name'])
            count += 1
    
    print(f"✅ {cc}: Saved {count} festivals.")
    return count

if __name__ == "__main__":
    # Test on one large country first
    count = process_country("BRA", "Brazil")
    print(f"Total for Brazil: {count}")
