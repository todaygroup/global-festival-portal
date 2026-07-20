import json
import os

def is_high_fi(festival):
    # Rule 1: No 'Unknown Festival' in names
    name_en = festival.get('identity', {}).get('name_en', '')
    name_local = festival.get('identity', {}).get('name_local', '')
    if name_en == 'Unknown Festival' or name_local == 'Unknown Festival':
        return False
    
    # Rule 2: Must have a name (not empty/null)
    if not name_en and not name_local:
        return False

    # Rule 3: Not null-heavy. 
    # High-Fi should at least have a description or some identifying logistics/temporal info.
    # If deep_description is null AND coordinates are null AND dates are null, it's too low quality.
    description = festival.get('experience', {}).get('deep_description')
    coords = festival.get('identity', {}).get('coordinates', {})
    dates = festival.get('temporal', {})
    
    has_description = description is not None and len(description.strip()) > 0
    has_coords = coords and coords.get('latitude') is not None and coords.get('longitude') is not None
    has_dates = dates.get('start_date') is not None or dates.get('end_date') is not None
    
    if not (has_description or has_coords or has_dates):
        return False

    return True

def clean_master_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    original_count = len(data['festivals'])
    cleaned_festivals = [f for f in data['festivals'] if is_high_fi(f)]
    new_count = len(cleaned_festivals)
    
    data['festivals'] = cleaned_festivals
    data['metadata']['total_records'] = new_count
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Original records: {original_count}")
    print(f"Cleaned records: {new_count}")
    print(f"Removed: {original_count - new_count}")

if __name__ == '__main__':
    path = '/home/aiagent/hyeongryeol_workspace/festivals_master.json'
    clean_master_json(path)
