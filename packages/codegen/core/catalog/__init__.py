"""
Catalog - Unified API for helper templates.

This module provides a hybrid approach:
- Templates are real Python files (testable, lintable)
- Can be imported for runtime use
- Can be read as strings for inline codegen

Usage:
    # Get template as string (for inline codegen)
    from packages.codegen.core.catalog import get_template
    code = get_template("ListNode")
    
    # Get helper metadata
    from packages.codegen.core.catalog import get_helper_meta
    meta = get_helper_meta("build_list_with_cycle")
    
    # Import for runtime (if needed)
    from packages.codegen.core.catalog.templates.classes import ListNode
"""

import inspect
import re
from pathlib import Path
from typing import Optional, List, Dict

from .registry import (
    HelperMeta,
    HelperCategory,
    Tier,
    get_helper_meta,
    get_all_registries,
    list_by_category,
    list_by_tier,
    get_dependencies,
    CLASS_REGISTRY,
    STRUCT_FUNC_REGISTRY,
    SEMANTIC_FUNC_REGISTRY,
)


# =============================================================================
# Template Loading
# =============================================================================

_TEMPLATES_DIR = Path(__file__).parent / "templates"


def get_template(name: str) -> Optional[str]:
    """
    Get template code as string.
    
    For codegen inline mode - extracts just the class/function definition
    without imports or module docstrings.
    
    Args:
        name: Helper name (e.g., "ListNode", "build_list_with_cycle")
        
    Returns:
        Template code string, or None if not found
    """
    meta = get_helper_meta(name)
    if not meta:
        return None
    
    template_path = _TEMPLATES_DIR / meta.module_path
    if not template_path.exists():
        return None
    
    content = template_path.read_text(encoding="utf-8")
    return _extract_definition(content, name, meta.category)


def get_template_raw(name: str) -> Optional[str]:
    """
    Get raw template file content (including imports/docstrings).
    
    Args:
        name: Helper name
        
    Returns:
        Full file content, or None if not found
    """
    meta = get_helper_meta(name)
    if not meta:
        return None
    
    template_path = _TEMPLATES_DIR / meta.module_path
    if not template_path.exists():
        return None
    
    return template_path.read_text(encoding="utf-8")


def _extract_definition(content: str, name: str, category: HelperCategory) -> str:
    """
    Extract just the class/function definition from template content.
    
    Removes:
    - Module docstring
    - Import statements
    - Try/except import blocks
    
    Preserves:
    - Docstrings inside the class/function definition
    """
    lines = content.split('\n')
    result_lines = []
    in_definition = False
    in_try_block = False
    in_module_docstring = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Once we're in the definition, include everything
        if in_definition:
            result_lines.append(line)
            continue
        
        # Handle module-level multiline docstring
        if in_module_docstring:
            if '"""' in stripped:
                in_module_docstring = False
            continue
        
        # Skip module docstring at start (single or multi-line)
        if stripped.startswith('"""') and not in_definition:
            if stripped.count('"""') >= 2:
                # Single line docstring like """text"""
                continue
            else:
                # Start of multiline docstring
                in_module_docstring = True
                continue
        
        # Skip imports
        if stripped.startswith(('from ', 'import ')):
            continue
        
        # Skip try/except import blocks
        if stripped == 'try:':
            in_try_block = True
            continue
        if in_try_block:
            if stripped.startswith('except'):
                in_try_block = False
                continue
            continue
        
        # Skip empty lines before definition
        if not stripped:
            continue
        
        # Start of definition
        if category == HelperCategory.CLASS and stripped.startswith('class '):
            in_definition = True
            result_lines.append(line)
        elif category != HelperCategory.CLASS and stripped.startswith('def '):
            in_definition = True
            result_lines.append(line)
    
    return '\n'.join(result_lines).rstrip()


# =============================================================================
# Convenience Functions
# =============================================================================

def get_class_template(name: str) -> Optional[str]:
    """Get a class template by name."""
    if name not in CLASS_REGISTRY:
        return None
    return get_template(name)


def get_function_template(name: str) -> Optional[str]:
    """Get a function template by name."""
    if name in STRUCT_FUNC_REGISTRY or name in SEMANTIC_FUNC_REGISTRY:
        return get_template(name)
    return None


def get_templates_for_helpers(names: List[str]) -> Dict[str, str]:
    """
    Get multiple templates at once, resolving dependencies.
    
    Args:
        names: List of helper names
        
    Returns:
        Dict of {name: template_code}
    """
    result = {}
    all_names = set(names)
    
    # Add dependencies
    for name in names:
        deps = get_dependencies(name)
        all_names.update(deps)
    
    # Get templates
    for name in all_names:
        template = get_template(name)
        if template:
            result[name] = template
    
    return result


def list_all_helpers() -> List[str]:
    """List all available helper names."""
    return list(get_all_registries().keys())


def list_classes() -> List[str]:
    """List all class helper names."""
    return list(CLASS_REGISTRY.keys())


def list_struct_functions() -> List[str]:
    """List all struct function names (Tier-1)."""
    return list(STRUCT_FUNC_REGISTRY.keys())


def list_semantic_functions() -> List[str]:
    """List all semantic function names (Tier-1.5)."""
    return list(SEMANTIC_FUNC_REGISTRY.keys())


# =============================================================================
# Backward Compatibility (with old catalog.py)
# =============================================================================

def get_helper_code(name: str) -> Optional[str]:
    """
    Get helper class code by name.
    
    Backward compatible with old catalog.py API.
    """
    return get_class_template(name)


def get_helper_function(name: str) -> Optional[str]:
    """
    Get helper function code by name.
    
    Backward compatible with old catalog.py API.
    """
    return get_function_template(name)


def get_helpers_for_class(class_name: str) -> List[str]:
    """
    Get related helper functions for a class.
    
    Backward compatible with old catalog.py API.
    """
    mapping = {
        "ListNode": ["list_to_linkedlist", "linkedlist_to_list"],
        "TreeNode": ["list_to_tree", "tree_to_list"],
        "Node": ["build_random_pointer_list", "encode_random_pointer_list"],
    }
    return mapping.get(class_name, [])


def get_tier_1_5_helpers() -> List[str]:
    """Get all Tier-1.5 helper function names."""
    return list_semantic_functions()


# Re-export registry functions
__all__ = [
    # Template loading
    "get_template",
    "get_template_raw",
    "get_class_template",
    "get_function_template",
    "get_templates_for_helpers",
    
    # Listing
    "list_all_helpers",
    "list_classes",
    "list_struct_functions",
    "list_semantic_functions",
    
    # Metadata
    "get_helper_meta",
    "get_dependencies",
    "HelperMeta",
    "HelperCategory",
    "Tier",
    
    # Backward compatibility
    "get_helper_code",
    "get_helper_function",
    "get_helpers_for_class",
    "get_tier_1_5_helpers",
]

