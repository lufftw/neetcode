# tools/patterndocs/problem_mapper.py
"""Problem mapping generation from meta/problems/*.toml files."""

from __future__ import annotations
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional

from .toml_parser import parse_toml_simple

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
META_PROBLEMS_DIR = PROJECT_ROOT / "meta" / "problems"

    # Pattern ID to category mapping for TwoPointersTraversal
PATTERN_CATEGORIES = {
    # Opposite Pointers
    "two_pointer_opposite": "Opposite Pointers (Two-End)",
    "two_pointer_opposite_search": "Opposite Pointers (Two-End)",
    "two_pointer_opposite_palindrome": "Opposite Pointers (Two-End)",
    "two_pointer_opposite_maximize": "Opposite Pointers (Two-End)",
    "opposite_pointers_maximize": "Opposite Pointers (Two-End)",
    "opposite_pointers": "Opposite Pointers (Two-End)",
    # Same-Direction
    "two_pointer_same_direction": "Same-Direction Pointers (Writer)",
    "two_pointer_writer_dedup": "Same-Direction Pointers (Writer)",
    "two_pointer_writer_remove": "Same-Direction Pointers (Writer)",
    "two_pointer_writer_compact": "Same-Direction Pointers (Writer)",
    "same_direction_writer": "Same-Direction Pointers (Writer)",
    # Fast-Slow (from FastSlowPointers kernel)
    "fast_slow_cycle_detect": "Fast–Slow Pointers",
    "fast_slow_cycle_start": "Fast–Slow Pointers",
    "fast_slow_midpoint": "Fast–Slow Pointers",
    "fast_slow_implicit_cycle": "Fast–Slow Pointers",
    # Partitioning (from TwoPointerPartition kernel)
    "dutch_flag_partition": "Partitioning / Dutch Flag",
    "two_way_partition": "Partitioning / Dutch Flag",
    "quickselect_partition": "Partitioning / Dutch Flag",
    "dutch_national_flag": "Partitioning / Dutch Flag",
    # Dedup Enumeration
    "two_pointer_three_sum": "Dedup + Sorted Enumeration",
    "two_pointer_k_sum": "Dedup + Sorted Enumeration",
    "dedup_sorted_enumeration": "Dedup + Sorted Enumeration",
    # Merge
    "merge_two_sorted": "Merge Pattern",
    "merge_k_sorted": "Merge Pattern",
    "merge_sorted_sequences": "Merge Pattern",
}


@dataclass
class ProblemInfo:
    """Problem information from meta/problems/*.toml."""
    leetcode_id: int
    title: str
    difficulty: str
    patterns: list[str]
    api_kernels: list[str]


def load_problem_metadata(problem_file: Path) -> Optional[ProblemInfo]:
    """Load problem metadata from a TOML file."""
    try:
        content = problem_file.read_text(encoding="utf-8")
        data = parse_toml_simple(content)
        
        leetcode_id = int(data.get("leetcode_id", 0))
        title = data.get("title", "")
        difficulty = data.get("difficulty", "unknown")
        
        # Get patterns and api_kernels from problem level or first solution
        patterns = data.get("patterns", [])
        api_kernels = data.get("api_kernels", [])
        
        # If empty at problem level, check first solution
        if not patterns and "solutions" in data and data["solutions"]:
            first_solution = data["solutions"][0]
            patterns = first_solution.get("patterns", patterns)
            api_kernels = first_solution.get("api_kernels", api_kernels)
        
        # Parse string arrays (TOML parser may return strings like '["item1", "item2"]')
        def parse_array(value):
            if isinstance(value, list):
                return value
            if isinstance(value, str):
                # Try to parse as JSON-like array
                import ast
                try:
                    parsed = ast.literal_eval(value)
                    if isinstance(parsed, list):
                        return parsed
                except:
                    pass
                # If it's a single string, wrap it
                if value and value != "[]":
                    return [value]
            return []
        
        patterns = parse_array(patterns)
        api_kernels = parse_array(api_kernels)
        
        return ProblemInfo(
            leetcode_id=leetcode_id,
            title=title,
            difficulty=difficulty,
            patterns=patterns,
            api_kernels=api_kernels,
        )
    except Exception as e:
        print(f"Warning: Failed to load {problem_file}: {e}")
        return None


def load_problem_from_solution(solution_file: Path) -> Optional[ProblemInfo]:
    """Load problem info from solution file comments."""
    import re
    try:
        content = solution_file.read_text(encoding="utf-8")
        lines = content.split("\n")
        
        # Extract problem info from comments
        leetcode_id = 0
        title = ""
        difficulty = "unknown"
        api_kernels = []
        patterns = []
        
        for i, line in enumerate(lines[:50]):  # Check first 50 lines
            line_stripped = line.strip()
            
            # Extract LeetCode number from "LeetCode 11:" format
            if "LeetCode" in line_stripped and ":" in line_stripped:
                match = re.search(r'LeetCode\s+(\d+):', line_stripped)
                if match:
                    leetcode_id = int(match.group(1))
                    # Extract title after colon
                    title_part = line_stripped.split(":", 1)[-1].strip()
                    if title_part:
                        title = title_part
            
            # Extract API Kernel
            if "API Kernel:" in line_stripped:
                kernel = line_stripped.split("API Kernel:")[-1].strip()
                if kernel:
                    api_kernels = [kernel]
            
            # Extract Pattern
            if "Pattern:" in line_stripped:
                pattern = line_stripped.split("Pattern:")[-1].strip()
                if pattern:
                    patterns = [pattern]
        
        # Extract problem number from filename if not found
        if leetcode_id == 0:
            filename = solution_file.stem
            match = re.match(r"(\d{4})_", filename)
            if match:
                leetcode_id = int(match.group(1))
        
        if leetcode_id == 0:
            return None
        
        # Try to get title from filename if not found
        if not title:
            filename = solution_file.stem
            match = re.match(r"\d{4}_(.+)", filename)
            if match:
                title = match.group(1).replace("_", " ").title()
        
        return ProblemInfo(
            leetcode_id=leetcode_id,
            title=title or f"Problem {leetcode_id}",
            difficulty=difficulty,
            patterns=patterns,
            api_kernels=api_kernels,
        )
    except Exception as e:
        return None


def collect_problems_by_kernel(kernel_id: str) -> dict[str, list[ProblemInfo]]:
    """
    Collect all problems for a given API kernel, grouped by pattern category.
    
    First tries meta/problems/*.toml, then falls back to solutions/*.py.
    
    Returns:
        Dictionary mapping category name to list of ProblemInfo
    """
    problems_by_category: dict[str, list[ProblemInfo]] = defaultdict(list)
    seen_ids: set[int] = set()
    
    # First: Load from meta/problems/*.toml
    if META_PROBLEMS_DIR.exists():
        for problem_file in META_PROBLEMS_DIR.glob("*.toml"):
            problem = load_problem_metadata(problem_file)
            if not problem:
                continue
            
            # Check if this problem uses the target kernel
            uses_kernel = kernel_id in problem.api_kernels
            
            # If no api_kernels but has patterns, infer from pattern categories
            if not uses_kernel and not problem.api_kernels:
                for pattern_id in problem.patterns:
                    if pattern_id in PATTERN_CATEGORIES:
                        uses_kernel = True
                        break
            
            if not uses_kernel:
                continue
            
            seen_ids.add(problem.leetcode_id)
            
            # Categorize by pattern
            categorized = False
            for pattern_id in problem.patterns:
                category = PATTERN_CATEGORIES.get(pattern_id)
                if category:
                    problems_by_category[category].append(problem)
                    categorized = True
                    break
            
            # If no pattern match, try to infer from kernel
            if not categorized:
                if kernel_id == "TwoPointersTraversal":
                    problems_by_category["Opposite Pointers (Two-End)"].append(problem)
    
    # Second: Fallback to solutions/*.py for missing problems
    SOLUTIONS_DIR = PROJECT_ROOT / "solutions"
    if SOLUTIONS_DIR.exists():
        for solution_file in SOLUTIONS_DIR.glob("*.py"):
            # Skip if already loaded from TOML
            filename = solution_file.stem
            import re
            match = re.match(r"(\d{4})_", filename)
            if not match:
                continue
            
            problem_id = int(match.group(1))
            if problem_id in seen_ids:
                continue
            
            problem = load_problem_from_solution(solution_file)
            if not problem:
                continue
            
            # Check if uses target kernel
            if kernel_id not in problem.api_kernels:
                continue
            
            seen_ids.add(problem.leetcode_id)
            
            # Categorize by pattern
            categorized = False
            for pattern_id in problem.patterns:
                category = PATTERN_CATEGORIES.get(pattern_id)
                if category:
                    problems_by_category[category].append(problem)
                    categorized = True
                    break
            
            # If no pattern match, default to Opposite Pointers for TwoPointersTraversal
            if not categorized and kernel_id == "TwoPointersTraversal":
                problems_by_category["Opposite Pointers (Two-End)"].append(problem)
    
    # Sort problems within each category by LeetCode ID
    for category in problems_by_category:
        problems_by_category[category].sort(key=lambda p: p.leetcode_id)
    
    return problems_by_category


def generate_problem_mapping_section(kernel_id: str) -> str:
    """
    Generate "LeetCode Problem Mapping" section from meta/problems/*.toml.
    
    Returns:
        Markdown content for the problem mapping section
    """
    problems_by_category = collect_problems_by_kernel(kernel_id)
    
    if not problems_by_category:
        return ""
    
    lines = ["## LeetCode Problem Mapping", ""]
    
    # Define category order
    category_order = [
        "Opposite Pointers (Two-End)",
        "Same-Direction Pointers (Writer)",
        "Fast–Slow Pointers",
        "Partitioning / Dutch Flag",
        "Dedup + Sorted Enumeration",
        "Merge Pattern",
    ]
    
    for category in category_order:
        if category not in problems_by_category:
            continue
        
        problems = problems_by_category[category]
        if not problems:
            continue
        
        # Category header
        lines.append(f"### {category}")
        lines.append("")
        lines.append("| ID | Problem Name | Difficulty |")
        lines.append("|----|--------------|------------|")
        
        # Problem rows
        for problem in problems:
            difficulty_capitalized = problem.difficulty.capitalize()
            lines.append(f"| {problem.leetcode_id} | {problem.title} | {difficulty_capitalized} |")
        
        lines.append("")
    
    return "\n".join(lines)

