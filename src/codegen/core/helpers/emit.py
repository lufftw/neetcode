"""
Helper code emission strategies.

Determines how helper classes are included in generated files:
- inline: Embed helper definitions directly (default)
- import: Import from shared module (future)
- none: Skip helpers
"""

from enum import Enum
from typing import Set, List, Optional

from .catalog import HELPER_CATALOG, HELPER_FUNCTIONS, get_helper_code, get_helper_function


class HelperEmitMode(Enum):
    """Helper emission modes."""
    INLINE = "inline"    # Embed helpers directly in file
    IMPORT = "import"    # Import from shared module
    NONE = "none"        # Don't include helpers


def emit_helpers(
    helper_names: Set[str],
    mode: HelperEmitMode = HelperEmitMode.INLINE,
) -> str:
    """
    Generate helper class code based on emission mode.
    
    Args:
        helper_names: Set of helper class names to emit
        mode: Emission mode (inline, import, none)
        
    Returns:
        Generated code string
        
    Example:
        >>> emit_helpers({'ListNode'}, HelperEmitMode.INLINE)
        '# ============================================\\n# Helper Classes\\n...'
    """
    if mode == HelperEmitMode.NONE or not helper_names:
        return ""
    
    if mode == HelperEmitMode.IMPORT:
        return _emit_import_mode(helper_names)
    
    # Default: INLINE mode
    return _emit_inline_mode(helper_names)


def _emit_inline_mode(helper_names: Set[str]) -> str:
    """Emit helpers as inline class definitions."""
    if not helper_names:
        return ""
    
    lines = [
        "# ============================================",
        "# Helper Classes",
        "# ============================================",
    ]
    
    # Sort for consistent output
    for name in sorted(helper_names):
        code = get_helper_code(name)
        if code:
            lines.append(code)
            lines.append("")
    
    return "\n".join(lines)


def _emit_import_mode(helper_names: Set[str]) -> str:
    """
    Emit helpers as imports from shared module.
    
    Note: This mode requires a shared helpers module to exist.
    """
    if not helper_names:
        return ""
    
    sorted_names = sorted(helper_names)
    names_str = ", ".join(sorted_names)
    
    return f"from packages.helpers import {names_str}"


def emit_helper_functions(
    function_names: Set[str],
    mode: HelperEmitMode = HelperEmitMode.INLINE,
) -> str:
    """
    Generate helper function code based on emission mode.
    
    Args:
        function_names: Set of helper function names to emit
        mode: Emission mode
        
    Returns:
        Generated code string
    """
    if mode == HelperEmitMode.NONE or not function_names:
        return ""
    
    if mode == HelperEmitMode.IMPORT:
        sorted_names = sorted(function_names)
        names_str = ", ".join(sorted_names)
        return f"from packages.helpers import {names_str}"
    
    # INLINE mode
    lines = [
        "# ============================================",
        "# Helper Functions",
        "# ============================================",
    ]
    
    for name in sorted(function_names):
        code = get_helper_function(name)
        if code:
            lines.append(code)
            lines.append("")
    
    return "\n".join(lines)


def emit_typing_imports(type_names: Set[str]) -> str:
    """
    Generate typing import statement.
    
    Args:
        type_names: Set of typing names (e.g., {'List', 'Optional'})
        
    Returns:
        Import statement string
    """
    if not type_names:
        return ""
    
    sorted_names = sorted(type_names)
    return f"from typing import {', '.join(sorted_names)}"


def emit_all_imports(
    typing_names: Set[str],
    include_runner: bool = True,
) -> str:
    """
    Generate all import statements for a solution file.
    
    Args:
        typing_names: Set of typing imports needed
        include_runner: Whether to include _runner import
        
    Returns:
        Complete import block string
    """
    lines = []
    
    # Typing imports
    if typing_names:
        lines.append(emit_typing_imports(typing_names))
    
    # Runner import
    if include_runner:
        lines.append("from _runner import get_solver")
    
    return "\n".join(lines)

