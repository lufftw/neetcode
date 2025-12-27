# tools/patterndocs/config.py
"""Configuration loading for pattern documentation generator."""

from __future__ import annotations
from pathlib import Path

from .toml_parser import parse_toml_simple

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = PROJECT_ROOT / "tools" / "patterndocs" / "generate_pattern_docs.toml"

# Load configuration cache
_config_cache: dict | None = None


def load_generator_config() -> dict:
    """Load generator configuration from generate_pattern_docs.toml."""
    global _config_cache
    if _config_cache is not None:
        return _config_cache
    
    if not CONFIG_FILE.exists():
        print(f"Warning: Config file not found: {CONFIG_FILE}")
        print("Using default configuration")
        _config_cache = {}
        return _config_cache
    
    try:
        content = CONFIG_FILE.read_text(encoding="utf-8")
        _config_cache = parse_toml_simple(content)
        return _config_cache
    except Exception as e:
        print(f"Warning: Failed to parse config file {CONFIG_FILE}: {e}")
        print("Using default configuration")
        _config_cache = {}
        return _config_cache


def get_paths() -> dict[str, Path]:
    """Get path configuration from config file or return defaults."""
    config = load_generator_config()
    
    paths_config = config.get("paths", {})
    
    return {
        "ontology_dir": PROJECT_ROOT / paths_config.get("ontology_dir", "ontology"),
        "meta_patterns_dir": PROJECT_ROOT / paths_config.get("meta_patterns_dir", "meta/patterns"),
        "output_dir": PROJECT_ROOT / paths_config.get("output_dir", "docs/patterns"),
    }

