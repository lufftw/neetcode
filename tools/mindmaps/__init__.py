# tools/mindmaps/__init__.py
"""Mind map generation module for NeetCode Practice Framework."""

from .config import (
    MindmapsConfig,
    load_config,
    get_config,
    MINDMAP_TYPES,
    DIFFICULTY_ICONS,
    PROJECT_ROOT,
    ONTOLOGY_DIR,
    META_PROBLEMS_DIR,
    DEFAULT_OUTPUT_DIR,
    PAGES_OUTPUT_DIR,
    META_DESCRIPTIONS_DIR,
)
from .toml_parser import parse_toml_simple, parse_toml_value
from .data import ProblemData
from .loader import OntologyData, load_ontology, load_problems
from .helpers import markmap_frontmatter, format_problem_entry, convert_tables_in_markmap, fix_table_links
from .generators import GENERATORS
from .html import generate_html_mindmap, markdown_to_html_content, setup_pages_directory
from .templates import INDEX_HTML_TEMPLATE, CARD_TEMPLATE

__all__ = [
    # Config
    "MindmapsConfig", "load_config", "get_config",
    "MINDMAP_TYPES", "DIFFICULTY_ICONS",
    "PROJECT_ROOT", "ONTOLOGY_DIR", "META_PROBLEMS_DIR",
    "DEFAULT_OUTPUT_DIR", "PAGES_OUTPUT_DIR", "META_DESCRIPTIONS_DIR",
    # TOML
    "parse_toml_simple", "parse_toml_value",
    # Data
    "ProblemData", "OntologyData", "load_ontology", "load_problems",
    # Helpers
    "markmap_frontmatter", "format_problem_entry", "convert_tables_in_markmap", "fix_table_links",
    # Generators
    "GENERATORS",
    # HTML
    "generate_html_mindmap", "markdown_to_html_content", "setup_pages_directory",
    "INDEX_HTML_TEMPLATE", "CARD_TEMPLATE",
]
