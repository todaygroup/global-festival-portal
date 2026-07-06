from dataclasses import dataclass, asdict
from typing import List, Optional

@dataclass
class DateInfo:
    start_date: str
    end_date: str
    period: Optional[str] = None

@dataclass
class BasicInfo:
    name_en: str
    name_local: str
    name_ko: str
    country: str
    city: str
    category: str
    date: DateInfo

@dataclass
class RichContent:
    description_en: str
    description_ko: str
    highlights: List[str]
    official_url: str
    ticket_info: Optional[str] = None

@dataclass
class MediaAsset:
    url: str
    tag: str
    quality: str

@dataclass
class MediaAssets:
    images: List[MediaAsset]
    video_clips: List[dict] # Simplified for now

@dataclass
class FestivalData:
    festival_id: str
    basic_info: BasicInfo
    rich_content: RichContent
    media_assets: MediaAssets
    metadata: dict

    def to_dict(self):
        return asdict(self)
