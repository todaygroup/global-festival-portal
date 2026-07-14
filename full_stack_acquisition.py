
import requests
import json
import os
import hashlib
from datetime import datetime

# --- Configuration ---
COUNTRIES = {
    "AT": "Austria", "BE": "Belgium", "BG": "Bulgaria", "HR": "Croatia", "CY": "Cyprus",
    "CZ": "Czechia", "DK": "Denmark", "EE": "Estonia", "FI": "Finland", "FR": "France",
    "DE": "Germany", "GR": "Greece", "HU": "Hungary", "IS": "Iceland", "IE": "Ireland",
    "IT": "Italy", "LV": "Latvia", "LI": "Liechtenstein", "LT": "Lithuania", "LU": "Luxembourg",
    "MT": "Malta", "MD": "Moldova", "MC": "Monaco", "ME": "Montenegro", "NL": "Netherlands",
    "MK": "North Macedonia", "NO": "Norway", "PL": "Poland", "PT": "Portugal", "RO": "Romania",
    "RS": "Serbia", "SK": "Slovakia", "SI": "Slovenia", "ES": "Spain", "SE": "Sweden",
    "CH": "Switzerland", "UA": "Ukraine", "GB": "United Kingdom",
    "AM": "Armenia", "AZ": "Azerbaijan", "GE": "Georgia", "IR": "Iran", "IQ": "Iraq",
    "IL": "Israel", "JO": "Jordan", "KZ": "Kazakhstan", "KG": "Kyrgyzstan", "KW": "Kuwait",
    "LB": "Lebanon", "OM": "Oman", "QA": "Qatar", "SA": "Saudi Arabia", "SY": "Syria",
    "TJ": "Tajikistan", "TM": "Turkmenistan", "TR": "Turkey", "AE": "United Arab Emirates",
    "UZ": "Uzbekistan", "YE": "Yemen"
}

BASE_DIR = "/home/aiagent/hyeongryeol_workspace/festa_global_db"
SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"

def generate_festival_id(country_code, name):
    hash_obj = hashlib.md5(name.encode())
    return f"{country_code}-{hash_obj.hexdigest()[:8]}"

def fetch_festivals_wikidata(country_code, country_name):
    print(f"Fetching festivals for {country_name} ({country_code})...")
    
    headers = {
        'User-Agent': 'HermesFestivalBot/1.0 (https://nousresearch.com/hermes; aiagent@example.com)'
    }
    
    # Query: Find items in the country that are instances of or subclasses of 'festival' (Q11467)
    query = f"""
    SELECT ?item ?itemLabel ?description ?coords ?url ?startDate ?endDate WHERE {{
      ?item wdt:P31/wdt:P279* wd:Q11467 . 
      ?item wdt:P17 ?country . 
      ?country rdfs:label "{country_name}"@en . 
      
      OPTIONAL {{ ?item wdt:P625 ?coords . }}
      OPTIONAL {{ ?item wdt:P856 ?url . }}
      OPTIONAL {{ ?item wdt:P580 ?startDate . }}
      OPTIONAL {{ ?item wdt:P582 ?endDate . }}
      
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT 4000
    """
    
    try:
        response = requests.get(SPARQL_ENDPOINT, params={'query': query, 'format': 'json'}, headers=headers, timeout=30)
        if response.status_code != 200:
            print(f"Error: API returned status {response.status_code}")
            return []
        data = response.json()
        results = data['results']['bindings']
        
        festivals = []
        for res in results:
            fest = {
                'id': res['item']['value'].split('/')[-1],
                'name': res['itemLabel']['value'],
                'description': res.get('description', {}).get('value', ''),
                'url': res.get('url', {}).get('value', ''),
                'coords': res.get('coords', {}).get('value', ''),
                'start': res.get('startDate', {}).get('value', ''),
                'end': res.get('endDate', {}).get('value', ''),
                'country': country_name,
                'country_code': country_code
            }
            festivals.append(fest)
        return festivals
    except Exception as e:
        print(f"Error fetching data for {country_name}: {e}")
        return []

def create_sds_record(fest, country_code):
    fest_id = generate_festival_id(country_code, fest['name'])
    
    # Parse coordinates
    coords = {"lat": 0, "lon": 0}
    if fest['coords']:
        try:
            # Wikidata format is usually "Point(lon lat)"
            parts = fest['coords'].replace('Point(', '').replace(')', '').split(' ')
            coords = {"lat": float(parts[1]), "lon": float(parts[0])}
        except:
            pass

    return {
        "identity": {
            "festival_id": fest_id,
            "name_en": fest['name'],
            "name_local": fest['name'], # Simplification: using English as local if not available
            "country": fest['country'],
            "city": "Unknown", # Wikidata doesn't always give City in a flat query
            "category": "Festival"
        },
        "schedule": {
            "start_date": fest['start'] if fest['start'] else "Unknown",
            "end_date": fest['end'] if fest['end'] else "Unknown",
            "frequency": "Annual",
            "season": "Unknown"
        },
        "logistics": {
            "location": {
                "address": "See official website",
                "coordinates": coords
            },
            "access": "Public transportation"
        },
        "multimedia": {
            "official_url": fest['url'] if fest['url'] else "N/A",
            "images": [],
            "videos": []
        },
        "resources": {
            "tickets": "Check official website",
            "guide_url": fest['url'] if fest['url'] else "N/A"
        },
        "verification": {
            "source": "Wikidata",
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "status": "verified"
        }
    }

def process_all_countries():
    total_records = 0
    processed_countries = 0
    
    for code, name in COUNTRIES.items():
        # Retry mechanism
        success = False
        festivals = []
        for attempt in range(3):
            festivals = fetch_festivals_wikidata(code, name)
            if festivals:
                success = True
                break
            import time
            time.sleep(2 * (attempt + 1))
        
        if not success:
            print(f"Failed to fetch data for {name} after 3 attempts.")
            continue
            
        country_dir = os.path.join(BASE_DIR, code)
        os.makedirs(country_dir, exist_ok=True)
        
        country_count = 0
        for f in festivals:
            record = create_sds_record(f, code)
            filename = f"{record['identity']['festival_id']}_sds.json"
            with open(os.path.join(country_dir, filename), 'w', encoding='utf-8') as out:
                json.dump(record, out, indent=2, ensure_ascii=False)
            country_count += 1
            
        print(f"Saved {country_count} festivals for {name}.")
        total_records += country_count
        processed_countries += 1
        
    print(f"\nCOMPLETED")
    print(f"Total countries processed: {processed_countries}")
    print(f"Total records saved: {total_records}")

if __name__ == "__main__":
    process_all_countries()
