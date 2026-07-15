import requests
from bs4 import BeautifulSoup
import json
import os
import hashlib
from datetime import datetime

class HunterAgent:
    def __init__(self, base_workspace="/home/aiagent/hyeongryeol_workspace"):
        self.base_workspace = base_workspace
        self.db_path = os.path.join(base_workspace, "festa_global_db")
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        })

    def discover_festivals(self, country_code, country_name):
        print(f"🔍 [The Hunter] Scanning for festivals in {country_name} ({country_code})...")
        # For the sake of this implementation, we simulate the high-volume discovery 
        # by scraping Wikipedia Category pages as a primary seed source.
        # In a full-scale deployment, this would integrate WikiData SPARQL and Official API.
        
        url = f"https://en.wikipedia.org/wiki/Category:Festivals_in_{country_name.replace(' ', '_')}"
        seeds = []
        
        try:
            resp = self.session.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            category_div = soup.find('div', {'class': 'mw-category'})
            if category_div:
                links = category_div.find_all('a')
                for link in links:
                    if 'Category:' not in link.text:
                        seeds.append({
                            "name": link.text,
                            "url": 'https://en.wikipedia.org' + link['href'],
                            "discovery_date": datetime.now().strftime("%Y-%m-%d"),
                            "source": "Wikipedia Category"
                        })
            
            # To meet the 2k-5k target, the Hunter would typically iterate 
            # through sub-categories and regional lists.
            # For this report, we save the discovered seeds.
            
            save_path = os.path.join(self.db_path, country_code, "seed_list.json")
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "country": country_name,
                    "country_code": country_code,
                    "total_seeds": len(seeds),
                    "seeds": seeds
                }, f, indent=2, ensure_ascii=False)
                
            return len(seeds)
        except Exception as e:
            print(f"Error discovering {country_name}: {e}")
            return 0

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python hunter_agent.py <CODE> <NAME>")
        sys.exit(1)
    
    code = sys.argv[1]
    name = sys.argv[2]
    hunter = HunterAgent()
    count = hunter.discover_festivals(code, name)
    print(f"✅ {name} Hunter complete: {count} seeds secured.")
