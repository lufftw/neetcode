# =============================================================================
# Short-Term Memory (STM)
# =============================================================================
# Manages current session context and recent interactions.
# STM is cleared when the program exits.
# =============================================================================

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class MemoryItem:
    """A single item in short-term memory."""
    
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    category: str = "general"
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "category": self.category,
            "metadata": self.metadata,
        }


class ShortTermMemory:
    """
    Short-term memory for current session context.
    
    Stores recent interactions, decisions, and context that agents
    can reference during the current execution.
    
    Features:
    - Fixed-size buffer (oldest items evicted when full)
    - Category-based filtering
    - Automatic timestamping
    """
    
    _instance: ShortTermMemory | None = None
    
    def __new__(cls, max_items: int = 50) -> ShortTermMemory:
        """Singleton pattern for consistent memory access."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, max_items: int = 50):
        """
        Initialize short-term memory.
        
        Args:
            max_items: Maximum number of items to store
        """
        if self._initialized:
            return
        
        self.max_items = max_items
        self._memory: deque[MemoryItem] = deque(maxlen=max_items)
        self._categories: dict[str, deque[MemoryItem]] = {}
        self._initialized = True
    
    def add(
        self,
        content: str,
        category: str = "general",
        metadata: dict[str, Any] | None = None,
    ) -> MemoryItem:
        """
        Add an item to short-term memory.
        
        Args:
            content: Content to remember
            category: Category for filtering (e.g., "decision", "feedback")
            metadata: Additional metadata
            
        Returns:
            The created memory item
        """
        item = MemoryItem(
            content=content,
            category=category,
            metadata=metadata or {},
        )
        
        self._memory.append(item)
        
        # Also add to category-specific storage
        if category not in self._categories:
            self._categories[category] = deque(maxlen=self.max_items)
        self._categories[category].append(item)
        
        return item
    
    def get_recent(
        self,
        n: int = 10,
        category: str | None = None,
    ) -> list[MemoryItem]:
        """
        Get the most recent memory items.
        
        Args:
            n: Number of items to retrieve
            category: Optional category filter
            
        Returns:
            List of recent memory items
        """
        if category and category in self._categories:
            items = list(self._categories[category])
        else:
            items = list(self._memory)
        
        return items[-n:]
    
    def search(
        self,
        keyword: str,
        category: str | None = None,
    ) -> list[MemoryItem]:
        """
        Search memory for items containing a keyword.
        
        Args:
            keyword: Keyword to search for
            category: Optional category filter
            
        Returns:
            List of matching memory items
        """
        if category and category in self._categories:
            items = self._categories[category]
        else:
            items = self._memory
        
        keyword_lower = keyword.lower()
        return [
            item for item in items
            if keyword_lower in item.content.lower()
        ]
    
    def get_context_string(
        self,
        n: int = 5,
        category: str | None = None,
    ) -> str:
        """
        Get recent memory as a formatted context string.
        
        Useful for including in prompts.
        
        Args:
            n: Number of items to include
            category: Optional category filter
            
        Returns:
            Formatted string of recent memory
        """
        items = self.get_recent(n, category)
        
        if not items:
            return "No relevant context in memory."
        
        lines = []
        for item in items:
            time_str = item.timestamp.strftime("%H:%M:%S")
            lines.append(f"[{time_str}] [{item.category}] {item.content}")
        
        return "\n".join(lines)
    
    def clear(self, category: str | None = None) -> None:
        """
        Clear memory.
        
        Args:
            category: If provided, only clear this category
        """
        if category:
            if category in self._categories:
                self._categories[category].clear()
        else:
            self._memory.clear()
            self._categories.clear()
    
    def __len__(self) -> int:
        return len(self._memory)
    
    def __repr__(self) -> str:
        return f"ShortTermMemory(items={len(self)}, max={self.max_items})"


# Global instance
_stm: ShortTermMemory | None = None


def get_stm(max_items: int = 50) -> ShortTermMemory:
    """
    Get the global short-term memory instance.
    
    Args:
        max_items: Maximum items (only used on first call)
        
    Returns:
        ShortTermMemory instance
    """
    global _stm
    if _stm is None:
        _stm = ShortTermMemory(max_items)
    return _stm


def update_stm(
    content: str,
    category: str = "general",
    metadata: dict[str, Any] | None = None,
) -> MemoryItem:
    """
    Add content to short-term memory.
    
    Convenience function for quick memory updates.
    
    Args:
        content: Content to remember
        category: Category for filtering
        metadata: Additional metadata
        
    Returns:
        Created memory item
    """
    return get_stm().add(content, category, metadata)


def get_recent_stm(
    n: int = 10,
    category: str | None = None,
) -> list[MemoryItem]:
    """
    Get recent items from short-term memory.
    
    Convenience function.
    
    Args:
        n: Number of items
        category: Optional category filter
        
    Returns:
        List of memory items
    """
    return get_stm().get_recent(n, category)

