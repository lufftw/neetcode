"""
Helper detection from StubInfo.

This module is responsible for determining which helper classes
are needed based on parsed stub information.

Responsibility separation:
- stub_parser: Only parses, does not infer
- detect: Only infers helpers from StubInfo
"""

from typing import Set

from ..stub_parser import StubInfo
from .catalog import HELPER_CATALOG


def detect_required_helpers(stub_info: StubInfo) -> Set[str]:
    """
    Detect which helper classes are required based on StubInfo.
    
    Examines parameter types and return type to determine if any
    helper classes (ListNode, TreeNode, etc.) are referenced.
    
    Args:
        stub_info: Parsed code stub information
        
    Returns:
        Set of helper class names that need to be included
        
    Example:
        >>> info = StubInfo(
        ...     class_name="Solution",
        ...     method_name="addTwoNumbers",
        ...     params=[("l1", "Optional[ListNode]"), ("l2", "Optional[ListNode]")],
        ...     return_type="Optional[ListNode]",
        ...     raw_signature="..."
        ... )
        >>> detect_required_helpers(info)
        {'ListNode'}
    """
    required: Set[str] = set()
    
    # Collect all type hints to check
    all_types = [t for _, t in stub_info.params]
    if stub_info.return_type:
        all_types.append(stub_info.return_type)
    
    # Check each helper class
    for helper_name in HELPER_CATALOG.keys():
        for type_hint in all_types:
            if _helper_in_type(helper_name, type_hint):
                required.add(helper_name)
                break
    
    return required


def _helper_in_type(helper_name: str, type_hint: str) -> bool:
    """
    Check if a helper class name appears in a type hint.
    
    This handles various type hint formats:
    - Direct: ListNode
    - Optional: Optional[ListNode]
    - List: List[ListNode]
    - Nested: Optional[List[TreeNode]]
    
    Args:
        helper_name: Name of helper class to look for
        type_hint: Type hint string to search in
        
    Returns:
        True if helper_name appears in type_hint
    """
    if not type_hint:
        return False
    
    # Simple check - helper name appears as a word boundary
    # This handles most cases correctly
    import re
    pattern = rf'\b{re.escape(helper_name)}\b'
    return bool(re.search(pattern, type_hint))


def detect_helper_functions(required_helpers: Set[str]) -> Set[str]:
    """
    Detect which helper functions should be included based on required helpers.
    
    Args:
        required_helpers: Set of required helper class names
        
    Returns:
        Set of helper function names to include
    """
    from .catalog import get_helpers_for_class
    
    functions: Set[str] = set()
    
    for helper_name in required_helpers:
        related = get_helpers_for_class(helper_name)
        functions.update(related)
    
    return functions


def suggest_imports(stub_info: StubInfo) -> Set[str]:
    """
    Suggest typing imports based on StubInfo.
    
    Args:
        stub_info: Parsed code stub information
        
    Returns:
        Set of typing module names that should be imported
        
    Example:
        >>> info = StubInfo(
        ...     params=[("nums", "List[int]")],
        ...     return_type="Optional[int]",
        ...     ...
        ... )
        >>> suggest_imports(info)
        {'List', 'Optional'}
    """
    imports: Set[str] = set()
    
    # Common typing imports to detect
    typing_names = ["List", "Optional", "Dict", "Set", "Tuple", "Any", "Union"]
    
    # Collect all type hints
    all_types = [t for _, t in stub_info.params]
    if stub_info.return_type:
        all_types.append(stub_info.return_type)
    
    type_string = " ".join(all_types)
    
    for name in typing_names:
        if name in type_string:
            imports.add(name)
    
    return imports

