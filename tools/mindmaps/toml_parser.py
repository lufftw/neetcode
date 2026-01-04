# tools/mindmaps/toml_parser.py
"""TOML parser for mind map configuration.

This module re-exports all TOML parsing functions from core.toml_parser
to maintain backward compatibility with existing imports.
"""

# Re-export everything from core.toml_parser
from .core.toml_parser import (
    parse_toml_simple,
    strip_inline_comment,
    parse_toml_value,
)

__all__ = [
    "parse_toml_simple",
    "strip_inline_comment",
    "parse_toml_value",
]

