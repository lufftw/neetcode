"""
LeetCodeDataSource - Main entry point for the leetcode_datasource package.

Provides unified access to LeetCode question data through:
    - Cache (ephemeral, fast lookups)
    - Store (persistent SQLite storage)
    - Fetcher (network layer, pluggable)
"""

import logging
from typing import Optional

from .config import DataSourceConfig
from .models.question import Question
from .storage.cache import Cache
from .storage.store import Store
from .fetchers.leetscrape_fetcher import LeetscrapeFecher
from .serialization.question_serializer import QuestionSerializer
from .exceptions import QuestionNotFoundError, NetworkError

logger = logging.getLogger(__name__)


class LeetCodeDataSource:
    """
    Unified data source for LeetCode questions.
    
    Provides a single interface for:
        - Fetching questions by slug or frontend ID
        - Caching for fast repeated lookups
        - Persistent storage for offline access
    
    Example:
        ds = LeetCodeDataSource()
        
        # Get by slug
        q = ds.get_by_slug("two-sum")
        print(q.title)  # "Two Sum"
        
        # Get by problem number
        q = ds.get_by_frontend_id(1)
        print(q.titleSlug)  # "two-sum"
        
        # Force refresh from network
        q = ds.get_by_slug("two-sum", refresh=True)
    """
    
    def __init__(self, config: Optional[DataSourceConfig] = None):
        """
        Initialize LeetCodeDataSource.
        
        Args:
            config: Configuration options. If None, uses defaults.
        """
        self.config = config or DataSourceConfig()
        
        # Initialize storage layers
        self._cache = Cache(
            cache_dir=self.config.cache_dir,
            ttl_hours=self.config.cache_ttl_hours,
        ) if self.config.cache_enabled else None
        
        self._store = Store(store_dir=self.config.store_dir)
        
        # Initialize fetcher
        self._fetcher = self.config.fetcher or LeetscrapeFecher(
            timeout=self.config.fetch_timeout,
            delay=self.config.rate_limit_delay,
        )
        
        # Stats tracking
        self._stats = {
            "cache_hits": 0,
            "cache_misses": 0,
            "store_hits": 0,
            "network_fetches": 0,
        }
        
        # Ensure directories exist
        self.config.cache_dir.mkdir(parents=True, exist_ok=True)
        self.config.store_dir.mkdir(parents=True, exist_ok=True)
    
    @property
    def store(self) -> Store:
        """Get direct access to the store."""
        return self._store
    
    @property
    def cache(self) -> Optional[Cache]:
        """Get direct access to the cache (None if disabled)."""
        return self._cache
    
    def get_by_slug(self, slug: str, *, refresh: bool = False) -> Question:
        """
        Get question by URL slug.
        
        Args:
            slug: Question slug (e.g., "two-sum")
            refresh: If True, bypass cache and fetch from network
            
        Returns:
            Question object
            
        Raises:
            QuestionNotFoundError: If question not found
        """
        slug = slug.strip().lower()
        
        # Try cache first (unless refresh requested)
        if not refresh and self._cache:
            question = self._cache.get(slug)
            if question:
                self._stats["cache_hits"] += 1
                return question
            self._stats["cache_misses"] += 1
        
        # Try store
        if not refresh:
            question = self._store.get_by_slug(slug)
            if question:
                self._stats["store_hits"] += 1
                # Populate cache
                if self._cache:
                    self._cache.put(question)
                return question
        
        # Fetch from network
        return self._fetch_and_store(slug)
    
    def get_by_frontend_id(self, frontend_id: int, *, refresh: bool = False) -> Question:
        """
        Get question by frontend question ID (problem number on website).
        
        Args:
            frontend_id: Problem number (e.g., 1 for "Two Sum")
            refresh: If True, bypass cache and fetch from network
            
        Returns:
            Question object
            
        Raises:
            QuestionNotFoundError: If question not found
        """
        # Try store first to get slug
        question = self._store.get_by_frontend_id(frontend_id)
        
        if question:
            if refresh:
                # Have slug, can refresh from network
                return self.get_by_slug(question.titleSlug, refresh=True)
            
            self._stats["store_hits"] += 1
            # Populate cache
            if self._cache:
                self._cache.put(question)
            return question
        
        # Cannot fetch by frontend_id directly from network
        # Would need an ID mapping service
        raise QuestionNotFoundError(
            str(frontend_id),
            f"Question with frontend_id={frontend_id} not found in store. "
            "Try importing questions first or use get_by_slug()."
        )
    
    def _fetch_and_store(self, slug: str) -> Question:
        """
        Fetch question from network and store it.
        
        Args:
            slug: Question slug
            
        Returns:
            Question object
            
        Raises:
            QuestionNotFoundError: If fetch fails or question not found
        """
        try:
            data = self._fetcher.fetch(slug)
            
            if data is None:
                raise QuestionNotFoundError(slug)
            
            self._stats["network_fetches"] += 1
            
            # Convert to Question
            question = QuestionSerializer.from_leetscrape(data)
            
            # Store persistently
            self._store.put(question)
            
            # Cache
            if self._cache:
                self._cache.put(question)
            
            return question
            
        except NetworkError as e:
            logger.error(f"Network error fetching {slug}: {e}")
            raise QuestionNotFoundError(slug, f"Failed to fetch: {e}")
    
    def exists(self, slug: str) -> bool:
        """
        Check if question exists in cache or store.
        
        Args:
            slug: Question slug
            
        Returns:
            True if exists, False otherwise
        """
        slug = slug.strip().lower()
        
        if self._cache:
            if self._cache.get(slug):
                return True
        
        return self._store.exists(slug)
    
    def invalidate(self, slug: str) -> bool:
        """
        Remove question from cache.
        
        Args:
            slug: Question slug
            
        Returns:
            True if removed, False if not found
        """
        slug = slug.strip().lower()
        
        if self._cache:
            return self._cache.invalidate(slug)
        return False
    
    def clear_cache(self) -> None:
        """Clear all cached data."""
        if self._cache:
            self._cache.clear()
            logger.info("Cache cleared")
    
    def stats(self) -> dict:
        """
        Get statistics.
        
        Returns:
            Dictionary with statistics
        """
        result = {
            "total_questions": self._store.count(),
            **self._stats,
        }
        
        if self._cache:
            result["cache"] = self._cache.stats()
        
        result["store"] = self._store.stats()
        result["config"] = {
            "data_dir": str(self.config.data_dir),
            "cache_enabled": self.config.cache_enabled,
        }
        
        return result

