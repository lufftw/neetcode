"""
Catalog - Template repository using directory-based dependencies.

Usage:
    from packages.codegen.core.catalog import get, get_with_deps
    
    code = get("ListNode")
    code = get_with_deps("build_list_with_cycle")  # includes ListNode

Directory structure defines dependencies:
    templates/classes/         → base types (no deps)
    templates/functions/<Class>/struct/    → Tier-1, depends on <Class>
    templates/functions/<Class>/semantic/  → Tier-1.5, depends on <Class>

See: docs/contracts/catalog-structure.md
"""

from pathlib import Path
from functools import lru_cache
from typing import Optional, List, Dict

_TEMPLATES_DIR = Path(__file__).parent / "templates"


@lru_cache(maxsize=1)
def _discover() -> Dict[str, Path]:
    """Scan directory → {name: path}"""
    return {
        p.stem: p 
        for p in _TEMPLATES_DIR.rglob("*.py") 
        if not p.name.startswith("_")
    }


@lru_cache(maxsize=1)
def _known_classes() -> set:
    """Get all class names from classes/ directory."""
    classes_dir = _TEMPLATES_DIR / "classes"
    return {p.stem for p in classes_dir.glob("*.py") if not p.name.startswith("_")}


def get(name: str) -> Optional[str]:
    """Get template code by name."""
    path = _discover().get(name)
    return path.read_text(encoding="utf-8").strip() if path else None


def deps(name: str) -> List[str]:
    """
    Get dependencies from directory structure.
    
    Rules (priority order):
    1. File has TEMPLATE_META["depends_on"] → use it
    2. Path is functions/<ClassName>/... → [<ClassName>]
    3. Otherwise → []
    """
    path = _discover().get(name)
    if not path:
        return []
    
    # Check for TEMPLATE_META in file (for exceptions)
    content = path.read_text(encoding="utf-8")
    if "TEMPLATE_META" in content:
        # Simple extraction: TEMPLATE_META = {"depends_on": [...]}
        import ast
        for node in ast.walk(ast.parse(content)):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "TEMPLATE_META":
                        try:
                            meta = ast.literal_eval(node.value)
                            if isinstance(meta, dict) and "depends_on" in meta:
                                return meta["depends_on"]
                        except:
                            pass
    
    # Infer from path: functions/<ClassName>/...
    parts = path.relative_to(_TEMPLATES_DIR).parts
    if len(parts) >= 2 and parts[0] == "functions":
        class_name = parts[1]
        if class_name in _known_classes():
            return [class_name]
    
    return []


def get_with_deps(name: str) -> str:
    """Get template code with all dependencies resolved."""
    seen = set()
    parts = []
    
    def collect(n: str):
        if n in seen:
            return
        seen.add(n)
        for dep in deps(n):
            collect(dep)
        code = get(n)
        if code:
            parts.append(code)
    
    collect(name)
    return "\n\n\n".join(parts)


def list_all() -> List[str]:
    """List all template names."""
    return list(_discover().keys())


def list_classes() -> List[str]:
    """List all class template names."""
    return list(_known_classes())


def list_functions() -> List[str]:
    """List all function template names."""
    return [name for name in _discover() if name not in _known_classes()]


def tier(name: str) -> Optional[str]:
    """
    Infer tier from path.
    
    Returns:
        "base" for classes/
        "1" for functions/*/struct/
        "1.5" for functions/*/semantic/
        None if unknown
    """
    path = _discover().get(name)
    if not path:
        return None
    
    parts = path.relative_to(_TEMPLATES_DIR).parts
    if parts[0] == "classes":
        return "base"
    if len(parts) >= 3 and parts[0] == "functions":
        if parts[2] == "struct":
            return "1"
        if parts[2] == "semantic":
            return "1.5"
    return None


# Backward compatibility aliases
get_template = get
get_helper_code = get
get_helper_function = get


def get_helpers_for_class(class_name: str) -> List[str]:
    """Get related helper functions for a class (backward compat)."""
    result = []
    for name, path in _discover().items():
        parts = path.relative_to(_TEMPLATES_DIR).parts
        if len(parts) >= 2 and parts[0] == "functions" and parts[1] == class_name:
            result.append(name)
    return result


def get_tier_1_5_helpers() -> List[str]:
    """Get all Tier-1.5 helper function names (backward compat)."""
    return [name for name in list_all() if tier(name) == "1.5"]


def list_all_helpers() -> List[str]:
    """Alias for list_all (backward compat)."""
    return list_all()
