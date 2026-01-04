"""
Helper class catalog.

DEPRECATED: This module is maintained for backward compatibility.
New code should use: packages.codegen.core.catalog

Canonical definitions of helper classes used in LeetCode problems.
These are the authoritative implementations for code generation.
"""

from typing import Optional, Dict

# Re-export from new catalog location
from codegen.core.catalog import (
    get as get_helper_code,
    get as get_helper_function,
    get_helpers_for_class,
    get_tier_1_5_helpers,
    list_classes as list_all_helpers,
    list_all as list_all_helper_functions,
)


# HELPER_CATALOG for backward compatibility
# This is a lazy dict that fetches templates on access
class _LazyHelperCatalog:
    """Lazy catalog that fetches templates on demand."""
    
    def __getitem__(self, key: str) -> str:
        from codegen.core.catalog import get
        result = get(key)
        if result is None:
            raise KeyError(key)
        return result
    
    def get(self, key: str, default=None) -> Optional[str]:
        from codegen.core.catalog import get
        result = get(key)
        return result if result is not None else default
    
    def __contains__(self, key: str) -> bool:
        from codegen.core.catalog import get
        return get(key) is not None
    
    def keys(self):
        from codegen.core.catalog import list_classes
        return list_classes()


HELPER_CATALOG = _LazyHelperCatalog()


# HELPER_FUNCTIONS for backward compatibility
class _LazyHelperFunctions:
    """Lazy functions dict that fetches templates on demand."""
    
    def __getitem__(self, key: str) -> str:
        from codegen.core.catalog import get, list_functions
        if key not in list_functions():
            raise KeyError(key)
        result = get(key)
        if result is None:
            raise KeyError(key)
        return result
    
    def get(self, key: str, default=None) -> Optional[str]:
        from codegen.core.catalog import get
        return get(key) or default
    
    def __contains__(self, key: str) -> bool:
        from codegen.core.catalog import get, list_functions
        return key in list_functions()
    
    def keys(self):
        from codegen.core.catalog import list_functions
        return list_functions()


HELPER_FUNCTIONS = _LazyHelperFunctions()

