import requests
from bs4 import BeautifulSoup
import json
import os
import re
import hashlib
from datetime import datetime
from collections import deque

class FestivalAcquisitionAgent:
    def __init__(self, base_workspace="/home/aiagent/hyeongryeol_workspace/festa_global_db"):
        self.base_workspace = base_workspace
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        })

    def get_festival_id(self, country_code, name):
        hash_val = hashlib.md5(name.encode()).hexdigest()[:8]
        return f"{country_code}-{hash_val}"

    def get_wikipedia_category(self, country_name):
        return f"https://en.wikipedia.org/wiki/Category:Festivals_in_{country_name.replace(' ', '_')}"

    def scrape_seed_list(self, country_code, country_name, target_count=4000):
        start_url = self.get_wikipedia_category(country_name)
        festivals = {} 
        visited_categories = set()
        queue = deque([start_url])
        
        print(f" Discovering festivals for {country_name}...")
        
        while queue and len(festivals) < target_count:
            url = queue.popleft()
            if url in visited_categories:
                continue
            visited_categories.add(url)
            
            try:
                response = self.session.get(url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                category_div = soup.find('div', {'class': 'mw-category'})
                if category_div:
                    links = category_div.find_all('a')
                    for link in links:
                        if not link.has_attr('href'): continue
                        href = link['href']
                        name = link.text
                        
                        if 'Category:' in name:
                            cat_url = 'https://en.wikipedia.org' + href
                            if cat_url not in visited_categories:
                                queue.append(cat_url)
                        else:
                            fest_url = 'https://en.wikipedia.org' + href
                            if fest_url not in festivals:
                                festivals[fest_url] = name
                                if len(festivals) >= target_count:
                                    break
                
                next_page = soup.find('a', string=re.compile(r'next page', re.I))
                if next_page:
                    next_url = 'https://en.wikipedia.org' + next_page['href']
                    queue.appendleft(next_url)

            except Exception as e:
                print(f" Error visiting {url}: {e}")
                
        return [{'name': name, 'url': url} for url, name in festivals.items()]

    def extract_sds_data(self, country_code, country_name, festival_seed):
        name = festival_seed['name']
        url = festival_seed['url']
        fest_id = self.get_festival_id(country_code, name)
        
        sds = {
            "identity": {
                "festival_id": fest_id,
                "name_en": name,
                "name_local": "Unknown",
                "country": country_name,
                "city": "Unknown",
                "category": "Cultural/Traditional"
            },
            "schedule": {
                "start_date": "Unknown",
                "end_date": "Unknown",
                "frequency": "Annual",
                "season": "Unknown"
            },
            "logistics": {
                "location": {
                    "address": "Unknown",
                    "coordinates": {"lat": None, "lon": None}
                },
                "access": "Unknown"
            },
            "multimedia": {
                "official_url": "Unknown",
                "images": [],
                "videos": []
            },
            "resources": {
                "tickets": "Unknown",
                "guide_url": "Unknown"
            },
            "verification": {
                "source": "Wikipedia",
                "last_updated": datetime.now().strftime("%Y-%m-%d"),
                "status": "collected"
            }
        }

        try:
            resp = self.session.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            first_p = soup.find('p')
            if first_p:
                text = first_p.text
                city_match = re.search(r'in ([^,.]+),', text)
                if city_match:
                    sds["identity"]["city"] = city_match.group(1).strip()

            infobox = soup.find('table', {'class': 'infobox'})
            if infobox:
                links = infobox.find_all('a')
                for link in links:
                    href = link.get('href', '')
                    if href.startswith('http') and 'wikipedia.org' not in href:
                        sds["multimedia"]["official_url"] = href
                        break
                
                coord_div = infobox.find('span', {'class': 'geo'})
                if coord_div:
                    coords = re.findall(r'([-+]?\d+\.\d+)', coord_div.text)
                    if len(coords) >= 2:
                        sds["logistics"]["location"]["coordinates"] = {"lat": float(coords[0]), "lon": float(coords[1])}

            text_content = soup.get_text()
            months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            for month in months:
                if month in text_content:
                    sds["schedule"]["start_date"] = month
                    break

        except Exception as e:
            pass

        return sds

    def process_country(self, country_code, country_name):
        print(f"Processing {country_name} ({country_code})...")
        
        seeds = self.scrape_seed_list(country_code, country_name)
        seed_path = os.path.join(self.base_workspace, country_code, "seed_list.json")
        os.makedirs(os.path.dirname(seed_path), exist_ok=True)
        with open(seed_path, 'w', encoding='utf-8') as f:
            json.dump(seeds, f, indent=2, ensure_ascii=False)
        
        print(f" Found {len(seeds)} festivals. Enriching...")
        
        count = 0
        for seed in seeds:
            sds = self.extract_sds_data(country_code, country_name, seed)
            fest_id = sds["identity"]["festival_id"]
            out_path = os.path.join(self.base_workspace, country_code, f"{fest_id}_sds.json")
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(sds, f, indent=2, ensure_ascii=False)
            count += 1
            if count % 100 == 0:
                print(f" Progress: {count}/{len(seeds)}")

        return len(seeds)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python festivals_collector.py <CODE> <NAME>")
        sys.exit(1)
    
    code = sys.argv[1]
    name = sys.argv[2]
    agent = FestivalAcquisitionAgent()
    total = agent.process_country(code, name)
    print(f"Completed {name}: {total} records saved.")
