"""
Helper class catalog.

DEPRECATED: This module is maintained for backward compatibility.
New code should use: packages.codegen.core.catalog

Canonical definitions of helper classes used in LeetCode problems.
These are the authoritative implementations for code generation.
"""

from typing import Optional

# Re-export from new catalog location
from packages.codegen.core.catalog import (
    get_template as get_helper_code,
    get_template as get_helper_function,
    get_helpers_for_class,
    get_tier_1_5_helpers,
    list_classes as list_all_helpers,
    list_all_helpers as list_all_helper_functions,
)

