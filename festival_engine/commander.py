import importlib
import os
import json
from typing import List, Dict, Any
from utils.monitor import monitor
from schema import FestivalData
from processor import AIProcessor
from script_gen import ScriptGenerator
from render_engine import RenderEngine
from distribution_manager import DistributionManager

class Commander:
    """
    The Chief Orchestrator (The Brain).
    Now supports Dynamic Global Expansion via expansion_map.json.
    """
    def __init__(self):
        self.workspace = "/home/aiagent/hyeongryeol_workspace/festival_engine"
        self.data_dir = os.path.join(self.workspace, "data")
        self.rules_path = os.path.join(self.workspace, "SYSTEM_RULES.md")
        self.arch_path = os.path.join(self.workspace, "SYSTEM_ARCHITECTURE.md")
        self.map_path = os.path.join(self.workspace, "expansion_map.json")
        
        # Initialize Teams
        self.processor = AIProcessor()
        self.script_gen = ScriptGenerator()
        self.renderer = RenderEngine()
        self.distributor = DistributionManager()

    def _load_rules(self) -> str:
        with open(self.rules_path, "r", encoding="utf-8") as f:
            return f.read()

    def _get_dynamic_providers(self) -> List:
        """
        Dynamically loads providers defined in expansion_map.json.
        """
        with open(self.map_path, "r", encoding="utf-8") as f:
            mapping = json.load(f)["provider_mapping"]
        
        providers = []
        for country, class_path in mapping.items():
            # Split 'providers.korea_provider.KoreaProvider'
            module_path, class_name = class_path.rsplit(".", 1)
            module = importlib.import_module(f"festival_engine.{module_path}")
            provider_class = getattr(module, class_name)
            providers.append(provider_class(country))
        
        return providers

    def _audit_quality(self, stage_name: str, data: Any, threshold: float = 0.7) -> bool:
        print(f"🔍 [Audit Team] Validating {stage_name} output...")
        if stage_name == "Processing":
            if not data or not any("viral_hooks" in item.get('rich_content', {}) for item in data):
                return False
        elif stage_name == "Scripting":
            if not data or len(data) == 0:
                return False
        return True

    def run_full_pipeline(self):
        with monitor.track("Full_Pipeline_Execution", estimated_tokens=15000):
            print("🚀 [Chief Orchestrator] Initializing Global Festival Pipeline...")
            
            # 1. Collection Phase (Dynamic Expansion)
            with monitor.track("Data_Collection", estimated_tokens=2000):
                providers = self._get_dynamic_providers()
                raw_data = []
                for p in providers:
                    print(f"📦 Fetching data from {p.country}...")
                    raw_data.extend(p.fetch_festivals())
                print(f"✅ Collected {len(raw_data)} festivals from {len(providers)} countries.")

            # 2. Processing Phase
            with monitor.track("AI_Processing", estimated_tokens=5000):
                processed_data = self.processor.translate_and_optimize([f.to_dict() for f in raw_data])
                if not self._audit_quality("Processing", processed_data):
                    return False
                print("✅ Data enriched with Viral Hooks.")

            # 3. Scripting Phase
            with monitor.track("Script_Generation", estimated_tokens=4000):
                scripts = self.script_gen.generate_viral_scripts(processed_data)
                if not self._audit_quality("Scripting", scripts):
                    return False
                print("✅ Viral scripts generated.")

            # 4. Rendering Phase
            with monitor.track("Content_Rendering", estimated_tokens=3000):
                assets = self.renderer.render_assets(scripts)
                print(f"✅ {len(assets)} video assets rendered.")

            # 5. Distribution Planning
            with monitor.track("Distribution_Scheduling", estimated_tokens=1000):
                self.distributor.schedule_uploads(assets)
                print("✅ Distribution schedule updated.")

            print("\n🎊 [Chief Orchestrator] Pipeline completed successfully.")
            return True

if __name__ == "__main__":
    commander = Commander()
    commander.run_full_pipeline()
