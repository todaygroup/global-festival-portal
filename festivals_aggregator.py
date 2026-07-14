import json
import os
import glob
from datetime import datetime

class FestaDataAggregator:
    def __init__(self, base_workspace="/home/aiagent/hyeongryeol_workspace"):
        self.base_workspace = base_workspace
        self.db_path = os.path.join(base_workspace, "festa_global_db")
        self.output_file = os.path.join(base_workspace, "festivals_master.json")

    def aggregate(self):
        print(f"Starting aggregation from {self.db_path}...")
        all_festivals = []
        processed_count = 0
        
        # Search for all *_sds.json files recursively
        search_pattern = os.path.join(self.db_path, "**", "*_sds.json")
        files = glob.glob(search_pattern, recursive=True)
        
        print(f"Found {len(files)} SDS files. Processing...")

        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    all_festivals.append(data)
                    processed_count += 1
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

        # Save the aggregated data to a master file
        output_data = {
            "metadata": {
                "last_aggregated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_records": len(all_festivals),
                "source_path": self.db_path
            },
            "festivals": all_festivals
        }

        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        print(f"Aggregation complete!")
        print(f"Total records aggregated: {processed_count}")
        print(f"Master file saved to: {self.output_file}")
        
        return processed_count

if __name__ == "__main__":
    aggregator = FestaDataAggregator()
    count = aggregator.aggregate()
    print(f"Successfully integrated {count} festival records into the master database.")
