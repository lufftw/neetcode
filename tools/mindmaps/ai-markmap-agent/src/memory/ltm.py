# =============================================================================
# Long-Term Memory (LTM)
# =============================================================================
# Persistent memory using vector store for semantic retrieval.
# Stores decisions, patterns, and learnings across sessions.
# =============================================================================

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

from langchain_openai import OpenAIEmbeddings

from ..config_loader import ConfigLoader


class LongTermMemory:
    """
    Long-term memory using ChromaDB vector store.
    
    Features:
    - Semantic search for relevant past decisions
    - Persistent storage across sessions
    - Automatic embedding generation
    """
    
    _instance: LongTermMemory | None = None
    
    def __new__(cls, config: dict[str, Any] | None = None) -> LongTermMemory:
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, config: dict[str, Any] | None = None):
        """
        Initialize long-term memory.
        
        Args:
            config: Configuration dictionary
        """
        if self._initialized:
            return
        
        self.config = config or ConfigLoader.get_config()
        memory_config = self.config.get("memory", {}).get("ltm", {})
        
        self.enabled = memory_config.get("enabled", True) and CHROMADB_AVAILABLE
        self.collection_name = memory_config.get("collection_name", "markmap_decisions")
        
        if not self.enabled:
            self._initialized = True
            return
        
        # Initialize ChromaDB
        chromadb_config = memory_config.get("chromadb", {})
        persist_dir = chromadb_config.get("persist_directory", "./data/chromadb")
        
        # Resolve persist directory
        base_dir = Path(__file__).parent.parent.parent
        self.persist_path = base_dir / persist_dir
        self.persist_path.mkdir(parents=True, exist_ok=True)
        
        # Create ChromaDB client
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=str(self.persist_path),
            anonymized_telemetry=False,
        ))
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "AI Markmap Agent decisions and learnings"}
        )
        
        # Embedding model
        embedding_model = memory_config.get("embedding_model", "text-embedding-3-small")
        api_key = ConfigLoader.get_api_key("openai")
        
        if api_key:
            self.embeddings = OpenAIEmbeddings(
                model=embedding_model,
                api_key=api_key,
            )
        else:
            self.embeddings = None
        
        # Retrieval settings
        retrieval_config = memory_config.get("retrieval", {})
        self.k = retrieval_config.get("k", 5)
        self.score_threshold = retrieval_config.get("score_threshold", 0.7)
        
        self._initialized = True
    
    def store(
        self,
        content: str,
        category: str = "decision",
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """
        Store content in long-term memory.
        
        Args:
            content: Content to store
            category: Category (e.g., "decision", "pattern", "feedback")
            metadata: Additional metadata
            
        Returns:
            Document ID
        """
        if not self.enabled:
            return ""
        
        # Generate unique ID
        doc_id = self._generate_id(content)
        
        # Prepare metadata
        full_metadata = {
            "category": category,
            "timestamp": datetime.now().isoformat(),
            **(metadata or {}),
        }
        
        # Generate embedding if available
        if self.embeddings:
            try:
                embedding = self.embeddings.embed_query(content)
                self.collection.add(
                    ids=[doc_id],
                    embeddings=[embedding],
                    documents=[content],
                    metadatas=[full_metadata],
                )
            except Exception as e:
                print(f"Warning: Failed to store in LTM: {e}")
                return ""
        else:
            # Store without embedding
            self.collection.add(
                ids=[doc_id],
                documents=[content],
                metadatas=[full_metadata],
            )
        
        return doc_id
    
    def query(
        self,
        query_text: str,
        n_results: int | None = None,
        category: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Query long-term memory for relevant items.
        
        Args:
            query_text: Query string
            n_results: Number of results (defaults to config.k)
            category: Optional category filter
            
        Returns:
            List of relevant memory items
        """
        if not self.enabled:
            return []
        
        n_results = n_results or self.k
        
        # Build where clause for filtering
        where = None
        if category:
            where = {"category": category}
        
        try:
            # Query with embedding if available
            if self.embeddings:
                query_embedding = self.embeddings.embed_query(query_text)
                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=n_results,
                    where=where,
                )
            else:
                results = self.collection.query(
                    query_texts=[query_text],
                    n_results=n_results,
                    where=where,
                )
        except Exception as e:
            print(f"Warning: LTM query failed: {e}")
            return []
        
        # Format results
        items = []
        if results and results.get("documents"):
            documents = results["documents"][0]
            metadatas = results.get("metadatas", [[]])[0]
            distances = results.get("distances", [[]])[0]
            
            for i, doc in enumerate(documents):
                items.append({
                    "content": doc,
                    "metadata": metadatas[i] if i < len(metadatas) else {},
                    "score": 1 - distances[i] if i < len(distances) else 0,
                })
        
        # Filter by score threshold
        items = [
            item for item in items
            if item.get("score", 0) >= self.score_threshold
        ]
        
        return items
    
    def get_context_string(
        self,
        query_text: str,
        n_results: int = 3,
        category: str | None = None,
    ) -> str:
        """
        Get relevant long-term memory as a context string.
        
        Useful for including in prompts.
        
        Args:
            query_text: Query to find relevant memories
            n_results: Number of results
            category: Optional category filter
            
        Returns:
            Formatted context string
        """
        items = self.query(query_text, n_results, category)
        
        if not items:
            return "No relevant past decisions found."
        
        lines = []
        for item in items:
            meta = item.get("metadata", {})
            category = meta.get("category", "general")
            timestamp = meta.get("timestamp", "unknown")
            score = item.get("score", 0)
            
            lines.append(
                f"[{category}] (relevance: {score:.2f})\n"
                f"{item.get('content', '')[:300]}..."
            )
        
        return "\n\n---\n\n".join(lines)
    
    def _generate_id(self, content: str) -> str:
        """Generate a unique ID for content."""
        timestamp = datetime.now().isoformat()
        hash_input = f"{content}{timestamp}".encode()
        return hashlib.sha256(hash_input).hexdigest()[:16]
    
    def clear(self) -> None:
        """Clear all long-term memory (use with caution)."""
        if not self.enabled:
            return
        
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "AI Markmap Agent decisions and learnings"}
            )
        except Exception as e:
            print(f"Warning: Failed to clear LTM: {e}")
    
    def __len__(self) -> int:
        if not self.enabled:
            return 0
        try:
            return self.collection.count()
        except Exception:
            return 0
    
    def __repr__(self) -> str:
        return f"LongTermMemory(items={len(self)}, enabled={self.enabled})"


# Global instance
_ltm: LongTermMemory | None = None


def get_ltm(config: dict[str, Any] | None = None) -> LongTermMemory:
    """
    Get the global long-term memory instance.
    
    Args:
        config: Configuration (only used on first call)
        
    Returns:
        LongTermMemory instance
    """
    global _ltm
    if _ltm is None:
        _ltm = LongTermMemory(config)
    return _ltm


def query_ltm(
    query_text: str,
    n_results: int = 5,
    category: str | None = None,
) -> list[dict[str, Any]]:
    """
    Query long-term memory.
    
    Convenience function.
    
    Args:
        query_text: Query string
        n_results: Number of results
        category: Optional category filter
        
    Returns:
        List of relevant items
    """
    return get_ltm().query(query_text, n_results, category)


def store_to_ltm(
    content: str,
    category: str = "decision",
    metadata: dict[str, Any] | None = None,
) -> str:
    """
    Store content in long-term memory.
    
    Convenience function.
    
    Args:
        content: Content to store
        category: Category
        metadata: Additional metadata
        
    Returns:
        Document ID
    """
    return get_ltm().store(content, category, metadata)

