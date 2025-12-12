"""
Scraper Utilities
Common functions for web scraping operations
"""

import requests
import time
import random
import logging
from typing import List, Dict, Optional, Callable
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

class ScraperUtils:
    """Utility functions for web scraping"""

    @staticmethod
    def get_user_agents() -> List[str]:
        """Get list of user agents for rotation"""
        return [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
        ]

    @staticmethod
    def get_random_user_agent() -> str:
        """Get random user agent"""
        return random.choice(ScraperUtils.get_user_agents())

    @staticmethod
    def create_session_with_retry() -> requests.Session:
        """Create requests session with retry strategy"""
        session = requests.Session()

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    @staticmethod
    def exponential_backoff(attempt: int, max_delay: float = 30.0) -> float:
        """Calculate exponential backoff delay"""
        base = 2
        delay = min(base ** attempt + random.uniform(0, 1), max_delay)
        return delay

    @staticmethod
    def rate_limited_request(
        session: requests.Session,
        method: str,
        url: str,
        min_delay: float = 1.0,
        max_delay: float = 3.0,
        **kwargs
    ) -> Optional[requests.Response]:
        """Make rate-limited request"""
        attempt = 0
        max_attempts = 3

        while attempt < max_attempts:
            try:
                # Random delay to avoid detection
                delay = random.uniform(min_delay, max_delay)
                time.sleep(delay)

                # Rotate user agent
                kwargs.setdefault('headers', {})
                kwargs['headers']['User-Agent'] = ScraperUtils.get_random_user_agent()

                response = session.request(method, url, **kwargs)

                # Check for rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 5))
                    logger.warning(f"Rate limited. Retrying after {retry_after} seconds...")
                    time.sleep(retry_after)
                    attempt += 1
                    continue

                response.raise_for_status()
                return response

            except requests.exceptions.RequestException as e:
                attempt += 1
                delay = ScraperUtils.exponential_backoff(attempt)
                logger.warning(f"Request failed (attempt {attempt}/{max_attempts}): {e}. Retrying in {delay:.1f}s...")
                time.sleep(delay)

        logger.error(f"Max attempts ({max_attempts}) reached for {url}")
        return None

    @staticmethod
    def get_proxy_list() -> List[str]:
        """Get list of proxy servers (mock for now)"""
        # In production, this would fetch from a proxy service
        return [
            # 'http://proxy1.example.com:8080',
            # 'http://proxy2.example.com:8080',
            # Add real proxies here
        ]

    @staticmethod
    def get_random_proxy() -> Optional[str]:
        """Get random proxy"""
        proxies = ScraperUtils.get_proxy_list()
        return random.choice(proxies) if proxies else None

    @staticmethod
    def validate_proxy(proxy: str, test_url: str = "https://www.google.com") -> bool:
        """Validate proxy connection"""
        try:
            proxies = {'http': proxy, 'https': proxy}
            response = requests.get(
                test_url,
                proxies=proxies,
                timeout=5,
                headers={'User-Agent': ScraperUtils.get_random_user_agent()}
            )
            return response.status_code == 200
        except:
            return False

    @staticmethod
    def scrape_with_retry(
        scraper_func: Callable,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        backoff_factor: float = 2.0
    ) -> Optional[any]:
        """Execute scraper function with retry logic"""
        attempt = 0

        while attempt < max_retries:
            try:
                result = scraper_func()
                return result
            except Exception as e:
                attempt += 1
                delay = initial_delay * (backoff_factor ** attempt)
                logger.warning(f"Scraping attempt {attempt} failed: {e}. Retrying in {delay:.1f}s...")
                time.sleep(delay)

        logger.error(f"Max retries ({max_retries}) reached for scraper function")
        return None

    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""

        # Remove excessive whitespace
        text = ' '.join(text.split())

        # Remove special characters (keep basic punctuation)
        text = re.sub(r'[^\w\s.,!?ğüşıöçĞÜŞIİÖÇ]', '', text)

        return text.strip()

    @staticmethod
    def extract_keywords(text: str, min_length: int = 3) -> List[str]:
        """Extract keywords from text"""
        if not text:
            return []

        # Simple keyword extraction (can be enhanced with NLP)
        words = text.lower().split()
        keywords = [word for word in words if len(word) >= min_length]

        return list(set(keywords))  # Remove duplicates