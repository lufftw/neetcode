"""
Module assembly.

Assembles all generated sections into a complete solution/practice file.
This provides a single point of control for file structure.
"""

from typing import Optional


def assemble_module(
    header: str,
    imports: str,
    helpers: str = "",
    judge_func: str = "",
    solutions_dict: str = "",
    solution_classes: str = "",
    helper_functions: str = "",
    solve_fn: str = "",
    include_main: bool = True,
) -> str:
    """
    Assemble a complete solution/practice module.
    
    This function combines all sections into a properly formatted
    Python file with consistent spacing.
    
    Args:
        header: File-level docstring (including triple quotes)
        imports: Import statements block
        helpers: Helper class definitions (e.g., ListNode)
        judge_func: JUDGE_FUNC definition (optional)
        solutions_dict: SOLUTIONS = {...} block
        solution_classes: Solution class(es) definition
        helper_functions: Helper function definitions
        solve_fn: solve() function definition
        include_main: Whether to include if __name__ == "__main__" block
        
    Returns:
        Complete Python module content as string
        
    Example:
        >>> content = assemble_module(
        ...     header='\"\"\"Problem: Two Sum...\"\"\"',
        ...     imports='from typing import List',
        ...     solutions_dict='SOLUTIONS = {...}',
        ...     solution_classes='class Solution: ...',
        ...     solve_fn='def solve(): ...',
        ... )
    """
    sections = []
    
    # Header (docstring)
    if header.strip():
        sections.append(header.strip())
    
    # Imports
    if imports.strip():
        sections.append(imports.strip())
    
    # Helper classes
    if helpers.strip():
        sections.append(helpers.strip())
    
    # JUDGE_FUNC (optional)
    if judge_func.strip():
        sections.append(judge_func.strip())
    
    # SOLUTIONS dict
    if solutions_dict.strip():
        sections.append(solutions_dict.strip())
    
    # Solution classes
    if solution_classes.strip():
        sections.append(solution_classes.strip())
    
    # Helper functions
    if helper_functions.strip():
        sections.append(helper_functions.strip())
    
    # solve() function
    if solve_fn.strip():
        sections.append(solve_fn.strip())
    
    # Main block
    if include_main:
        sections.append('if __name__ == "__main__":\n    solve()')
    
    # Join with double newlines for proper spacing
    content = "\n\n\n".join(sections)
    
    # Ensure single trailing newline
    return content.rstrip() + "\n"


def assemble_solutions_dict(
    method_name: str,
    class_name: str = "Solution",
    complexity: str = "TODO: O(?)",
    description: str = "TODO: describe your approach",
) -> str:
    """
    Generate SOLUTIONS metadata dictionary.
    
    Args:
        method_name: The solution method name
        class_name: The solution class name (default: "Solution")
        complexity: Complexity description
        description: Approach description
        
    Returns:
        SOLUTIONS dict definition string
    """
    return f'''# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# Polymorphic pattern: each entry specifies class + method
# ============================================
SOLUTIONS = {{
    "default": {{
        "class": "{class_name}",
        "method": "{method_name}",
        "complexity": "{complexity}",
        "description": "{description}",
    }},
}}'''


def assemble_solution_class(
    method_name: str,
    params_str: str,
    return_type: str,
    class_name: str = "Solution",
    body: str = "# TODO: Implement your solution\n        pass",
    docstring: Optional[str] = None,
) -> str:
    """
    Generate Solution class definition.
    
    Args:
        method_name: Method name
        params_str: Formatted parameters string (without self)
        return_type: Return type annotation
        class_name: Class name (default: "Solution")
        body: Method body (default: TODO placeholder)
        docstring: Optional method docstring
        
    Returns:
        Complete class definition string
    """
    # Build signature
    if params_str:
        signature = f"def {method_name}(self, {params_str})"
    else:
        signature = f"def {method_name}(self)"
    
    if return_type:
        signature += f" -> {return_type}"
    signature += ":"
    
    # Build method content
    method_content = []
    if docstring:
        method_content.append(f'        """{docstring}"""')
    method_content.append(f"        {body}")
    
    return f"""# ============================================
# Solution
# ============================================
class {class_name}:
    {signature}
{chr(10).join(method_content)}"""


def assemble_solve_function(
    method_name: str,
    input_format: str = "TODO: Define input format",
    example_input: str = "TODO: Add example",
    parse_code: str = "# TODO: Parse input\n    pass",
    call_code: Optional[str] = None,
    output_format: str = "# TODO: Print result\n    # print(result)",
) -> str:
    """
    Generate solve() function.
    
    Args:
        method_name: Solution method name
        input_format: Description of input format
        example_input: Example input
        parse_code: Code for parsing input
        call_code: Code for calling solution method
        output_format: Code for formatting output
        
    Returns:
        solve() function definition string
    """
    if call_code is None:
        call_code = f"# result = solver.{method_name}(...)"
    
    return f'''# ============================================
# solve() - stdin/stdout interface
# ============================================
def solve():
    """
    Input format:
        {input_format}
        
    Example:
        {example_input}
    """
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    
    {parse_code}
    
    solver = get_solver(SOLUTIONS)
    {call_code}
    
    {output_format}'''


def assemble_practice_marker(
    reference_path: str,
    solution_count: int = 1,
) -> str:
    """
    Generate practice file marker comment.
    
    Args:
        reference_path: Path to reference solution
        solution_count: Number of solutions in reference
        
    Returns:
        Marker comment block
    """
    if solution_count > 1:
        hint = f"# 💡 Reference has {solution_count} approaches: {reference_path}"
    else:
        hint = f"# 💡 Reference: {reference_path}"
    
    return f"""# ============================================================
# 👇 YOUR SOLUTION - Implement below
{hint}
# ============================================================"""

