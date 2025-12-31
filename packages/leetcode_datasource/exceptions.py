"""
Custom exceptions for leetcode_datasource package.

Exception Hierarchy:
    LeetCodeDataSourceError (base)
    ├── QuestionNotFoundError
    ├── NetworkError
    ├── ParseError
    └── ConfigError
"""


class LeetCodeDataSourceError(Exception):
    """Base exception for all leetcode_datasource errors."""
    pass


class QuestionNotFoundError(LeetCodeDataSourceError):
    """Raised when a question cannot be found (cache miss + network fail)."""
    
    def __init__(self, identifier: str, message: str = None):
        self.identifier = identifier
        super().__init__(message or f"Question not found: {identifier}")


class NetworkError(LeetCodeDataSourceError):
    """Raised when a network/fetch operation fails."""
    
    def __init__(self, message: str, cause: Exception = None):
        self.cause = cause
        super().__init__(message)


class ParseError(LeetCodeDataSourceError):
    """Raised when data parsing fails."""
    
    def __init__(self, message: str, data: any = None):
        self.data = data
        super().__init__(message)


class ConfigError(LeetCodeDataSourceError):
    """Raised when configuration is invalid."""
    pass

