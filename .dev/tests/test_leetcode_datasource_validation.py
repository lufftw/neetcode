"""
Phase 4 Validation Tests for leetcode_datasource package.

Run with: pytest .dev/tests/test_leetcode_datasource_validation.py -v
"""

import pytest
from pathlib import Path


class TestLeetCodeDataSourceValidation:
    """Validation tests for the leetcode_datasource package."""
    
    def test_import_from_package(self):
        """Test that package can be imported."""
        from leetcode_datasource import LeetCodeDataSource, Question
        from leetcode_datasource.exceptions import (
            LeetCodeDataSourceError,
            QuestionNotFoundError,
        )
        assert LeetCodeDataSource is not None
        assert Question is not None
    
    def test_datasource_initialization(self):
        """Test DataSource initializes correctly."""
        from leetcode_datasource import LeetCodeDataSource
        
        ds = LeetCodeDataSource()
        assert ds is not None
        assert ds.store is not None
        assert ds.config is not None
    
    def test_store_has_data(self):
        """Test that migrated data exists in store."""
        from leetcode_datasource import LeetCodeDataSource
        
        ds = LeetCodeDataSource()
        count = ds.store.count()
        assert count > 2000, f"Expected 2000+ questions, got {count}"
    
    def test_get_by_slug(self):
        """Test get_by_slug retrieves correct question."""
        from leetcode_datasource import LeetCodeDataSource
        
        ds = LeetCodeDataSource()
        q = ds.get_by_slug("two-sum")
        
        assert q is not None
        assert q.title == "Two Sum"
        assert q.titleSlug == "two-sum"
        assert q.frontend_question_id == 1
        assert q.difficulty == "Easy"
    
    def test_get_by_frontend_id(self):
        """Test get_by_frontend_id retrieves correct question."""
        from leetcode_datasource import LeetCodeDataSource
        
        ds = LeetCodeDataSource()
        q = ds.get_by_frontend_id(922)
        
        assert q is not None
        assert q.title == "Sort Array By Parity II"
        assert q.titleSlug == "sort-array-by-parity-ii"
        assert q.frontend_question_id == 922
    
    def test_frontend_id_is_not_internal_id(self):
        """Verify frontend_id != internal question_id for problem 922."""
        from leetcode_datasource import LeetCodeDataSource
        
        ds = LeetCodeDataSource()
        # Problem 922 has internal question_id 958, but frontend_id 922
        q = ds.get_by_frontend_id(922)
        
        assert q.frontend_question_id == 922
        # This confirms we're using frontend_id, not internal id
    
    def test_exists(self):
        """Test exists() method."""
        from leetcode_datasource import LeetCodeDataSource
        
        ds = LeetCodeDataSource()
        assert ds.exists("two-sum") is True
        assert ds.exists("nonexistent-problem-xyz") is False
    
    def test_question_fields(self):
        """Test that Question has all expected fields."""
        from leetcode_datasource import LeetCodeDataSource
        
        ds = LeetCodeDataSource()
        q = ds.get_by_slug("two-sum")
        
        # Required fields
        assert hasattr(q, 'QID')
        assert hasattr(q, 'frontend_question_id')
        assert hasattr(q, 'title')
        assert hasattr(q, 'titleSlug')
        assert hasattr(q, 'difficulty')
        
        # Content fields
        assert hasattr(q, 'Body')
        assert hasattr(q, 'Code')
        assert hasattr(q, 'Hints')
        
        # Metadata fields
        assert hasattr(q, 'acceptanceRate')
        assert hasattr(q, 'topicTags')
        assert hasattr(q, 'isPaidOnly')
    
    def test_stats(self):
        """Test stats() returns expected structure."""
        from leetcode_datasource import LeetCodeDataSource
        
        ds = LeetCodeDataSource()
        stats = ds.stats()
        
        assert 'total_questions' in stats
        assert 'config' in stats
        assert stats['total_questions'] > 2000
    
    def test_data_dir_is_neetcode(self):
        """Test that data directory is .neetcode in repo root."""
        from leetcode_datasource import LeetCodeDataSource
        
        ds = LeetCodeDataSource()
        data_dir = ds.config.data_dir
        
        assert data_dir.name == ".neetcode"
        assert (data_dir / "leetcode_datasource" / "store").exists()


class TestImportFromDifferentLocations:
    """Test that import works from different directories."""
    
    def test_import_works(self):
        """Basic import test - runs from .dev/tests/ directory."""
        from leetcode_datasource import LeetCodeDataSource
        ds = LeetCodeDataSource()
        assert ds.store.count() > 0

