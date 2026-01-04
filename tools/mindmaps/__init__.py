# tools/mindmaps/__init__.py
"""Mind map generation module for NeetCode Practice Framework.

This module re-exports all public APIs from the core submodule
to maintain backward compatibility with existing imports.
"""

# Re-export everything from core to maintain backward compatibility
from .core import (
    # Config
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
    # TOML
    parse_toml_simple,
    parse_toml_value,
    # Data
    ProblemData,
    OntologyData,
    load_ontology,
    load_problems,
    # Helpers
    markmap_frontmatter,
    format_problem_entry,
    convert_tables_in_markmap,
    fix_table_links,
    # Generators
    GENERATORS,
    # HTML
    generate_html_mindmap,
    markdown_to_html_content,
    setup_pages_directory,
    INDEX_HTML_TEMPLATE,
    CARD_TEMPLATE,
    # Post-processing
    PostProcessor,
    post_process_content,
)

# Import link post-processing functions
from .link_post_processor import (
    add_links_to_mindmap,
    simplify_leetcode_links,
    preprocess_for_llm,
    LinkPostProcessor,
)

__all__ = [
    # Config
    "MindmapsConfig",
    "load_config",
    "get_config",
    "MINDMAP_TYPES",
    "DIFFICULTY_ICONS",
    "PROJECT_ROOT",
    "ONTOLOGY_DIR",
    "META_PROBLEMS_DIR",
    "DEFAULT_OUTPUT_DIR",
    "PAGES_OUTPUT_DIR",
    "META_DESCRIPTIONS_DIR",
    # TOML
    "parse_toml_simple",
    "parse_toml_value",
    # Data
    "ProblemData",
    "OntologyData",
    "load_ontology",
    "load_problems",
    # Helpers
    "markmap_frontmatter",
    "format_problem_entry",
    "convert_tables_in_markmap",
    "fix_table_links",
    # Generators
    "GENERATORS",
    # HTML
    "generate_html_mindmap",
    "markdown_to_html_content",
    "setup_pages_directory",
    "INDEX_HTML_TEMPLATE",
    "CARD_TEMPLATE",
    # Post-processing
    "PostProcessor",
    "post_process_content",
    # Link post-processing
    "add_links_to_mindmap",
    "simplify_leetcode_links",
    "preprocess_for_llm",
    "LinkPostProcessor",
]

