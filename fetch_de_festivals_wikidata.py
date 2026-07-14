import requests
import json
import os

def fetch_festivals_wikidata():
    url = 'https://query.wikidata.org/sparql'
    # Try to find items that are in Germany and have "festival" in their English label
    # but we will avoid the strict P31 check for a moment to see if it's the bottleneck
    query = """
    SELECT ?fest ?festLabel ?city ?cityLabel ?url WHERE {
      ?fest wdt:P17 wd:Q183 .
      ?fest rdfs:label ?label .
      FILTER(LANG(?label) = "en")
      FILTER(CONTAINS(LCASE(?label), "festival"))
      OPTIONAL { ?fest wdt:P131 ?city . }
      OPTIONAL { ?fest wdt:P856 ?url . }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    LIMIT 2000
    """
    
    params = {
        'query': query,
        'format': 'json'
    }
    
    headers = {
        'User-Agent': 'HermesAgent/1.0 (Knowledge Acquisition for Germany Festivals)'
    }
    
    print("Querying Wikidata with label filter...")
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        print(f"Error querying Wikidata: {response.status_code}")
        return []
    
    data = response.json()
    results = data['results']['bindings']
    
    festivals = []
    for item in results:
        name = item.get('festLabel', {}).get('value', 'Unknown')
        city = item.get('cityLabel', {}).get('value', 'Unknown')
        url = item.get('url', {}).get('value')
        if not url:
            entity_id = item.get('fest', {}).get('value', '').split('/')[-1]
            url = f"https://www.wikidata.org/wiki/{entity_id}"
            
        festivals.append({
            'name': name,
            'city': city,
            'source_url': url
        })
        
    return festivals

def main():
    festivals = fetch_festivals_wikidata()
    print(f"Found {len(festivals)} festivals.")
    
    output_path = '/home/aiagent/hyeongryeol_workspace/festa_global_db/DE/seed_list.json'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(festivals, f, indent=2, ensure_ascii=False)
        
    print(f"Saved to {output_path}")

if __name__ == '__main__':
    main()
