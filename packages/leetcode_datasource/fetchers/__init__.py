"""
Network fetchers for leetcode_datasource.

Provides pluggable network layer for fetching LeetCode question data.
Default implementation uses LeetScrape.
"""

from typing import Protocol, Optional, Dict, Any


class BaseFetcher(Protocol):
    """
    Protocol for question fetchers.
    
    Note: This is a Protocol (structural typing), not an ABC.
    We intentionally avoid creating an abstract base class to prevent
    premature abstraction. The interface is documented here but
    implementations just need to provide matching methods.
    """
    
    def fetch(self, slug: str) -> Optional[Dict[str, Any]]:
        """
        Fetch question data by slug.
        
        Args:
            slug: Question slug (e.g., "two-sum")
            
        Returns:
            Dictionary with question data, or None if not found
            
        Raises:
            NetworkError: If fetch fails due to network issues
        """
        ...
    
    def is_available(self) -> bool:
        """
        Check if the fetcher is available (dependencies installed, etc.)
        
        Returns:
            True if available, False otherwise
        """
        ...


from .leetscrape_fetcher import LeetscrapeFecher

__all__ = ["BaseFetcher", "LeetscrapeFecher"]

