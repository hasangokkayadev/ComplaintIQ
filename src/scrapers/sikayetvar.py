"""
Şikayetvar Scraper Implementation
Scrapes customer complaints from Şikayetvar platform
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Optional
import time
import random
from datetime import datetime
from .base import BaseScraper, ScrapedComplaint
from ..config import BUSINESS_RULES
import logging

logger = logging.getLogger(__name__)

class SikayetvarScraper(BaseScraper):
    """Şikayetvar platform scraper"""

    def __init__(self):
        super().__init__("Şikayetvar")
        self.base_url = "https://www.sikayetvar.com"
        self.search_url = f"{self.base_url}/ara"
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7'
        }

    def initialize(self) -> bool:
        """Initialize scraper"""
        try:
            self.session.headers.update(self.headers)
            logger.info("Şikayetvar scraper initialized")
            return True
        except Exception as e:
            logger.error(f"Şikayetvar scraper initialization failed: {e}")
            return False

    def scrape(self, query: str = None, max_results: int = 100) -> List[ScrapedComplaint]:
        """Scrape complaints from Şikayetvar"""
        complaints = []

        try:
            # Build search URL
            params = {'q': query} if query else {}
            response = self.session.get(self.search_url, params=params)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find complaint items
            complaint_items = soup.find_all('div', class_='complaint-item', limit=max_results)

            for item in complaint_items:
                try:
                    complaint = self._parse_complaint_item(item)
                    if complaint and self.validate_complaint(complaint):
                        complaints.append(complaint)

                    # Rate limiting
                    time.sleep(random.uniform(0.5, 1.5))

                except Exception as e:
                    logger.error(f"Error parsing complaint item: {e}")
                    continue

            logger.info(f"Scraped {len(complaints)} complaints from Şikayetvar")
            return complaints

        except Exception as e:
            logger.error(f"Şikayetvar scraping failed: {e}")
            return []

    def _parse_complaint_item(self, item) -> Optional[ScrapedComplaint]:
        """Parse individual complaint item"""
        try:
            # Extract basic info
            title_elem = item.find('h3', class_='complaint-title')
            title = title_elem.text.strip() if title_elem else "No Title"

            url_elem = title_elem.find('a') if title_elem else None
            url = url_elem['href'] if url_elem else ""
            if not url.startswith('http'):
                url = f"{self.base_url}{url}"

            author_elem = item.find('span', class_='author')
            author = author_elem.text.strip() if author_elem else "Anonymous"

            date_elem = item.find('span', class_='date')
            date_text = date_elem.text.strip() if date_elem else ""
            date = self._parse_date(date_text)

            text_elem = item.find('div', class_='complaint-text')
            text = text_elem.text.strip() if text_elem else ""

            # Extract company (from URL or text)
            company = self._extract_company(url, text)

            # Create complaint object
            complaint = ScrapedComplaint(
                platform=self.platform_name,
                source_id=url.split('/')[-1],
                author=author,
                rating=None,  # Şikayetvar doesn't have ratings
                date=date,
                text=text,
                url=url,
                company=company,
                product=None,
                channel="web"
            )

            return complaint

        except Exception as e:
            logger.error(f"Error parsing complaint item: {e}")
            return None

    def _parse_date(self, date_text: str) -> str:
        """Parse Turkish date format"""
        try:
            # Handle different date formats
            if "saat" in date_text or "dakika" in date_text:
                # Recent complaints (hours/minutes ago)
                return datetime.now().strftime('%Y-%m-%d')
            elif "dün" in date_text:
                # Yesterday
                return (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            else:
                # Standard date format
                return datetime.strptime(date_text, '%d.%m.%Y').strftime('%Y-%m-%d')
        except:
            return datetime.now().strftime('%Y-%m-%d')

    def _extract_company(self, url: str, text: str) -> Optional[str]:
        """Extract company name from URL or text"""
        try:
            # Try to extract from URL
            if "/firma/" in url:
                parts = url.split('/firma/')
                if len(parts) > 1:
                    company_slug = parts[1].split('/')[0]
                    return company_slug.replace('-', ' ').title()

            # Try to extract from text
            common_companies = ['Trendyol', 'Hepsiburada', 'Amazon', 'N11', 'GittiGidiyor']
            for company in common_companies:
                if company.lower() in text.lower():
                    return company

            return None
        except:
            return None

    def get_complaint_details(self, complaint_id: str) -> Optional[ScrapedComplaint]:
        """Get detailed complaint information"""
        try:
            url = f"{self.base_url}/{complaint_id}"
            response = self.session.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Parse detailed page
            title = soup.find('h1', class_='complaint-title').text.strip()
            author = soup.find('span', class_='author').text.strip()
            date_text = soup.find('span', class_='date').text.strip()
            date = self._parse_date(date_text)
            text = soup.find('div', class_='complaint-content').text.strip()

            company = self._extract_company(url, text)

            complaint = ScrapedComplaint(
                platform=self.platform_name,
                source_id=complaint_id,
                author=author,
                rating=None,
                date=date,
                text=text,
                url=url,
                company=company,
                product=None,
                channel="web"
            )

            return complaint

        except Exception as e:
            logger.error(f"Error getting complaint details: {e}")
            return None