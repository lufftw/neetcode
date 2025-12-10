# tools/patterndocs/loader.py
"""Ontology loading for pattern documentation."""

from __future__ import annotations
from pathlib import Path

from .toml_parser import parse_toml_simple
from .data import APIKernel, Pattern

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ONTOLOGY_DIR = PROJECT_ROOT / "ontology"
META_PATTERNS_DIR = PROJECT_ROOT / "meta" / "patterns"
OUTPUT_DIR = PROJECT_ROOT / "docs" / "patterns"

# Directory name to Kernel ID mapping
KERNEL_MAPPING = {
    "sliding_window": "SubstringSlidingWindow",
    "bfs_grid": "GridBFSMultiSource",
    "backtracking": "BacktrackingExploration",
    "k_way_merge": "KWayMerge",
    "binary_search": "BinarySearchBoundary",
    "two_pointers": "TwoPointerPartition",
    "linked_list_reversal": "LinkedListInPlaceReversal",
    "monotonic_stack": "MonotonicStack",
    "prefix_sum": "PrefixSumRangeQuery",
    "tree_dfs": "TreeTraversalDFS",
    "tree_bfs": "TreeTraversalBFS",
    "dp_sequence": "DPSequence",
    "dp_interval": "DPInterval",
    "union_find": "UnionFindConnectivity",
    "trie": "TriePrefixSearch",
    "heap_top_k": "HeapTopK",
    "topological_sort": "TopologicalSort",
}


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
    """Convert directory name to API Kernel ID."""
    return KERNEL_MAPPING.get(dir_name, dir_name)

