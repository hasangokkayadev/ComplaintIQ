"""
Trendyol Scraper Implementation
Scrapes customer reviews and complaints from Trendyol platform
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
import re

logger = logging.getLogger(__name__)

class TrendyolScraper(BaseScraper):
    """Trendyol platform scraper"""

    def __init__(self):
        super().__init__("Trendyol")
        self.base_url = "https://www.trendyol.com"
        self.search_url = f"{self.base_url}/sr"
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'https://www.trendyol.com/'
        }

    def initialize(self) -> bool:
        """Initialize scraper"""
        try:
            self.session.headers.update(self.headers)
            logger.info("Trendyol scraper initialized")
            return True
        except Exception as e:
            logger.error(f"Trendyol scraper initialization failed: {e}")
            return False

    def scrape(self, query: str = None, max_results: int = 100) -> List[ScrapedComplaint]:
        """Scrape reviews from Trendyol"""
        complaints = []

        try:
            # Search for products
            search_params = {'q': query} if query else {'q': 'şikayet'}
            response = self.session.get(self.search_url, params=search_params)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find product items
            product_items = soup.find_all('div', class_='p-card-wrppr', limit=10)  # Limit to 10 products

            for product_item in product_items:
                try:
                    # Get product URL
                    product_url_elem = product_item.find('a', class_='p-card-chld')
                    if not product_url_elem:
                        continue

                    product_url = product_url_elem['href']
                    if not product_url.startswith('http'):
                        product_url = f"{self.base_url}{product_url}"

                    # Get product reviews
                    product_complaints = self._scrape_product_reviews(product_url, max_results // len(product_items))
                    complaints.extend(product_complaints)

                    # Rate limiting between products
                    time.sleep(random.uniform(1.0, 2.0))

                except Exception as e:
                    logger.error(f"Error processing product: {e}")
                    continue

            logger.info(f"Scraped {len(complaints)} complaints from Trendyol")
            return complaints

        except Exception as e:
            logger.error(f"Trendyol scraping failed: {e}")
            return []

    def _scrape_product_reviews(self, product_url: str, max_reviews: int = 10) -> List[ScrapedComplaint]:
        """Scrape reviews for a specific product"""
        complaints = []

        try:
            # Get product page
            response = self.session.get(product_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find review section
            review_section = soup.find('div', class_='reviews')
            if not review_section:
                return complaints

            # Find review items
            review_items = review_section.find_all('div', class_='review-item', limit=max_reviews)

            for review_item in review_items:
                try:
                    complaint = self._parse_review_item(review_item, product_url)
                    if complaint and self.validate_complaint(complaint):
                        # Only add negative reviews (1-2 stars)
                        if complaint.rating and complaint.rating <= 2:
                            complaints.append(complaint)

                    # Rate limiting between reviews
                    time.sleep(random.uniform(0.3, 0.8))

                except Exception as e:
                    logger.error(f"Error parsing review: {e}")
                    continue

            return complaints

        except Exception as e:
            logger.error(f"Error scraping product reviews: {e}")
            return []

    def _parse_review_item(self, review_item, product_url: str) -> Optional[ScrapedComplaint]:
        """Parse individual review item"""
        try:
            # Extract author
            author_elem = review_item.find('span', class_='reviewer-name')
            author = author_elem.text.strip() if author_elem else "Trendyol Kullanıcısı"

            # Extract rating
            rating_elem = review_item.find('div', class_='rating')
            rating = None
            if rating_elem:
                rating_text = rating_elem.get('class', [''])[-1]
                rating_match = re.search(r'star-(\d)', rating_text)
                if rating_match:
                    rating = int(rating_match.group(1))

            # Extract date
            date_elem = review_item.find('span', class_='review-date')
            date_text = date_elem.text.strip() if date_elem else ""
            date = self._parse_date(date_text)

            # Extract text
            text_elem = review_item.find('div', class_='review-text')
            text = text_elem.text.strip() if text_elem else ""

            # Extract product name from URL
            product_name = self._extract_product_name(product_url)

            # Create complaint object
            complaint = ScrapedComplaint(
                platform=self.platform_name,
                source_id=f"trendyol_{random.randint(100000, 999999)}",
                author=author,
                rating=rating,
                date=date,
                text=text,
                url=product_url,
                company="Trendyol",
                product=product_name,
                channel="ecommerce"
            )

            return complaint

        except Exception as e:
            logger.error(f"Error parsing review item: {e}")
            return None

    def _parse_date(self, date_text: str) -> str:
        """Parse Turkish date format"""
        try:
            # Handle relative dates
            if "gün önce" in date_text:
                days_ago = int(re.search(r'(\d+) gün önce', date_text).group(1))
                return (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
            elif "hafta önce" in date_text:
                weeks_ago = int(re.search(r'(\d+) hafta önce', date_text).group(1))
                return (datetime.now() - timedelta(weeks=weeks_ago)).strftime('%Y-%m-%d')
            elif "ay önce" in date_text:
                months_ago = int(re.search(r'(\d+) ay önce', date_text).group(1))
                return (datetime.now() - timedelta(days=30*months_ago)).strftime('%Y-%m-%d')
            else:
                # Standard date format
                return datetime.strptime(date_text, '%d.%m.%Y').strftime('%Y-%m-%d')
        except:
            return datetime.now().strftime('%Y-%m-%d')

    def _extract_product_name(self, url: str) -> Optional[str]:
        """Extract product name from URL"""
        try:
            # Extract from URL path
            parts = url.split('/')
            for part in parts:
                if '-' in part and len(part) > 5:
                    return part.replace('-', ' ').title()

            return "Trendyol Ürünü"
        except:
            return "Trendyol Ürünü"

    def get_complaint_details(self, complaint_id: str) -> Optional[ScrapedComplaint]:
        """Get detailed complaint information"""
        try:
            # Note: This would require the actual complaint URL
            # For now, return mock data

            mock_complaint = ScrapedComplaint(
                platform=self.platform_name,
                source_id=complaint_id,
                author="Trendyol Kullanıcısı",
                rating=1,
                date=datetime.now().strftime('%Y-%m-%d'),
                text="Ürün hasarlı geldi, iade süreci çok uzun sürdü",
                url=f"https://www.trendyol.com/urun/12345",
                company="Trendyol",
                product="Test Ürünü",
                channel="ecommerce"
            )

            return mock_complaint

        except Exception as e:
            logger.error(f"Error getting complaint details: {e}")
            return None