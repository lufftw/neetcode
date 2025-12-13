# =============================================================================
# Data Compressor
# =============================================================================
# Token-efficient data formatting for LLM consumption.
# Reduces problem/ontology/roadmap data to minimal representation.
#
# See docs/DATA_SOURCES.md for full specification.
# =============================================================================

from __future__ import annotations

import json
from typing import Any

from .config_loader import ConfigLoader


class DataCompressor:
    """
    Compresses problem, ontology, and roadmap data for token-efficient LLM transmission.
    
    Compression Formats:
    - compact_json: Minimal JSON with short keys (~70% reduction)
    - tabular: Pipe-separated values (~85% reduction)
    - minimal: Only IDs and status (~95% reduction)
    
    Key Mappings:
        i = id, t = title, d = difficulty, p = patterns, 
        s = has_solution, sf = solution_file, tp = topics
    """
    
    # Short key mappings for compact JSON
    KEY_MAP = {
        "id": "i",
        "title": "t",
        "difficulty": "d",
        "patterns": "p",
        "has_solution": "s",
        "solution_file": "sf",
        "topics": "tp",
        "algorithms": "a",
        "data_structures": "ds",
        "families": "f",
        "complexity": "c",
        "roadmaps": "r",
        "order": "o",
        "problem": "pr",
        "role": "rl",
        "prerequisite": "pq",
        "delta": "dt",
    }
    
    # Reverse mapping for decompression
    REVERSE_KEY_MAP = {v: k for k, v in KEY_MAP.items()}
    
    # Difficulty abbreviations
    DIFF_MAP = {"easy": "E", "medium": "M", "hard": "H"}
    REVERSE_DIFF_MAP = {v: k for k, v in DIFF_MAP.items()}
    
    # Role abbreviations for roadmaps
    ROLE_MAP = {"base": "B", "variant": "V", "advanced": "A"}
    
    def __init__(self, config: dict[str, Any] | None = None):
        """
        Initialize the data compressor.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or ConfigLoader.get_config()
        compression_config = self.config.get("data_compression", {})
        
        self.enabled = compression_config.get("enabled", True)
        self.format = compression_config.get("format", "compact_json")
        self.problem_fields = compression_config.get("problem_fields", [
            "id", "title", "difficulty", "patterns", "has_solution"
        ])
        self.max_problems = compression_config.get("max_problems_per_batch", 200)
        self.ontology_summary = compression_config.get("ontology_summary", True)
        
        # URL config
        urls_config = self.config.get("urls", {})
        self.github_template = urls_config.get("github", {}).get(
            "solution_template",
            "https://github.com/lufftw/neetcode/blob/main/{solution_file}"
        )
        self.leetcode_template = urls_config.get("leetcode", {}).get(
            "problem_template",
            "https://leetcode.com/problems/{slug}/"
        )
    
    # =========================================================================
    # Problem Compression
    # =========================================================================
    
    def compress_problems(self, problems: dict[str, Any]) -> str:
        """
        Compress problem data for LLM consumption.
        
        Args:
            problems: Dictionary of problem_slug -> problem_data
            
        Returns:
            Compressed string representation
        """
        if not self.enabled:
            return json.dumps(problems, ensure_ascii=False)
        
        if self.format == "tabular":
            return self._compress_problems_tabular(problems)
        elif self.format == "minimal":
            return self._compress_problems_minimal(problems)
        else:  # compact_json
            return self._compress_problems_compact_json(problems)
    
    def _compress_problems_compact_json(self, problems: dict[str, Any]) -> str:
        """
        Compress to compact JSON with short keys.
        
        Format: [{"i":"0003","t":"Longest...","d":"M","p":["sliding_window"],"s":true}]
        """
        compressed = []
        
        for slug, data in list(problems.items())[:self.max_problems]:
            item = {}
            
            # Core fields
            item["i"] = data.get("id", slug[:4])
            item["t"] = data.get("title", "")
            item["d"] = self.DIFF_MAP.get(data.get("difficulty", "medium"), "M")
            item["p"] = data.get("patterns", [])
            
            # Solution status - key field for URL selection
            files = data.get("files", {})
            solution_file = files.get("solution", "")
            item["s"] = bool(solution_file)
            if solution_file:
                item["sf"] = solution_file
            
            # Optional fields (only if requested)
            if "topics" in self.problem_fields:
                topics = data.get("topics", [])
                if topics:
                    item["tp"] = topics
            
            compressed.append(item)
        
        return json.dumps(compressed, ensure_ascii=False, separators=(',', ':'))
    
    def _compress_problems_tabular(self, problems: dict[str, Any]) -> str:
        """
        Compress to tabular pipe-separated format.
        
        Format:
        id|title|diff|solved|patterns
        0003|Longest Substring...|M|✓|sliding_window_unique
        """
        lines = ["id|title|diff|solved|patterns"]
        
        for slug, data in list(problems.items())[:self.max_problems]:
            problem_id = data.get("id", slug[:4])
            title = data.get("title", "")[:40]  # Truncate long titles
            diff = self.DIFF_MAP.get(data.get("difficulty", "medium"), "M")
            
            files = data.get("files", {})
            has_sol = "✓" if files.get("solution") else "○"
            
            patterns = ",".join(data.get("patterns", [])[:3])
            
            lines.append(f"{problem_id}|{title}|{diff}|{has_sol}|{patterns}")
        
        return "\n".join(lines)
    
    def _compress_problems_minimal(self, problems: dict[str, Any]) -> str:
        """
        Compress to minimal format - just IDs with solution status.
        
        Format:
        SOLVED: 0001,0003,0015
        UNSOLVED: 0002,0004
        """
        solved = []
        unsolved = []
        
        for slug, data in problems.items():
            problem_id = data.get("id", slug[:4])
            files = data.get("files", {})
            
            if files.get("solution"):
                solved.append(problem_id)
            else:
                unsolved.append(problem_id)
        
        lines = []
        if solved:
            lines.append(f"SOLVED: {','.join(sorted(solved))}")
        if unsolved:
            lines.append(f"UNSOLVED: {','.join(sorted(unsolved))}")
        
        return "\n".join(lines)
    
    # =========================================================================
    # Ontology Compression
    # =========================================================================
    
    def compress_ontology(self, ontology: dict[str, Any]) -> str:
        """
        Compress ontology data for LLM consumption.
        
        Extracts only essential taxonomy information:
        - Category names and IDs
        - Parent-child relationships
        - Brief summaries
        
        Args:
            ontology: Dictionary of ontology categories
            
        Returns:
            Compressed string representation
        """
        if not self.enabled:
            return json.dumps(ontology, ensure_ascii=False)
        
        if self.ontology_summary:
            return self._compress_ontology_summary(ontology)
        else:
            return self._compress_ontology_full(ontology)
    
    def _compress_ontology_summary(self, ontology: dict[str, Any]) -> str:
        """
        Compress ontology to just IDs and hierarchy.
        
        Output format:
        {
          "algorithms": {"core": ["bfs","dfs"], "technique": ["sliding_window"]},
          "patterns": ["sliding_window_unique", "two_pointer_opposite"],
          "data_structures": ["array", "hash_map", "linked_list"]
        }
        """
        summary = {}
        
        for category, data in ontology.items():
            if category == "algorithms":
                summary[category] = self._extract_algorithms_hierarchy(data)
            elif category == "patterns":
                summary[category] = self._extract_pattern_list(data)
            elif category == "data_structures":
                summary[category] = self._extract_ds_list(data)
            elif category == "api_kernels":
                summary[category] = self._extract_kernel_list(data)
            elif category == "families":
                summary[category] = self._extract_family_list(data)
            else:
                # Generic extraction
                if isinstance(data, dict):
                    summary[category] = list(data.keys())[:30]
                elif isinstance(data, list):
                    summary[category] = [
                        item.get("id", str(item))[:30] 
                        for item in data[:30]
                        if isinstance(item, dict)
                    ]
        
        return json.dumps(summary, ensure_ascii=False, separators=(',', ':'))
    
    def _extract_algorithms_hierarchy(self, data: Any) -> dict[str, list]:
        """Extract algorithms grouped by kind."""
        if not isinstance(data, dict):
            return {}
        
        # Handle list format from TOML
        algorithms = data.get("algorithms", data)
        if isinstance(algorithms, list):
            grouped = {"core": [], "technique": [], "paradigm": []}
            for algo in algorithms:
                if isinstance(algo, dict):
                    kind = algo.get("kind", "core")
                    algo_id = algo.get("id", "")
                    if kind in grouped and algo_id:
                        grouped[kind].append(algo_id)
            return {k: v for k, v in grouped.items() if v}
        
        return {}
    
    def _extract_pattern_list(self, data: Any) -> list[str]:
        """Extract pattern IDs."""
        if isinstance(data, dict):
            patterns = data.get("patterns", [])
        elif isinstance(data, list):
            patterns = data
        else:
            return []
        
        return [
            p.get("id", "") for p in patterns
            if isinstance(p, dict) and p.get("id")
        ][:50]
    
    def _extract_ds_list(self, data: Any) -> list[str]:
        """Extract data structure IDs."""
        if isinstance(data, dict):
            items = data.get("data_structures", data.get("items", []))
        elif isinstance(data, list):
            items = data
        else:
            return []
        
        if isinstance(items, list):
            return [
                item.get("id", "") for item in items
                if isinstance(item, dict) and item.get("id")
            ][:30]
        elif isinstance(items, dict):
            return list(items.keys())[:30]
        
        return []
    
    def _extract_kernel_list(self, data: Any) -> list[str]:
        """Extract API kernel IDs."""
        if isinstance(data, dict):
            kernels = data.get("api_kernels", data.get("kernels", []))
        elif isinstance(data, list):
            kernels = data
        else:
            return []
        
        return [
            k.get("id", "") for k in kernels
            if isinstance(k, dict) and k.get("id")
        ][:20]
    
    def _extract_family_list(self, data: Any) -> list[str]:
        """Extract family IDs."""
        if isinstance(data, dict):
            families = data.get("families", [])
        elif isinstance(data, list):
            families = data
        else:
            return []
        
        return [
            f.get("id", "") for f in families
            if isinstance(f, dict) and f.get("id")
        ][:20]
    
    def _compress_ontology_full(self, ontology: dict[str, Any]) -> str:
        """Compress ontology with summaries included."""
        compressed = {}
        
        for category, data in ontology.items():
            if isinstance(data, dict):
                items = data.get(category, data.get("items", []))
                if isinstance(items, list):
                    compressed[category] = [
                        {"id": item.get("id"), "sum": item.get("summary", "")[:50]}
                        for item in items[:30]
                        if isinstance(item, dict)
                    ]
                else:
                    compressed[category] = list(data.keys())[:30]
        
        return json.dumps(compressed, ensure_ascii=False, separators=(',', ':'))
    
    # =========================================================================
    # Roadmap Compression
    # =========================================================================
    
    def compress_roadmaps(self, roadmaps: dict[str, Any]) -> str:
        """
        Compress roadmap data for LLM consumption.
        
        Extracts learning path order and problem relationships.
        
        Args:
            roadmaps: Dictionary of roadmap_name -> roadmap_data
            
        Returns:
            Compressed string representation
        """
        if not self.enabled:
            return json.dumps(roadmaps, ensure_ascii=False)
        
        compressed = {}
        
        for name, data in roadmaps.items():
            roadmap_id = data.get("id", name)
            steps = data.get("steps", [])
            
            # Compress steps
            compressed_steps = []
            for step in steps:
                compressed_step = {
                    "o": step.get("order", 0),
                    "pr": step.get("problem", "")[:4],  # Just problem ID
                    "rl": self.ROLE_MAP.get(step.get("role", "base"), "B"),
                    "p": step.get("pattern", ""),
                }
                
                # Only include prerequisite if non-empty
                prereqs = step.get("prerequisite", [])
                if prereqs:
                    compressed_step["pq"] = [p[:4] for p in prereqs]
                
                # Only include delta if meaningful
                delta = step.get("delta", "")
                if delta and len(delta) > 5:
                    compressed_step["dt"] = delta[:60]
                
                compressed_steps.append(compressed_step)
            
            compressed[roadmap_id] = {
                "name": data.get("name", name),
                "kernel": data.get("api_kernel", ""),
                "steps": compressed_steps,
            }
        
        return json.dumps(compressed, ensure_ascii=False, separators=(',', ':'))
    
    # =========================================================================
    # URL Generation
    # =========================================================================
    
    def get_problem_url(self, problem_data: dict[str, Any]) -> str:
        """
        Get the appropriate URL for a problem.
        
        Logic:
        - If has solution file → GitHub solution URL
        - If no solution → LeetCode problem URL
        
        Args:
            problem_data: Problem data dictionary
            
        Returns:
            URL string
        """
        files = problem_data.get("files", {})
        solution_file = files.get("solution", "")
        
        if solution_file:
            return self.github_template.format(solution_file=solution_file)
        else:
            # Extract slug
            slug = problem_data.get("slug", "")
            if "_" in slug:
                slug = slug.split("_", 1)[1]
            return self.leetcode_template.format(slug=slug)
    
    # =========================================================================
    # Utility Methods
    # =========================================================================
    
    def decompress_key(self, short_key: str) -> str:
        """Convert short key back to full key."""
        return self.REVERSE_KEY_MAP.get(short_key, short_key)
    
    def decompress_difficulty(self, short_diff: str) -> str:
        """Convert short difficulty back to full name."""
        return self.REVERSE_DIFF_MAP.get(short_diff, short_diff)
    
    def compress_all(
        self,
        problems: dict[str, Any],
        ontology: dict[str, Any],
        roadmaps: dict[str, Any] | None = None,
    ) -> dict[str, str]:
        """
        Compress all data sources at once.
        
        Args:
            problems: Problem data dictionary
            ontology: Ontology data dictionary
            roadmaps: Roadmap data dictionary (optional)
            
        Returns:
            Dictionary with compressed strings for each source
        """
        result = {
            "problems": self.compress_problems(problems),
            "ontology": self.compress_ontology(ontology),
        }
        
        if roadmaps:
            result["roadmaps"] = self.compress_roadmaps(roadmaps)
        
        return result


# =============================================================================
# Convenience Functions
# =============================================================================

def compress_for_llm(
    problems: dict[str, Any],
    ontology: dict[str, Any],
    roadmaps: dict[str, Any] | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, str]:
    """
    Compress all data for LLM consumption.
    
    Args:
        problems: Problem data dictionary
        ontology: Ontology data dictionary
        roadmaps: Roadmap data dictionary (optional)
        config: Optional configuration
        
    Returns:
        Dictionary with compressed 'problems', 'ontology', and 'roadmaps' strings
    """
    compressor = DataCompressor(config)
    return compressor.compress_all(problems, ontology, roadmaps)


def get_link_for_problem(
    problem_data: dict[str, Any],
    config: dict[str, Any] | None = None,
) -> str:
    """
    Get the appropriate link for a problem.
    
    Args:
        problem_data: Problem data dictionary
        config: Optional configuration
        
    Returns:
        URL string (GitHub if solved, LeetCode if not)
    """
    compressor = DataCompressor(config)
    return compressor.get_problem_url(problem_data)
