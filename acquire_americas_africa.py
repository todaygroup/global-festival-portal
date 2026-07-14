
import os
import json
import hashlib
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
BASE_DIR = "/home/aiagent/hyeongryeol_workspace/festa_global_db"
COUNTRIES = {
    "Americas": [
        "USA", "CAN", "MEX", "GTM", "BLZ", "HND", "SLV", "NIC", "CRI", "PAN", 
        "CUB", "JAM", "HTI", "DOM", "BHS", "ATG", "DMA", "GRD", "KNA", "LCA", 
        "MTQ", "MSK", "TTO", "VGB", "VIR", "GUY", "SUR", "BOL", "COL", "ECU", 
        "PER", "BRA", "CHL", "ARG", "URY", "PYR"
    ],
    "Africa": [
        "DZA", "AGO", "BGN", "BDI", "BFA", "BWA", "BHL", "CMR", "CPV", "TCD", 
        "CGF", "COG", "COM", "DJI", "EGY", "GNQ", "ERI", "SWZ", "ETH", "GAB", 
        "GMB", "GHA", "GNB", "GWE", "CIV", "KEN", "LSO", "LBR", "LBY", "MDG", 
        "MWI", "MLI", "MRT", "MUS", "MAR", "MOZ", "NAM", "NER", "NGA", "RWA", 
        "STP", "SEN", "SYC", "SLA", "SOM", "ZAF", "SSD", "SDN", "TZA", "TGO", 
        "TUN", "UGA", "ZMB", "ZWE"
    ]
}

COUNTRY_NAMES = {
    "USA": "United States", "CAN": "Canada", "MEX": "Mexico", "GTM": "Guatemala", "BLZ": "Belize",
    "HND": "Honduras", "SLV": "El Salvador", "NIC": "Nicaragua", "CRI": "Costa Rica", "PAN": "Panama",
    "CUB": "Cuba", "JAM": "Jamaica", "HTI": "Haiti", "DOM": "Dominican Republic", "BHS": "Bahamas",
    "ATG": "Antigua and Barbuda", "DMA": "Dominica", "GRD": "Grenada", "KNA": "Saint Kitts and Nevis",
    "LCA": "Saint Lucia", "MTQ": "Martinique", "MSK": "Montserrat", "TTO": "Trinidad and Tobago",
    "VGB": "British Virgin Islands", "VIR": "US Virgin Islands", "GUY": "Guyana", "SUR": "Suriname",
    "BOL": "Bolivia", "COL": "Colombia", "ECU": "Ecuador", "PER": "Peru", "BRA": "Brazil", "CHL": "Chile",
    "ARG": "Argentina", "URY": "Uruguay", "PYR": "Paraguay", "DZA": "Algeria", "AGO": "Angola",
    "BGN": "Benin", "BDI": "Burundi", "BFA": "Burkina Faso", "BWA": "Botswana", "BHL": "Botswana",
    "CMR": "Cameroon", "CPV": "Cape Verde", "TCD": "Chad", "CGF": "Republic of the Congo", "COG": "Democratic Republic of the Congo",
    "COM": "Comoros", "DJI": "Djibouti", "EGY": "Egypt", "GNQ": "Equatorial Guinea", "ERI": "Eritrea",
    "SWZ": "Eswatini", "ETH": "Ethiopia", "GAB": "Gabon", "GMB": "Gambia", "GHA": "Ghana",
    "GNB": "Guinea-Bissau", "GWE": "Guinea", "CIV": "Ivory Coast", "KEN": "Kenya", "LSO": "Lesotho",
    "LBR": "Liberia", "LBY": "Libya", "MDG": "Madagascar", "MWI": "Malawi", "MLI": "Mali",
    "MRT": "Mauritania", "MUS": "Mauritius", "MAR": "Morocco", "MOZ": "Mozambique", "NAM": "Namibia",
    "NER": "Niger", "NGA": "Nigeria", "RWA": "Rwanda", "STP": "Sao Tome and Principe", "SEN": "Senegal",
    "SYC": "Seychelles", "SLA": "Sierra Leone", "SOM": "Somalia", "ZAF": "South Africa", "SSD": "South Sudan",
    "SDN": "Sudan", "TZA": "Tanzania", "TGO": "Togo", "TUN": "Tunisia", "UGA": "Uganda", "ZMB": "Zambia", "ZWE": "Zimbabwe"
}

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

def get_wikipedia_pages(country_name):
    """Use Wikipedia API to find pages related to festivals in the country."""
    pages = []
    search_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": f"festivals in {country_name}",
        "srlimit": 10,
        "format": "json"
    }
    try:
        r = requests.get(search_url, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            for item in data.get("query", {}).get("search", []):
                pages.append(item["title"])
    except Exception as e:
        print(f"⚠️ API Error for {country_name}: {e}")
    return pages

def scrape_page_for_festivals(page_title, country_name):
    """Scrape a specific Wikipedia page for festival names."""
    festivals = []
    url = f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            # Look for tables first (higher density)
            for table in soup.find_all('table', class_='wikitable'):
                for row in table.find_all('tr')[1:]: # Skip header
                    cols = row.find_all('td')
                    if cols:
                        name = cols[0].text.strip()
                        if name and len(name) < 100:
                            festivals.append({"name": name, "country": country_name, "url": url})
            
            # Then look for lists
            for li in soup.find_all('li'):
                text = li.text.strip()
                if 5 < len(text) < 150 and any(w in text.lower() for w in ["festival", "carnival", "holiday"]):
                    name = text.split('(')[0].strip()
                    festivals.append({"name": name, "country": country_name, "url": url})
                    
    except Exception as e:
        print(f"⚠️ Scrape Error for {page_title}: {e}")
    
    # Unique only
    seen = set()
    unique = []
    for f in festivals:
        if f['name'] not in seen:
            unique.append(f)
            seen.add(f['name'])
    return unique

def main():
    total_records = 0
    processed_countries = 0
    
    for region, countries in COUNTRIES.items():
        for cc in countries:
            cc = cc.strip()
            country_name = COUNTRY_NAMES.get(cc, cc)
            
            country_dir = os.path.join(BASE_DIR, cc)
            os.makedirs(country_dir, exist_ok=True)
            
            # 1. Find relevant pages
            pages = get_wikipedia_pages(country_name)
            # Always try the direct "List of festivals in..." page too
            pages.append(f"List of festivals in {country_name}")
            
            found_fests = []
            for page in pages:
                found_fests.extend(scrape_page_for_festivals(page, country_name))
            
            # De-duplicate across all pages for this country
            final_fests = []
            seen = set()
            for f in found_fests:
                if f['name'] not in seen:
                    final_fests.append(f)
                    seen.add(f['name'])
            
            country_count = 0
            for f in final_fests:
                record = create_sds_record(f, cc)
                fname = f"{record['identity']['festival_id']}_sds.json"
                with open(os.path.join(country_dir, fname), 'w', encoding='utf-8') as fout:
                    json.dump(record, fout, indent=2, ensure_ascii=False)
                country_count += 1
                
            print(f"✅ {cc} ({country_name}): Saved {country_count} festivals.")
            total_records += country_count
            processed_countries += 1

    print(f"\n--- FINAL SUMMARY ---")
    print(f"Total Countries Processed: {processed_countries}")
    print(f"Total Records Saved: {total_records}")

if __name__ == '__main__':
    main()
