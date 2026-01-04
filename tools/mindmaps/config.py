# tools/mindmaps/config.py
"""Configuration for mind map generation.

This module re-exports all configuration constants, classes, and functions
from core.config to maintain backward compatibility with existing imports.
"""

# Re-export everything from core.config
from .core.config import (
    # Paths
    PROJECT_ROOT,
    ONTOLOGY_DIR,
    META_PROBLEMS_DIR,
    DEFAULT_OUTPUT_DIR,
    PAGES_OUTPUT_DIR,
    CONFIG_FILE,
    META_DESCRIPTIONS_DIR,
    # Defaults
    DEFAULT_GITHUB_REPO_URL,
    DEFAULT_GITHUB_BRANCH,
    DEFAULT_USE_GITHUB_LINKS,
    # Constants
    MINDMAP_TYPES,
    DIFFICULTY_ICONS,
    # Classes
    MindmapsConfig,
    # Functions
    load_config,
    get_config,
)

__all__ = [
    # Paths
    "PROJECT_ROOT",
    "ONTOLOGY_DIR",
    "META_PROBLEMS_DIR",
    "DEFAULT_OUTPUT_DIR",
    "PAGES_OUTPUT_DIR",
    "CONFIG_FILE",
    "META_DESCRIPTIONS_DIR",
    # Defaults
    "DEFAULT_GITHUB_REPO_URL",
    "DEFAULT_GITHUB_BRANCH",
    "DEFAULT_USE_GITHUB_LINKS",
    # Constants
    "MINDMAP_TYPES",
    "DIFFICULTY_ICONS",
    # Classes
    "MindmapsConfig",
    # Functions
    "load_config",
    "get_config",
]

