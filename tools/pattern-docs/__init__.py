# tools/patterndocs/__init__.py
"""Pattern documentation generation module."""

from .toml_parser import parse_toml_simple
from .data import APIKernel, Pattern, PatternDocConfig
from .loader import (
    load_api_kernels,
    load_patterns,
    get_available_patterns,
    get_kernel_id_from_dir_name,
    PROJECT_ROOT,
    ONTOLOGY_DIR,
    META_PATTERNS_DIR,
    OUTPUT_DIR,
)
from .mapping import get_kernel_id, get_all_mappings, has_mapping
from .files import collect_source_files, STRUCTURAL_FILES_ORDER, STRUCTURAL_FILES_FOOTER
from .sections import generate_toc, create_anchor, add_section_numbers
from .composer import compose_document

__all__ = [
    # TOML
    "parse_toml_simple",
    # Data
    "APIKernel", "Pattern", "PatternDocConfig",
    # Loader
    "load_api_kernels", "load_patterns", "get_available_patterns", "get_kernel_id_from_dir_name",
    "PROJECT_ROOT", "ONTOLOGY_DIR", "META_PATTERNS_DIR", "OUTPUT_DIR",
    # Mapping
    "get_kernel_id", "get_all_mappings", "has_mapping",
    # Files
    "collect_source_files", "STRUCTURAL_FILES_ORDER", "STRUCTURAL_FILES_FOOTER",
    # Sections
    "generate_toc", "create_anchor", "add_section_numbers",
    # Composer
    "compose_document",
]

