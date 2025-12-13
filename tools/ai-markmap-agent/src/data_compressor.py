# =============================================================================
# Data Compressor
# =============================================================================
# Token-efficient data formatting for LLM consumption.
# Reduces problem data to minimal representation while preserving essential info.
# =============================================================================

from __future__ import annotations

import json
from typing import Any

from .config_loader import ConfigLoader


class DataCompressor:
    """
    Compresses problem and ontology data for token-efficient LLM transmission.
    
    Strategies:
    1. compact_json: Minimal JSON with short keys
    2. tabular: Pipe-separated values (very compact)
    3. minimal: Only essential fields, abbreviated
    """
    
    # Short key mappings for compact JSON
    KEY_MAP = {
        "id": "i",
        "title": "t",
        "difficulty": "d",
        "patterns": "p",
        "has_solution": "s",  # Boolean: has solution file
        "topics": "tp",
        "algorithms": "a",
        "data_structures": "ds",
        "families": "f",
        "complexity": "c",
        "roadmaps": "r",
    }
    
    # Reverse mapping for decompression
    REVERSE_KEY_MAP = {v: k for k, v in KEY_MAP.items()}
    
    # Difficulty abbreviations
    DIFF_MAP = {"easy": "E", "medium": "M", "hard": "H"}
    REVERSE_DIFF_MAP = {v: k for k, v in DIFF_MAP.items()}
    
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
            "id", "title", "difficulty", "patterns", "has_solution", "topics"
        ])
        self.max_problems = compression_config.get("max_problems_per_batch", 200)
        
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
            return self._compress_tabular(problems)
        elif self.format == "minimal":
            return self._compress_minimal(problems)
        else:  # compact_json
            return self._compress_compact_json(problems)
    
    def _compress_compact_json(self, problems: dict[str, Any]) -> str:
        """
        Compress to compact JSON with short keys.
        
        Format:
        [{"i":"0003","t":"Longest...","d":"M","p":["sliding_window"],"s":true}]
        """
        compressed = []
        
        for slug, data in list(problems.items())[:self.max_problems]:
            item = {}
            
            # Extract essential fields with short keys
            if "id" in self.problem_fields:
                item["i"] = data.get("id", slug[:4])
            
            if "title" in self.problem_fields:
                item["t"] = data.get("title", "")
            
            if "difficulty" in self.problem_fields:
                diff = data.get("difficulty", "medium")
                item["d"] = self.DIFF_MAP.get(diff, "M")
            
            if "patterns" in self.problem_fields:
                item["p"] = data.get("patterns", [])
            
            if "has_solution" in self.problem_fields:
                # Check if solution file exists
                files = data.get("files", {})
                solution_file = files.get("solution", "")
                item["s"] = bool(solution_file)
                if solution_file:
                    item["sf"] = solution_file  # Include path for URL generation
            
            if "topics" in self.problem_fields:
                item["tp"] = data.get("topics", [])
            
            if "algorithms" in self.problem_fields:
                item["a"] = data.get("algorithms", [])
            
            if "families" in self.problem_fields:
                item["f"] = data.get("families", [])
            
            compressed.append(item)
        
        return json.dumps(compressed, ensure_ascii=False, separators=(',', ':'))
    
    def _compress_tabular(self, problems: dict[str, Any]) -> str:
        """
        Compress to tabular pipe-separated format.
        
        Format:
        id|title|diff|has_sol|patterns
        0003|Longest Substring...|M|✓|sliding_window,two_pointers
        """
        lines = ["id|title|diff|solved|patterns"]
        
        for slug, data in list(problems.items())[:self.max_problems]:
            problem_id = data.get("id", slug[:4])
            title = data.get("title", "")[:40]  # Truncate long titles
            diff = self.DIFF_MAP.get(data.get("difficulty", "medium"), "M")
            
            files = data.get("files", {})
            has_sol = "✓" if files.get("solution") else "○"
            
            patterns = ",".join(data.get("patterns", [])[:3])  # Max 3 patterns
            
            lines.append(f"{problem_id}|{title}|{diff}|{has_sol}|{patterns}")
        
        return "\n".join(lines)
    
    def _compress_minimal(self, problems: dict[str, Any]) -> str:
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
            lines.append(f"SOLVED: {','.join(sorted(solved)[:100])}")
        if unsolved:
            lines.append(f"UNSOLVED: {','.join(sorted(unsolved)[:100])}")
        
        return "\n".join(lines)
    
    def compress_ontology(self, ontology: dict[str, Any]) -> str:
        """
        Compress ontology data for LLM consumption.
        
        Args:
            ontology: Dictionary of ontology categories
            
        Returns:
            Compressed string representation
        """
        if not self.enabled:
            return json.dumps(ontology, ensure_ascii=False)
        
        # Extract key information from each ontology category
        summary = {}
        
        for category, data in ontology.items():
            if isinstance(data, dict):
                # Extract just the keys/names from each category
                if "items" in data:
                    summary[category] = list(data["items"].keys())[:50]
                elif isinstance(data, dict):
                    # For nested structures, get top-level keys
                    summary[category] = list(data.keys())[:30]
            elif isinstance(data, list):
                summary[category] = data[:30]
        
        return json.dumps(summary, ensure_ascii=False, separators=(',', ':'))
    
    def get_problem_url(self, problem_data: dict[str, Any]) -> str:
        """
        Get the appropriate URL for a problem.
        
        Args:
            problem_data: Problem data dictionary
            
        Returns:
            GitHub solution URL if has solution, else LeetCode problem URL
        """
        files = problem_data.get("files", {})
        solution_file = files.get("solution", "")
        
        if solution_file:
            return self.github_template.format(solution_file=solution_file)
        else:
            # Extract slug from problem data
            slug = problem_data.get("slug", "")
            # Remove the ID prefix if present (e.g., "0003_longest..." -> "longest...")
            if "_" in slug:
                slug = slug.split("_", 1)[1]
            return self.leetcode_template.format(slug=slug)
    
    def decompress_key(self, short_key: str) -> str:
        """
        Convert short key back to full key.
        
        Args:
            short_key: Abbreviated key
            
        Returns:
            Full key name
        """
        return self.REVERSE_KEY_MAP.get(short_key, short_key)


# Convenience functions

def compress_for_llm(
    problems: dict[str, Any],
    ontology: dict[str, Any],
    config: dict[str, Any] | None = None,
) -> dict[str, str]:
    """
    Compress all data for LLM consumption.
    
    Args:
        problems: Problem data dictionary
        ontology: Ontology data dictionary
        config: Optional configuration
        
    Returns:
        Dictionary with compressed 'problems' and 'ontology' strings
    """
    compressor = DataCompressor(config)
    
    return {
        "problems": compressor.compress_problems(problems),
        "ontology": compressor.compress_ontology(ontology),
    }


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

