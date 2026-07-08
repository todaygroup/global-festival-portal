from abc import ABC, abstractmethod
from typing import List
from festival_engine.schema import FestivalData

class BaseProvider(ABC):
    """Base class for all festival data providers."""
    
    def __init__(self, country: str):
        self.country = country

    @abstractmethod
    def fetch_festivals(self) -> List[FestivalData]:
        """Fetch and normalize festival data from the source."""
        pass
