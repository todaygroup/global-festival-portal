import requests
from bs4 import BeautifulSoup
import json
import os

def get_festivals_from_category(category_url):
    festivals = []
    try:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all links in the category members section
        category_members = soup.find('div', {'id': 'mw-categories'})
        if not category_members:
            # Try another selector for the category members
            category_members = soup.find('div', {'class': 'mw-category'})
            
        if category_members:
            links = category_members.find_all('a')
            for link in links:
                name = link.text
                url = 'https://en.wikipedia.org' + link['href']
                # We don't have the city yet, we'll need to visit each page
                festivals.append({'name': name, 'url': url})
        
        # Handle pagination if necessary
        next_page = soup.find('a', string='next page')
        if next_page:
            next_url = 'https://en.wikipedia.org' + next_page['href']
            festivals.extend(get_festivals_from_category(next_url))
            
    except Exception as e:
        print(f"Error scraping category {category_url}: {e}")
        
    return festivals

def get_city_from_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find city in the first paragraph
        first_paragraph = soup.find('p')
        if first_paragraph:
            text = first_paragraph.text
            # Very naive city extraction: look for "in [City], Germany"
            import re
            match = re.search(r'in ([^,.]+), Germany', text)
            if match:
                return match.group(1)
            
            # Try "located in [City]"
            match = re.search(r'located in ([^,.]+)', text)
            if match:
                return match.group(1)
                
    except Exception as e:
        print(f"Error scraping page {url}: {e}")
        
    return "Unknown"

def main():
    start_url = 'https://en.wikipedia.org/wiki/Category:Festivals_in_Germany'
    print(f"Fetching festivals from {start_url}...")
    festivals_list = get_festivals_from_category(start_url)
    print(f"Found {len(festivals_list)} festivals. Now extracting cities...")
    
    final_list = []
    for i, fest in enumerate(festivals_list):
        city = get_city_from_page(fest['url'])
        final_list.append({
            'name': fest['name'],
            'city': city,
            'source_url': fest['url']
        })
        if (i + 1) % 100 == 0:
            print(f"Processed {i+1}/{len(festivals_list)}...")
            
    output_path = '/home/aiagent/hyeongryeol_workspace/festa_global_db/DE/seed_list.json'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(final_list)} festivals to {output_path}")

if __name__ == '__main__':
    main()
