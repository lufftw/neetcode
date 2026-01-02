"""
IO Schema - Infer input/output format rules from LeetCode signature.

This module bridges LeetCode method signatures to the test file format.
It does NOT generate tests - it only defines the IO contract.

Architecture:
    StubInfo (from stub_parser) → IOSchema → used by checker/generator

Responsibility:
    - Infer parameter formats from type hints
    - Define separator priority for each type
    - Identify special structures (LinkedList, TreeNode, etc.)
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Set
from enum import Enum

from .stub_parser import StubInfo


class ParamFormat(Enum):
    """Format types for input parameters."""
    SCALAR = "scalar"           # int, float, bool
    STRING = "string"           # str (single line, no quotes)
    ARRAY_1D = "array_1d"       # List[int], List[str]
    ARRAY_2D = "array_2d"       # List[List[int]]
    LINKED_LIST = "linked_list" # Optional[ListNode]
    TREE = "tree"               # Optional[TreeNode]
    UNKNOWN = "unknown"


@dataclass
class ParamSchema:
    """
    Schema for a single parameter.
    
    Attributes:
        name: Parameter name (e.g., "nums", "target")
        type_hint: Original type hint string (e.g., "List[int]")
        format: Detected format type
        separator_priority: Preferred separators to try (e.g., [",", " "])
        needs_dimension: Whether 2D array needs dimension prefix
    """
    name: str
    type_hint: str
    format: ParamFormat
    separator_priority: List[str] = field(default_factory=lambda: [",", " "])
    needs_dimension: bool = False
    
    def __repr__(self) -> str:
        return f"ParamSchema({self.name}: {self.type_hint} → {self.format.value})"


@dataclass
class IOSchema:
    """
    Complete IO schema inferred from LeetCode signature.
    
    Attributes:
        method_name: The solution method name
        params: List of parameter schemas
        return_type: Return type hint string
        return_format: Detected format for output
        needs_helpers: Set of helper classes needed (ListNode, TreeNode)
    """
    method_name: str
    params: List[ParamSchema]
    return_type: str
    return_format: ParamFormat
    needs_helpers: Set[str] = field(default_factory=set)
    
    def __repr__(self) -> str:
        param_str = ", ".join(p.name for p in self.params)
        return f"IOSchema({self.method_name}({param_str}) → {self.return_type})"


# =============================================================================
# Type Inference Rules
# =============================================================================

# Mapping from type hint patterns to ParamFormat
_TYPE_PATTERNS = [
    # Order matters - more specific patterns first
    (["List[List[int]]", "List[List[str]]", "List[List[float]]"], ParamFormat.ARRAY_2D),
    (["Optional[ListNode]", "ListNode"], ParamFormat.LINKED_LIST),
    (["Optional[TreeNode]", "TreeNode"], ParamFormat.TREE),
    (["List[int]", "List[str]", "List[float]", "List[bool]"], ParamFormat.ARRAY_1D),
    (["int", "float", "bool"], ParamFormat.SCALAR),
    (["str"], ParamFormat.STRING),
]

# Helper classes that require special IO handling
_HELPER_CLASSES = {"ListNode", "TreeNode", "Node"}

# Default separator priority by format
_SEPARATOR_PRIORITY = {
    ParamFormat.SCALAR: [],
    ParamFormat.STRING: [],
    ParamFormat.ARRAY_1D: [",", " "],
    ParamFormat.ARRAY_2D: [",", " "],
    ParamFormat.LINKED_LIST: [",", " "],
    ParamFormat.TREE: [",", " "],
    ParamFormat.UNKNOWN: [",", " "],
}


def _detect_format(type_hint: str) -> ParamFormat:
    """
    Detect ParamFormat from a type hint string.
    
    Args:
        type_hint: Type annotation string (e.g., "List[int]", "Optional[ListNode]")
        
    Returns:
        ParamFormat enum value
    """
    if not type_hint:
        return ParamFormat.UNKNOWN
    
    # Normalize: remove spaces
    normalized = type_hint.replace(" ", "")
    
    # Check patterns
    for patterns, fmt in _TYPE_PATTERNS:
        for pattern in patterns:
            if pattern in normalized or normalized == pattern:
                return fmt
    
    # Check for helper classes
    for helper in _HELPER_CLASSES:
        if helper in normalized:
            if "ListNode" in helper:
                return ParamFormat.LINKED_LIST
            elif "TreeNode" in helper or "Node" in helper:
                return ParamFormat.TREE
    
    # Check generic List pattern
    if normalized.startswith("List["):
        # Check if it's nested
        inner = normalized[5:-1]  # Remove "List[" and "]"
        if inner.startswith("List["):
            return ParamFormat.ARRAY_2D
        return ParamFormat.ARRAY_1D
    
    return ParamFormat.UNKNOWN


def _detect_helpers(type_hints: List[str]) -> Set[str]:
    """
    Detect required helper classes from type hints.
    
    Args:
        type_hints: List of type hint strings
        
    Returns:
        Set of helper class names
    """
    helpers = set()
    all_types = " ".join(type_hints)
    
    for helper in _HELPER_CLASSES:
        if helper in all_types:
            helpers.add(helper)
    
    return helpers


def infer_io_schema(stub: StubInfo) -> IOSchema:
    """
    Infer IO schema from parsed LeetCode code stub.
    
    This is the main entry point for IO schema inference.
    
    Args:
        stub: Parsed StubInfo from stub_parser
        
    Returns:
        IOSchema with inferred format rules for all parameters
        
    Example:
        >>> from packages.codegen.core.stub_parser import parse_code_stub
        >>> code = '''
        ... class Solution:
        ...     def twoSum(self, nums: List[int], target: int) -> List[int]:
        ...         pass
        ... '''
        >>> stub = parse_code_stub(code)
        >>> schema = infer_io_schema(stub)
        >>> schema.params[0].format
        <ParamFormat.ARRAY_1D: 'array_1d'>
        >>> schema.params[1].format
        <ParamFormat.SCALAR: 'scalar'>
    """
    # Infer parameter schemas
    param_schemas = []
    for name, type_hint in stub.params:
        fmt = _detect_format(type_hint)
        param_schemas.append(ParamSchema(
            name=name,
            type_hint=type_hint,
            format=fmt,
            separator_priority=_SEPARATOR_PRIORITY.get(fmt, [",", " "]),
            needs_dimension=(fmt == ParamFormat.ARRAY_2D),
        ))
    
    # Infer return type format
    return_format = _detect_format(stub.return_type)
    
    # Detect helper classes
    all_types = [t for _, t in stub.params] + [stub.return_type]
    helpers = _detect_helpers(all_types)
    
    return IOSchema(
        method_name=stub.method_name,
        params=param_schemas,
        return_type=stub.return_type,
        return_format=return_format,
        needs_helpers=helpers,
    )


# =============================================================================
# Utility Functions
# =============================================================================

def format_value_for_test(value: str, param: ParamSchema, separator: str = ",") -> str:
    """
    Format a value string for test file based on param schema.
    
    This converts LeetCode example format to test file format.
    
    Args:
        value: Raw value string (e.g., "[2,7,11,15]" or "9")
        param: Parameter schema
        separator: Separator to use
        
    Returns:
        Formatted string for .in file
        
    Example:
        >>> param = ParamSchema("nums", "List[int]", ParamFormat.ARRAY_1D)
        >>> format_value_for_test("[2,7,11,15]", param)
        '2,7,11,15'
    """
    value = value.strip()
    
    if param.format == ParamFormat.SCALAR:
        # Remove any quotes or whitespace
        return value.strip('"\'')
    
    elif param.format == ParamFormat.STRING:
        # Remove surrounding quotes if present
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            return value[1:-1]
        return value
    
    elif param.format in (ParamFormat.ARRAY_1D, ParamFormat.LINKED_LIST):
        # [2,7,11,15] → 2,7,11,15 (or with space separator)
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1]
            # Normalize to requested separator
            inner = inner.replace(" ", "").replace(",", separator)
            return inner
        return value
    
    elif param.format == ParamFormat.ARRAY_2D:
        # [[2,1,1],[1,1,0],[0,1,1]] → rows\ncols\n2,1,1\n1,1,0\n0,1,1
        import ast
        try:
            matrix = ast.literal_eval(value)
            if isinstance(matrix, list) and matrix and isinstance(matrix[0], list):
                rows = len(matrix)
                cols = len(matrix[0]) if matrix else 0
                lines = [str(rows), str(cols)]
                for row in matrix:
                    lines.append(separator.join(str(x) for x in row))
                return "\n".join(lines)
        except (ValueError, SyntaxError):
            pass
        return value
    
    return value


def parse_test_value(lines: List[str], param: ParamSchema, 
                     start_idx: int = 0, separator: str = ",") -> Tuple[any, int]:
    """
    Parse test file lines into a Python value based on param schema.
    
    This is the inverse of format_value_for_test.
    
    Args:
        lines: Lines from .in file
        param: Parameter schema
        start_idx: Starting line index
        separator: Expected separator
        
    Returns:
        Tuple of (parsed_value, next_line_index)
    """
    if start_idx >= len(lines):
        return None, start_idx
    
    if param.format == ParamFormat.SCALAR:
        value = lines[start_idx].strip()
        # Try int, then float
        try:
            return int(value), start_idx + 1
        except ValueError:
            try:
                return float(value), start_idx + 1
            except ValueError:
                return value, start_idx + 1
    
    elif param.format == ParamFormat.STRING:
        return lines[start_idx].strip(), start_idx + 1
    
    elif param.format in (ParamFormat.ARRAY_1D, ParamFormat.LINKED_LIST):
        line = lines[start_idx].strip()
        # Try both separators
        for sep in [separator] + param.separator_priority:
            if sep in line:
                parts = [p.strip() for p in line.split(sep)]
                # Try to convert to int/float
                try:
                    return [int(p) for p in parts], start_idx + 1
                except ValueError:
                    try:
                        return [float(p) for p in parts], start_idx + 1
                    except ValueError:
                        return parts, start_idx + 1
        # Single element or string
        return [line] if line else [], start_idx + 1
    
    elif param.format == ParamFormat.ARRAY_2D:
        # First two lines are dimensions
        rows = int(lines[start_idx].strip())
        cols = int(lines[start_idx + 1].strip())
        matrix = []
        for i in range(rows):
            line = lines[start_idx + 2 + i].strip()
            for sep in [separator] + param.separator_priority:
                if sep in line:
                    parts = [p.strip() for p in line.split(sep)]
                    try:
                        matrix.append([int(p) for p in parts])
                    except ValueError:
                        matrix.append(parts)
                    break
            else:
                matrix.append([line] if line else [])
        return matrix, start_idx + 2 + rows
    
    return lines[start_idx], start_idx + 1


if __name__ == "__main__":
    # Demo
    from .stub_parser import parse_code_stub
    
    test_cases = [
        """
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        pass
""",
        """
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        pass
""",
        """
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        pass
""",
    ]
    
    for code in test_cases:
        stub = parse_code_stub(code)
        schema = infer_io_schema(stub)
        print(f"\n{schema}")
        for p in schema.params:
            print(f"  {p}")
        print(f"  Return: {schema.return_format.value}")
        if schema.needs_helpers:
            print(f"  Helpers: {schema.needs_helpers}")


