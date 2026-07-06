import json
import os
from typing import List
from schema import FestivalData, BasicInfo, DateInfo, RichContent, MediaAsset, MediaAssets

class AIProcessor:
    """
    Simulates the AI Intelligence Layer.
    In production, this would call LLM APIs (GPT, Claude, etc.) 
    to perform translation and viral point extraction.
    """
    
    def __init__(self):
        self.processed_dir = "/home/aiagent/hyeongryeol_workspace/festival_engine/data/processed"
        os.makedirs(self.processed_dir, exist_ok=True)

    def translate_and_optimize(self, raw_data: list) -> list:
        print("🧠 AI Layer: Starting Translation and Viral Point Extraction...")
        processed_data = []
        
        for item in raw_data:
            # 1. Simulated Translation (Real AI would do this)
            name_ko = self._mock_translate(item['basic_info']['name_en'], "name")
            desc_ko = self._mock_translate(item['rich_content']['description_en'], "desc")
            
            # 2. Viral Point Extraction
            # Converting boring descriptions into "Viral Hooks" for short-form videos
            viral_hooks = self._generate_viral_hooks(
                item['basic_info']['name_en'], 
                item['rich_content']['highlights']
            )
            
            # Update the data structure
            item['basic_info']['name_ko'] = name_ko
            item['rich_content']['description_ko'] = desc_ko
            item['rich_content']['viral_hooks'] = viral_hooks
            
            processed_data.append(item)
            print(f"✨ Optimized: {name_ko}")
            
        return processed_data

    def _mock_translate(self, text: str, mode: str) -> str:
        # Simple mapping for demo; real AI layer would use a Translation Model
        translations = {
            "Sapporo Snow Festival": "삿포로 눈축제",
            "Aomori Nebuta Matsuri": "아오모리 네부타 축제",
            "One of the most famous winter festivals in Japan, featuring massive snow and ice sculptures.": "거대한 설상과 얼음 조각이 펼쳐지는 일본 최고의 겨울 축제입니다.",
            "A festival featuring enormous illuminated floats depicting mythical creatures and historical figures.": "신화 속 생물과 역사적 인물을 묘사한 거대한 빛의 등불 행렬이 장관을 이루는 축제입니다."
        }
        return translations.get(text, f"[Translated] {text}")

    def _generate_viral_hooks(self, name: str, highlights: List[str]) -> List[str]:
        # Upgraded Viral Engineering: Trigger-based Blueprint System
        # Instead of simple matching, it applies psychological triggers to each highlight.
        
        blueprints = {
            "curiosity": "🤫 {hl} $\\rightarrow$ 아무도 알려주지 않은 {name}의 비밀, 여기서만 공개합니다.",
            "fomo": "⏰ {hl} $\\rightarrow$ 일 년에 딱 한 번! 지금 안 가면 내년까지 기다려야 하는 역대급 포인트.",
            "authority": "🌍 {hl} $\\rightarrow$ 전 세계 여행자들이 입을 모아 극찬한 {name} 최고의 순간!",
            "contrast": "✨ {hl} $\\rightarrow$ 그냥 축제라고 생각했다면 오산, 상상을 초월하는 스케일의 정체는?",
        }
        
        hooks = []
        # Distribute different triggers across highlights for diversity
        trigger_keys = list(blueprints.keys())
        for i, hl in enumerate(highlights):
            trigger_key = trigger_keys[i % len(trigger_keys)]
            blueprint = blueprints[trigger_key]
            hooks.append(blueprint.format(hl=hl, name=name))
            
        return hooks

    def save_processed(self, data: list):
        filename = os.path.join(self.processed_dir, "processed_festivals.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 All processed data saved to {filename}")

if __name__ == "__main__":
    # Load raw data
    raw_path = "/home/aiagent/hyeongryeol_workspace/festival_engine/data/raw/raw_festivals.json"
    if not os.path.exists(raw_path):
        print("❌ Raw data not found. Please run the collector first.")
        exit(1)
        
    with open(raw_path, "r", encoding="utf-8") as f:
        raw_festivals = json.load(f)
    
    processor = AIProcessor()
    processed_festivals = processor.translate_and_optimize(raw_festivals)
    processor.save_processed(processed_festivals)
