import json
import os
import re
from datetime import datetime

WORKSPACE = "/home/aiagent/hyeongryeol_workspace"
STATUS_FILE = os.path.join(WORKSPACE, "PROJECT_STATUS.md")
RAW_DATA_FILE = os.path.join(WORKSPACE, "festival_engine/data/raw/raw_festivals.json")
PROCESSED_DATA_FILE = os.path.join(WORKSPACE, "festival_engine/data/processed/processed_festivals.json")
OUTPUT_JSON = os.path.join(WORKSPACE, "web/status.json")

def read_file_builtin(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_maturity(text):
    match = re.search(r"Overall Project Maturity: (\d+)%", text)
    return int(match.group(1)) if match else 0

def extract_phase(text):
    match = re.search(r"Current Phase: ([^\n\r]+)", text)
    return match.group(1).strip() if match else "Unknown"

def extract_teams(text):
    teams = []
    sections = re.split(r"### \[Team", text)
    for section in sections[1:]:
        lines = section.split('\n')
        name = lines[0].split(']')[0] + ']'
        status_line = next((l for l in lines if "- **Status:**" in l), "")
        status_text = status_line.replace("- **Status:**", "").strip()
        status_icon = status_text[0] if status_text else '⚪'
        status_name = status_text[1:].strip() if status_text else "Unknown"
        prog_line = next((l for l in lines if "- **Progress:**" in l), "")
        prog_val = re.search(r"(\d+)%", prog_line)
        prog_val = int(prog_val.group(1)) if prog_val else 0
        block_line = next((l for l in lines if "- **Blockers:**" in l), "")
        blocker = block_line.replace("- **Blockers:**", "").strip()
        teams.append({
            "name": name,
            "status_icon": status_icon,
            "status": status_name,
            "progress": prog_val,
            "blocker": blocker
        })
    return teams

def count_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return len(data) if isinstance(data, list) else 0
    except: return 0

def main():
    try:
        text = read_file_builtin(STATUS_FILE)
    except Exception as e:
        print(f"Error reading status file: {e}")
        return

    payload = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "overall_maturity": extract_maturity(text),
        "current_phase": extract_phase(text),
        "data_counts": {
            "raw": count_json(RAW_DATA_FILE),
            "processed": count_json(PROCESSED_DATA_FILE)
        },
        "teams": extract_teams(text)
    }

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully exported status to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
