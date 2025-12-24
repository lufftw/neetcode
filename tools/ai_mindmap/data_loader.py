"""
Data loading functions for AI Mind Map Generator.

Handles loading of ontology, patterns, and problems data.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

# Paths
TOOLS_DIR = Path(__file__).parent.parent
PROJECT_ROOT = TOOLS_DIR.parent
DOCS_PATTERNS_DIR = PROJECT_ROOT / "docs" / "patterns"
META_PATTERNS_DIR = PROJECT_ROOT / "meta" / "patterns"


def load_ontology_data(config: dict[str, Any]) -> dict[str, Any]:
    """Load ontology data based on config."""
    from mindmaps import load_ontology
    
    ontology_config = config.get("ontology", {})
    ontology = load_ontology()
    
    data = {}
    field_map = {
        "api_kernels": ontology.api_kernels,
        "patterns": ontology.patterns,
        "algorithms": ontology.algorithms,
        "data_structures": ontology.data_structures,
        "families": ontology.families,
        "topics": ontology.topics,
        "difficulties": ontology.difficulties,
        "companies": ontology.companies,
        "roadmaps": ontology.roadmaps,
    }
    
    for field, values in field_map.items():
        if ontology_config.get(field, True):
            data[field] = values
    
    return data


def load_docs_patterns(config: dict[str, Any]) -> dict[str, str]:
    """Load pattern documentation from docs/patterns/ (supports both flat and nested structures)."""
    docs_config = config.get("docs", {}).get("patterns", {})
    
    if not docs_config.get("enabled", True):
        return {}
    
    if not DOCS_PATTERNS_DIR.exists():
        return {}
    
    include = docs_config.get("include", [])
    exclude = docs_config.get("exclude", ["README"])
    
    docs = {}
    
    # Support both flat structure (*.md in root) and nested structure (*/intuition.md, */templates.md)
    # First, check root level .md files
    for md_file in DOCS_PATTERNS_DIR.glob("*.md"):
        name = md_file.stem
        
        # Filter by include/exclude
        if include and name not in include:
            continue
        if name in exclude:
            continue
        
        docs[name] = md_file.read_text(encoding="utf-8")
    
    # Then, check subdirectories for nested structure (e.g., sliding_window/intuition.md)
    for subdir in DOCS_PATTERNS_DIR.iterdir():
        if not subdir.is_dir():
            continue
        
        # Pattern name is the subdirectory name
        pattern_name = subdir.name
        
        # Filter by include/exclude (check if pattern name matches)
        if include and pattern_name not in include:
            continue
        if pattern_name in exclude:
            continue
        
        # Load all .md files in this subdirectory
        for md_file in subdir.glob("*.md"):
            # Use pattern_name/filename as key (e.g., "sliding_window/intuition")
            file_stem = md_file.stem
            key = f"{pattern_name}/{file_stem}"
            docs[key] = md_file.read_text(encoding="utf-8")
    
    return docs


def load_meta_patterns(config: dict[str, Any]) -> dict[str, dict[str, str]]:
    """Load pattern snippets from meta/patterns/."""
    meta_config = config.get("meta", {}).get("patterns", {})
    
    if not meta_config.get("enabled", True):
        return {}
    
    if not META_PATTERNS_DIR.exists():
        return {}
    
    include_dirs = meta_config.get("include", [])
    include_headers = meta_config.get("include_headers", True)
    include_comparisons = meta_config.get("include_comparisons", True)
    include_decisions = meta_config.get("include_decisions", True)
    include_templates = meta_config.get("include_templates", True)
    include_problems = meta_config.get("include_problems", True)
    
    patterns = {}
    for pattern_dir in META_PATTERNS_DIR.iterdir():
        if not pattern_dir.is_dir():
            continue
        
        name = pattern_dir.name
        if include_dirs and name not in include_dirs:
            continue
        
        snippets = {}
        for md_file in pattern_dir.glob("*.md"):
            filename = md_file.name
            
            # Filter by type
            if filename.startswith("_header") and not include_headers:
                continue
            if filename.startswith("_comparison") and not include_comparisons:
                continue
            if filename.startswith("_decision") and not include_decisions:
                continue
            if filename.startswith("_templates") and not include_templates:
                continue
            if not filename.startswith("_") and not include_problems:
                continue
            
            snippets[filename] = md_file.read_text(encoding="utf-8")
        
        if snippets:
            patterns[name] = snippets
    
    return patterns


def load_problems_data(config: dict[str, Any]) -> list[dict[str, Any]]:
    """Load problem metadata based on config filters."""
    from mindmaps import load_problems
    
    problems_config = config.get("problems", {})
    
    if not problems_config.get("enabled", True):
        return []
    
    problems = load_problems()
    
    # Apply filters
    difficulties = problems_config.get("difficulties", [])
    topics = problems_config.get("topics", [])
    api_kernels = problems_config.get("api_kernels", [])
    roadmaps = problems_config.get("roadmaps", [])
    specific_ids = problems_config.get("specific_ids", [])
    limit = problems_config.get("limit", 50)
    
    filtered = []
    for p in problems.values():
        # Specific IDs override other filters
        if specific_ids:
            if p.id not in specific_ids:
                continue
        else:
            # Apply filters
            if difficulties and p.difficulty.lower() not in [d.lower() for d in difficulties]:
                continue
            if topics and not any(t in p.topics for t in topics):
                continue
            if api_kernels and not any(k in p.api_kernels for k in api_kernels):
                continue
            if roadmaps and not any(r in p.roadmaps for r in roadmaps):
                continue
        
        filtered.append({
            "id": p.id,
            "leetcode_id": p.leetcode_id,
            "title": p.title,
            "slug": p.slug,
            "url": p.url,
            "difficulty": p.difficulty,
            "topics": p.topics,
            "patterns": p.patterns,
            "api_kernels": p.api_kernels,
            "families": p.families,
            "data_structures": p.data_structures,
            "algorithms": p.algorithms,
            "related_problems": p.related_problems,
            "companies": p.companies,
            "roadmaps": p.roadmaps,
            "solution_file": p.solution_file,
        })
    
    # Sort by leetcode_id and limit
    filtered.sort(key=lambda x: x.get("leetcode_id", 0))
    if limit > 0:
        filtered = filtered[:limit]
    
    return filtered

