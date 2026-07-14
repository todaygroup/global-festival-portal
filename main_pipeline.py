import subprocess
import sys
import os
from datetime import datetime

class FestaPipeline:
    def __init__(self):
        self.workspace = "/home/aiagent/hyeongryeol_workspace"
        self.collector_script = os.path.join(self.workspace, "festivals_collector.py")
        self.aggregator_script = os.path.join(self.workspace, "festivals_aggregator.py")

    def run_collector(self, country_code, country_name):
        print(f"--- Phase 1: Collecting data for {country_name} ({country_code}) ---")
        try:
            result = subprocess.run(
                ["python3", self.collector_script, country_code, country_name],
                capture_output=True, text=True, check=True
            )
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error during collection: {e.stderr}")
            return False
        return True

    def run_aggregator(self):
        print(f"--- Phase 2: Aggregating all collected data ---")
        try:
            result = subprocess.run(
                ["python3", self.aggregator_script],
                capture_output=True, text=True, check=True
            )
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error during aggregation: {e.stderr}")
            return False
        return True

    def execute_full_cycle(self, target_countries=None):
        """
        target_countries: List of (code, name) tuples. 
        If None, just runs aggregation to refresh master file.
        """
        start_time = datetime.now()
        print(f"Pipeline started at {start_time}")

        if target_countries:
            for code, name in target_countries:
                if not self.run_collector(code, name):
                    print(f"Skipping aggregation due to failure in {name}")
                    return False

        if self.run_aggregator():
            end_time = datetime.now()
            print(f"Pipeline successfully completed at {end_time}")
            print(f"Total duration: {end_time - start_time}")
            return True
        
        return False

if __name__ == "__main__":
    pipeline = FestaPipeline()
    
    # If arguments are provided, collect for those countries then aggregate
    # Usage: python main_pipeline.py US "United States" KR "South Korea"
    if len(sys.argv) > 1:
        countries = []
        for i in range(1, len(sys.argv), 2):
            if i + 1 < len(sys.argv):
                countries.append((sys.argv[i], sys.argv[i+1]))
        
        if countries:
            pipeline.execute_full_cycle(target_countries=countries)
        else:
            pipeline.run_aggregator()
    else:
        # Default: Just run aggregation to ensure master file is up to date
        pipeline.run_aggregator()
