import random
import uuid
from typing import List
from .schema import FestivalData, BasicInfo, DateInfo, RichContent, MediaAsset, MediaAssets
from .base_provider import BaseProvider

class MockProvider(BaseProvider):
    """
    Simulates data fetching for verification purposes.
    This will be replaced by actual API/Scraper implementations.
    """
    
    def fetch_festivals(self) -> List[FestivalData]:
        # Mocking data for Japan and Spain to test the pipeline
        mock_festivals = [
            {
                "country": "Japan",
                "name_en": "Sapporo Snow Festival",
                "name_local": "さっぽろ雪まつり",
                "city": "Sapporo",
                "category": "Winter",
                "start_date": "2025-02-04",
                "end_date": "2025-02-11",
                "desc_en": "One of the world's largest snow and ice festivals with giant snow sculptures.",
                "highlights": ["Giant ice sculptures", "Illuminated night views", "Local winter delicacies"],
                "url": "https://www.snowfes.com"
            },
            {
                "country": "Spain",
                "name_en": "La Tomatina",
                "name_local": "La Tomatina",
                "city": "Buñol",
                "category": "Unique",
                "start_date": "2025-08-24",
                "end_date": "2025-08-24",
                "desc_en": "The world's most famous tomato-throwing festival.",
                "highlights": ["Tomato fight", "Local culture experience", "High energy vibe"],
                "url": "https://latomatina.info"
            }
        ]
        
        results = []
        for fest in mock_festivals:
            f_id = str(uuid.uuid4())[:8]
            results.append(FestivalData(
                festival_id=f_id,
                basic_info=BasicInfo(
                    name_en=fest["name_en"],
                    name_local=fest["name_local"],
                    name_ko="AI-translated name", # Real AI layer will replace this
                    country=fest["country"],
                    city=fest["city"],
                    category=fest["category"],
                    date=DateInfo(fest["start_date"], fest["end_date"])
                ),
                rich_content=RichContent(
                    description_en=fest["desc_en"],
                    description_ko="AI-translated description",
                    highlights=fest["highlights"],
                    official_url=fest["url"]
                ),
                media_assets=MediaAssets(
                    images=[MediaAsset("https://example.com/image1.jpg", "main", "high")],
                    video_clips=[]
                ),
                metadata={"source": f"{fest['country']} Provider", "popularity_score": random.uniform(0, 10)}
            ))
        return results
