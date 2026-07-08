import uuid
from typing import List
from festival_engine.schema import FestivalData, BasicInfo, DateInfo, RichContent, MediaAsset, MediaAssets
from .base_provider import BaseProvider

class JapanProvider(BaseProvider):
    """
    Real Provider for Japan Tourism Data.
    Handles normalization from raw website data to Standard Schema.
    """
    
    def fetch_festivals(self) -> List[FestivalData]:
        # In a fully automated system, this would be a call to a scraper/API.
        # For this milestone, we use the data captured by the 'Data Hunter' (Agent).
        raw_captured_data = [
            {
                "name": "Sapporo Snow Festival",
                "local_name": "さっぽろ雪まつり",
                "city": "Sapporo",
                "region": "Hokkaido",
                "dates": "Early February",
                "desc": "One of the most famous winter festivals in Japan, featuring massive snow and ice sculptures.",
                "key_points": ["Giant Snow Sculptures", "Odori Park Exhibition", "Ice carvings in Susukino"],
                "url": "https://www.snowfes.com"
            },
            {
                "name": "Aomori Nebuta Matsuri",
                "local_name": "青森ねぶた祭",
                "city": "Aomori",
                "region": "Tohoku",
                "dates": "August 2-7",
                "desc": "A festival featuring enormous illuminated floats depicting mythical creatures and historical figures.",
                "key_points": ["Giant illuminated floats", "Haneto dancing", "Nightly parades"],
                "url": "https://www.nebuta.jp"
            }
        ]
        
        normalized_results = []
        for item in raw_captured_data:
            f_id = f"JP-{uuid.uuid4().hex[:8]}"
            normalized_results.append(FestivalData(
                festival_id=f_id,
                basic_info=BasicInfo(
                    name_en=item["name"],
                    name_local=item["local_name"],
                    name_ko="AI-Translation-Pending", # To be handled by Translation Layer
                    country="Japan",
                    city=item["city"],
                    category="Traditional/Winter",
                    date=DateInfo(start_date=item["dates"], end_date=item["dates"])
                ),
                rich_content=RichContent(
                    description_en=item["desc"],
                    description_ko="AI-Translation-Pending",
                    highlights=item["key_points"],
                    official_url=item["url"]
                ),
                media_assets=MediaAssets(
                    images=[MediaAsset(f"https://cdn.example.com/jp/{f_id}.jpg", "main", "high")],
                    video_clips=[]
                ),
                metadata={"source": "JNTO Official", "popularity_score": 9.5}
            ))
            
        return normalized_results
