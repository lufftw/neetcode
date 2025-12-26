#!/usr/bin/env python3
"""
Question API - Unified interface for LeetCode question data.

This module provides a single entry point for fetching LeetCode questions.
It transparently handles:
    - Checking local SQLite cache first
    - Fetching from LeetScrape if not cached
    - Persisting new data to cache
    - Returning Question objects compatible with LeetScrape

Usage:
    from question_api import get_question
    
    # Get question (from cache or network)
    q = get_question("two-sum")
    
    # Use like LeetScrape Question
    print(q.title)
    print(q.Body)
    print(q.Hints)
"""

from typing import Optional, Union
import logging

from question_store import QuestionStore, get_default_store
from question_serializer import Question, QuestionSerializer, deserialize

# Configure logging
logger = logging.getLogger(__name__)


class QuestionAPI:
    """
    Unified API for fetching LeetCode question data.
    
    This class coordinates between:
        - LeetScrape (network fetcher)
        - QuestionStore (SQLite cache)
        - QuestionSerializer (format conversion)
    
    Design Goals:
        1. Cache-first: Always check local cache before network
        2. Transparent: Callers get same Question interface regardless of source
        3. Fail-safe: Network errors don't crash; return None gracefully
    """
    
    def __init__(self, store: Optional[QuestionStore] = None):
        """
        Initialize the Question API.
        
        Args:
            store: Optional QuestionStore instance. Uses default if not provided.
        """
        self.store = store or get_default_store()
        self._leetscrape_available: Optional[bool] = None
    
    def _check_leetscrape(self) -> bool:
        """Check if leetscrape is available."""
        if self._leetscrape_available is None:
            try:
                from leetscrape import GetQuestion
                self._leetscrape_available = True
            except ImportError:
                self._leetscrape_available = False
                logger.warning("leetscrape not available. Install with: pip install leetscrape")
        return self._leetscrape_available
    
    def _fetch_from_network(self, title_slug: str) -> Optional[Question]:
        """
        Fetch question from LeetScrape and cache it.
        
        Args:
            title_slug: The question slug (e.g., 'two-sum')
            
        Returns:
            Question object or None if fetch fails
        """
        if not self._check_leetscrape():
            return None
        
        try:
            from leetscrape import GetQuestion
            
            logger.info(f"Fetching from LeetScrape: {title_slug}")
            q = GetQuestion(titleSlug=title_slug).scrape()
            
            # Convert to storage format and save
            data = QuestionSerializer.from_leetscrape(q)
            self.store.save(data)
            
            logger.info(f"Cached: {title_slug}")
            
            # Return as Question object (mark as from cache since we just saved)
            return deserialize(self.store.get_by_slug(title_slug))
            
        except Exception as e:
            logger.error(f"Failed to fetch {title_slug}: {e}")
            return None
    
    def get(self, title_slug: str, force_refresh: bool = False) -> Optional[Question]:
        """
        Get a question by its slug.
        
        This is the main entry point. It:
            1. Checks local cache first (unless force_refresh)
            2. Fetches from network if not cached
            3. Returns Question object compatible with LeetScrape
        
        Args:
            title_slug: The question slug (e.g., 'two-sum')
            force_refresh: If True, bypass cache and fetch from network
            
        Returns:
            Question object or None if not found/fetch failed
        """
        # Normalize slug
        title_slug = title_slug.strip().lower()
        
        # Check cache first (unless force refresh)
        if not force_refresh:
            data = self.store.get_by_slug(title_slug)
            if data and QuestionSerializer.is_valid(data):
                logger.debug(f"Cache hit: {title_slug}")
                return deserialize(data)
            logger.debug(f"Cache miss: {title_slug}")
        
        # Fetch from network
        return self._fetch_from_network(title_slug)
    
    def get_by_id(self, qid: Union[str, int], force_refresh: bool = False) -> Optional[Question]:
        """
        Get a question by its LeetCode QID.
        
        Note: If not in cache and force_refresh is False, returns None
        because we can't fetch by QID directly (need slug).
        
        Args:
            qid: The question ID (e.g., 1, "1", "0001")
            force_refresh: Not applicable for ID lookup
            
        Returns:
            Question object or None if not found
        """
        # Normalize QID to integer
        qid_int = int(str(qid).lstrip('0') or '0')
        
        data = self.store.get_by_qid(str(qid_int))
        if data and QuestionSerializer.is_valid(data):
            return deserialize(data)
        
        return None
    
    def exists(self, title_slug: str) -> bool:
        """Check if a question exists in cache."""
        return self.store.exists(title_slug.strip().lower())
    
    def invalidate(self, title_slug: str) -> bool:
        """
        Remove a question from cache.
        
        Args:
            title_slug: The question slug
            
        Returns:
            True if removed, False if not found
        """
        return self.store.delete(title_slug.strip().lower())
    
    def cache_stats(self) -> dict:
        """Get cache statistics."""
        return {
            'total_questions': self.store.count(),
            'db_path': str(self.store.db_path),
        }


# Module-level singleton
_default_api: Optional[QuestionAPI] = None


def get_default_api() -> QuestionAPI:
    """Get the default QuestionAPI instance."""
    global _default_api
    if _default_api is None:
        _default_api = QuestionAPI()
    return _default_api


# Convenience function - main public interface
def get_question(slug: str, force_refresh: bool = False) -> Optional[Question]:
    """
    Get a LeetCode question by slug.
    
    This is the primary public interface. It returns a Question object
    that is API-compatible with LeetScrape's Question class.
    
    Args:
        slug: The question slug (e.g., 'two-sum', 'merge-k-sorted-lists')
        force_refresh: If True, bypass cache and fetch fresh data
        
    Returns:
        Question object or None if not found
        
    Example:
        >>> q = get_question("two-sum")
        >>> print(q.title)
        Two Sum
        >>> print(q.difficulty)
        Easy
        >>> print(q.Body[:50])
        <p>Given an array of integers <code>nums</code>...
    """
    return get_default_api().get(slug, force_refresh)


def get_question_by_id(qid: Union[str, int]) -> Optional[Question]:
    """
    Get a LeetCode question by its ID (from cache only).
    
    Args:
        qid: The question ID (e.g., 1, "1", "0001")
        
    Returns:
        Question object or None if not in cache
    """
    return get_default_api().get_by_id(qid)


if __name__ == "__main__":
    import sys
    
    # Enable logging for demo
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    # Demo usage
    if len(sys.argv) > 1:
        slug = sys.argv[1]
    else:
        slug = input("Enter LeetCode problem slug (e.g., two-sum): ").strip()
    
    print(f"\nFetching: {slug}")
    print("=" * 50)
    
    q = get_question(slug)
    
    if q:
        print(f"Title: {q.title}")
        print(f"QID: {q.QID}")
        print(f"Difficulty: {q.difficulty}")
        print(f"Acceptance Rate: {q.acceptanceRate:.2f}%")
        print(f"Topic Tags: {q.topicTags}")
        print(f"Category: {q.categorySlug}")
        print(f"Similar Questions: {q.SimilarQuestions[:5]}{'...' if len(q.SimilarQuestions) > 5 else ''}")
        print(f"Hints: {len(q.Hints)} hint(s)")
        print(f"Code template: {len(q.Code)} chars")
        print(f"Body length: {len(q.Body)} chars")
        print(f"From cache: {q._from_cache}")
        
        # Show cache stats
        api = get_default_api()
        stats = api.cache_stats()
        print(f"\nCache: {stats['total_questions']} questions in {stats['db_path']}")
    else:
        print("Failed to fetch question")

