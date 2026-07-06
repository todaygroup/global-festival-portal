import json
import os
from script_gen import ScriptGenerator, ContentFormat

class CreativeDirector:
    """
    Orchestrates the process of turning data into a production-ready content plan.
    """
    
    def __init__(self):
        self.generator = ScriptGenerator()
        self.output_dir = "/home/aiagent/hyeongryeol_workspace/festival_engine/data/scripts"
        os.makedirs(self.output_dir, exist_ok=True)

    def produce_content_plans(self, processed_data: list):
        print("🎬 Creative Director: Starting production of viral scripts...")
        all_scripts = []
        
        for fest in processed_data:
            # For each festival, we can generate scripts in all 3 formats to see which one performs best (A/B testing strategy)
            for fmt in ContentFormat:
                script = self.generator.generate_script(fest, fmt)
                script_id = f"{fest['festival_id']}_{fmt.value}"
                
                plan = {
                    "script_id": script_id,
                    "festival_name": fest['basic_info']['name_ko'],
                    "format": fmt.value,
                    "content": script
                }
                all_scripts.append(plan)
        
        # Save script plans
        filename = os.path.join(self.output_dir, "viral_scripts.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(all_scripts, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Total {len(all_scripts)} viral scripts generated and saved to {filename}")
        return all_scripts

if __name__ == "__main__":
    # Load processed data
    input_path = "/home/aiagent/hyeongryeol_workspace/festival_engine/data/processed/processed_festivals.json"
    if not os.path.exists(input_path):
        print("❌ Processed data not found. Please run the processor first.")
        exit(1)
        
    with open(input_path, "r", encoding="utf-8") as f:
        processed_festivals = json.load(f)
    
    director = CreativeDirector()
    director.produce_content_plans(processed_festivals)
