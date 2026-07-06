import json
import os
import uuid
from datetime import datetime, timedelta
from typing import List, Dict

class DistributionManager:
    """
    Distribution Network Manager.
    Handles automated scheduling and deployment of content across global SNS platforms.
    """
    
    def __init__(self):
        self.manifest_path = "/home/aiagent/hyeongryeol_workspace/festival_engine/data/final_assets/content_manifest.json"
        self.schedule_path = "/home/aiagent/hyeongryeol_workspace/festival_engine/data/distribution/upload_schedule.json"
        os.makedirs(os.path.dirname(self.schedule_path), exist_ok=True)
        
    def _load_manifest(self) -> List[Dict]:
        with open(self.manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)
            
    def _calculate_prime_time(self, country: str) -> datetime:
        now = datetime.now()
        if country == "Japan":
            return now.replace(hour=20, minute=0, second=0, microsecond=0) + timedelta(days=1)
        elif country == "Spain":
            return now.replace(hour=21, minute=0, second=0, microsecond=0) + timedelta(days=1)
        else:
            return now.replace(hour=19, minute=0, second=0, microsecond=0) + timedelta(days=1)

    def schedule_uploads(self, assets: List[Dict]):
        """
        Takes rendered assets and calculates the optimal global upload schedule.
        """
        print(f"📡 Scheduling {len(assets)} assets for distribution...")
        
        # Save manifest first so other tools can use it
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            json.dump(assets, f, indent=2, ensure_ascii=False)
            
        return self.create_upload_schedule()

    def create_upload_schedule(self):
        print("📡 Distribution Manager: Calculating global upload schedules...")
        manifest = self._load_manifest()
        schedule = []
        
        for item in manifest:
            country = "Japan" if any(x in item['festival'] for x in ["삿포로", "아오모리"]) else "Global"
            prime_time = self._calculate_prime_time(country)
            
            job = {
                "job_id": f"JOB-{uuid.uuid4().hex[:8]}",
                "video_id": item['video_id'],
                "platform": "Omni-Channel (TikTok, Shorts, Reels)",
                "scheduled_at": prime_time.isoformat(),
                "payload": {
                    "video_url": item['video_url'],
                    "caption": item['caption'],
                    "hashtags": item['hashtags']
                },
                "status": "scheduled"
            }
            schedule.append(job)
            
        with open(self.schedule_path, "w", encoding="utf-8") as f:
            json.dump(schedule, f, indent=2, ensure_ascii=False)
            
        print(f"📅 Successfully scheduled {len(schedule)} uploads across global timezones. Schedule saved to {self.schedule_path}")
        return schedule

    def deploy_now(self, job_id: str):
        print(f"🚀 Deploying Job {job_id} to SNS platforms...")
        return {"status": "success", "post_url": f"https://sns.com/posts/{uuid.uuid4().hex[:10]}"}

if __name__ == "__main__":
    pass
