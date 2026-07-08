import importlib
import os
import json
from typing import List, Dict, Any, Tuple
from festival_engine.utils.monitor import monitor
from festival_engine.schema import FestivalData
from festival_engine.processor import AIProcessor
from festival_engine.script_gen import ScriptGenerator
from festival_engine.render_engine import RenderEngine
from festival_engine.distribution_manager import DistributionManager

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

    def _audit_quality(self, stage_name: str, data: Any, threshold: float = 0.7) -> Tuple[bool, float, str]:
        print(f"🔍 [Audit Team] Validating {stage_name} output...")
        from festival_engine.quality import QualityAuditor
        auditor = QualityAuditor(threshold=threshold)
        
        if stage_name == "Processing":
            return auditor.audit_processing(data)
        elif stage_name == "Scripting":
            return auditor.audit_scripting(data)
        
        return True, 1.0, "No auditor for this stage"

    def run_full_pipeline(self):
        with monitor.track("Full_Pipeline_Execution", estimated_tokens=15000):
            print("🚀 [Chief Orchestrator] Initializing Global Festival Pipeline with Validation Loops...")
            
            # 1. Collection Phase
            with monitor.track("Data_Collection", estimated_tokens=2000):
                providers = self._get_dynamic_providers()
                raw_data = []
                for p in providers:
                    print(f"📦 Fetching data from {p.country}...")
                    raw_data.extend(p.fetch_festivals())
                print(f"✅ Collected {len(raw_data)} festivals from {len(providers)} countries.")

            # 2. Processing Phase with Validation Loop
            max_retries = 3
            for attempt in range(1, max_retries + 1):
                with monitor.track(f"AI_Processing_Attempt_{attempt}", estimated_tokens=5000):
                    processed_data = self.processor.translate_and_optimize(raw_data)
                    success, score, reason = self._audit_quality("Processing", processed_data)
                    if success:
                        print(f"✅ Data enriched. Quality Score: {score:.2f}")
                        break
                    else:
                        print(f"⚠️ [Audit Failure] Attempt {attempt}/{max_retries} - Score: {score:.2f}. Reason: {reason}")
                        if attempt == max_retries: 
                            print("❌ Critical Quality Failure in Processing. Aborting.")
                            return False
            else:
                return False

            # 3. Scripting Phase with Validation Loop
            for attempt in range(1, max_retries + 1):
                with monitor.track(f"Script_Generation_Attempt_{attempt}", estimated_tokens=4000):
                    scripts = self.script_gen.generate_viral_scripts(processed_data)
                    success, score, reason = self._audit_quality("Scripting", scripts)
                    if success:
                        print(f"✅ Viral scripts generated. Quality Score: {score:.2f}")
                        break
                    else:
                        print(f"⚠️ [Audit Failure] Attempt {attempt}/{max_retries} - Score: {score:.2f}. Reason: {reason}")
                        if attempt == max_retries:
                            print("❌ Critical Quality Failure in Scripting. Aborting.")
                            return False
            else:
                return False

            # 4. Rendering Phase
            with monitor.track("Content_Rendering", estimated_tokens=3000):
                assets = self.renderer.render_assets(scripts)
                print(f"✅ {len(assets)} video assets rendered.")

            # 5. Distribution Planning
            with monitor.track("Distribution_Scheduling", estimated_tokens=1000):
                self.distributor.schedule_uploads(assets)
                print("✅ Distribution schedule updated.")

            print("\\n🎊 [Chief Orchestrator] Pipeline completed successfully with high-quality assets.")
            return True

if __name__ == "__main__":
    commander = Commander()
    commander.run_full_pipeline()
