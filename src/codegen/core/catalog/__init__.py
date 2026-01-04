"""
Catalog - Extract code from runner/utils/codec/ using AST.

Single Source of Truth: runner/utils/codec/
    ├── classes/           - Data structure definitions
    │   ├── list_node.py   - ListNode
    │   ├── tree_node.py   - TreeNode
    │   └── node.py        - Node
    └── functions/         - Conversion functions
        ├── list_node/     - Depends on ListNode
        │   ├── struct.py  - Tier-1
        │   └── semantic.py- Tier-1.5
        ├── tree_node/     - Depends on TreeNode
        └── node/          - Depends on Node

Usage:
    from codegen.core.catalog import get, get_with_deps, deps
    
    code = get("ListNode")           # Get class definition
    code = get("list_to_tree")       # Get function definition
    deps_list = deps("list_to_tree") # ["TreeNode"]
    full_code = get_with_deps("build_list_with_cycle")  # includes ListNode
"""

import ast
import inspect
from pathlib import Path
from functools import lru_cache
from typing import Optional, List, Dict, Set

# Import the codec package to get source locations
from runner.utils import codec


# =============================================================================
# Discovery: Map names to source files and line ranges
# =============================================================================

@lru_cache(maxsize=1)
def _discover() -> Dict[str, dict]:
    """
    Discover all classes and functions in codec package.
    
    Returns:
        {name: {"file": Path, "start": int, "end": int, "type": "class"|"function"}}
    """
    result = {}
    codec_dir = Path(codec.__file__).parent
    
    # Scan all Python files in codec/
    for py_file in codec_dir.rglob("*.py"):
        if py_file.name.startswith("_"):
            continue
        
        source = py_file.read_text(encoding="utf-8")
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                result[node.name] = {
                    "file": py_file,
                    "start": node.lineno,
                    "end": node.end_lineno,
                    "type": "class",
                }
            elif isinstance(node, ast.FunctionDef):
                result[node.name] = {
                    "file": py_file,
                    "start": node.lineno,
                    "end": node.end_lineno,
                    "type": "function",
                }
    
    return result


@lru_cache(maxsize=1)
def _known_classes() -> Set[str]:
    """Get all class names from classes/ directory."""
    return {name for name, info in _discover().items() if info["type"] == "class"}


# =============================================================================
# Core API: get, deps, get_with_deps
# =============================================================================

def get(name: str) -> Optional[str]:
    """
    Get class/function source code by name using AST extraction.
    
    Args:
        name: Class or function name (e.g., "ListNode", "list_to_tree")
        
    Returns:
        Source code string, or None if not found
    """
    info = _discover().get(name)
    if not info:
        return None
    
    source_lines = info["file"].read_text(encoding="utf-8").splitlines()
    extracted = source_lines[info["start"] - 1 : info["end"]]
    return "\n".join(extracted)


def deps(name: str) -> List[str]:
    """
    Get dependencies from directory structure.
    
    Rules:
    - functions/list_node/*.py → depends on ListNode
    - functions/tree_node/*.py → depends on TreeNode
    - functions/node/*.py → depends on Node
    - classes/*.py → no dependencies
    
    Args:
        name: Function or class name
        
    Returns:
        List of dependency names (e.g., ["ListNode"])
    """
    info = _discover().get(name)
    if not info:
        return []
    
    # Classes have no dependencies
    if info["type"] == "class":
        return []
    
    # Infer from path: codec/functions/<dep_name>/...
    codec_dir = Path(codec.__file__).parent
    try:
        rel_path = info["file"].relative_to(codec_dir)
        parts = rel_path.parts
        
        # functions/<dep_dir>/struct.py or functions/<dep_dir>/semantic.py
        if len(parts) >= 2 and parts[0] == "functions":
            dep_dir = parts[1]  # e.g., "list_node", "tree_node"
            
            # Map directory name to class name
            dir_to_class = {
                "list_node": "ListNode",
                "tree_node": "TreeNode",
                "node": "Node",
                "node_graph": "NodeGraph",
                "node_nary": "NodeNary",
                "doubly_list_node": "DoublyListNode",
            }
            
            if dep_dir in dir_to_class:
                return [dir_to_class[dep_dir]]
    except ValueError:
        pass
    
    return []


def get_with_deps(name: str) -> str:
    """
    Get source code with all dependencies resolved (deps first).
    
    Args:
        name: Class or function name
        
    Returns:
        Complete source code with dependencies
    """
    seen: Set[str] = set()
    parts: List[str] = []
    
    def collect(n: str):
        if n in seen:
            return
        seen.add(n)
        # Add dependencies first
        for dep in deps(n):
            collect(dep)
        code = get(n)
        if code:
            parts.append(code)
    
    collect(name)
    return "\n\n\n".join(parts)


# =============================================================================
# Utility Functions
# =============================================================================

def list_all() -> List[str]:
    """List all available names (classes + functions)."""
    return list(_discover().keys())


def list_classes() -> List[str]:
    """List all class names."""
    return list(_known_classes())


def list_functions() -> List[str]:
    """List all function names."""
    return [name for name in _discover() if name not in _known_classes()]


def tier(name: str) -> Optional[str]:
    """
    Infer tier from directory structure.
    
    Returns:
        "base" for classes
        "1" for functions/*/struct.py
        "1.5" for functions/*/semantic.py
        None if unknown
    """
    info = _discover().get(name)
    if not info:
        return None
    
    if info["type"] == "class":
        return "base"
    
    # Check file path
    codec_dir = Path(codec.__file__).parent
    try:
        rel_path = info["file"].relative_to(codec_dir)
        if "struct" in rel_path.name:
            return "1"
        if "semantic" in rel_path.name:
            return "1.5"
    except ValueError:
        pass
    
    return None


def get_typing_imports() -> str:
    """Get common typing imports for inline mode."""
    return "from typing import List, Optional, Tuple, Any"


# =============================================================================
# Backward Compatibility
# =============================================================================

get_template = get
get_helper_code = get
get_helper_function = get


def get_helpers_for_class(class_name: str) -> List[str]:
    """Get related helper functions for a class."""
    class_to_dir = {
        "ListNode": "list_node",
        "TreeNode": "tree_node",
        "Node": "node",
        "NodeGraph": "node_graph",
        "NodeNary": "node_nary",
        "DoublyListNode": "doubly_list_node",
    }
    
    dir_name = class_to_dir.get(class_name)
    if not dir_name:
        return []
    
    result = []
    for name, info in _discover().items():
        if info["type"] == "function" and dir_name in str(info["file"]):
            result.append(name)
    return result


def get_tier_1_5_helpers() -> List[str]:
    """Get all Tier-1.5 helper function names."""
    return [name for name in list_all() if tier(name) == "1.5"]


def list_all_helpers() -> List[str]:
    """Alias for list_all."""
    return list_all()
