# tools/patterndocs/config.py
"""Configuration loading for pattern documentation generator."""

from __future__ import annotations
from pathlib import Path

from .toml_parser import parse_toml_simple

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = PROJECT_ROOT / "tools" / "generate_pattern_docs.toml"

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


def _find_matching_patterns(dir_name: str, patterns: dict) -> list:
    """Find patterns matching a directory name."""
    matching_patterns = []
    
    # Strategy 1: Exact prefix match (dir_name_*)
    for ps in patterns.values():
        for p in ps:
            if p.id.startswith(dir_name + "_"):
                matching_patterns.append(p)
    
    # Strategy 2: Handle singular/plural variations
    if not matching_patterns:
        dir_variants = [dir_name]
        if dir_name.endswith("s") and not dir_name.endswith("ss"):
            dir_variants.append(dir_name[:-1])
        
        if "_" in dir_name:
            parts = dir_name.split("_")
            if len(parts) >= 2 and parts[-1].endswith("s"):
                dir_variants.append("_".join(parts[:-1] + [parts[-1][:-1]]))
        
        for variant in dir_variants:
            for ps in patterns.values():
                for p in ps:
                    if p.id.startswith(variant + "_"):
                        matching_patterns.append(p)
    
    # Strategy 3: Word-order independent matching
    # Example: "bfs_grid" should match "grid_bfs_propagation"
    if not matching_patterns:
        dir_keywords = set(dir_name.split("_"))
        for ps in patterns.values():
            for p in ps:
                pattern_parts = p.id.split("_")
                # Check if all directory keywords appear in pattern (order-independent)
                pattern_keywords = set(pattern_parts[:min(3, len(pattern_parts))])  # Check first 3 parts
                if dir_keywords.issubset(pattern_keywords) or pattern_keywords.issubset(dir_keywords):
                    matching_patterns.append(p)
    
    # Strategy 4: Match by keyword parts (ordered)
    if not matching_patterns:
        dir_keywords = dir_name.split("_")
        for ps in patterns.values():
            for p in ps:
                pattern_parts = p.id.split("_")
                if len(pattern_parts) >= len(dir_keywords):
                    if pattern_parts[:len(dir_keywords)] == dir_keywords:
                        matching_patterns.append(p)
                    elif (dir_name.endswith("s") and 
                          len(pattern_parts) >= len(dir_keywords) - 1 and
                          pattern_parts[:len(dir_keywords)-1] == dir_keywords[:-1] and
                          pattern_parts[len(dir_keywords)-1] == dir_keywords[-1][:-1]):
                        matching_patterns.append(p)
    
    return matching_patterns


def _match_by_api_kernel_name(dir_name: str, patterns: dict) -> list:
    """Match directory name to patterns by converting to API Kernel name format."""
    # Convert directory name to potential API Kernel name
    # Examples: "monotonic_stack" -> "MonotonicStack", "tree_bfs" -> "TreeTraversalBFS"
    
    # Try direct conversion: snake_case to PascalCase
    kernel_name_parts = [part.capitalize() for part in dir_name.split("_")]
    potential_kernels = [
        "".join(kernel_name_parts),  # MonotonicStack
        kernel_name_parts[0] + "".join(p.capitalize() for p in kernel_name_parts[1:]),  # TreeBfs
    ]
    
    # Special cases
    special_mappings = {
        "monotonic_stack": "MonotonicStack",
        "tree_bfs": "TreeTraversalBFS",
        "tree_dfs": "TreeTraversalDFS",
        "linked_list_reversal": "LinkedListInPlaceReversal",
        "bfs_grid": "GridBFSMultiSource",
        "k_way_merge": "KWayMerge",
        "dp_sequence": "DPSequence",
        "dp_interval": "DPInterval",
        "trie": "TriePrefixSearch",
        "topological_sort": "TopologicalSort",
    }
    
    if dir_name in special_mappings:
        target_kernel = special_mappings[dir_name]
        matching_patterns = []
        for ps in patterns.values():
            for p in ps:
                if p.api_kernel == target_kernel:
                    matching_patterns.append(p)
        return matching_patterns
    
    return []


def _auto_infer_kernel_mapping() -> dict[str, str]:
    """Auto-infer kernel mapping from ontology patterns."""
    from .loader import load_patterns
    
    patterns = load_patterns()
    mapping = {}
    
    # Get all pattern directories
    meta_patterns_dir = PROJECT_ROOT / "meta" / "patterns"
    if meta_patterns_dir.exists():
        dirs = [d.name for d in meta_patterns_dir.iterdir() 
                if d.is_dir() and not d.name.startswith(".")]
        
        for dir_name in dirs:
            # Try pattern ID matching first
            matching_patterns = _find_matching_patterns(dir_name, patterns)
            
            # If no pattern ID match, try API kernel name matching
            if not matching_patterns:
                matching_patterns = _match_by_api_kernel_name(dir_name, patterns)
            
            if matching_patterns:
                kernels = set(p.api_kernel for p in matching_patterns)
                if len(kernels) == 1:
                    mapping[dir_name] = list(kernels)[0]
                elif len(kernels) > 1:
                    # Ambiguous: multiple kernels match
                    # For now, skip (will use config file or default)
                    pass
    
    return mapping


def get_kernel_mapping() -> dict[str, str]:
    """Get kernel mapping from config file, with auto-inference as fallback.
    
    Priority:
    1. Manual configuration in generate_pattern_docs.toml (highest priority)
    2. Simple auto-inference (for unambiguous cases)
    3. Default fallback mappings
    
    Manual configuration is recommended for clarity and maintainability,
    as mapping relationships involve semantic decisions.
    """
    config = load_generator_config()
    
    # Start with manual configuration (highest priority)
    mapping = {}
    if "kernel_mapping" in config:
        mapping.update(config["kernel_mapping"])
    
    # Add auto-inferred mappings for directories not in config
    auto_mapped = _auto_infer_kernel_mapping()
    for key, value in auto_mapped.items():
        if key not in mapping:
            mapping[key] = value
    
    # Fallback defaults for common mappings
    defaults = {
        "bfs_grid": "GridBFSMultiSource",
        "k_way_merge": "KWayMerge",
        "linked_list_reversal": "LinkedListInPlaceReversal",
        "monotonic_stack": "MonotonicStack",
        "tree_bfs": "TreeTraversalBFS",
        "dp_sequence": "DPSequence",
        "dp_interval": "DPInterval",
        "trie": "TriePrefixSearch",
        "topological_sort": "TopologicalSort",
    }
    
    # Only add defaults that aren't already in mapping
    for key, value in defaults.items():
        if key not in mapping:
            mapping[key] = value
    
    return mapping


def get_paths() -> dict[str, Path]:
    """Get path configuration from config file or return defaults."""
    config = load_generator_config()
    
    paths_config = config.get("paths", {})
    
    return {
        "ontology_dir": PROJECT_ROOT / paths_config.get("ontology_dir", "ontology"),
        "meta_patterns_dir": PROJECT_ROOT / paths_config.get("meta_patterns_dir", "meta/patterns"),
        "output_dir": PROJECT_ROOT / paths_config.get("output_dir", "docs/patterns"),
    }

