"""
LeetCodeDataSource - Main entry point for the leetcode_datasource package.

Provides unified access to LeetCode question data through:
    - Cache (ephemeral, fast lookups)
    - Store (persistent SQLite storage)
    - Problem Index (fast ID lookups)
    - Fetcher (network layer, pluggable)
"""

import json
import logging
import urllib.request
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

from .config import DataSourceConfig
from .models.question import Question
from .models.problem_info import ProblemInfo
from .storage.cache import Cache
from .storage.store import Store
from .fetchers.leetscrape_fetcher import LeetscrapeFecher
from .serialization.question_serializer import QuestionSerializer
from .exceptions import QuestionNotFoundError, NetworkError

logger = logging.getLogger(__name__)

# LeetCode API endpoint for problem list
LEETCODE_PROBLEMS_API = "https://leetcode.com/api/problems/all/"

# Cache settings
PROBLEM_LIST_CACHE_FILE = "problem_list.json"
PROBLEM_LIST_CACHE_META_FILE = "problem_list_meta.json"
PROBLEM_LIST_CACHE_EXPIRY_DAYS = 7


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
            "problem_index_count": self._store.problem_index_count(),
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
    
    # ========== Problem Index API ==========
    
    def sync_problem_list(self, *, refresh: bool = False) -> int:
        """
        Sync problem index from LeetCode API.
        
        Args:
            refresh: If True, force fetch from API even if cache is fresh
            
        Returns:
            Number of problems synced
        """
        cache_file = self.config.cache_dir / PROBLEM_LIST_CACHE_FILE
        meta_file = self.config.cache_dir / PROBLEM_LIST_CACHE_META_FILE
        
        # Check if we can use cached data
        if not refresh and cache_file.exists() and meta_file.exists():
            try:
                with open(meta_file, 'r', encoding='utf-8') as f:
                    meta = json.load(f)
                
                cached_at_str = meta.get('cached_at')
                if cached_at_str:
                    cached_at = datetime.fromisoformat(cached_at_str)
                    expiry = cached_at + timedelta(days=PROBLEM_LIST_CACHE_EXPIRY_DAYS)
                    
                    if datetime.now() < expiry:
                        # Cache is fresh, use it to sync to DB
                        with open(cache_file, 'r', encoding='utf-8') as f:
                            problems = json.load(f)
                        
                        if problems:
                            logger.info(f"Using cached problem list ({len(problems)} problems)")
                            return self._store.sync_problem_index(list(problems.values()))
            except (json.JSONDecodeError, IOError, KeyError) as e:
                logger.warning(f"Failed to read cache: {e}")
        
        # Fetch from API
        problems = self._fetch_problem_list()
        
        if not problems:
            logger.warning("No problems fetched from API")
            return 0
        
        # Save to cache (as fallback for next time)
        self._save_problem_list_cache(problems, cache_file, meta_file)
        
        # Sync to database
        return self._store.sync_problem_index(list(problems.values()))
    
    def _fetch_problem_list(self) -> Dict[str, Dict[str, Any]]:
        """
        Fetch problem list from LeetCode API.
        
        Returns:
            Dict of problems keyed by question_id
        """
        logger.info("Fetching problem list from LeetCode API...")
        
        try:
            with urllib.request.urlopen(LEETCODE_PROBLEMS_API, timeout=30) as response:
                data = json.loads(response.read().decode())
        except urllib.error.URLError as e:
            logger.error(f"Failed to fetch from LeetCode API: {e}")
            raise NetworkError(f"Failed to fetch problem list: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse API response: {e}")
            raise NetworkError(f"Failed to parse problem list: {e}")
        
        # Extract and transform problem data
        problems = {}
        difficulty_map = {1: "Easy", 2: "Medium", 3: "Hard"}
        
        for pair in data.get('stat_status_pairs', []):
            stat = pair.get('stat', {})
            qid = stat.get('question_id')
            
            if not qid:
                continue
            
            slug = stat.get('question__title_slug', '')
            title = stat.get('question__title', '')
            difficulty_level = pair.get('difficulty', {}).get('level', 0)
            
            problem = {
                'question_id': qid,
                'frontend_question_id': stat.get('frontend_question_id', qid),
                'title': title,
                'slug': slug,
                'url': f"https://leetcode.com/problems/{slug}/description/" if slug else "",
                'difficulty': difficulty_map.get(difficulty_level, "Unknown"),
                'difficulty_level': difficulty_level,
                'paid_only': pair.get('paid_only', False),
                'total_acs': stat.get('total_acs', 0),
                'total_submitted': stat.get('total_submitted', 0),
                'is_new_question': stat.get('is_new_question', False),
            }
            
            problems[str(qid)] = problem
        
        logger.info(f"Fetched {len(problems)} problems from API")
        return problems
    
    def _save_problem_list_cache(
        self, 
        problems: Dict[str, Dict[str, Any]], 
        cache_file, 
        meta_file
    ) -> None:
        """Save problem list to cache files."""
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(problems, f, indent=2, ensure_ascii=False)
            
            meta = {
                'cached_at': datetime.now().isoformat(),
                'total_problems': len(problems),
                'cache_version': '1.0',
            }
            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump(meta, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"Saved problem list cache: {len(problems)} problems")
        except IOError as e:
            logger.warning(f"Failed to save cache: {e}")
    
    def get_slug(self, frontend_id: int) -> Optional[str]:
        """
        Get slug by frontend_question_id.
        
        Args:
            frontend_id: Problem number on LeetCode website
            
        Returns:
            title_slug if found, None otherwise
        """
        return self._store.get_slug_by_frontend_id(frontend_id)
    
    def get_frontend_id(self, slug: str) -> Optional[int]:
        """
        Get frontend_question_id by slug.
        
        Args:
            slug: Question slug (e.g., "two-sum")
            
        Returns:
            frontend_question_id if found, None otherwise
        """
        return self._store.get_frontend_id_by_slug(slug)
    
    def get_problem_info(self, frontend_id: int) -> Optional[ProblemInfo]:
        """
        Get minimal problem metadata by frontend_question_id.
        
        Args:
            frontend_id: Problem number on LeetCode website
            
        Returns:
            ProblemInfo if found, None otherwise
        """
        return self._store.get_problem_info_by_frontend_id(frontend_id)

