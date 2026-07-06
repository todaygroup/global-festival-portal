import json
import os
from typing import List, Dict
from enum import Enum

class ContentFormat(Enum):
    TOP_N = "Top_N"
    HIDDEN_GEM = "Hidden_Gem"
    TRAVEL_GUIDE = "Travel_Guide"

class ScriptGenerator:
    """
    Viral Script Engine. 
    Transforms processed data into high-retention scripts for short-form videos.
    """
    
    def __init__(self):
        self.templates = {
            ContentFormat.TOP_N: self._template_top_n,
            ContentFormat.HIDDEN_GEM: self._template_hidden_gem,
            ContentFormat.TRAVEL_GUIDE: self._template_travel_guide
        }

    def generate_script(self, festival: Dict, format: ContentFormat) -> Dict:
        """
        Generates a single script for a specific festival and format.
        """
        print(f"✍️ Generating script for {festival['basic_info']['name_ko']} in {format.value} format...")
        return self.templates[format](festival)

    def generate_viral_scripts(self, processed_festivals: List[Dict]) -> List[Dict]:
        """
        Batch process festivals into various viral formats.
        Integrates with the GrowthOptimizer's strategy weights.
        """
        all_scripts = []
        formats_to_generate = [ContentFormat.TOP_N, ContentFormat.HIDDEN_GEM, ContentFormat.TRAVEL_GUIDE]
        
        for fest in processed_festivals:
            for fmt in formats_to_generate:
                script = self.generate_script(fest, fmt)
                all_scripts.append({
                    "festival": fest['basic_info']['name_ko'],
                    "format": fmt.value,
                    "blueprint": script
                })
        return all_scripts

    def _template_top_n(self, fest: Dict) -> Dict:
        return {
            "scenes": [
                {"time": "0-3s", "text": f"🌟 전 세계가 주목하는 레전드 축제 TOP 3! 과연 {fest['basic_info']['name_ko']}는 몇 위일까요?", "visual": "Fast cuts of festival highlights"},
                {"time": "3-10s", "text": f"여기가 바로 {fest['basic_info']['city']}의 {fest['basic_info']['name_ko']}! {fest['rich_content']['viral_hooks'][0]}", "visual": "Main wide shot of the festival"},
                {"time": "10-15s", "text": f"특히 {fest['rich_content']['viral_hooks'][1]} 부분은 절대 놓치지 마세요!", "visual": "Close up of the most unique activity"},
                {"time": "15-20s", "text": f"더 많은 글로벌 축제 꿀팁이 궁금하다면? 지금 바로 프로필 링크의 앱을 확인하세요!", "visual": "App UI call to action"}
            ]
        }

    def _template_hidden_gem(self, fest: Dict) -> Dict:
        return {
            "scenes": [
                {"time": "0-3s", "text": f"🤫 나만 알고 싶었지만... 공개합니다. {fest['basic_info']['city']}의 숨은 보석, {fest['basic_info']['name_ko']}!", "visual": "Mysterious atmospheric shot"},
                {"time": "3-10s", "text": f"이곳의 진짜 매력은 바로 {fest['rich_content']['viral_hooks'][2]}입니다. 뻔한 관광지는 이제 그만!", "visual": "Unique/rare angle of the festival"},
                {"time": "10-15s", "text": f"인생샷 100% 보장! 올해가 가기 전에 여기 꼭 가보세요.", "visual": "Beautiful aesthetic shot"},
                {"time": "15-20s", "text": f"상세 일정과 예약 방법은 앱에서 바로 확인 가능합니다!", "visual": "App download screen"}
            ]
        }

    def _template_travel_guide(self, fest: Dict) -> Dict:
        return {
            "scenes": [
                {"time": "0-3s", "text": f"✈️ {fest['basic_info']['name_ko']} 가기 전 필수 시청! 실패 없는 여행 꿀팁 알려드립니다.", "visual": "Travel preparation / Map shot"},
                {"time": "3-10s", "text": f"핵심 포인트는 {fest['rich_content']['viral_hooks'][0]}! 이걸 알아야 진짜 즐길 수 있습니다.", "visual": "Helpful tip visual / Activity shot"},
                {"time": "10-15s", "text": f"추천 방문 시기는 {fest['basic_info']['date']['start_date']}부터! 늦으면 자리 없습니다.", "visual": "Calendar/Crowd shot"},
                {"time": "15-20s", "text": f"더 자세한 가이드와 리워드 혜택은 앱에서 확인하세요!", "visual": "App reward screen"}
            ]
        }
