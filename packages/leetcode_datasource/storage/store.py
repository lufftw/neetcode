"""
Persistent store for leetcode_datasource.

Provides SQLite-based persistent storage for Question data.
"""

import json
import logging
import sqlite3
from pathlib import Path
from typing import Optional, List
from datetime import datetime

from ..models.question import Question
from ..models.schema import SCHEMA_VERSION

logger = logging.getLogger(__name__)


class Store:
    """
    Persistent SQLite store for Question data.
    
    Features:
        - SQLite-based storage
        - Lookup by slug or frontend_question_id
        - Schema versioning support
    """
    
    # Schema compatible with existing tools/leetcode-api database
    # Note: qid is used as frontend_question_id in existing data
    SCHEMA_SQL = """
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
    );
    
    CREATE INDEX IF NOT EXISTS idx_qid ON questions(qid);
    CREATE INDEX IF NOT EXISTS idx_title_slug ON questions(title_slug);
    """
    
    def __init__(self, store_dir: Path):
        """
        Initialize store.
        
        Args:
            store_dir: Directory to store SQLite database
        """
        self.store_dir = store_dir
        self.db_path = store_dir / "leetcode.sqlite3"
        self._ensure_dir()
        self._init_db()
    
    def _ensure_dir(self) -> None:
        """Ensure store directory exists."""
        self.store_dir.mkdir(parents=True, exist_ok=True)
    
    def _init_db(self) -> None:
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(self.SCHEMA_SQL)
    
    def _row_to_question(self, row: tuple) -> Question:
        """Convert database row to Question object.
        
        Schema (compatible with existing tools/leetcode-api):
            0: id, 1: qid, 2: title, 3: title_slug, 4: difficulty,
            5: acceptance_rate, 6: paid_only, 7: topic_tags, 8: category_slug,
            9: hints, 10: companies, 11: similar_questions, 12: code, 13: body,
            14: is_paid_only, 15: created_at, 16: updated_at
        
        Note: qid is used as frontend_question_id in existing data.
        """
        qid = row[1]  # qid is the frontend_question_id
        return Question(
            QID=qid,  # Use qid for both QID and frontend_question_id
            frontend_question_id=qid,
            title=row[2],
            titleSlug=row[3],
            difficulty=row[4] or "",
            acceptanceRate=row[5] or 0.0,
            isPaidOnly=bool(row[6]) or bool(row[14]),  # Check both paid_only and is_paid_only
            topicTags=row[7] or "",
            categorySlug=row[8] or "",
            Hints=json.loads(row[9]) if row[9] else [],
            Companies=json.loads(row[10]) if row[10] else None,
            SimilarQuestions=json.loads(row[11]) if row[11] else [],
            Code=row[12] or "",
            Body=row[13] or "",
            _schema_version=SCHEMA_VERSION,
            _from_cache=True,
        )
    
    def get_by_slug(self, slug: str) -> Optional[Question]:
        """
        Get question by slug.
        
        Args:
            slug: Question slug (e.g., "two-sum")
            
        Returns:
            Question if found, None otherwise
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT * FROM questions WHERE title_slug = ?",
                (slug.lower(),)
            )
            row = cursor.fetchone()
            
        if row:
            logger.debug(f"Store hit (slug): {slug}")
            return self._row_to_question(row)
        return None
    
    def get_by_frontend_id(self, frontend_id: int) -> Optional[Question]:
        """
        Get question by frontend question ID.
        
        Args:
            frontend_id: Problem number on LeetCode website
            
        Returns:
            Question if found, None otherwise
        """
        with sqlite3.connect(self.db_path) as conn:
            # Note: qid column stores frontend_question_id in existing schema
            cursor = conn.execute(
                "SELECT * FROM questions WHERE qid = ?",
                (frontend_id,)
            )
            row = cursor.fetchone()
            
        if row:
            logger.debug(f"Store hit (frontend_id): {frontend_id}")
            return self._row_to_question(row)
        return None
    
    def put(self, question: Question) -> None:
        """
        Save question to store (insert or update).
        
        Args:
            question: Question to save
        """
        now = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            # Schema compatible with existing tools/leetcode-api database
            # Note: qid stores frontend_question_id
            conn.execute("""
                INSERT INTO questions (
                    qid, title, title_slug, difficulty,
                    acceptance_rate, paid_only, topic_tags, category_slug,
                    hints, companies, similar_questions, code, body,
                    is_paid_only, updated_at
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
                question.frontend_question_id,  # qid = frontend_question_id
                question.title,
                question.titleSlug.lower(),
                question.difficulty,
                question.acceptanceRate,
                int(question.isPaidOnly),
                question.topicTags,
                question.categorySlug,
                json.dumps(question.Hints, ensure_ascii=False),
                json.dumps(question.Companies, ensure_ascii=False) if question.Companies else None,
                json.dumps(question.SimilarQuestions),
                question.Code,
                question.Body,
                int(question.isPaidOnly),  # is_paid_only
                now,
            ))
        
        logger.debug(f"Stored: {question.titleSlug}")
    
    def count(self) -> int:
        """Get total number of questions in store."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM questions")
            return cursor.fetchone()[0]
    
    def exists(self, slug: str) -> bool:
        """Check if question exists in store."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT 1 FROM questions WHERE title_slug = ? LIMIT 1",
                (slug.lower(),)
            )
            return cursor.fetchone() is not None
    
    def delete(self, slug: str) -> bool:
        """
        Delete question from store.
        
        Args:
            slug: Question slug
            
        Returns:
            True if deleted, False if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM questions WHERE title_slug = ?",
                (slug.lower(),)
            )
            return cursor.rowcount > 0
    
    def stats(self) -> dict:
        """Get store statistics."""
        return {
            "total_questions": self.count(),
            "db_path": str(self.db_path),
        }

