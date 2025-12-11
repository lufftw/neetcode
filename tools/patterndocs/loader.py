# tools/patterndocs/loader.py
"""Ontology loading for pattern documentation."""

from __future__ import annotations
from pathlib import Path

from .toml_parser import parse_toml_simple
from .data import APIKernel, Pattern
from .config import get_paths, PROJECT_ROOT
from .mapping import get_kernel_id

# Initialize paths from config
_paths = get_paths()
ONTOLOGY_DIR = _paths["ontology_dir"]
META_PATTERNS_DIR = _paths["meta_patterns_dir"]
OUTPUT_DIR = _paths["output_dir"]


def load_api_kernels() -> dict[str, APIKernel]:
    """Load API kernels from ontology."""
    path = ONTOLOGY_DIR / "api_kernels.toml"
    if not path.exists():
        print(f"Warning: {path} not found")
        return {}

    data = parse_toml_simple(path.read_text(encoding="utf-8"))
    return {
        item.get("id", ""): APIKernel(id=item.get("id", ""), summary=item.get("summary", ""))
        for item in data.get("api_kernels", [])
    }


def load_patterns() -> dict[str, list[Pattern]]:
    """Load patterns grouped by API kernel."""
    path = ONTOLOGY_DIR / "patterns.toml"
    if not path.exists():
        print(f"Warning: {path} not found")
        return {}

    data = parse_toml_simple(path.read_text(encoding="utf-8"))
    patterns_by_kernel: dict[str, list[Pattern]] = {}
    
    for item in data.get("patterns", []):
        pattern = Pattern(
            id=item.get("id", ""),
            api_kernel=item.get("api_kernel", ""),
            summary=item.get("summary", ""),
        )
        patterns_by_kernel.setdefault(pattern.api_kernel, []).append(pattern)
    
    return patterns_by_kernel


def get_available_patterns() -> list[str]:
    """Get list of pattern directories with source files."""
    if not META_PATTERNS_DIR.exists():
        return []
    return sorted([
        p.name for p in META_PATTERNS_DIR.iterdir()
        if p.is_dir() and not p.name.startswith(".") and (p / "_header.md").exists()
    ])


def get_kernel_id_from_dir_name(dir_name: str) -> str:
    """
    Convert directory name to API Kernel ID.
    
    Priority:
    1. Extract from _header.md file (if exists) - highest priority
    2. Use unified mapping from mapping.py
    3. Fallback to directory name
    
    All mappings are centrally managed in tools/patterndocs/mapping.py.
    """
    # Try to extract from _header.md first (highest priority)
    header_file = META_PATTERNS_DIR / dir_name / "_header.md"
    if header_file.exists():
        from .kernel_extractor import extract_kernel_from_header
        kernel_id = extract_kernel_from_header(header_file)
        if kernel_id:
            return kernel_id
    
    # Use unified mapping (primary source)
    return get_kernel_id(dir_name)

