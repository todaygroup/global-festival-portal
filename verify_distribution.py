import json
from datetime import datetime

schedule_path = "/home/aiagent/hyeongryeol_workspace/festival_engine/data/distribution/upload_schedule.json"

try:
    with open(schedule_path, "r", encoding="utf-8") as f:
        schedule = json.load(f)

    now = datetime.now()
    delays = []
    failures = []
    upcoming = []

    for job in schedule:
        scheduled_at = datetime.fromisoformat(job["scheduled_at"])
        status = job["status"]
        
        if status == "failed":
            failures.append(job)
        elif status == "scheduled" and scheduled_at < now:
            delays.append(job)
        elif status == "scheduled" and scheduled_at >= now:
            upcoming.append(job)

    print(f"--- Distribution Status Report ---")
    print(f"Current Time: {now.isoformat()}")
    print(f"Total Jobs in Schedule: {len(schedule)}")
    print(f"Upcoming Jobs: {len(upcoming)}")
    print(f"Delayed Jobs: {len(delays)}")
    print(f"Failed Jobs: {len(failures)}")

    if delays:
        print("\n[!] Delayed Jobs (Status: scheduled, but time has passed):")
        for j in delays:
            print(f"- {j['job_id']} | ID: {j['video_id']} | Scheduled: {j['scheduled_at']}")

    if failures:
        print("\n[X] Failed Jobs:")
        for j in failures:
            print(f"- {j['job_id']} | ID: {j['video_id']}")
            
    if not delays and not failures:
        print("\n✅ All planned uploads are on track.")

except Exception as e:
    print(f"Error during verification: {e}")
