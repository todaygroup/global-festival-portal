import requests
import json
import os
from datetime import datetime

class HunterAgentV2:
    def __init__(self, base_workspace="/home/aiagent/hyeongryeol_workspace"):
        self.base_workspace = base_workspace
        self.db_path = os.path.join(base_workspace, "festa_global_db")
        self.wikidata_url = "https://query.wikidata.org/sparql"

    def get_festivals_sparql(self, country_code):
        country_qids = {
            "DE": "Q183", "JP": "Q17", "FR": "Q142", "US": "Q30", "KR": "Q1056",
            "IT": "Q38", "ES": "Q160", "CN": "Q148", "GB": "Q145", "CA": "Q1"
        }
        qid = country_qids.get(country_code)
        if not qid:
            return []

        query = f"""
        SELECT ?festival ?festivalLabel ?url WHERE {{
          ?festival wdt:P31 wd:Q484222;
                    wdt:P17 wd:{qid}.
          OPTIONAL {{ ?festival wdt:P856 ?url. }}
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT 5000
        """
        params = {'query': query, 'format': 'json'}
        try:
            response = requests.get(self.wikidata_url, params=params, timeout=15)
            data = response.json()
            results = data['results']['bindings']
            seeds = []
            for res in results:
                seeds.append({
                    "id": res['festival'].split('/')[-1] if isinstance(res['festival'], str) else res['festival']['value'].split('/')[-1],
                    "name": res['festivalLabel']['value'],
                    "url": res.get('url', {}).get('value', 'Unknown') if 'url' in res else 'Unknown',
                    "source": "WikiData SPARQL",
                    "discovery_date": datetime.now().strftime("%Y-%m-%d")
                })
            return seeds
        except Exception as e:
            print(f"SPARQL Error for {country_code}: {e}")
            return []

    def execute_discovery(self, country_list):
        total_global_seeds = 0
        for country in country_list:
            code = country['code']
            name = country['name']
            print(f"📡 [The Hunter V2] Querying WikiData for {name} ({code})...")
            seeds = self.get_festivals_sparql(code)
            count = len(seeds)
            save_path = os.path.join(self.base_workspace, "festa_global_db", code, "seed_list.json")
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump({"country": name, "country_code": code, "total_seeds": count, "seeds": seeds}, f, indent=2, ensure_ascii=False)
            print(f"✅ Secured {count} seeds for {name}.")
            total_global_seeds += count
        return total_global_seeds

if __name__ == "__main__":
    targets = [
        {"code": "DE", "name": "Germany"},
        {"code": "JP", "name": "Japan"},
        {"code": "FR", "name": "France"},
        {"code": "US", "name": "United States"},
        {"code": "KR", "name": "South Korea"},
        {"code": "IT", "name": "Italy"},
        {"code": "ES", "name": "Spain"},
        {"code": "CN", "name": "China"},
        {"code": "GB", "name": "United Kingdom"},
        {"code": "CA", "name": "Canada"}
    ]
    hunter = HunterAgentV2()
    total = hunter.execute_discovery(targets)
    print(f"\n🚀 Discovery Phase Complete. Total seeds secured across 10 major nations: {total}")
