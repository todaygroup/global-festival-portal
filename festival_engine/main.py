import os
import json
from typing import List
from providers.japan_provider import JapanProvider
from providers.europe_provider import EuropeProvider
from festival_engine.schema import FestivalData

class Collector:
    def __init__(self, providers: List):
        self.providers = providers
        self.output_dir = "/home/aiagent/hyeongryeol_workspace/festival_engine/data/raw"
        os.makedirs(self.output_dir, exist_ok=True)

    def run(self):
        all_festivals = []
        print("🚀 Starting The Collector (Production Mode)...")
        
        for provider in self.providers:
            print(f"📦 Fetching real data from {provider.country} provider...")
            data = provider.fetch_festivals()
            all_festivals.extend(data)
            
        # Save raw data for audit
        filename = os.path.join(self.output_dir, "raw_festivals.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([f.to_dict() for f in all_festivals], f, indent=2, ensure_ascii=False)
            
        print(f"✅ Successfully collected {len(all_festivals)} festivals. Saved to {filename}")
        return all_festivals

if __name__ == "__main__":
    # Now using the real JapanProvider
    providers_to_use = [
        JapanProvider("Japan"),
        EuropeProvider("Europe")
    ]
    
    collector = Collector(providers_to_use)
    collector.run()
