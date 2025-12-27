# tools/patterndocs/mapping.py
"""Unified Directory Name → API Kernel ID mapping for pattern documentation generation.

This module provides access to the centralized mapping between pattern directory names
and their corresponding API Kernel IDs. The mapping is loaded from 
tools/generate_pattern_docs.toml, which serves as the single source of truth.

All mappings should be defined in generate_pattern_docs.toml for easy maintenance.
"""

from .config import load_generator_config

# Cache for mappings
_mapping_cache: dict[str, str] | None = None


def _load_mappings() -> dict[str, str]:
    """Load mappings from config file."""
    global _mapping_cache
    if _mapping_cache is not None:
        return _mapping_cache
    
    config = load_generator_config()
    _mapping_cache = config.get("kernel_mapping", {})
    return _mapping_cache


def get_kernel_id(dir_name: str) -> str:
    """
    Get API Kernel ID for a given directory name.
    
    Args:
        dir_name: Pattern directory name (e.g., "sliding_window")
        
    Returns:
        API Kernel ID (e.g., "SubstringSlidingWindow")
        Returns dir_name if mapping not found (fallback)
    """
    mappings = _load_mappings()
    return mappings.get(dir_name, dir_name)


def get_all_mappings() -> dict[str, str]:
    """
    Get all directory-to-kernel mappings from config file.
    
    Returns:
        Dictionary mapping directory names to kernel IDs
    """
    return _load_mappings().copy()


def has_mapping(dir_name: str) -> bool:
    """
    Check if a mapping exists for a directory name.
    
    Args:
        dir_name: Pattern directory name
        
    Returns:
        True if mapping exists, False otherwise
    """
    mappings = _load_mappings()
    return dir_name in mappings


def reload_mappings() -> None:
    """Reload mappings from config file (clears cache)."""
    global _mapping_cache
    _mapping_cache = None

