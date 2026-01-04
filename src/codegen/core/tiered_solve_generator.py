"""
Tiered Solve Generator - Generate solve() for Tier-1 and Tier-1.5 problems.

This module generates solve() functions that:
1. Read problem config to determine tier and codec needs
2. Use codec functions to parse/encode complex types
3. Support both inline and import codec modes

Tier Coverage:
- Tier-0: Primitive types (handled by solve_generator.py)
- Tier-1: ListNode, TreeNode with value-based I/O
- Tier-1.5: Semantic I/O (cycles, random pointers, intersections)
"""

from typing import List, Set, Optional, Tuple
from dataclasses import dataclass

from .stub_parser import StubInfo
from .io_schema import IOSchema, ParamSchema, ParamFormat, infer_io_schema
from .problem_support import load_problem_config, ProblemConfig
from codegen.core.catalog import get, get_with_deps


@dataclass
class TieredSolveResult:
    """Result of tiered solve() generation."""
    solve_code: str
    helper_code: str  # Inline helpers (if codec_mode is inline)
    codec_import: str  # Import statement for codec (if codec_mode is import)
    imports: Set[str]
    tier: str
    codec_mode: str


# =============================================================================
# Tier-1: Value-based I/O Templates
# =============================================================================

TIER1_TEMPLATES = {
    # ListNode: list -> linked list -> solution -> linked list -> list
    "list_to_list": '''def solve():
    """
    Input: JSON array (one per line for each param)
    Output: JSON array
    """
    import sys
    import json
    
    lines = sys.stdin.read().strip().split('\\n')
    {parse_code}
    
    solver = get_solver(SOLUTIONS)
    result = solver.{method_name}({call_params})
    
    {output_code}''',

    # TreeNode: list -> tree -> solution -> tree -> list
    "tree_to_tree": '''def solve():
    """
    Input: Level-order tree as JSON array
    Output: Level-order tree as JSON array
    """
    import sys
    import json
    
    lines = sys.stdin.read().strip().split('\\n')
    {parse_code}
    
    solver = get_solver(SOLUTIONS)
    result = solver.{method_name}({call_params})
    
    {output_code}''',
}


def _detect_type_category(type_hint: str) -> str:
    """Detect the category of a type hint."""
    if not type_hint:
        return "primitive"
    
    type_lower = type_hint.lower()
    
    if "listnode" in type_lower:
        return "listnode"
    if "treenode" in type_lower:
        return "treenode"
    if "node" in type_lower:
        # Could be N-ary, Graph, or Random Pointer
        return "node"
    
    return "primitive"


def _generate_parse_code(params: List[ParamSchema], config: ProblemConfig) -> Tuple[str, str]:
    """
    Generate parse code for parameters.
    
    Returns:
        Tuple of (parse_code, call_params)
    """
    parse_lines = []
    call_params = []
    
    hints = set(config.codec_hints)
    
    for i, param in enumerate(params):
        cat = _detect_type_category(param.type_hint)
        
        if cat == "listnode":
            if "build_list_with_cycle" in hints:
                # Tier-1.5: Cycle list (2 lines: values, pos)
                parse_lines.append(f"    values = json.loads(lines[{i * 2}])")
                parse_lines.append(f"    pos = int(lines[{i * 2 + 1}])")
                parse_lines.append(f"    {param.name}, nodes = build_list_with_cycle(values, pos)")
                call_params.append(param.name)
            else:
                # Tier-1: Simple list
                parse_lines.append(f"    {param.name}_list = json.loads(lines[{i}])")
                parse_lines.append(f"    {param.name} = list_to_linkedlist({param.name}_list)")
                call_params.append(param.name)
        
        elif cat == "treenode":
            parse_lines.append(f"    {param.name}_list = json.loads(lines[{i}])")
            parse_lines.append(f"    {param.name} = list_to_tree({param.name}_list)")
            call_params.append(param.name)
        
        elif cat == "node":
            if "build_random_pointer_list" in hints:
                parse_lines.append(f"    {param.name}_pairs = json.loads(lines[{i}])")
                parse_lines.append(f"    {param.name} = build_random_pointer_list({param.name}_pairs)")
                call_params.append(param.name)
            elif "adjacency_to_graph" in hints:
                parse_lines.append(f"    {param.name}_adj = json.loads(lines[{i}])")
                parse_lines.append(f"    {param.name} = adjacency_to_graph({param.name}_adj)")
                call_params.append(param.name)
            else:
                # Fallback
                parse_lines.append(f"    {param.name} = json.loads(lines[{i}])")
                call_params.append(param.name)
        
        else:
            # Primitive
            type_hint = param.type_hint or ""
            if type_hint == "int":
                parse_lines.append(f"    {param.name} = int(lines[{i}])")
            elif type_hint == "bool":
                parse_lines.append(f"    {param.name} = lines[{i}].strip().lower() == 'true'")
            else:
                parse_lines.append(f"    {param.name} = json.loads(lines[{i}])")
            call_params.append(param.name)
    
    return "\n".join(parse_lines), ", ".join(call_params)


def _generate_output_code(return_type: str, config: ProblemConfig) -> str:
    """Generate output code based on return type and config."""
    cat = _detect_type_category(return_type)
    hints = set(config.codec_hints)
    
    if cat == "listnode":
        if "node_to_index" in hints:
            # Tier-1.5: Return node index
            return "    idx = node_to_index(result, nodes)\n    print(idx)"
        else:
            # Tier-1: Return list
            return "    out = linkedlist_to_list(result)\n    print(json.dumps(out))"
    
    elif cat == "treenode":
        return "    out = tree_to_list(result)\n    print(json.dumps(out))"
    
    elif cat == "node":
        if "encode_random_pointer_list" in hints:
            return "    out = encode_random_pointer_list(result)\n    print(json.dumps(out))"
        elif "graph_to_adjacency" in hints:
            return "    out = graph_to_adjacency(result)\n    print(json.dumps(out))"
        else:
            return "    print(result)"
    
    elif return_type == "bool":
        return "    print('true' if result else 'false')"
    
    elif return_type == "int":
        return "    print(result)"
    
    elif "List" in return_type or "list" in return_type:
        return "    print(json.dumps(result))"
    
    else:
        return "    print(result)"


def generate_tiered_solve(
    stub_info: StubInfo,
    problem_id: str,
    io_schema: IOSchema = None,
    codec_mode_override: Optional[str] = None,
) -> TieredSolveResult:
    """
    Generate solve() function for Tier-1/1.5 problems.
    
    Args:
        stub_info: Parsed stub information
        problem_id: Problem ID for config lookup
        io_schema: Optional pre-computed IO schema
        
    Returns:
        TieredSolveResult with solve code and helpers
    """
    if io_schema is None:
        io_schema = infer_io_schema(stub_info)
    
    # Load problem config (then apply optional CLI override)
    config = load_problem_config(problem_id)
    if codec_mode_override in ("import", "inline"):
        config.codec_mode = codec_mode_override
    
    # Generate parse and output code
    parse_code, call_params = _generate_parse_code(io_schema.params, config)
    output_code = _generate_output_code(io_schema.return_type or "", config)
    
    # Build solve function
    solve_lines = [
        "def solve():",
        '    """',
        "    Auto-generated solve() for Tier-{} problem.".format(config.tier),
        "    Codec mode: {}".format(config.codec_mode),
        '    """',
        "    import sys",
        "    import json",
        "",
        "    lines = sys.stdin.read().strip().split('\\n')",
        "",
        parse_code,
        "",
        "    solver = get_solver(SOLUTIONS)",
        f"    result = solver.{io_schema.method_name}({call_params})",
        "",
        output_code,
    ]
    
    solve_code = "\n".join(solve_lines)
    
    # Generate helper code
    helper_code = ""
    if config.codec_mode == "inline":
        # Inline mode: embed all codec functions (deduplicated, deps first)
        from codegen.core.catalog import deps
        
        # Collect all needed templates with proper ordering
        seen = set()
        ordered = []
        
        def add_with_deps(name):
            if name in seen:
                return
            # Add dependencies first
            for dep in deps(name):
                add_with_deps(dep)
            seen.add(name)
            ordered.append(name)
        
        for hint in config.codec_hints:
            add_with_deps(hint)
        
        # Get code for each
        helper_parts = []
        for name in ordered:
            code = get(name)
            if code:
                helper_parts.append(code)
        
        helper_code = "\n\n\n".join(helper_parts)
    
    # Generate codec import for import mode (include classes + functions)
    codec_import = ""
    if config.codec_mode == "import" and config.codec_hints:
        from codegen.core.catalog import deps
        
        # Collect all imports (functions + their class dependencies)
        all_imports = set()
        for hint in config.codec_hints:
            all_imports.add(hint)
            for dep in deps(hint):
                all_imports.add(dep)
        
        # Sort: classes first (capitalized), then functions
        sorted_imports = sorted(all_imports, key=lambda x: (not x[0].isupper(), x))
        codec_import = f"from runner.utils.codec import {', '.join(sorted_imports)}"
    
    return TieredSolveResult(
        solve_code=solve_code,
        helper_code=helper_code,
        codec_import=codec_import,
        imports={"sys", "json"},
        tier=config.tier,
        codec_mode=config.codec_mode,
    )


def generate_import_statement(config: ProblemConfig) -> str:
    """Generate import statement for import mode."""
    if config.codec_mode != "import":
        return ""
    
    funcs = config.codec_hints
    if not funcs:
        return ""
    
    return f"from runner.utils.codec import {', '.join(funcs)}"

