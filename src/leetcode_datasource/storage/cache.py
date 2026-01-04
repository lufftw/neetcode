"""
Cache layer for leetcode_datasource.

Provides ephemeral caching to speed up repeated lookups.
Cache data can be safely deleted and will be rebuilt on demand.
"""

import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from ..models.question import Question

logger = logging.getLogger(__name__)


class Cache:
    """
    Ephemeral cache layer for Question data.
    
    Features:
        - File-based JSON cache
        - TTL-based expiration
        - Safe to delete (will rebuild from store/network)
    """
    
    def __init__(self, cache_dir: Path, ttl_hours: int = 24 * 7):
        """
        Initialize cache.
        
        Args:
            cache_dir: Directory to store cache files
            ttl_hours: Time-to-live in hours (default: 1 week)
        """
        self.cache_dir = cache_dir
        self.ttl_hours = ttl_hours
        self._memory_cache: Dict[str, Question] = {}
        self._ensure_dir()
    
    def _ensure_dir(self) -> None:
        """Ensure cache directory exists."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_file(self, slug: str) -> Path:
        """Get cache file path for a slug."""
        return self.cache_dir / f"{slug}.json"
    
    def _is_expired(self, cached_at: str) -> bool:
        """Check if cache entry is expired."""
        try:
            cached_time = datetime.fromisoformat(cached_at)
            expiry_time = cached_time + timedelta(hours=self.ttl_hours)
            return datetime.now() > expiry_time
        except (ValueError, TypeError):
            return True
    
    def get(self, slug: str) -> Optional[Question]:
        """
        Get question from cache.
        
        Args:
            slug: Question slug
            
        Returns:
            Question if found and not expired, None otherwise
        """
        # Check memory cache first
        if slug in self._memory_cache:
            q = self._memory_cache[slug]
            if q._cached_at and not self._is_expired(q._cached_at):
                logger.debug(f"Memory cache hit: {slug}")
                return q
            else:
                del self._memory_cache[slug]
        
        # Check file cache
        cache_file = self._get_cache_file(slug)
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            cached_at = data.get("_cached_at")
            if cached_at and self._is_expired(cached_at):
                logger.debug(f"Cache expired: {slug}")
                return None
            
            # Convert to Question (basic implementation)
            # Full serialization will be in serialization module
            q = Question(
                QID=data.get("QID", 0),
                frontend_question_id=data.get("frontend_question_id", 0),
                title=data.get("title", ""),
                titleSlug=data.get("titleSlug", slug),
                difficulty=data.get("difficulty", ""),
                Body=data.get("Body", ""),
                Code=data.get("Code", ""),
                Hints=data.get("Hints", []),
                acceptanceRate=data.get("acceptanceRate", 0.0),
                topicTags=data.get("topicTags", ""),
                categorySlug=data.get("categorySlug", ""),
                isPaidOnly=data.get("isPaidOnly", False),
                SimilarQuestions=data.get("SimilarQuestions", []),
                Companies=data.get("Companies"),
                _schema_version=data.get("_schema_version", "1.0"),
                _cached_at=cached_at,
                _from_cache=True,
            )
            
            self._memory_cache[slug] = q
            logger.debug(f"File cache hit: {slug}")
            return q
            
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Cache read error for {slug}: {e}")
            return None
    
    def put(self, question: Question) -> None:
        """
        Store question in cache.
        
        Args:
            question: Question to cache
        """
        slug = question.titleSlug
        cached_at = datetime.now().isoformat()
        
        # Update question metadata
        question._cached_at = cached_at
        question._from_cache = True
        
        # Store in memory
        self._memory_cache[slug] = question
        
        # Store in file
        data = {
            "QID": question.QID,
            "frontend_question_id": question.frontend_question_id,
            "title": question.title,
            "titleSlug": question.titleSlug,
            "difficulty": question.difficulty,
            "Body": question.Body,
            "Code": question.Code,
            "Hints": question.Hints,
            "acceptanceRate": question.acceptanceRate,
            "topicTags": question.topicTags,
            "categorySlug": question.categorySlug,
            "isPaidOnly": question.isPaidOnly,
            "SimilarQuestions": question.SimilarQuestions,
            "Companies": question.Companies,
            "_schema_version": question._schema_version,
            "_cached_at": cached_at,
        }
        
        cache_file = self._get_cache_file(slug)
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.debug(f"Cached: {slug}")
        except IOError as e:
            logger.warning(f"Cache write error for {slug}: {e}")
    
    def invalidate(self, slug: str) -> bool:
        """
        Remove question from cache.
        
        Args:
            slug: Question slug
            
        Returns:
            True if removed, False if not found
        """
        removed = False
        
        if slug in self._memory_cache:
            del self._memory_cache[slug]
            removed = True
        
        cache_file = self._get_cache_file(slug)
        if cache_file.exists():
            cache_file.unlink()
            removed = True
        
        return removed
    
    def clear(self) -> int:
        """
        Clear all cache entries.
        
        Returns:
            Number of entries cleared
        """
        count = len(self._memory_cache)
        self._memory_cache.clear()
        
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
            count += 1
        
        logger.info(f"Cache cleared: {count} entries")
        return count
    
    def stats(self) -> dict:
        """Get cache statistics."""
        file_count = len(list(self.cache_dir.glob("*.json")))
        return {
            "memory_entries": len(self._memory_cache),
            "file_entries": file_count,
            "cache_dir": str(self.cache_dir),
        }

