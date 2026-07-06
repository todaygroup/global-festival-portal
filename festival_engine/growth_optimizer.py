import json
import os
import random
from typing import List, Dict

class GrowthOptimizer:
    """
    Growth & Evolution Optimizer.
    The "Brain" that analyzes performance and evolves the system's strategies.
    """
    
    def __init__(self):
        self.performance_log_path = "/home/aiagent/hyeongryeol_workspace/festival_engine/data/analytics/performance_logs.json"
        self.strategy_path = "/home/aiagent/hyeongryeol_workspace/festival_engine/data/strategy/active_strategy.json"
        os.makedirs(os.path.dirname(self.performance_log_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.strategy_path), exist_ok=True)
        self._init_strategy()

    def _init_strategy(self):
        # Initial strategy: Equal weight to all formats
        initial_strategy = {
            "format_weights": {
                "Top_N": 0.33,
                "Hidden_Gem": 0.33,
                "Travel_Guide": 0.34
            },
            "top_performing_keywords": [],
            "version": 1.0
        }
        with open(self.strategy_path, "w", encoding="utf-8") as f:
            json.dump(initial_strategy, f, indent=2)

    def collect_performance_data(self, manifest: List[Dict]):
        """
        Simulates collecting data from SNS APIs (Views, CTR, Conversion to App).
        """
        print("📊 Growth Optimizer: Collecting performance data from SNS...")
        logs = []
        for item in manifest:
            # Mocking analytics: Randomly assign performance scores
            # In production, this comes from YouTube/TikTok API
            views = random.randint(1000, 100000)
            ctr = random.uniform(0.01, 0.08)
            conversions = int(views * ctr * random.uniform(0.5, 1.5))
            
            logs.append({
                "video_id": item['video_id'],
                "festival": item['festival'],
                "format": item['format'],
                "metrics": {
                    "views": views,
                    "ctr": ctr,
                    "conversions": conversions,
                    "score": (views * ctr) / 100 # Simple efficiency score
                }
            })
        
        with open(self.performance_log_path, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
        return logs

    def evolve_strategy(self):
        """
        Analyzes logs and updates the strategy for the next production cycle.
        """
        print("🧬 Growth Optimizer: Analyzing patterns and evolving strategy...")
        if not os.path.exists(self.performance_log_path):
            return {"status": "no_data"}

        with open(self.performance_log_path, "r", encoding="utf-8") as f:
            logs = json.load(f)

        # Calculate average score per format
        format_scores = {}
        for log in logs:
            fmt = log['format']
            score = log['metrics']['score']
            format_scores[fmt] = format_scores.get(fmt, []) + [score]

        avg_scores = {fmt: sum(s)/len(s) for fmt, s in format_scores.items()}
        
        # Update weights based on performance (Softmax-like re-weighting)
        total_score = sum(avg_scores.values())
        new_weights = {fmt: s/total_score for fmt, s in avg_scores.items()}
        
        # Find top performing keyword (Mock)
        top_keyword = "Epic Scale" if avg_scores.get("Top_N", 0) > 0.5 else "Hidden Gem"

        updated_strategy = {
            "format_weights": new_weights,
            "top_performing_keywords": [top_keyword],
            "version": os.path.getmtime(self.strategy_path) # simplified versioning
        }
        
        with open(self.strategy_path, "w", encoding="utf-8") as f:
            json.dump(updated_strategy, f, indent=2)
            
        print(f"✅ Strategy Evolved! New Weights: {new_weights}")
        return updated_strategy

if __name__ == "__main__":
    # This would be part of the master orchestrator
    optimizer = GrowthOptimizer()
    
    # Load existing manifest to simulate tracking
    manifest_path = "/home/aiagent/hyeongryeol_workspace/festival_engine/data/final_assets/content_manifest.json"
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
            optimizer.collect_performance_data(manifest)
            optimizer.evolve_strategy()
    else:
        print("❌ No manifest found to optimize.")
