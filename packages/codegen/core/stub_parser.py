"""
Code stub parser.

Parses LeetCode code stubs to extract structural information.
This module only parses - it does NOT infer or guess anything.
"""

import ast
import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class StubInfo:
    """
    Parsed code stub information.
    
    Attributes:
        class_name: The class name (usually "Solution")
        method_name: The method name (e.g., "twoSum", "addTwoNumbers")
        params: List of (name, type_hint) tuples, excluding 'self'
        return_type: Return type annotation string
        raw_signature: Original method signature string
        raw_stub: Original code stub
        additional_classes: Any additional class definitions (e.g., ListNode, TreeNode)
    """
    class_name: str
    method_name: str
    params: List[Tuple[str, str]]
    return_type: str
    raw_signature: str
    raw_stub: str = ""
    additional_classes: List[str] = field(default_factory=list)


def parse_code_stub(code_stub: str) -> StubInfo:
    """
    Parse LeetCode Python code stub.
    
    Args:
        code_stub: LeetCode-provided Python code template
        
    Returns:
        StubInfo: Structured information about the stub
        
    Example:
        >>> stub = '''
        ... class Solution:
        ...     def twoSum(self, nums: List[int], target: int) -> List[int]:
        ...         pass
        ... '''
        >>> info = parse_code_stub(stub)
        >>> info.method_name
        'twoSum'
        >>> info.params
        [('nums', 'List[int]'), ('target', 'int')]
        >>> info.return_type
        'List[int]'
        
    Note:
        This function only parses the stub. It does NOT:
        - Infer which helpers are needed
        - Modify or enhance the code
        - Make assumptions about the problem type
    """
    code_stub = code_stub.strip()
    
    # Try AST parsing first (most reliable)
    try:
        return _parse_with_ast(code_stub)
    except SyntaxError:
        pass
    
    # LeetCode stubs often have empty function bodies (no pass/...)
    # Try adding 'pass' to make it valid Python
    try:
        # Add 'pass' after the last colon that ends a def line
        lines = code_stub.split('\n')
        fixed_lines = []
        for i, line in enumerate(lines):
            fixed_lines.append(line)
            # Check if this line ends with ':' and looks like a def
            stripped = line.rstrip()
            if stripped.endswith(':') and 'def ' in line:
                # Check if next line is not indented code
                if i + 1 >= len(lines) or not lines[i + 1].strip():
                    # Add pass with proper indentation
                    indent = len(line) - len(line.lstrip()) + 4
                    fixed_lines.append(' ' * indent + 'pass')
        
        fixed_code = '\n'.join(fixed_lines)
        return _parse_with_ast(fixed_code)
    except SyntaxError:
        pass
    
    # Fallback to regex parsing
    return _parse_with_regex(code_stub)


def _parse_with_ast(code_stub: str) -> StubInfo:
    """Parse code stub using Python AST."""
    tree = ast.parse(code_stub)
    
    class_name = "Solution"
    method_name = ""
    params: List[Tuple[str, str]] = []
    return_type = ""
    raw_signature = ""
    additional_classes: List[str] = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if node.name == "Solution":
                class_name = node.name
                # Find the first method that's not __init__
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and not item.name.startswith("_"):
                        method_name = item.name
                        params = _extract_params(item)
                        return_type = _extract_return_type(item)
                        raw_signature = _reconstruct_signature(item, params, return_type)
                        break
            else:
                # Additional class (e.g., ListNode)
                additional_classes.append(node.name)
    
    # Also check for commented-out class definitions (LeetCode style)
    # e.g., "# class ListNode:"
    for match in re.finditer(r'#\s*class\s+(\w+)\s*:', code_stub):
        name = match.group(1)
        if name != "Solution" and name not in additional_classes:
            additional_classes.append(name)
    
    return StubInfo(
        class_name=class_name,
        method_name=method_name,
        params=params,
        return_type=return_type,
        raw_signature=raw_signature,
        raw_stub=code_stub,
        additional_classes=additional_classes,
    )


def _extract_params(func_def: ast.FunctionDef) -> List[Tuple[str, str]]:
    """Extract parameter names and type hints from function definition."""
    params = []
    
    for arg in func_def.args.args:
        if arg.arg == "self":
            continue
        
        type_hint = ""
        if arg.annotation:
            type_hint = ast.unparse(arg.annotation)
        
        params.append((arg.arg, type_hint))
    
    return params


def _extract_return_type(func_def: ast.FunctionDef) -> str:
    """Extract return type annotation from function definition."""
    if func_def.returns:
        return ast.unparse(func_def.returns)
    return ""


def _reconstruct_signature(
    func_def: ast.FunctionDef,
    params: List[Tuple[str, str]],
    return_type: str,
) -> str:
    """Reconstruct the method signature string."""
    param_strs = ["self"]
    for name, type_hint in params:
        if type_hint:
            param_strs.append(f"{name}: {type_hint}")
        else:
            param_strs.append(name)
    
    params_str = ", ".join(param_strs)
    
    if return_type:
        return f"def {func_def.name}({params_str}) -> {return_type}:"
    else:
        return f"def {func_def.name}({params_str}):"


def _parse_with_regex(code_stub: str) -> StubInfo:
    """Fallback regex-based parsing for malformed stubs."""
    
    # Remove comment lines first to avoid parsing commented-out code
    lines = code_stub.split('\n')
    non_comment_lines = [line for line in lines if not line.strip().startswith('#')]
    clean_code = '\n'.join(non_comment_lines)
    
    # Find class name (prefer Solution)
    class_match = re.search(r'class\s+Solution\s*:', clean_code)
    if not class_match:
        class_match = re.search(r'class\s+(\w+)\s*:', clean_code)
    class_name = "Solution" if class_match and 'Solution' in class_match.group(0) else (
        class_match.group(1) if class_match else "Solution"
    )
    
    # Find method signature inside Solution class
    # First, try to find the Solution class block
    solution_match = re.search(r'class\s+Solution\s*:(.+?)(?=\nclass\s|\Z)', clean_code, re.DOTALL)
    search_area = solution_match.group(1) if solution_match else clean_code
    
    # Pattern: def method_name(self, params...) -> return_type:
    method_pattern = r'def\s+(\w+)\s*\(\s*self\s*(?:,\s*(.+?))?\s*\)\s*(?:->\s*(.+?))?\s*:'
    method_match = re.search(method_pattern, search_area, re.DOTALL)
    
    if not method_match:
        return StubInfo(
            class_name=class_name,
            method_name="",
            params=[],
            return_type="",
            raw_signature="",
            raw_stub=code_stub,
        )
    
    method_name = method_match.group(1)
    params_str = method_match.group(2) or ""
    return_type = (method_match.group(3) or "").strip()
    
    # Parse parameters
    params = _parse_params_str(params_str)
    
    # Reconstruct signature
    raw_signature = method_match.group(0)
    
    # Find additional classes (from original code, including comments for class names)
    additional_classes = []
    # Look for class definitions in comments (LeetCode style: # class ListNode:)
    for match in re.finditer(r'#\s*class\s+(\w+)\s*:', code_stub):
        name = match.group(1)
        if name != "Solution":
            additional_classes.append(name)
    # Also look for actual class definitions
    for match in re.finditer(r'(?<!#\s*)class\s+(\w+)\s*:', code_stub):
        name = match.group(1)
        if name != "Solution" and name not in additional_classes:
            additional_classes.append(name)
    
    return StubInfo(
        class_name=class_name,
        method_name=method_name,
        params=params,
        return_type=return_type,
        raw_signature=raw_signature,
        raw_stub=code_stub,
        additional_classes=additional_classes,
    )


def _parse_params_str(params_str: str) -> List[Tuple[str, str]]:
    """Parse parameter string into list of (name, type) tuples."""
    if not params_str.strip():
        return []
    
    params = []
    # Split by comma, but respect brackets
    current = ""
    bracket_depth = 0
    
    for char in params_str + ",":
        if char in "([{":
            bracket_depth += 1
            current += char
        elif char in ")]}":
            bracket_depth -= 1
            current += char
        elif char == "," and bracket_depth == 0:
            param = current.strip()
            if param:
                if ":" in param:
                    name, type_hint = param.split(":", 1)
                    params.append((name.strip(), type_hint.strip()))
                else:
                    params.append((param, ""))
            current = ""
        else:
            current += char
    
    return params


def format_params_for_signature(params: List[Tuple[str, str]]) -> str:
    """
    Format parameter list for method signature.
    
    Args:
        params: List of (name, type_hint) tuples
        
    Returns:
        Formatted parameter string (without 'self')
        
    Example:
        >>> params = [('nums', 'List[int]'), ('target', 'int')]
        >>> format_params_for_signature(params)
        'nums: List[int], target: int'
    """
    parts = []
    for name, type_hint in params:
        if type_hint:
            parts.append(f"{name}: {type_hint}")
        else:
            parts.append(name)
    return ", ".join(parts)

