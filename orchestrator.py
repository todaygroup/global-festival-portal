import json
import subprocess
import os

COUNTRIES = {
    "East Asia": {
        "CN": "China", "JP": "Japan", "KR": "South Korea", "KP": "North Korea", "MN": "Mongolia", "TW": "Taiwan", "HK": "Hong Kong", "MO": "Macau"
    },
    "South Asia": {
        "IN": "India", "PK": "Pakistan", "BD": "Bangladesh", "LK": "Sri Lanka", "NP": "Nepal", "BT": "Bhutan", "MV": "Maldives"
    },
    "South East Asia": {
        "TH": "Thailand", "VN": "Vietnam", "MY": "Malaysia", "ID": "Indonesia", "PH": "Philippines", "SG": "Singapore", "MM": "Myanmar", "KH": "Cambodia", "LA": "Laos", "BN": "Brunei", "TL": "Timor-Leste"
    },
    "Oceania": {
        "AU": "Australia", "NZ": "New Zealand", "PG": "Papua New Guinea", "FJ": "Fiji", "SB": "Solomon Islands", "VU": "Vanuatu", "WS": "Samoa", "KI": "Kiribati", "TO": "Tonga", "FM": "Micronesia", "PW": "Palau", "MH": "Marshall Islands"
    }
}

def run_collector(code, name):
    print(f"Starting collection for {name} ({code})...")
    cmd = ["python3", "/home/aiagent/hyeongryeol_workspace/festivals_collector.py", code, name]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

def main():
    total_records = 0
    processed_countries = 0
    
    for region, countries in COUNTRIES.items():
        print(f"--- Processing Region: {region} ---")
        for code, name in countries.items():
            output = run_collector(code, name)
            print(output)
            
            # Try to extract record count from output
            if "records saved" in output:
                try:
                    count = int(output.split("records saved")[0].split()[-1])
                    total_records += count
                except:
                    pass
            processed_countries += 1
            
    print(f"\nFINAL SUMMARY\nTotal countries processed: {processed_countries}\nTotal records saved: {total_records}")

if __name__ == "__main__":
    main()
