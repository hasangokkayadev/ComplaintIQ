"""
Base Scraper Interface
Scraping framework for customer complaints from various platforms
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ScrapedComplaint:
    """Standardized complaint data structure"""
    platform: str
    source_id: str
    author: str
    rating: Optional[float]
    date: str
    text: str
    url: str
    company: Optional[str] = None
    product: Optional[str] = None
    channel: str = "web"

class BaseScraper(ABC):
    """Abstract base class for all scrapers"""

    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.session = None
        self.proxies = None
        self.headers = {}

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize scraper with required settings"""
        pass

    @abstractmethod
    def scrape(self, query: str = None, max_results: int = 100) -> List[ScrapedComplaint]:
        """Scrape complaints based on query"""
        pass

    @abstractmethod
    def get_complaint_details(self, complaint_id: str) -> Optional[ScrapedComplaint]:
        """Get detailed information for a specific complaint"""
        pass

    def cleanup(self):
        """Cleanup resources"""
        if self.session:
            self.session.close()
            logger.info(f"{self.platform_name} scraper cleaned up")

    def validate_complaint(self, complaint: ScrapedComplaint) -> bool:
        """Validate scraped complaint data"""
        required_fields = ['platform', 'source_id', 'text', 'url']
        return all(getattr(complaint, field, None) for field in required_fields)

    def to_dict(self, complaint: ScrapedComplaint) -> Dict:
        """Convert complaint to dictionary"""
        return {
            'platform': complaint.platform,
            'source_id': complaint.source_id,
            'author': complaint.author,
            'rating': complaint.rating,
            'date': complaint.date,
            'text': complaint.text,
            'url': complaint.url,
            'company': complaint.company,
            'product': complaint.product,
            'channel': complaint.channel
        }