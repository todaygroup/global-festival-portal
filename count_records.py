import json
def get_count(path):
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            return len(data) if isinstance(data, list) else 0
    except:
        return -1

print(f"RAW:{get_count('/home/aiagent/hyeongryeol_workspace/festival_engine/data/raw/raw_festivals.json')}")
print(f"PROCESSED:{get_count('/home/aiagent/hyeongryeol_workspace/festival_engine/data/raw/processed_festivals.json')}")
