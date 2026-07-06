import json
import os
from typing import List, Dict

class VisualDirector:
    """
    Visual Director Agent.
    Matches script visual cues to actual assets and generates AI prompts for missing visuals.
    """
    
    def __init__(self, processed_data_path: str):
        self.processed_data_path = processed_data_path
        self.festivals_db = self._load_db()

    def _load_db(self) -> Dict:
        with open(self.processed_data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {fest['festival_id']: fest for fest in data}

    def generate_visual_blueprint(self, script: Dict) -> Dict:
        fest_id = script['festival_id']
        fest = self.festivals_db.get(fest_id)
        
        if not fest:
            return {"error": "Festival not found in DB"}

        blueprint = []
        for scene in script['scenes']:
            visual_cue = scene['visual']
            
            # 1. Try to match with existing assets
            asset = self._match_asset(visual_cue, fest['media_assets'])
            
            if asset:
                final_visual = {"type": "existing_asset", "url": asset['url'], "meta": asset['tag']}
            else:
                # 2. If no asset, generate a high-fidelity AI Prompt for Generation (Runway/Midjourney/Pika)
                final_visual = {
                    "type": "ai_generated",
                    "prompt": self._generate_ai_prompt(visual_cue, fest),
                    "suggested_tool": "Runway Gen-2 / Luma Dream Machine"
                }
            
            blueprint.append({
                "time": scene['time'],
                "text": scene['text'],
                "visual": final_visual
            })
            
        return blueprint

    def _match_asset(self, cue: str, assets: Dict) -> Dict:
        # Simple keyword matching for prototype
        cue_lower = cue.lower()
        for img in assets['images']:
            if img['tag'].lower() in cue_lower:
                return img
        return None

    def _generate_ai_prompt(self, cue: str, fest: Dict) -> str:
        # Prompt Engineering: Transform "Main wide shot" -> "Cinematic 4k drone shot of [Festival Name]..."
        fest_name = fest['basic_info']['name_en']
        city = fest['basic_info']['city']
        
        prompt = f"Cinematic 4k, highly detailed, drone footage of {fest_name} in {city}, "
        if "wide shot" in cue.lower():
            prompt += "establishing shot, panoramic view, epic scale, professional color grading"
        elif "close up" in cue.lower():
            prompt += "extreme close-up, slow motion, capturing emotional expressions, vivid textures"
        elif "atmospheric" in cue.lower() or "mysterious" in cue.lower():
            prompt += "moody lighting, ethereal atmosphere, fog, sunset, cinematic lighting"
        else:
            prompt += "dynamic movement, vibrant colors, high energy, travel vlog style"
            
        return prompt

if __name__ == "__main__":
    # Load scripts
    scripts_path = "/home/aiagent/hyeongryeol_workspace/festival_engine/data/scripts/viral_scripts.json"
    processed_path = "/home/aiagent/hyeongryeol_workspace/festival_engine/data/processed/processed_festivals.json"
    
    with open(scripts_path, "r", encoding="utf-8") as f:
        scripts = json.load(f)
        
    director = VisualDirector(processed_path)
    production_blueprints = []
    
    for s in scripts:
        # Re-structuring script for the director
        fest_id = s['script_id'].split('_')[0]
        script_content = s['content']
        
        blueprint = director.generate_visual_blueprint({
            "festival_id": fest_id,
            "scenes": script_content['scenes']
        })
        
        production_blueprints.append({
            "script_id": s['script_id'],
            "festival": s['festival_name'],
            "format": s['format'],
            "blueprint": blueprint
        })
        
    # Save final production blueprint
    output_path = "/home/aiagent/hyeongryeol_workspace/festival_engine/data/blueprints/production_blueprints.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(production_blueprints, f, indent=2, ensure_ascii=False)
        
    print(f"🎬 Visual Director: Production blueprints generated for {len(production_blueprints)} scripts.")
