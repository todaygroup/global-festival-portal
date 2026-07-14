import requests
import json

def test_wikidata():
    url = 'https://query.wikidata.org/sparql'
    query = """
    SELECT ?item ?itemLabel WHERE {
      ?item wdt:P17 wd:Q183 .
      ?item wdt:P31 wd:Q11352 .
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    LIMIT 10
    """
    params = {'query': query, 'format': 'json'}
    headers = {'User-Agent': 'TestAgent/1.0'}
    r = requests.get(url, params=params, headers=headers)
    print(f"Status: {r.status_code}")
    print(r.text)

if __name__ == '__main__':
    test_wikidata()
