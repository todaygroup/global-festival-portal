import uuid
from typing import List
from festival_engine.schema import FestivalData, BasicInfo, DateInfo, RichContent, MediaAsset, MediaAssets
from .base_provider import BaseProvider

class EuropeProvider(BaseProvider):
    """
    Provider for European Tourism Data.
    Expands the global reach of the Festival Portal.
    """
    
    def fetch_festivals(self) -> List[FestivalData]:
        # Raw data for European festivals
        raw_captured_data = [
            {
                "name": "Carnival of Venice",
                "local_name": "Carnevale di Venezia",
                "city": "Venice",
                "region": "Veneto",
                "dates": "February (dates vary)",
                "desc": "One of the most famous festivals in the world, known for its elaborate masks and costumes.",
                "key_points": ["Mysterious Masks", "Grand Canal Parades", "Historic Palaces"],
                "url": "https://www.carnevaledivenezia.it"
            },
            {
                "name": "Oktoberfest",
                "local_name": "Oktoberfest",
                "city": "Munich",
                "region": "Bavaria",
                "dates": "Late September to early October",
                "desc": "The world's largest folk festival, celebrating Bavarian culture and beer.",
                "key_points": ["Massive Beer Tents", "Traditional Dirndls and Lederhosen", "Fairground Rides"],
                "url": "https://www.oktoberfest.de"
            }
        ]
        
        normalized_results = []
        for item in raw_captured_data:
            f_id = f"EU-{uuid.uuid4().hex[:8]}"
            normalized_results.append(FestivalData(
                festival_id=f_id,
                basic_info=BasicInfo(
                    name_en=item["name"],
                    name_local=item["local_name"],
                    name_ko="AI-Translation-Pending",
                    country="Europe",
                    city=item["city"],
                    category="Cultural/Traditional",
                    date=DateInfo(start_date=item["dates"], end_date=item["dates"])
                ),
                rich_content=RichContent(
                    description_en=item["desc"],
                    description_ko="AI-Translation-Pending",
                    highlights=item["key_points"],
                    official_url=item["url"]
                ),
                media_assets=MediaAssets(
                    images=[MediaAsset(f"https://cdn.example.com/eu/{f_id}.jpg", "main", "high")],
                    video_clips=[]
                ),
                metadata={"source": "European Tourism Board", "popularity_score": 9.8}
            ))
            
        return normalized_results
