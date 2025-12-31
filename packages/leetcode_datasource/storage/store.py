"""
Persistent store for leetcode_datasource.

Provides SQLite-based persistent storage for Question data.
Includes problem_index table for fast ID lookups.
"""

import json
import logging
import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

from ..models.question import Question
from ..models.problem_info import ProblemInfo
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
    
    # Problem Index table for fast ID lookups and minimal metadata
    # Data source: LeetCode /api/problems/all/
    PROBLEM_INDEX_SCHEMA_SQL = """
    CREATE TABLE IF NOT EXISTS problem_index (
        frontend_question_id INTEGER PRIMARY KEY,
        title_slug TEXT UNIQUE NOT NULL,
        question_id INTEGER,
        title TEXT NOT NULL,
        difficulty TEXT,
        difficulty_level INTEGER,
        paid_only INTEGER DEFAULT 0,
        url TEXT,
        total_acs INTEGER DEFAULT 0,
        total_submitted INTEGER DEFAULT 0,
        is_new_question INTEGER DEFAULT 0,
        updated_at TEXT
    );
    
    CREATE UNIQUE INDEX IF NOT EXISTS idx_problem_index_slug 
        ON problem_index(title_slug);
    CREATE INDEX IF NOT EXISTS idx_problem_index_question_id 
        ON problem_index(question_id) WHERE question_id IS NOT NULL;
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
            conn.executescript(self.PROBLEM_INDEX_SCHEMA_SQL)
    
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
            "problem_index_count": self.problem_index_count(),
            "db_path": str(self.db_path),
        }
    
    # ========== Problem Index Methods ==========
    
    def _row_to_problem_info(self, row: tuple) -> ProblemInfo:
        """Convert database row to ProblemInfo object.
        
        Schema:
            0: frontend_question_id, 1: title_slug, 2: question_id, 3: title,
            4: difficulty, 5: difficulty_level, 6: paid_only, 7: url,
            8: total_acs, 9: total_submitted, 10: is_new_question, 11: updated_at
        """
        return ProblemInfo(
            frontend_question_id=row[0],
            title_slug=row[1],
            question_id=row[2],
            title=row[3] or "",
            difficulty=row[4] or "",
            difficulty_level=row[5] or 0,
            paid_only=bool(row[6]),
            url=row[7] or "",
            total_acs=row[8] or 0,
            total_submitted=row[9] or 0,
            is_new_question=bool(row[10]),
            updated_at=row[11],
        )
    
    def get_slug_by_frontend_id(self, frontend_id: int) -> Optional[str]:
        """
        Get title_slug by frontend_question_id.
        
        Args:
            frontend_id: Problem number on LeetCode website
            
        Returns:
            title_slug if found, None otherwise
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT title_slug FROM problem_index WHERE frontend_question_id = ?",
                (frontend_id,)
            )
            row = cursor.fetchone()
        return row[0] if row else None
    
    def get_frontend_id_by_slug(self, slug: str) -> Optional[int]:
        """
        Get frontend_question_id by title_slug.
        
        Args:
            slug: Question slug (e.g., "two-sum")
            
        Returns:
            frontend_question_id if found, None otherwise
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT frontend_question_id FROM problem_index WHERE title_slug = ?",
                (slug.lower(),)
            )
            row = cursor.fetchone()
        return row[0] if row else None
    
    def get_problem_info_by_frontend_id(self, frontend_id: int) -> Optional[ProblemInfo]:
        """
        Get ProblemInfo by frontend_question_id.
        
        Args:
            frontend_id: Problem number on LeetCode website
            
        Returns:
            ProblemInfo if found, None otherwise
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT * FROM problem_index WHERE frontend_question_id = ?",
                (frontend_id,)
            )
            row = cursor.fetchone()
        
        if row:
            logger.debug(f"Problem index hit (frontend_id): {frontend_id}")
            return self._row_to_problem_info(row)
        return None
    
    def get_problem_info_by_slug(self, slug: str) -> Optional[ProblemInfo]:
        """
        Get ProblemInfo by title_slug.
        
        Args:
            slug: Question slug (e.g., "two-sum")
            
        Returns:
            ProblemInfo if found, None otherwise
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT * FROM problem_index WHERE title_slug = ?",
                (slug.lower(),)
            )
            row = cursor.fetchone()
        
        if row:
            logger.debug(f"Problem index hit (slug): {slug}")
            return self._row_to_problem_info(row)
        return None
    
    def put_problem_info(self, info: ProblemInfo) -> None:
        """
        Save ProblemInfo to problem_index (insert or update).
        
        Args:
            info: ProblemInfo to save
        """
        now = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO problem_index (
                    frontend_question_id, title_slug, question_id, title,
                    difficulty, difficulty_level, paid_only, url,
                    total_acs, total_submitted, is_new_question, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(frontend_question_id) DO UPDATE SET
                    title_slug = excluded.title_slug,
                    question_id = excluded.question_id,
                    title = excluded.title,
                    difficulty = excluded.difficulty,
                    difficulty_level = excluded.difficulty_level,
                    paid_only = excluded.paid_only,
                    url = excluded.url,
                    total_acs = excluded.total_acs,
                    total_submitted = excluded.total_submitted,
                    is_new_question = excluded.is_new_question,
                    updated_at = excluded.updated_at
            """, (
                info.frontend_question_id,
                info.title_slug.lower(),
                info.question_id,
                info.title,
                info.difficulty,
                info.difficulty_level,
                int(info.paid_only),
                info.url,
                info.total_acs,
                info.total_submitted,
                int(info.is_new_question),
                now,
            ))
    
    def sync_problem_index(self, problems: List[Dict[str, Any]]) -> int:
        """
        Bulk sync problem_index from API data.
        
        Args:
            problems: List of problem dicts from LeetCode API
            
        Returns:
            Number of problems synced
        """
        now = datetime.now().isoformat()
        count = 0
        
        with sqlite3.connect(self.db_path) as conn:
            for p in problems:
                frontend_id = p.get("frontend_question_id")
                slug = p.get("slug", "")
                
                if not frontend_id or not slug:
                    continue
                
                conn.execute("""
                    INSERT INTO problem_index (
                        frontend_question_id, title_slug, question_id, title,
                        difficulty, difficulty_level, paid_only, url,
                        total_acs, total_submitted, is_new_question, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(frontend_question_id) DO UPDATE SET
                        title_slug = excluded.title_slug,
                        question_id = excluded.question_id,
                        title = excluded.title,
                        difficulty = excluded.difficulty,
                        difficulty_level = excluded.difficulty_level,
                        paid_only = excluded.paid_only,
                        url = excluded.url,
                        total_acs = excluded.total_acs,
                        total_submitted = excluded.total_submitted,
                        is_new_question = excluded.is_new_question,
                        updated_at = excluded.updated_at
                """, (
                    frontend_id,
                    slug.lower(),
                    p.get("question_id"),
                    p.get("title", ""),
                    p.get("difficulty", ""),
                    p.get("difficulty_level", 0),
                    int(p.get("paid_only", False)),
                    p.get("url", ""),
                    p.get("total_acs", 0),
                    p.get("total_submitted", 0),
                    int(p.get("is_new_question", False)),
                    now,
                ))
                count += 1
        
        logger.info(f"Synced {count} problems to problem_index")
        return count
    
    def problem_index_count(self) -> int:
        """Get total number of problems in problem_index."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM problem_index")
            return cursor.fetchone()[0]
    
    def problem_index_exists(self, frontend_id: int) -> bool:
        """Check if problem exists in problem_index."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT 1 FROM problem_index WHERE frontend_question_id = ? LIMIT 1",
                (frontend_id,)
            )
            return cursor.fetchone() is not None

