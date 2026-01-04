"""
Practice file infrastructure reuse.

Extracts and transforms components from reference solutions
for use in practice files.
"""

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Dict, Any


@dataclass
class ExtractedInfrastructure:
    """Infrastructure extracted from a reference solution."""
    
    # File-level docstring
    header: str = ""
    
    # Import statements
    imports: str = ""
    
    # Helper classes (ListNode, TreeNode, etc.)
    helper_classes: str = ""
    
    # JUDGE_FUNC and related functions
    judge_func: str = ""
    
    # SOLUTIONS dictionary (original)
    solutions_dict_raw: str = ""
    
    # Solution class definitions (original)
    solution_classes: Dict[str, str] = field(default_factory=dict)
    
    # Helper functions (list_to_linkedlist, etc.)
    helper_functions: str = ""
    
    # solve() function
    solve_fn: str = ""
    
    # Metadata
    method_name: str = ""
    solution_count: int = 0
    solution_names: List[str] = field(default_factory=list)


def extract_infrastructure(reference_path: Path) -> ExtractedInfrastructure:
    """
    Extract all infrastructure components from a reference solution.
    
    Args:
        reference_path: Path to reference solution file
        
    Returns:
        ExtractedInfrastructure containing all components
    """
    content = reference_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    
    result = ExtractedInfrastructure()
    
    # Extract header (docstring at start of file)
    result.header = _extract_docstring(content)
    
    # Parse with AST for structured extraction
    try:
        tree = ast.parse(content)
        result = _extract_with_ast(content, tree, result)
    except SyntaxError:
        # Fallback to regex-based extraction
        result = _extract_with_regex(content, result)
    
    return result


def _extract_docstring(content: str) -> str:
    """Extract file-level docstring."""
    # Skip leading comments and find the docstring
    lines = content.split('\n')
    
    # Skip leading comments and blank lines
    start_idx = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('#') or stripped == '':
            continue
        start_idx = i
        break
    
    # Check if we have a docstring
    remaining = '\n'.join(lines[start_idx:])
    
    # Match triple-quoted docstring
    match = re.match(r'^("""[\s\S]*?""")', remaining)
    if match:
        return match.group(1)
    
    match = re.match(r"^('''[\s\S]*?''')", remaining)
    if match:
        return match.group(1)
    
    return ""


def _extract_with_ast(
    content: str,
    tree: ast.Module,
    result: ExtractedInfrastructure,
) -> ExtractedInfrastructure:
    """Extract components using AST parsing."""
    lines = content.split("\n")
    
    # Track what we've extracted
    imports_lines = []
    helper_class_names = {"ListNode", "TreeNode", "Node", "DoublyListNode", "NestedInteger"}
    solution_class_names = set()
    
    for node in tree.body:
        start_line = node.lineno - 1  # AST lines are 1-indexed
        end_line = node.end_lineno
        node_text = "\n".join(lines[start_line:end_line])
        
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            imports_lines.append(node_text)
        
        elif isinstance(node, ast.ClassDef):
            if node.name in helper_class_names:
                result.helper_classes += node_text + "\n\n"
            elif node.name.startswith("Solution"):
                solution_class_names.add(node.name)
                result.solution_classes[node.name] = node_text
                # Extract method name from first non-dunder method
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and not item.name.startswith("_"):
                        result.method_name = item.name
                        break
        
        elif isinstance(node, ast.FunctionDef):
            func_name = node.name
            if func_name == "solve":
                result.solve_fn = node_text
            elif func_name == "judge":
                result.judge_func += node_text + "\n\n"
            elif func_name.startswith(("list_to_", "linkedlist_to_", "tree_to_", "_")):
                # Helper functions or private functions for judge
                if "judge" in content[:content.find(node_text)] or func_name.startswith("_"):
                    result.judge_func += node_text + "\n\n"
                else:
                    result.helper_functions += node_text + "\n\n"
        
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if target.id == "SOLUTIONS":
                        result.solutions_dict_raw = node_text
                    elif target.id == "JUDGE_FUNC":
                        result.judge_func += node_text + "\n"
    
    result.imports = "\n".join(imports_lines)
    result.solution_count = len(solution_class_names)
    result.solution_names = sorted(solution_class_names)
    
    return result


def _extract_with_regex(content: str, result: ExtractedInfrastructure) -> ExtractedInfrastructure:
    """Fallback regex-based extraction."""
    
    # Extract imports (lines starting with import or from)
    import_lines = []
    for line in content.split("\n"):
        if line.strip().startswith(("import ", "from ")):
            import_lines.append(line)
    result.imports = "\n".join(import_lines)
    
    # Extract SOLUTIONS dict
    match = re.search(r'(SOLUTIONS\s*=\s*\{[\s\S]*?\n\})', content)
    if match:
        result.solutions_dict_raw = match.group(1)
    
    # Extract solve function
    match = re.search(r'(def solve\(\)[\s\S]*?)(?=\nif __name__|$)', content)
    if match:
        result.solve_fn = match.group(1).rstrip()
    
    return result


def clear_solution_body(
    solution_code: str,
    rename_to_solution: bool = True,
) -> str:
    """
    Clear the body of a Solution class, keeping only LeetCode-style methods.
    
    Keeps:
      - __init__ (for design problems like LRU Cache, MinStack)
      - All public methods (not starting with _)
    
    Removes:
      - Private helper methods (starting with single _, like _mergeTwoLists)
      - Other dunder methods (except __init__)
    
    Args:
        solution_code: Complete Solution class code
        rename_to_solution: If True, rename class to "Solution" (LeetCode style)
        
    Returns:
        Solution class with cleared body (TODO placeholder)
    """
    try:
        tree = ast.parse(solution_code)
    except SyntaxError:
        return _clear_body_regex(solution_code, rename_to_solution)
    
    lines = solution_code.split("\n")
    result_lines = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Keep class definition line, optionally rename to "Solution"
            class_line = lines[node.lineno - 1]
            if rename_to_solution and node.name.startswith("Solution"):
                class_line = re.sub(r'class\s+Solution\w*', 'class Solution', class_line)
            result_lines.append(class_line)
            
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    method_name = item.name
                    
                    # Keep: __init__ (design problems) + public methods
                    # Skip: private helpers (_method) and other dunders (__str__ etc.)
                    if method_name == "__init__":
                        pass  # Keep __init__ for design problems
                    elif method_name.startswith("_"):
                        continue  # Skip private helpers and other dunders
                    
                    # Get method signature
                    sig_line = lines[item.lineno - 1]
                    result_lines.append(sig_line)
                    result_lines.append("        # TODO: Implement your solution")
                    result_lines.append("        pass")
                    result_lines.append("")
    
    return "\n".join(result_lines).rstrip()


def _clear_body_regex(
    solution_code: str,
    rename_to_solution: bool = True,
) -> str:
    """Regex fallback for clearing solution body."""
    result = solution_code
    
    # Optionally rename class to "Solution"
    if rename_to_solution:
        result = re.sub(r'class\s+Solution\w*', 'class Solution', result)
    
    # Keep __init__ and public methods, skip private helpers (_method)
    # Pattern matches: __init__ OR public methods (not starting with _)
    pattern = r'(def\s+(?:__init__|(?!_)\w+)\(self[^)]*\)[^:]*:)\s*(?:"""[\s\S]*?""")?[\s\S]*?(?=\n    def |\nclass |\Z)'
    
    def replacer(match):
        sig = match.group(1)
        return f"{sig}\n        # TODO: Implement your solution\n        pass\n"
    
    return re.sub(pattern, replacer, result)


def transform_solutions_dict_for_practice(
    solutions_dict_raw: str,
    mode: str = "single",
    leetcode_style: bool = True,
) -> str:
    """
    Transform SOLUTIONS dict for practice file.
    
    Args:
        solutions_dict_raw: Original SOLUTIONS dictionary string
        mode: "single" (only default) or "all" (keep all entries)
        leetcode_style: If True, rename class to "Solution" (LeetCode style)
        
    Returns:
        Transformed SOLUTIONS dict with cleared complexity/description
    """
    try:
        # Parse the dict to get structure
        # Extract dict literal from assignment
        match = re.search(r'SOLUTIONS\s*=\s*(\{[\s\S]*\})', solutions_dict_raw)
        if not match:
            return solutions_dict_raw
        
        dict_str = match.group(1)
        solutions = ast.literal_eval(dict_str)
        
        if mode == "single":
            # Keep only default
            default_entry = solutions.get("default", {})
            solutions = {"default": default_entry}
        
        # Clear complexity and description, optionally rename class
        for key, entry in solutions.items():
            entry["complexity"] = "TODO: O(?)"
            entry["description"] = "TODO: describe your approach"
            if leetcode_style:
                entry["class"] = "Solution"
        
        # Format back to string
        lines = [
            "# ============================================",
            "# SOLUTIONS metadata - tells test_runner which solutions are available",
            "# Polymorphic pattern: each entry specifies class + method",
            "# ============================================",
            "SOLUTIONS = {",
        ]
        
        for key, entry in solutions.items():
            lines.append(f'    "{key}": {{')
            lines.append(f'        "class": "{entry.get("class", "Solution")}",')
            lines.append(f'        "method": "{entry.get("method", "")}",')
            lines.append(f'        "complexity": "{entry.get("complexity", "TODO: O(?)")}",')
            lines.append(f'        "description": "{entry.get("description", "TODO: describe your approach")}",')
            lines.append("    },")
        
        lines.append("}")
        
        return "\n".join(lines)
        
    except (ValueError, SyntaxError):
        # Fallback: return original with regex replacement
        result = re.sub(
            r'"complexity":\s*"[^"]*"',
            '"complexity": "TODO: O(?)"',
            solutions_dict_raw
        )
        result = re.sub(
            r'"description":\s*"[^"]*"',
            '"description": "TODO: describe your approach"',
            result
        )
        if leetcode_style:
            result = re.sub(
                r'"class":\s*"Solution\w*"',
                '"class": "Solution"',
                result
            )
        return result


def get_solution_classes_for_practice(
    infrastructure: ExtractedInfrastructure,
    mode: str = "single",
    leetcode_style: bool = True,
) -> str:
    """
    Get Solution class(es) for practice file.
    
    Args:
        infrastructure: Extracted infrastructure
        mode: "single" or "all"
        leetcode_style: If True, rename class to "Solution" (LeetCode style)
        
    Returns:
        Solution class(es) with cleared bodies (only public methods + __init__)
    """
    if mode == "single":
        # Get the class name from SOLUTIONS["default"]["class"]
        default_class = _get_default_class_name(infrastructure.solutions_dict_raw)
        
        if default_class and default_class in infrastructure.solution_classes:
            return clear_solution_body(
                infrastructure.solution_classes[default_class],
                rename_to_solution=leetcode_style,
            )
        
        # Fallback: try "Solution" (generic name)
        if "Solution" in infrastructure.solution_classes:
            return clear_solution_body(
                infrastructure.solution_classes["Solution"],
                rename_to_solution=leetcode_style,
            )
        
        # Last resort: first available
        if infrastructure.solution_classes:
            first_name = sorted(infrastructure.solution_classes.keys())[0]
            return clear_solution_body(
                infrastructure.solution_classes[first_name],
                rename_to_solution=leetcode_style,
            )
        return ""
    
    # "all" mode - include all Solution classes (keep original names)
    cleared = []
    for name in sorted(infrastructure.solution_classes.keys()):
        cleared.append(clear_solution_body(
            infrastructure.solution_classes[name],
            rename_to_solution=False,  # Keep original names in "all" mode
        ))
    
    return "\n\n".join(cleared)


def _get_default_class_name(solutions_dict_raw: str) -> Optional[str]:
    """
    Extract the class name from SOLUTIONS["default"]["class"].
    
    Args:
        solutions_dict_raw: Raw SOLUTIONS dictionary string
        
    Returns:
        Class name or None if not found
    """
    return _get_default_field(solutions_dict_raw, "class")


def _get_default_method_name(solutions_dict_raw: str) -> Optional[str]:
    """
    Extract the method name from SOLUTIONS["default"]["method"].
    
    Args:
        solutions_dict_raw: Raw SOLUTIONS dictionary string
        
    Returns:
        Method name or None if not found
    """
    return _get_default_field(solutions_dict_raw, "method")


def _get_default_field(solutions_dict_raw: str, field: str) -> Optional[str]:
    """
    Extract a field value from SOLUTIONS["default"].
    
    Args:
        solutions_dict_raw: Raw SOLUTIONS dictionary string
        field: Field name to extract ("class" or "method")
        
    Returns:
        Field value or None if not found
    """
    try:
        match = re.search(r'SOLUTIONS\s*=\s*(\{[\s\S]*\})', solutions_dict_raw)
        if not match:
            return None
        
        dict_str = match.group(1)
        solutions = ast.literal_eval(dict_str)
        
        default_entry = solutions.get("default", {})
        return default_entry.get(field)
    except (ValueError, SyntaxError):
        # Regex fallback
        match = re.search(rf'"default"[^}}]*"{field}"\s*:\s*"([^"]+)"', solutions_dict_raw)
        if match:
            return match.group(1)
        return None

