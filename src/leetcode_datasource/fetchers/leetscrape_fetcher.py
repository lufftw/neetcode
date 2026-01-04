"""
LeetScrape-based fetcher implementation.

Uses the leetscrape package to fetch LeetCode question data.
"""

import logging
from typing import Optional, Dict, Any

from ..exceptions import NetworkError

logger = logging.getLogger(__name__)


class LeetscrapeFecher:
    """
    Fetcher implementation using LeetScrape.
    
    LeetScrape is a third-party package that scrapes LeetCode question data.
    https://github.com/nikhil-ravi/LeetScrape
    """
    
    def __init__(self, timeout: int = 30, delay: float = 0.5):
        """
        Initialize fetcher.
        
        Args:
            timeout: Request timeout in seconds
            delay: Delay between requests (rate limiting)
        """
        self.timeout = timeout
        self.delay = delay
        self._available: Optional[bool] = None
    
    def is_available(self) -> bool:
        """Check if leetscrape is installed."""
        if self._available is None:
            try:
                from leetscrape import GetQuestion
                self._available = True
            except ImportError:
                self._available = False
                logger.warning(
                    "leetscrape not available. Install with: pip install leetscrape"
                )
        return self._available
    
    def fetch(self, slug: str) -> Optional[Dict[str, Any]]:
        """
        Fetch question data from LeetCode via LeetScrape.
        
        Args:
            slug: Question slug (e.g., "two-sum")
            
        Returns:
            Dictionary with question data, or None if not found
            
        Raises:
            NetworkError: If fetch fails
        """
        if not self.is_available():
            raise NetworkError(
                "leetscrape not installed. Install with: pip install leetscrape"
            )
        
        try:
            from leetscrape import GetQuestion
            import time
            
            logger.info(f"Fetching from LeetScrape: {slug}")
            
            # Rate limiting
            time.sleep(self.delay)
            
            # Fetch from LeetScrape
            q = GetQuestion(titleSlug=slug).scrape()
            
            if q is None:
                logger.warning(f"Question not found: {slug}")
                return None
            
            # Convert LeetScrape Question to dict
            data = {
                "QID": getattr(q, "QID", 0),
                "title": getattr(q, "title", ""),
                "titleSlug": getattr(q, "titleSlug", slug),
                "difficulty": getattr(q, "difficulty", ""),
                "Body": getattr(q, "Body", ""),
                "Code": getattr(q, "Code", ""),
                "Hints": getattr(q, "Hints", []),
                "acceptanceRate": getattr(q, "acceptanceRate", 0.0),
                "topicTags": getattr(q, "topicTags", ""),
                "categorySlug": getattr(q, "categorySlug", ""),
                "isPaidOnly": getattr(q, "isPaidOnly", False) or getattr(q, "paidOnly", False),
                "SimilarQuestions": getattr(q, "SimilarQuestions", []),
                "Companies": getattr(q, "Companies", None),
            }
            
            logger.info(f"Fetched: {slug} ({data.get('title', 'Unknown')})")
            return data
            
        except ImportError as e:
            raise NetworkError(f"leetscrape import error: {e}")
        except Exception as e:
            logger.error(f"Fetch error for {slug}: {e}")
            raise NetworkError(f"Failed to fetch {slug}: {e}", cause=e)

