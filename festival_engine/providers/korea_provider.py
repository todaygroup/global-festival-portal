import uuid
from typing import List
from schema import FestivalData, BasicInfo, DateInfo, RichContent, MediaAsset, MediaAssets
from .base_provider import BaseProvider

class KoreaProvider(BaseProvider):
    """
    Provider for Korean Tourism Data.
    Ensures the home market is fully integrated and optimized.
    """
    
    def fetch_festivals(self) -> List[FestivalData]:
        # Raw data for Korean festivals
        raw_captured_data = [
            {
                "name": "Boryeong Mud Festival",
                "local_name": "보령 머드 축제",
                "city": "Boryeong",
                "region": "Chungcheongnam-do",
                "dates": "July",
                "desc": "A worldwide famous festival where participants enjoy the therapeutic properties of mud through various activities.",
                "key_points": ["Mud Slidings", "Mud Wrestling", "Nightly Music Parties"],
                "url": "https://www.mudfestival.or.kr"
            },
            {
                "name": "Andong Mask Dance Festival",
                "local_name": "안동 국제 탈춤 페스티벌",
                "city": "Andong",
                "region": "Gyeongsangbuk-do",
                "dates": "September/October",
                "desc": "A celebration of traditional Korean mask dances, showcasing the artistic and satirical nature of Korean culture.",
                "key_points": ["Traditional Mask Performances", "Interactive Dance Workshops", "Historical Village Tours"],
                "url": "https://www.maskdance.com"
            },
            {
                "name": "Jeju Fire Festival",
                "local_name": "제주 들불 축제",
                "city": "Jeju",
                "region": "Jeju-do",
                "dates": "March",
                "desc": "A spectacular event where a mountain is set ablaze to pray for a good harvest and ward off evil spirits.",
                "key_points": ["Massive Fire Ritual", "Jeju Local Food Market", "Island Landscape Views"],
                "url": "https://www.jeju.go.kr"
            }
        ]
        
        normalized_results = []
        for item in raw_captured_data:
            f_id = f"KR-{uuid.uuid4().hex[:8]}"
            normalized_results.append(FestivalData(
                festival_id=f_id,
                basic_info=BasicInfo(
                    name_en=item["name"],
                    name_local=item["local_name"],
                    name_ko=item["local_name"],
                    country="Korea",
                    city=item["city"],
                    category="Cultural/Nature",
                    date=DateInfo(start_date=item["dates"], end_date=item["dates"])
                ),
                rich_content=RichContent(
                    description_en=item["desc"],
                    description_ko="AI-Translation-Pending",
                    highlights=item["key_points"],
                    official_url=item["url"]
                ),
                media_assets=MediaAssets(
                    images=[MediaAsset(f"https://cdn.example.com/kr/{f_id}.jpg", "main", "high")],
                    video_clips=[]
                ),
                metadata={"source": "KTO Official", "popularity_score": 9.7}
            ))
            
        return normalized_results
