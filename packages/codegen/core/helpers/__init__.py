"""
Helper class management for CodeGen.

Provides:
    - HELPER_CATALOG: Canonical helper definitions
    - detect_required_helpers(): Detect helpers from StubInfo
    - emit_helpers(): Generate helper code based on strategy
"""

from .catalog import HELPER_CATALOG, get_helper_code
from .detect import detect_required_helpers
from .emit import emit_helpers, emit_helper_functions, HelperEmitMode

__all__ = [
    "HELPER_CATALOG",
    "get_helper_code",
    "detect_required_helpers",
    "emit_helpers",
    "emit_helper_functions",
    "HelperEmitMode",
]

