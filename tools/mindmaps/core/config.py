# tools/mindmaps/config.py
"""Configuration for mind map generation."""

from __future__ import annotations
import os
from dataclasses import dataclass, field
from pathlib import Path

from .toml_parser import parse_toml_simple

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ONTOLOGY_DIR = PROJECT_ROOT / "ontology"
META_PROBLEMS_DIR = PROJECT_ROOT / "meta" / "problems"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "docs" / "mindmaps"
PAGES_OUTPUT_DIR = PROJECT_ROOT / "docs" / "pages"
CONFIG_FILE = Path(__file__).resolve().parent.parent / "generate_mindmaps.toml"
META_DESCRIPTIONS_DIR = Path(__file__).resolve().parent / "meta"

# Defaults
DEFAULT_GITHUB_REPO_URL = "https://github.com/lufftw/neetcode"
DEFAULT_GITHUB_BRANCH = "main"
DEFAULT_USE_GITHUB_LINKS = True

# Mind map types
MINDMAP_TYPES = [
    "pattern-hierarchy", "family-derivation", "algorithm-usage",
    "data-structure", "company-coverage", "roadmap-paths",
    "problem-relations", "solution-variants", "difficulty-topics",
]

# Difficulty icons
DIFFICULTY_ICONS = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}


@dataclass
class MindmapsConfig:
    """Configuration for mind maps generation."""
    github_repo_url: str = DEFAULT_GITHUB_REPO_URL
    github_branch: str = DEFAULT_GITHUB_BRANCH
    use_github_links: bool = DEFAULT_USE_GITHUB_LINKS
    descriptions: dict[str, str] = field(default_factory=dict)


_config: MindmapsConfig | None = None


def load_config() -> MindmapsConfig:
    """Load config from file/env/defaults."""
    config = MindmapsConfig()
    
    if CONFIG_FILE.exists():
        try:
            parsed = parse_toml_simple(CONFIG_FILE.read_text(encoding="utf-8"))
            github = parsed.get("github", {})
            links = parsed.get("links", {})
            descriptions = parsed.get("descriptions", {})
            config.github_repo_url = github.get("repo_url", config.github_repo_url)
            config.github_branch = github.get("branch", config.github_branch)
            config.use_github_links = links.get("use_github_links", config.use_github_links)
            if isinstance(descriptions, dict):
                config.descriptions = descriptions
        except Exception as e:
            print(f"Warning: Failed to load config: {e}")
    
    # Environment overrides
    config.github_repo_url = os.getenv("GITHUB_REPO_URL", config.github_repo_url)
    config.github_branch = os.getenv("GITHUB_BRANCH", config.github_branch)
    return config


def get_config() -> MindmapsConfig:
    """Get config singleton."""
    global _config
    if _config is None:
        _config = load_config()
    return _config
