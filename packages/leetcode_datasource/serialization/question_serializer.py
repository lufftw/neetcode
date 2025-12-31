"""
Question serialization/deserialization.

Handles conversion between Question objects and dict/JSON formats,
with support for schema versioning and migration.
"""

from typing import Dict, Any, Optional
from datetime import datetime

from ..models.question import Question
from ..models.schema import SCHEMA_VERSION, migrate_question_data


class QuestionSerializer:
    """
    Serializer for Question objects.
    
    Supports:
        - Question <-> dict conversion
        - LeetScrape format compatibility
        - Schema versioning
    """
    
    @staticmethod
    def to_dict(question: Question) -> Dict[str, Any]:
        """
        Serialize Question to dictionary.
        
        Args:
            question: Question object
            
        Returns:
            Dictionary representation
        """
        return {
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
            "_cached_at": question._cached_at,
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Question:
        """
        Deserialize dictionary to Question.
        
        Args:
            data: Dictionary with question data
            
        Returns:
            Question object
        """
        # Check schema version and migrate if needed
        schema_version = data.get("_schema_version", "1.0")
        if schema_version != SCHEMA_VERSION:
            data = migrate_question_data(data, schema_version)
        
        return Question(
            QID=data.get("QID", 0),
            frontend_question_id=data.get("frontend_question_id", 0),
            title=data.get("title", ""),
            titleSlug=data.get("titleSlug", ""),
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
            _schema_version=SCHEMA_VERSION,
            _cached_at=data.get("_cached_at"),
            _from_cache=True,
        )
    
    @staticmethod
    def from_leetscrape(ls_question: Any) -> Question:
        """
        Convert LeetScrape Question to our Question format.
        
        Args:
            ls_question: LeetScrape Question object
            
        Returns:
            Question object
        """
        # Handle both object and dict formats
        if isinstance(ls_question, dict):
            data = ls_question
        else:
            # LeetScrape Question object
            data = {
                "QID": getattr(ls_question, "QID", 0),
                "title": getattr(ls_question, "title", ""),
                "titleSlug": getattr(ls_question, "titleSlug", ""),
                "difficulty": getattr(ls_question, "difficulty", ""),
                "Body": getattr(ls_question, "Body", ""),
                "Code": getattr(ls_question, "Code", ""),
                "Hints": getattr(ls_question, "Hints", []),
                "acceptanceRate": getattr(ls_question, "acceptanceRate", 0.0),
                "topicTags": getattr(ls_question, "topicTags", ""),
                "categorySlug": getattr(ls_question, "categorySlug", ""),
                "isPaidOnly": getattr(ls_question, "isPaidOnly", False) or getattr(ls_question, "paidOnly", False),
                "SimilarQuestions": getattr(ls_question, "SimilarQuestions", []),
                "Companies": getattr(ls_question, "Companies", None),
            }
        
        # Note: LeetScrape uses QID as the question_id
        # We need to separately track frontend_question_id
        # This may need to be populated from another source
        frontend_id = data.get("frontend_question_id", data.get("QID", 0))
        
        return Question(
            QID=data.get("QID", 0),
            frontend_question_id=frontend_id,
            title=data.get("title", ""),
            titleSlug=data.get("titleSlug", ""),
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
            _schema_version=SCHEMA_VERSION,
            _cached_at=datetime.now().isoformat(),
            _from_cache=False,
        )
    
    @staticmethod
    def is_valid(data: Dict[str, Any]) -> bool:
        """
        Check if dictionary has required fields for a valid Question.
        
        Args:
            data: Dictionary to validate
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ["titleSlug", "title"]
        return all(field in data and data[field] for field in required_fields)


# Convenience functions
def serialize(question: Question) -> Dict[str, Any]:
    """Serialize Question to dictionary."""
    return QuestionSerializer.to_dict(question)


def deserialize(data: Dict[str, Any]) -> Question:
    """Deserialize dictionary to Question."""
    return QuestionSerializer.from_dict(data)

