"""
Solve Function Generator - Generate solve() function based on IO schema.

This module generates the solve() function that:
1. Reads input from stdin
2. Parses input according to parameter types
3. Calls the solution method
4. Formats and prints the output

Tier 0 Coverage:
- Scalar types: int, float, bool, str
- 1D arrays: List[int], List[float], List[str]
- 2D arrays: List[List[int]]
- Return types: Same as above, plus simple scalar

Supported Input Format: JSON literal (one per line for each parameter)
"""

from dataclasses import dataclass
from typing import List, Set
from .stub_parser import StubInfo
from .io_schema import IOSchema, ParamSchema, ParamFormat, infer_io_schema


@dataclass
class SolveGenerationResult:
    """Result of solve() generation."""
    code: str
    imports: Set[str]
    is_placeholder: bool = False
    unsupported_types: List[str] = None
    
    def __post_init__(self):
        if self.unsupported_types is None:
            self.unsupported_types = []


def _get_parse_code(param: ParamSchema, line_var: str = "line") -> str:
    """
    Generate parsing code for a parameter.
    
    Args:
        param: Parameter schema
        line_var: Variable name holding the line
        
    Returns:
        Python expression to parse the parameter
    """
    type_hint = param.type_hint or ""
    
    # Scalar types
    if type_hint == "int":
        return f"int({line_var}.strip())"
    if type_hint == "float":
        return f"float({line_var}.strip())"
    if type_hint == "str":
        # Could be quoted or plain
        return f"json.loads({line_var}.strip()) if {line_var}.strip().startswith('\"') else {line_var}.strip()"
    if type_hint == "bool":
        return f"{line_var}.strip().lower() == 'true'"
    
    # 1D arrays
    if type_hint in ("List[int]", "list[int]"):
        return f"json.loads({line_var}.strip())"
    if type_hint in ("List[float]", "list[float]"):
        return f"json.loads({line_var}.strip())"
    if type_hint in ("List[str]", "list[str]"):
        return f"json.loads({line_var}.strip())"
    if type_hint in ("List[bool]", "list[bool]"):
        return f"json.loads({line_var}.strip())"
    
    # 2D arrays
    if type_hint in ("List[List[int]]", "list[list[int]]"):
        return f"json.loads({line_var}.strip())"
    if type_hint in ("List[List[str]]", "list[list[str]]"):
        return f"json.loads({line_var}.strip())"
    
    # Fallback: try json.loads
    return f"json.loads({line_var}.strip())"


def _get_output_code(return_type: str, result_var: str = "result") -> str:
    """
    Generate output formatting code.
    
    Args:
        return_type: Return type hint
        result_var: Variable name holding the result
        
    Returns:
        Python code to print the result
    """
    if not return_type:
        return f"print({result_var})"
    
    # Boolean - print lowercase
    if return_type == "bool":
        return f"print('true' if {result_var} else 'false')"
    
    # Scalar types
    if return_type in ("int", "float", "str"):
        return f"print({result_var})"
    
    # Arrays - print as JSON
    if "List" in return_type or "list" in return_type:
        return f"print(json.dumps({result_var}, separators=(',', ':')))"
    
    # Default: just print
    return f"print({result_var})"


def generate_solve_function(stub_info: StubInfo, io_schema: IOSchema = None) -> SolveGenerationResult:
    """
    Generate solve() function code.
    
    Args:
        stub_info: Parsed stub information
        io_schema: Optional pre-computed IO schema
        
    Returns:
        SolveGenerationResult with generated code
    """
    if io_schema is None:
        io_schema = infer_io_schema(stub_info)
    
    # Check for unsupported types (Tier 1+)
    unsupported = []
    for param in io_schema.params:
        if param.format in (ParamFormat.LINKED_LIST, ParamFormat.TREE):
            unsupported.append(f"{param.name}: {param.type_hint}")
    
    if io_schema.return_format in (ParamFormat.LINKED_LIST, ParamFormat.TREE):
        unsupported.append(f"return: {io_schema.return_type}")
    
    # Generate placeholder if unsupported types
    if unsupported:
        code = _generate_placeholder_solve(stub_info, io_schema, unsupported)
        return SolveGenerationResult(
            code=code,
            imports={"sys"},
            is_placeholder=True,
            unsupported_types=unsupported,
        )
    
    # Generate full solve function
    imports = {"sys", "json"}
    
    lines = []
    lines.append("def solve():")
    lines.append('    """')
    lines.append("    Input format (JSON literal, one per line):")
    for param in io_schema.params:
        lines.append(f"        {param.name}: {param.type_hint}")
    lines.append("")
    lines.append(f"    Output: {io_schema.return_type}")
    lines.append('    """')
    lines.append("    import sys")
    lines.append("    import json")
    lines.append("")
    lines.append("    data = sys.stdin.read().strip().split('\\n')")
    lines.append("")
    
    # Parse each parameter
    for i, param in enumerate(io_schema.params):
        parse_code = _get_parse_code(param, f"data[{i}]")
        lines.append(f"    {param.name} = {parse_code}")
    
    lines.append("")
    
    # Call the solution method
    params_str = ", ".join(p.name for p in io_schema.params)
    lines.append("    solver = get_solver(SOLUTIONS)")
    lines.append(f"    result = solver.{io_schema.method_name}({params_str})")
    lines.append("")
    
    # Output
    output_code = _get_output_code(io_schema.return_type)
    lines.append(f"    {output_code}")
    
    return SolveGenerationResult(
        code="\n".join(lines),
        imports=imports,
        is_placeholder=False,
    )


def _generate_placeholder_solve(stub_info: StubInfo, io_schema: IOSchema, 
                                 unsupported: List[str]) -> str:
    """Generate a placeholder solve() for unsupported types."""
    lines = []
    lines.append("def solve():")
    lines.append('    """')
    lines.append("    TODO: Implement input/output handling for this problem.")
    lines.append("")
    lines.append("    Unsupported types detected:")
    for u in unsupported:
        lines.append(f"        - {u}")
    lines.append("")
    lines.append("    Input format (suggested):")
    for param in io_schema.params:
        lines.append(f"        {param.name}: {param.type_hint}")
    lines.append("")
    lines.append(f"    Output: {io_schema.return_type}")
    lines.append('    """')
    lines.append("    import sys")
    lines.append("")
    lines.append("    # TODO: Parse input")
    lines.append("    data = sys.stdin.read().strip().split('\\n')")
    lines.append("")
    
    # Generate parameter stubs
    for i, param in enumerate(io_schema.params):
        if "ListNode" in param.type_hint:
            lines.append(f"    # {param.name}: Parse linked list from data[{i}]")
            lines.append(f"    # Example: [1,2,3] -> ListNode chain")
            lines.append(f"    {param.name} = None  # TODO")
        elif "TreeNode" in param.type_hint:
            lines.append(f"    # {param.name}: Parse tree from data[{i}]")
            lines.append(f"    # Example: [1,null,2,3] -> TreeNode")
            lines.append(f"    {param.name} = None  # TODO")
        else:
            parse_code = _get_parse_code(param, f"data[{i}]")
            lines.append(f"    {param.name} = {parse_code}")
    
    lines.append("")
    lines.append("    solver = get_solver(SOLUTIONS)")
    params_str = ", ".join(p.name for p in io_schema.params)
    lines.append(f"    result = solver.{io_schema.method_name}({params_str})")
    lines.append("")
    
    # Output placeholder
    if "ListNode" in io_schema.return_type:
        lines.append("    # TODO: Convert ListNode to output format")
        lines.append("    # Example: ListNode chain -> [1,2,3]")
        lines.append("    print(result)")
    elif "TreeNode" in io_schema.return_type:
        lines.append("    # TODO: Convert TreeNode to output format")
        lines.append("    # Example: TreeNode -> [1,null,2,3]")
        lines.append("    print(result)")
    else:
        output_code = _get_output_code(io_schema.return_type)
        lines.append(f"    {output_code}")
    
    return "\n".join(lines)


def generate_solve_for_problem(code_stub: str) -> SolveGenerationResult:
    """
    Convenience function to generate solve() from code stub.
    
    Args:
        code_stub: LeetCode Python code stub
        
    Returns:
        SolveGenerationResult
    """
    from .stub_parser import parse_code_stub
    stub_info = parse_code_stub(code_stub)
    io_schema = infer_io_schema(stub_info)
    return generate_solve_function(stub_info, io_schema)


if __name__ == "__main__":
    # Test with a few examples
    from .stub_parser import parse_code_stub
    
    # Test 1: Two Sum (simple case)
    stub1 = """
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        pass
"""
    print("=" * 60)
    print("Test 1: Two Sum")
    print("=" * 60)
    result1 = generate_solve_for_problem(stub1)
    print(result1.code)
    print(f"\nIs placeholder: {result1.is_placeholder}")
    
    # Test 2: Linked List (placeholder case)
    stub2 = """
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        pass
"""
    print("\n" + "=" * 60)
    print("Test 2: Reverse Linked List (placeholder)")
    print("=" * 60)
    result2 = generate_solve_for_problem(stub2)
    print(result2.code)
    print(f"\nIs placeholder: {result2.is_placeholder}")
    print(f"Unsupported: {result2.unsupported_types}")

