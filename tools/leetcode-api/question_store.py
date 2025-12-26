#!/usr/bin/env python3
"""
Question Store - SQLite-backed storage for LeetCode questions.

This module provides persistent storage for LeetCode question data,
enabling caching to avoid redundant API calls and improve performance.

Architecture:
    - Storage layer only - no business logic
    - Handles schema management, CRUD operations
    - Uses titleSlug as unique identifier
"""

import sqlite3
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

# Default database location
DEFAULT_DB_PATH = Path(__file__).parent / "db" / "leetcode.db"


class QuestionStore:
    """SQLite-backed storage for LeetCode questions."""
    
    # Current schema version for migrations
    SCHEMA_VERSION = 1
    
    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize the question store.
        
        Args:
            db_path: Path to SQLite database. Defaults to tools/.cache/leetcode_questions.db
        """
        self.db_path = db_path or DEFAULT_DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_db(self) -> None:
        """Initialize database schema.
        
        Schema matches LeetScrape JSON format:
        https://raw.githubusercontent.com/nikhil-ravi/LeetScrape/refs/heads/main/example/data/all.json
        """
        with self._get_connection() as conn:
            # Create questions table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    qid INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    title_slug TEXT NOT NULL UNIQUE,
                    difficulty TEXT,
                    acceptance_rate REAL,
                    paid_only INTEGER DEFAULT 0,
                    topic_tags TEXT,
                    category_slug TEXT,
                    hints TEXT,
                    companies TEXT,
                    similar_questions TEXT,
                    code TEXT,
                    body TEXT,
                    is_paid_only INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create index on title_slug for fast lookups
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_title_slug ON questions(title_slug)
            """)
            
            # Create index on qid for lookups by question ID
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_qid ON questions(qid)
            """)
            
            # Schema version table for future migrations
            conn.execute("""
                CREATE TABLE IF NOT EXISTS schema_version (
                    version INTEGER PRIMARY KEY
                )
            """)
            
            # Set initial schema version if not exists
            cursor = conn.execute("SELECT version FROM schema_version LIMIT 1")
            if cursor.fetchone() is None:
                conn.execute("INSERT INTO schema_version (version) VALUES (?)", 
                           (self.SCHEMA_VERSION,))
            
            conn.commit()
    
    def exists(self, title_slug: str) -> bool:
        """
        Check if a question exists in the store.
        
        Args:
            title_slug: The unique slug identifier (e.g., 'two-sum')
            
        Returns:
            True if question exists, False otherwise
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT 1 FROM questions WHERE title_slug = ? LIMIT 1",
                (title_slug,)
            )
            return cursor.fetchone() is not None
    
    def get_by_slug(self, title_slug: str) -> Optional[Dict[str, Any]]:
        """
        Get a question by its slug.
        
        Args:
            title_slug: The unique slug identifier (e.g., 'two-sum')
            
        Returns:
            Dictionary with question data, or None if not found
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM questions WHERE title_slug = ?",
                (title_slug,)
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return self._row_to_dict(row)
    
    def get_by_qid(self, qid: str) -> Optional[Dict[str, Any]]:
        """
        Get a question by its LeetCode QID.
        
        Args:
            qid: The LeetCode question ID (e.g., '1', '23')
            
        Returns:
            Dictionary with question data, or None if not found
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM questions WHERE qid = ?",
                (str(qid),)
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return self._row_to_dict(row)
    
    def save(self, data: Dict[str, Any]) -> None:
        """
        Save or update a question in the store.
        
        Uses title_slug as unique key. If exists, updates; otherwise inserts.
        
        Schema matches LeetScrape JSON format:
        https://raw.githubusercontent.com/nikhil-ravi/LeetScrape/refs/heads/main/example/data/all.json
        
        Args:
            data: Dictionary containing question data with at least:
                  - title_slug (required)
                  - qid (int)
                  - title (str)
                  - difficulty (str)
                  - acceptance_rate (float)
                  - paid_only (bool)
                  - topic_tags (str, comma-separated)
                  - category_slug (str)
                  - hints (list of str)
                  - companies (list or None)
                  - similar_questions (list of int QIDs)
                  - code (str)
                  - body (str, HTML)
                  - is_paid_only (bool)
        """
        title_slug = data.get('title_slug')
        if not title_slug:
            raise ValueError("title_slug is required")
        
        # Serialize list fields to JSON
        hints = json.dumps(data.get('hints', []))
        companies = json.dumps(data.get('companies') or [])
        similar_questions = json.dumps(data.get('similar_questions', []))
        
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO questions (
                    qid, title, title_slug, difficulty, acceptance_rate,
                    paid_only, topic_tags, category_slug, hints, companies,
                    similar_questions, code, body, is_paid_only, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(title_slug) DO UPDATE SET
                    qid = excluded.qid,
                    title = excluded.title,
                    difficulty = excluded.difficulty,
                    acceptance_rate = excluded.acceptance_rate,
                    paid_only = excluded.paid_only,
                    topic_tags = excluded.topic_tags,
                    category_slug = excluded.category_slug,
                    hints = excluded.hints,
                    companies = excluded.companies,
                    similar_questions = excluded.similar_questions,
                    code = excluded.code,
                    body = excluded.body,
                    is_paid_only = excluded.is_paid_only,
                    updated_at = excluded.updated_at
            """, (
                int(data.get('qid', 0)),
                data.get('title', ''),
                title_slug,
                data.get('difficulty', ''),
                float(data.get('acceptance_rate', 0.0)),
                1 if data.get('paid_only') else 0,
                data.get('topic_tags', ''),
                data.get('category_slug', ''),
                hints,
                companies,
                similar_questions,
                data.get('code', ''),
                data.get('body', ''),
                1 if data.get('is_paid_only') else 0,
                datetime.now().isoformat()
            ))
            conn.commit()
    
    def delete(self, title_slug: str) -> bool:
        """
        Delete a question from the store.
        
        Args:
            title_slug: The unique slug identifier
            
        Returns:
            True if deleted, False if not found
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM questions WHERE title_slug = ?",
                (title_slug,)
            )
            conn.commit()
            return cursor.rowcount > 0
    
    def list_all(self) -> List[Dict[str, Any]]:
        """
        List all questions in the store.
        
        Returns:
            List of question dictionaries
        """
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM questions ORDER BY qid")
            return [self._row_to_dict(row) for row in cursor.fetchall()]
    
    def count(self) -> int:
        """
        Get the total number of questions in the store.
        
        Returns:
            Number of questions
        """
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM questions")
            return cursor.fetchone()[0]
    
    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """
        Convert a database row to a dictionary with deserialized JSON fields.
        
        Returns data matching LeetScrape JSON format:
        https://raw.githubusercontent.com/nikhil-ravi/LeetScrape/refs/heads/main/example/data/all.json
        
        Args:
            row: SQLite Row object
            
        Returns:
            Dictionary with deserialized data
        """
        return {
            'qid': row['qid'],
            'title': row['title'],
            'title_slug': row['title_slug'],
            'difficulty': row['difficulty'],
            'acceptance_rate': row['acceptance_rate'],
            'paid_only': bool(row['paid_only']),
            'topic_tags': row['topic_tags'] or '',
            'category_slug': row['category_slug'] or '',
            'hints': json.loads(row['hints']) if row['hints'] else [],
            'companies': json.loads(row['companies']) if row['companies'] else None,
            'similar_questions': json.loads(row['similar_questions']) if row['similar_questions'] else [],
            'code': row['code'] or '',
            'body': row['body'] or '',
            'is_paid_only': bool(row['is_paid_only']),
            'created_at': row['created_at'],
            'updated_at': row['updated_at'],
        }


# Module-level convenience functions
_default_store: Optional[QuestionStore] = None


def get_default_store() -> QuestionStore:
    """Get the default QuestionStore instance (singleton)."""
    global _default_store
    if _default_store is None:
        _default_store = QuestionStore()
    return _default_store


if __name__ == "__main__":
    # Simple test
    store = QuestionStore()
    print(f"Database: {store.db_path}")
    print(f"Questions in store: {store.count()}")

