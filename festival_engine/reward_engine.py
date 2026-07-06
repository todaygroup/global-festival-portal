import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Optional

class RewardEngine:
    """
    AppTech Reward Engine.
    Manages user points, missions, and rewards to ensure high retention.
    """
    
    def __init__(self):
        self.db_path = "/home/aiagent/hyeongryeol_workspace/festival_engine/data/platform/user_db.json"
        self.mission_path = "/home/aiagent/hyeongryeol_workspace/festival_engine/data/platform/missions.json"
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_missions()

    def _init_missions(self):
        # Standard app-tech missions
        default_missions = [
            {"id": "M1", "title": "Daily Festival View", "action": "VIEW_VIDEO", "reward": 10, "limit": "daily"},
            {"id": "M2", "title": "Save My Dream Festival", "action": "SAVE_FESTIVAL", "reward": 50, "limit": "once"},
            {"id": "M3", "title": "Invite a Friend", "action": "SHARE_LINK", "reward": 100, "limit": "per_user"},
            {"id": "M4", "title": "Complete Festival Quiz", "action": "QUIZ_COMPLETE", "reward": 30, "limit": "daily"}
        ]
        with open(self.mission_path, "w", encoding="utf-8") as f:
            json.dump(default_missions, f, indent=2)

    def create_user(self, user_id: str, name: str) -> Dict:
        users = self._load_users()
        if user_id not in users:
            users[user_id] = {
                "name": name,
                "points": 0,
                "joined_at": datetime.now().isoformat(),
                "completed_missions": []
            }
            self._save_users(users)
        return users[user_id]

    def process_action(self, user_id: str, action_type: str, metadata: Dict = None) -> Dict:
        """
        Processes a user action and rewards points if a mission is matched.
        """
        users = self._load_users()
        missions = self._load_missions()
        
        if user_id not in users:
            return {"status": "error", "message": "User not found"}
        
        # Find matching mission
        mission = next((m for m in missions if m['action'] == action_type), None)
        if not mission:
            return {"status": "ignored", "message": "No reward associated with this action"}

        # Check if mission is already completed (for 'once' type)
        if mission['limit'] == "once" and mission['id'] in users[user_id]['completed_missions']:
            return {"status": "already_completed", "message": "Reward already claimed for this mission"}

        # Award points
        reward = mission['reward']
        users[user_id]['points'] += reward
        if mission['limit'] == "once":
            users[user_id]['completed_missions'].append(mission['id'])
        
        self._save_users(users)
        
        return {
            "status": "success",
            "rewarded_points": reward,
            "total_points": users[user_id]['points'],
            "message": f"Mission '{mission['title']}' completed! {reward} points added."
        }

    def _load_users(self) -> Dict:
        if not os.path.exists(self.db_path): return {}
        with open(self.db_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_users(self, users: Dict):
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2)

    def _load_missions(self) -> List[Dict]:
        with open(self.mission_path, "r", encoding="utf-8") as f:
            return json.load(f)

if __name__ == "__main__":
    engine = RewardEngine()
    
    # Simulation: User Journey
    uid = "user_001"
    engine.create_user(uid, "Hyeongryeol")
    
    print("User Activity Simulation...")
    # Action 1: User enters from SNS (Watch video)
    res1 = engine.process_action(uid, "VIEW_VIDEO")
    print(f"Action 1: {res1['message']} | Current Points: {res1['total_points']}")
    
    # Action 2: User saves a festival (Hidden Gem)
    res2 = engine.process_action(uid, "SAVE_FESTIVAL")
    print(f"Action 2: {res2['message']} | Current Points: {res2['total_points']}")
    
    # Action 3: User tries to save again (Once limit test)
    res3 = engine.process_action(uid, "SAVE_FESTIVAL")
    print(f"Action 3: {res3['message']}")
    
    # Action 4: User refers a friend
    res4 = engine.process_action(uid, "SHARE_LINK")
    print(f"Action 4: {res4['message']} | Final Points: {res4['total_points']}")
